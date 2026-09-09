# Render Blueprint — render.yaml

Infrastructure as Code for the SIH-OCEAN backend on Render.

---

## render.yaml (place at repo root or in backend/)

```yaml
# Render Blueprint for SIH-OCEAN backend
# Deploy with: https://render.com/deploy?repo=https://github.com/VMAX-OCEAN/ocean-docs
# Or: Manual create in Render Dashboard using this file

services:
  # ─── Backend Web Service ──────────────────────────────────────
  - type: web
    name: sih-ocean-backend
    runtime: python          # Use "docker" if PyVista/VTK needs system deps
    plan: starter            # $7/mo, 512 MB RAM, 0.5 CPU, no spin-down
    region: oregon           # Closest to Copernicus/INCOIS data sources
    branch: main
    rootDir: backend         # Backend code lives in backend/
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    autoDeployTrigger: commit  # Auto-deploy on push to main

    # Persistent disk for Zarr data + SQLite + cache
    disk:
      name: ocean-data
      mountPath: /var/data
      sizeGB: 10             # Start small, expand as needed

    # Environment variables
    envVars:
      # Non-secret config (hardcoded)
      - key: ZARR_DATA_PATH
        value: /var/data/zarr
      - key: SQLITE_PATH
        value: /var/data/sqlite/ocean.db
      - key: CACHE_PATH
        value: /var/data/cache
      - key: PYTHONPATH
        value: /opt/render/project/src
      - key: PYTHON_VERSION
        value: "3.11.9"

      # Secret config (prompt in Render Dashboard)
      - key: CESIUM_ION_TOKEN
        sync: false          # Set manually in Dashboard
      - key: CORS_ORIGINS
        sync: false          # Set to Vercel URL after frontend deploys

    # Run data ingestion on first deploy only
    initialDeployHook: python scripts/download_samples.py
```

---

## Alternative: Docker Runtime

If the native Python runtime can't handle PyVista/VTK, use Docker:

```yaml
services:
  - type: web
    name: sih-ocean-backend
    runtime: docker
    plan: starter
    region: oregon
    branch: main
    rootDir: backend
    dockerfilePath: ./Dockerfile
    dockerContext: .
    healthCheckPath: /health

    disk:
      name: ocean-data
      mountPath: /var/data
      sizeGB: 10

    envVars:
      - key: ZARR_DATA_PATH
        value: /var/data/zarr
      - key: SQLITE_PATH
        value: /var/data/sqlite/ocean.db
      - key: CORS_ORIGINS
        sync: false
      - key: CESIUM_ION_TOKEN
        sync: false

    initialDeployHook: python scripts/download_samples.py
```

---

## Backend Dockerfile (for Docker runtime)

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

# System dependencies for scientific Python (PyVista/VTK)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directories
RUN mkdir -p /var/data/zarr /var/data/sqlite /var/data/cache

EXPOSE 10000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:10000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
```

---

## Backend requirements.txt

```
# Web framework
fastapi
uvicorn[standard]

# xarray server
xpublish
xpublish-opendap

# Data handling
xarray
netCDF4
zarr
blosc
numcodecs

# Argo data
argopy

# Scientific
numpy
scipy
pandas

# Isosurface computation
pyvista
vtk

# HTTP client (for Copernicus data download)
copernicusmarine
httpx

# Database
aiosqlite
```

---

## Deploy via Blueprint

### Option A: One-click deploy button

Add this to the repo README:

```markdown
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/VMAX-OCEAN/ocean-docs)
```

### Option B: Manual Blueprint sync

1. Push `render.yaml` to repo root
2. Render Dashboard → New → Blueprint
3. Select the `VMAX-OCEAN/ocean-docs` repo
4. Render reads `render.yaml` and creates all services
5. Set secret env vars (`sync: false`) in Dashboard
6. Deploy

---

## Post-Deploy Steps

1. **Wait for backend to deploy** — note the URL: `https://sih-ocean-backend.onrender.com`
2. **Set CORS_ORIGINS** in Render Dashboard:
   ```
   https://sih-ocean.vercel.app,https://ocean-docs.vercel.app
   ```
3. **Verify health check**: `curl https://sih-ocean-backend.onrender.com/health`
4. **Verify Zarr endpoint**: `curl https://sih-ocean-backend.onrender.com/glorys_temp/zarr/.zmetadata`
5. **Verify OPeNDAP**: `curl https://sih-ocean-backend.onrender.com/glorys_temp/opendap/`
6. **Deploy frontend on Vercel** with `VITE_API_URL` = backend URL
