# Deployment Architecture — Vercel + Render

How the SIH-OCEAN 3-tier architecture maps onto Vercel (frontend) + Render (backend).

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  USER BROWSER                                                    │
│                                                                  │
│  React + CesiumJS + zarrita.js                                   │
│  (loaded from Vercel CDN)                                        │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │  HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  VERCEL (Frontend)                                               │
│  ─────────────────────────────                                   │
│  Service type: Static Site (CDN-served SPA)                      │
│  URL: https://sih-ocean.vercel.app                               │
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐          │
│  │ React app   │  │ Cesium assets│  │ API client     │          │
│  │ (JS chunks) │  │ (Workers,    │  │ (calls Render) │          │
│  │             │  │  Assets,    │  │                │          │
│  │             │  │  Widgets)   │  │                │          │
│  └─────────────┘  └──────────────┘  └────────┬───────┘          │
│                                             │                    │
└─────────────────────────────────────────────┼────────────────────┘
                                              │
                                              │  HTTPS (CORS)
                                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  RENDER (Backend)                                                │
│  ─────────────────────────                                       │
│  Service type: Web Service (Python/Docker)                       │
│  URL: https://sih-ocean-backend.onrender.com                     │
│  Plan: Starter ($7/mo, 512 MB RAM, 0.5 CPU)                     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐        │
│  │ FastAPI + xpublish                                  │        │
│  │  ├── /zarr/...        → Zarr REST chunks (ms lat)   │        │
│  │  ├── /opendap/...     → OPeNDAP endpoints          │        │
│  │  ├── /argo/floats     → Argo markers (SQLite)      │        │
│  │  ├── /argo/profile    → Argo profile (SQLite)      │        │
│  │  ├── /isosurface      → Marching cubes (cached)    │        │
│  │  └── /health          → Health check              │        │
│  └────────────────────────┬───────────────────────────┘        │
│                            │                                     │
│  ┌────────────────────────▼───────────────────────────┐        │
│  │ Persistent Disk (10 GB SSD, $2.50/mo)              │        │
│  │  /var/data/zarr/     → GLORYS Zarr stores          │        │
│  │  /var/data/sqlite/   → Argo/Glider metadata        │        │
│  │  /var/data/cache/    → Isosurface mesh cache       │        │
│  └────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow (Runtime)

### 1. Page Load (Vercel)
```
Browser → Vercel CDN → index.html + JS chunks + Cesium assets
         (~2-3s first paint)
```

### 2. Globe Render (Cesium ion)
```
Browser → Cesium ion API → terrain tiles + imagery tiles
         (Cesium ion handles this, not our backend)
```

### 3. Ocean Data Load (Vercel → Render)
```
Browser → https://sih-ocean-backend.onrender.com/zarr/.zmetadata
         → Zarr metadata (small, ~100ms)
Browser → https://sih-ocean-backend.onrender.com/zarr/thetao/0.1.2.3
         → Zarr chunk (~100 KB, ~200ms)
         → GPU texture → Cesium renders SST overlay
```

### 4. Argo Profile (Vercel → Render)
```
Browser → https://sih-ocean-backend.onrender.com/argo/floats?bbox=...
         → SQLite R-tree query (~10ms)
         → JSON markers
User clicks marker
Browser → https://sih-ocean-backend.onrender.com/argo/profile?id=6901254
         → SQLite lookup (~10ms)
         → JSON profile data
         → Plotly renders depth-vs-temp chart
```

### 5. Isosurface (Vercel → Render)
```
Browser → https://sih-ocean-backend.onrender.com/isosurface?var=thetao&value=20
         → PyVista marching cubes (~500ms first, ~50ms cached)
         → glTF mesh
         → Cesium renders 3D primitive
```

---

## Why Split Vercel + Render?

| Concern | Vercel (frontend) | Render (backend) |
|---|---|---|
| Static asset delivery | Edge CDN (fast globally) | — |
| SPA routing | Built-in (rewrites) | — |
| Python server | — | Native Python runtime or Docker |
| Persistent storage | — | Persistent disks (SSD) |
| Scientific Python (xarray, PyVista) | — | Full Python environment |
| SQLite | — | Persistent disk |
| Cost | Free tier sufficient | $7/mo Starter + $2.50/mo disk |
| Preview deployments | Every PR gets a URL | Manual or Blueprint previews |

**Why not Vercel for both?** Vercel's serverless functions have:
- 10-60s timeout (too short for marching cubes isosurface compute)
- No persistent disk (SQLite/Zarr data lost between invocations)
- Cold starts on every request (bad for xarray lazy loading)
- Not designed for long-running Python processes

**Why not Render for both?** Render static sites work but:
- Vercel's edge CDN is faster for global static delivery
- Vercel has better preview deployment UX
- Vercel's free tier is more generous for static sites

---

## Environment Variable Wiring

### Vercel (Frontend)
| Variable | Value | Set in |
|---|---|---|
| `VITE_CESIUM_ION_TOKEN` | `eyJhbGci...` | Vercel Dashboard → Env Vars |
| `VITE_API_URL` | `https://sih-ocean-backend.onrender.com` | Vercel Dashboard → Env Vars |

### Render (Backend)
| Variable | Value | Set in |
|---|---|---|
| `CORS_ORIGINS` | `https://sih-ocean.vercel.app` | Render Dashboard → Env Vars |
| `ZARR_DATA_PATH` | `/var/data/zarr` | render.yaml |
| `SQLITE_PATH` | `/var/data/sqlite/ocean.db` | render.yaml |
| `CACHE_PATH` | `/var/data/cache` | render.yaml |

### Cross-service wiring
```
Vercel frontend → VITE_API_URL → Render backend URL
Render backend  → CORS_ORIGINS → Vercel frontend URL
```

Both URLs are only known after the first deploy (when `.onrender.com` and
`.vercel.app` subdomains are assigned). Set them after first deploy, then redeploy.

---

## Deployment Order

1. **Deploy backend on Render first** (needs to be running for frontend to call)
2. Note the Render URL: `https://sih-ocean-backend.onrender.com`
3. **Deploy frontend on Vercel** with `VITE_API_URL` set to the Render URL
4. Note the Vercel URL: `https://sih-ocean.vercel.app`
5. **Update Render CORS** to allow the Vercel URL
6. Test end-to-end

---

## Monorepo Structure (for both Vercel + Render)

```
sih-ocean/
├── frontend/          ← Vercel deploys this (Root Directory: frontend/)
│   ├── src/
│   ├── public/
│   ├── index.html
│   ├── vite.config.ts
│   ├── vercel.json     ← Vercel config (SPA rewrites, cache headers)
│   └── package.json
├── backend/           ← Render deploys this (Root Directory: backend/)
│   ├── main.py
│   ├── api/
│   ├── ingest/
│   ├── requirements.txt
│   ├── Dockerfile      ← (optional, if Docker runtime needed)
│   └── render.yaml     ← Render Blueprint (can also be at repo root)
├── docs/
├── lakshya-research/
└── README.md
```

**Vercel** reads `frontend/` as root, builds with Vite, serves `dist/` on CDN.
**Render** reads `backend/` as root, builds with pip, runs uvicorn on a web service.

Both deploy from the same GitHub repo — Vercel watches `frontend/`, Render watches
`backend/`. Pushes to `main` trigger both to redeploy independently.
