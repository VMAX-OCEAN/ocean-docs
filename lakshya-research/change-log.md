# Detailed Change Log — All Decisions & Architecture Changes

Complete record of every decision made during the research and planning phase of
the SIH-OCEAN project. This document tracks what changed, why it changed, and what
the final decision was.

---

## Change #1: Rendering Engine — Three.js to CesiumJS

### What changed
Replaced the hand-rolled Three.js globe (`realistic-earth-globe.html`) with
**CesiumJS** as the primary rendering engine.

### Why it changed
The original file was a static visual demo — a Three.js sphere with a CDN texture.
For a "perfect" Google-Earth-quality globe with accurate day/night, temperature,
and water levels, hand-rolling Three.js is the wrong approach:

| Issue | Hand-rolled Three.js | CesiumJS |
|---|---|---|
| Day/night terminator | Must write shader (sun position math + dot product + smoothstep — error-prone) | Built-in: `enableLighting = true` — sun position auto-derived from clock |
| Atmosphere | Cheap additive fresnel approximation | Built-in atmospheric scattering (Rayleigh + Mie, single-scatter volumetric) |
| Terrain/bathymetry | Flat sphere, no elevation | Streams Cesium World Terrain + GEBCO bathymetry |
| Imagery | One static NASA Blue Marble JPG | Streams Bing/ArcGIS/MapTiler satellite imagery at any zoom |
| Geospatial accuracy | Sphere geometry, wrong for Argo/Glider overlay | WGS84 ellipsoid + hybrid log-depth buffer |
| LOD streaming | None — one static texture | Quadtree LOD + Screen-Space Error tile selection |
| Light theme | Hardcoded black background | Default is light; fully themeable |

### Final decision
**CesiumJS** (with `resium` React bindings) as the primary globe engine. Three.js
reserved only for custom volume rendering if needed.

### Impact
- Removed dependency on hand-rolled shaders
- Day/night terminator is now a one-liner (`enableLighting = true`)
- Terrain, bathymetry, imagery all stream automatically
- Argo/Glider markers are geospatially accurate

---

## Change #2: Data Format — NetCDF Direct to Zarr

### What changed
Replaced direct NetCDF file serving with **Zarr** (chunked, cloud-streamed format).

### Why it changed
GLORYS12 is petabyte-scale. Loading and serving NetCDF files naively fails:

| Format | Access | Performance |
|---|---|---|
| NetCDF direct | File-level download | Heavy downloads, no parallel chunk access |
| OPeNDAP | Server-mediated subset | CPU/memory bound, slower than Zarr |
| **Zarr** | Direct chunk access | 40× faster time-series access, ms latency, parallel reads |

### Final decision
- **One-time conversion:** NetCDF → Zarr (via xarray)
- **Browser streaming:** zarrita.js fetches chunks directly from R2
- **OPeNDAP retained** for standards compliance (via xpublish-opendap plugin)
- **Dual chunking** strategy: time-series optimized + map/slice optimized

### Impact
- Browser fetches only visible chunks (~100 KB each, ms latency)
- Colormap changes are instant (shader uniform, no re-fetch)
- Time animation is smooth (one chunk per frame)

---

## Change #3: Backend Strategy — FastAPI to xpublish

### What changed
Replaced a custom FastAPI-only backend with **xpublish** (FastAPI + Zarr REST +
OPeNDAP plugin).

### Why it changed
A custom FastAPI backend would require writing Zarr-serving logic from scratch.
xpublish provides:

- Zarr-compatible REST API (browser streams chunks directly)
- OPeNDAP plugin (standards compliance for INCOIS portals)
- Custom FastAPI endpoints for profiles, isosurfaces, metadata
- All in one server

### Final decision
**xpublish** as the backend framework, with:
- Zarr REST for the hot path (chunk streaming)
- OPeNDAP for standards compliance
- Custom endpoints for isosurfaces (marching cubes, cached)
- SQLite/Supabase for Argo/Glider metadata

### Impact
- One server handles streaming + standards + compute
- No need for separate OPeNDAP server
- Isosurfaces cached server-side (or in R2 for free tier)

