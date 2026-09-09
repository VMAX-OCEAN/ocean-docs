# Render Deployment — Backend Strategy

Complete deployment plan for the SIH-OCEAN **backend** on Render.com.

> **Architecture:** Frontend on Vercel (see [`vercel-deployment.md`](vercel-deployment.md)),
> Backend on Render (this document).

---

## Why Render for the Backend

| Requirement | Render support |
|---|---|
| FastAPI + xpublish server | Web Service (Python runtime or Docker) |
| Zarr data storage (chunked ocean arrays) | Persistent Disk (SSD, survives deploys) |
| SQLite (Argo/Glider metadata) | Persistent Disk (same disk) |
| OPeNDAP endpoints | Web Service (long-running Python process) |
| Isosurface compute (marching cubes) | Web Service (CPU available) |
| Custom domains + HTTPS | Built-in (Let's Encrypt auto-renew) |
| Auto-deploy from GitHub | Built-in (push → deploy) |
| Infrastructure as Code | `render.yaml` Blueprint |

---

## Service Configuration

### Backend Web Service

| Setting | Value |
|---|---|
| Service type | **Web Service** |
| Name | `sih-ocean-backend` |
| Runtime | **Python 3** (or Docker) |
| Region | Oregon (closest to Copernicus/INCOIS data) |
| Plan | **Starter** ($7/month, 512 MB RAM, 0.5 CPU) |
| Branch | `main` |
| Root Directory | `backend/` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Health Check | `/health` |

### Persistent Disk

| Setting | Value |
|---|---|
| Name | `ocean-data` |
| Mount Path | `/var/data` |
| Size | 10 GB (minimum; upgrade as data grows) |
| Cost | $2.50/month |

The disk stores:
- `/var/data/zarr/` — GLORYS Zarr stores (chunked ocean arrays)
- `/var/data/sqlite/` — Argo/Glider metadata databases
- `/var/data/cache/` — Isosurface mesh cache

**Important:** Persistent disks attach to a single instance. The backend cannot
autoscale with a disk attached. This is fine for our use case — one backend instance
is sufficient for the SIH demo.

---

## Environment Variables

| Variable | Value | Notes |
|---|---|---|
| `CESIUM_ION_TOKEN` | (your token) | For terrain/imagery if backend fetches tiles |
| `CORS_ORIGINS` | `https://sih-ocean.vercel.app,https://*.vercel.app` | Allow Vercel frontend |
| `ZARR_DATA_PATH` | `/var/data/zarr` | Path to Zarr stores on disk |
| `SQLITE_PATH` | `/var/data/sqlite/ocean.db` | SQLite database path |
| `CACHE_PATH` | `/var/data/cache` | Isosurface cache |
| `PYTHONPATH` | `/opt/render/project/src` | Fix import issues |

---

## CORS Configuration (Critical for Vercel + Render split)

Since frontend (Vercel) and backend (Render) are on different domains, CORS is
mandatory:

```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sih-ocean.vercel.app",      # Vercel production
        "https://*-sih-ocean.vercel.app",    # Vercel preview deployments
        "http://localhost:5173",              # Local dev (Vite)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

The frontend calls the backend at `https://sih-ocean-backend.onrender.com/...`

---

## Data Upload Strategy

The persistent disk is empty on first deploy. Upload data via:

### Option A: Pre-deploy script (recommended for sample data)
```yaml
# In render.yaml
preDeployCommand: "python scripts/download_samples.py"
```

```python
# scripts/download_samples.py
import copernicusmarine
from pathlib import Path

ZARR_PATH = Path("/var/data/zarr")
ZARR_PATH.mkdir(parents=True, exist_ok=True)

# Download Indian Ocean subset
copernicusmarine.subset(
    dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
    variables=["thetao", "so", "uo", "vo"],
    minimum_longitude=60, maximum_longitude=100,
    minimum_latitude=-5, maximum_latitude=30,
    start_datetime="2026-01-01", end_datetime="2026-01-31",
    output_filename=str(ZARR_PATH / "glorys_indian_ocean")
)
```

### Option B: SSH + SCP (for larger data)
```bash
# Render allows SSH access to web services
scp -r data/zarr/ root@sih-ocean-backend.onrender.com:/var/data/zarr/
```

### Option C: Initial deploy hook
```yaml
# In render.yaml
initialDeployHook: "python scripts/ingest_all.py"
```

This runs only on the first deploy, ingesting all sample data.

---

## Free Tier Limitations (for testing)

If using the Free plan ($0/month):

| Limitation | Impact |
|---|---|
| 512 MB RAM, 0.1 CPU | May be tight for xarray + Zarr + marching cubes |
| Spins down after 15 min inactivity | First request after idle takes ~30s to wake |
| 750 instance hours/month | ~31 days of 24/7 running — enough for testing |
| No persistent disk | Data lost on redeploy — must re-upload |

**Recommendation:** Use Free tier for initial testing, then upgrade to Starter ($7/mo)
with persistent disk for the actual demo.

---

## Docker Option (if Python runtime is insufficient)

If the native Python runtime can't handle all dependencies (PyVista/VTK can be tricky),
use Docker:

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

# System dependencies for scientific Python
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
```

In `render.yaml`, set `runtime: docker` instead of `runtime: python`.