---

## Change #4: Deployment — Single Platform to Split (Vercel + Render)

### What changed
Originally planned a single-platform deployment (Render only). Changed to a split:
**Frontend on Vercel, Backend on Render.**

### Why it changed
| Concern | Vercel | Render |
|---|---|---|
| Static asset delivery | Edge CDN (fast globally) | Slower for static |
| SPA routing | Built-in (rewrites) | Works but less polished |
| Python server | Serverless (10-60s timeout, no disk) | Native Python + Docker |
| Persistent storage | No | Persistent disks (SSD) |
| Preview deployments | Every PR gets URL | Manual |

Neither platform alone handles both frontend and backend well:
- Vercel serverless can't run persistent Python with disk
- Render static sites work but Vercel's CDN is faster

### Final decision
- **Frontend:** Vercel (CDN, preview deploys, free tier)
- **Backend:** Render (persistent disk, Python runtime, always-on on paid)

### Impact
- Frontend loads fast globally (Vercel edge CDN)
- Backend has persistent storage (Render disk)
- CORS required (cross-domain)
- Two deploy pipelines (both auto-deploy from GitHub)

---

## Change #5: Deployment — Paid to 100% Free Tier

### What changed
Originally planned Render Starter ($7/mo) + persistent disk ($2.50/mo) = $9.50/mo.
Changed to a **100% free** architecture using Cloudflare R2 + Supabase + Render free.

### Why it changed
The user requested a fully free plan with no extra costs. Render's free tier has no
persistent disk — but we don't need the backend to store data at all:

| Data | Free Service | Access Pattern |
|---|---|---|
| Zarr chunks (ocean arrays) | Cloudflare R2 (10 GB free, zero egress) | Browser fetches directly |
| Argo/Glider metadata | Supabase (500 MB Postgres free) | Frontend queries directly |
| Isosurface compute | Render free web service | On demand only |

### The key insight
**No backend in the hot path.** The browser fetches Zarr from R2 and metadata from
Supabase directly. The Render backend is only for occasional isosurface compute.

### Final decision
- **Vercel** (free) — frontend
- **Cloudflare R2** (free, 10 GB, zero egress) — Zarr data
- **Supabase** (free, 500 MB) — Argo/Glider database
- **Render** (free, 750 hours) — isosurface compute only
- **cron-job.org** (free) — keep Render warm during working hours
- **Cesium ion** (free) — terrain + imagery

### Impact
- **$0/month** total cost
- Faster hot path (R2 CDN + Supabase direct > Render backend)
- More scalable (R2 + Supabase handle concurrent reads natively)
- No cold-start penalty for hot path (R2 + Supabase always on)
- Render only cold-starts for isosurface (acceptable)

---

## Change #6: Database — SQLite to Supabase (Postgres)

### What changed
Replaced SQLite (on Render persistent disk) with **Supabase** (managed Postgres,
free tier).

### Why it changed
- Render free tier has no persistent disk → SQLite data lost on redeploy
- Supabase provides free 500 MB Postgres with PostGIS spatial extension
- Supabase has a JS client → frontend queries directly (no backend needed)
- Supabase has REST API auto-generated from tables

### Final decision
**Supabase** for Argo/Glider metadata:
- `floats` table (wmo, cycle, lat, lon, date, variables)
- `profiles` table (wmo, cycle, depth[], temperature[], salinity[])
- PostGIS extension for spatial (R-tree) queries
- Frontend queries via `@supabase/supabase-js` (direct, no backend)

### Impact
- No backend needed for marker queries or profile fetches
- PostGIS spatial queries (bbox filtering) are fast
- 500 MB is sufficient for ~4000 Argo floats with metadata
- Supabase pauses after 1 week inactivity (wakes on next request)

---

## Change #7: Zarr Storage — Render Disk to Cloudflare R2

### What changed
Replaced Render persistent disk (paid) with **Cloudflare R2** (free, 10 GB,
zero egress).

### Why it changed
- Render free tier has no persistent disk
- R2 provides 10 GB free storage with **zero egress fees**
- R2 is S3-compatible → zarrita.js works directly
- R2 has a public bucket URL → browser fetches chunks directly
- R2 is a CDN → chunks load fast globally

### Final decision
**Cloudflare R2** for Zarr storage:
- Public bucket: `sih-ocean-zarr`
- Browser fetches via `https://pub-xxx.r2.dev/sih-ocean-zarr/...`
- zarrita.js opens the store directly from the R2 URL
- 10 GB holds ~5 GLORYS variables × Indian Ocean × 1-2 months

### Impact
- Zero egress cost (no bandwidth bills regardless of traffic)
- Browser fetches chunks directly (no backend proxy)
- S3-compatible API for uploads (rclone, aws-cli)
- 10 GB limit → use Indian Ocean subset, monthly data only

---

## Change #8: Backend Role — Hot Path to Compute-Only

### What changed
The backend went from being the primary data server to a **compute-only** service
for isosurfaces.

### Why it changed
With Zarr on R2 and metadata on Supabase (both accessed directly by the browser),
the backend is no longer in the hot path. Its only remaining job is:
- Isosurface computation (marching cubes via PyVista) — on demand
- OPeNDAP endpoints (standards compliance) — on demand
- Data ingestion scripts — occasional

### Final decision
**Render free web service** for compute only:
- `/isosurface` endpoint — marching cubes (reads Zarr from R2, returns glTF)
- `/opendap` endpoint — OPeNDAP (standards)
- `/health` endpoint — health check
- Spins down after 15 min idle (cold start ~30s, acceptable for isosurface)
- Keep-warm via cron-job.org during working hours (08:00-18:00)

### Impact
- Backend can be on free tier (no persistent disk needed)
- Cold start only affects isosurface (not the hot path)
- 310 hours/month with keep-warm (well under 750 free hours)
- Backend reads Zarr from R2 via S3 API (no local storage)

---

## Change #9: Multi-Account Render Strategy

### What changed
Added a **multi-account Render strategy** for running multiple backend services
without exceeding the 750 free hours per workspace.

### Why it changed
Render's 750 free hours are per **workspace** (account), not per service. One
always-on service uses ~744 hours. Two always-on services would need ~1488 hours —
over the limit.

### Final decision
Use multiple Render accounts (workspaces), each with its own 750 hours:

| Account | Service | Purpose | Hours/month |
|---|---|---|---|
| Account 1 | `sih-ocean-compute` | Isosurface + OPeNDAP | ~310 (keep-warm 8-18h) |
| Account 2 | `sih-ocean-ingest` | Data ingestion (cron) | ~50 (occasional) |

Keep-warm only during working hours (08:00-18:00) via cron-job.org → 310 hours/month,
well under 750.

### Impact
- Multiple backend services possible on free tier
- Each account gets its own 750 hours
- Keep-warm limited to working hours to conserve hours
- cron-job.org handles the ping schedule (free)

---

## Change #10: Frontend Data Access — Backend Proxy to Direct

### What changed
Frontend data access changed from proxying through the backend to **direct
browser-to-storage** access.

### Why it changed
With Zarr on R2 and metadata on Supabase, the frontend can access both directly:

### Before (backend proxy)
```
Browser → Render backend → Disk (Zarr + SQLite) → Backend → Browser
         (backend is bottleneck, needs persistent disk = $)
```

### After (direct access)
```
Browser → R2 (Zarr chunks directly)     ← zero egress, ms latency
Browser → Supabase (metadata directly)  ← direct JS client
Browser → Render (only for isosurface)  ← occasional, can cold-start
```

### Final decision
- **zarrita.js** opens Zarr store directly from R2 public URL
- **@supabase/supabase-js** queries Postgres directly from the browser
- **fetch()** calls Render backend only for isosurfaces

### Impact
- Faster (no backend proxy hop)
- More scalable (R2 + Supabase handle concurrent reads natively)
- No cold-start penalty for hot path
- Backend only for compute (isosurface)

---

## Summary: All Changes

| # | What changed | From | To | Reason |
|---|---|---|---|---|
| 1 | Rendering engine | Hand-rolled Three.js | CesiumJS | Geospatial accuracy, built-in day/night, terrain, LOD |
| 2 | Data format | NetCDF direct | Zarr (chunked) | 40× faster, ms latency, parallel reads |
| 3 | Backend framework | Custom FastAPI | xpublish | Zarr REST + OPeNDAP + custom endpoints in one |
| 4 | Deployment platform | Single (Render) | Split (Vercel + Render) | CDN for frontend, Python for backend |
| 5 | Deployment cost | Paid ($9.50/mo) | Free ($0/mo) | User requested free tier only |
| 6 | Database | SQLite (Render disk) | Supabase (Postgres) | Free tier, direct browser access, PostGIS |
| 7 | Zarr storage | Render persistent disk | Cloudflare R2 | Free 10 GB, zero egress, S3-compatible |
| 8 | Backend role | Hot path data server | Compute-only (isosurface) | R2 + Supabase handle hot path directly |
| 9 | Multi-account | Single workspace | Multiple Render accounts | 750 hours per workspace limit |
| 10 | Frontend access | Backend proxy | Direct to R2 + Supabase | Faster, more scalable, no backend needed |

---

## Final Architecture (After All Changes)

```
┌─────────────────────────────────────────────────────────────────┐
│  USER BROWSER                                                    │
│  React + CesiumJS + zarrita.js + Supabase JS client             │
└────────────────────────────┬─────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼

┌─────────────────┐ ┌──────────────┐ ┌─────────────────────┐
│  VERCEL (free)   │ │ CLOUDFLARE R2 │ │  SUPABASE (free)    │
│  Frontend SPA    │ │ (free, 10 GB) │ │  (free, 500 MB)    │
│                  │ │               │ │                     │
│  React + Vite +  │ │ Zarr chunks   │ │ Argo/Glider metadata│
│  CesiumJS       │ │ (ocean data)  │ │ (Postgres + PostGIS)│
│                  │ │               │ │                     │
│  CDN-served      │ │ Zero egress   │ │ Direct JS client    │
│  vercel.app URL  │ │ S3-compatible │ │ supabase.co URL    │
└─────────────────┘ └───────────────┘ └─────────────────────┘
                             │
                             │ (browser fetches directly — no backend in hot path)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  RENDER (free) — compute only, not data storage                  │
│  Web Service (free, 512 MB RAM, 0.1 CPU)                        │
│  Spins down after 15 min idle (keep-warm via cron-job.org)      │
│  750 instance hours/month per workspace                         │
│                                                                  │
│  Endpoints:                                                      │
│  ├── /isosurface  → marching cubes (reads Zarr from R2)        │
│  ├── /opendap     → OPeNDAP (standards)                        │
│  └── /health      → health check                                │
│                                                                  │
│  Multi-account: Account 1 (compute) + Account 2 (ingest)       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Cost Evolution

| Stage | Architecture | Cost |
|---|---|---|
| Initial plan | Render only (Starter + disk) | $9.50/month |
| After split | Vercel free + Render paid | $9.50/month |
| Final (free tier) | Vercel + R2 + Supabase + Render free | **$0/month** |

---

## What Did NOT Change

These decisions remained constant throughout:

| Decision | Why it stayed |
|---|---|
| CesiumJS as globe engine | Best for geospatial accuracy + day/night + terrain |
| zarr-cesium for ocean rendering | Drop-in Cesium providers for Zarr |
| cesium-wind-layer for currents | GPU particle advection, 10k+ particles |
| Plotly.js for profile charts | Best for depth-vs-variable scientific plots |
| d3-scale-chromatic for colormaps | Scientific colormaps as GPU LUT |
| React + Vite + TypeScript | Used by all reference projects (DOVis, nordicseas3d) |
| Light theme | User requirement |
| GLORYS12 as primary dataset | INCOIS/Copernicus, 1/12° resolution, 50 depth levels |
| argopy for Argo ingestion | Purpose-built library, eliminates parsing pain |
| Vertical-slice MVP first | Proves complete workflow before full system |
