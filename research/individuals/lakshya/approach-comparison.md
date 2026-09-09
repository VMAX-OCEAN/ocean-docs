# Detailed Approach Comparison — What We Had vs What We Chose

Complete record of every approach we considered, what was bad about each, why we
rejected it, and why we shifted to the current plan. This is the full reasoning
behind every choice.

---

## Overview: The Evolution

Our plan went through **5 major shifts**. Each shift happened because the previous
approach had a fundamental problem:

| Shift | From | To | Reason |
|---|---|---|---|
| 1 | Hand-rolled Three.js globe | CesiumJS | Three.js can't do geospatial accurately |
| 2 | Single platform (Render only) | Split (Vercel + Render) | No single platform handles both frontend + backend well |
| 3 | Paid deployment ($9.50/mo) | Free tier ($0/mo) | User requested free only |
| 4 | Backend in hot path | No backend in hot path | R2 + Supabase eliminate the need |
| 5 | Commit to zarr-cesium blindly | De-risk first, then build | zarr-cesium is v0.1.4 — too new to trust blindly |

---

## Shift 1: Three.js Globe → CesiumJS

### What we had: Hand-rolled Three.js

The original `realistic-earth-globe.html` used:
- Three.js r128 from cdnjs
- `THREE.SphereGeometry(1, 96, 96)` — a unit sphere
- NASA Blue Marble texture from CDN
- Cloud texture from CDN
- Black background
- ~1,500 starfield points
- Additive atmosphere shader (fresnel approximation)
- Pointer-drag rotation + slow auto-rotation
- Camera at `(0, 0, 3.1)`

### Why it was bad

| Problem | Detail |
|---|---|
| **Wrong geometry** | A perfect sphere is wrong — Earth is an oblate spheroid (WGS84 ellipsoid). Argo/Glider markers placed at real lat/lon would be offset from the sphere surface. |
| **No terrain** | Flat sphere — no Himalayas, no ocean trenches. Can't show bathymetry. |
| **No imagery streaming** | One static JPG. Can't zoom from globe view to city level. |
| **No LOD** | One 96×96 sphere — no level-of-detail. Either too low-poly at zoom or too heavy at globe view. |
| **Fake day/night** | Would need a custom shader computing sun position (azimuth/elevation from date), dot product with surface normal, smoothstep for terminator. Error-prone — common bug is using view-space normals with world-space sun vector. |
| **Fake atmosphere** | Additive fresnel is a cheap approximation. Real atmosphere is Rayleigh + Mie scattering (volumetric). |
| **No geospatial system** | No coordinate system. Placing Argo floats, drawing bounding boxes, doing spatial queries — all would need to be built from scratch. |
| **No camera controls** | Pointer-drag rotation is not geospatial navigation. Real globe apps need fly-to-location, zoom-to-altitude, compass, etc. |
| **Not scalable** | Adding temperature overlays, depth slices, currents, particles — each would be a custom shader. Months of work. |

### What we chose: CesiumJS

CesiumJS provides all of the above for free:
- WGS84 ellipsoid (geospatially accurate)
- Cesium World Terrain (streamed, LOD)
- Bing/ArcGIS/MapTiler imagery (streamed, LOD)
- Quadtree LOD with Screen-Space Error
- `enableLighting = true` → real sun position, real terminator
- Built-in atmospheric scattering (Rayleigh + Mie)
- Full geospatial coordinate system (Cartographic, Cartesain, etc.)
- Camera controls (flyTo, lookAt, zoom, etc.)
- `CustomShader` API for custom rendering
- `ImageryProvider` API for custom overlays
- `Primitive` API for custom 3D objects

### Alternatives we considered

| Alternative | Why rejected |
|---|---|
| **Keep Three.js + build everything** | Months of work to replicate what CesiumJS gives for free. Geospatial math, terrain LOD, imagery streaming — all from scratch. |
| **Three.js + three-globe library** | three-globe is for data viz (arcs, bars on a globe), not geospatial accuracy. Still a sphere, still no terrain, still no real day/night. |
| **MapboxGL JS** | 2D map library with 3D terrain. Not a true 3D globe. Can't do ocean depth slices or volumetric rendering. |
| **Google Maps JS API** | Proprietary, rate-limited, no custom rendering pipeline, no WebGL access for ocean shaders. |
| **deck.gl** | Works with MapboxGL — 2D/3D layers but not a full globe. Good for overlays but not the globe itself. |
| **CesiumJS** ✅ | Everything we need, built for geospatial, free, open-source, well-documented. |

### The verdict
**Three.js was fundamentally the wrong tool.** It's a general 3D library, not a
geospatial engine. Building a geospatially accurate globe in Three.js is like
building a database in C — possible, but why would you when PostgreSQL exists?

---

## Shift 2: Single Platform → Split (Vercel + Render)

### What we had: Render only

Originally planned to deploy everything on Render:
- Frontend as a Render Static Site
- Backend as a Render Web Service
- Data on a Render Persistent Disk

### Why it was bad

| Problem | Detail |
|---|---|
| **Render Static Sites are slower** | Render's CDN is good but not as fast as Vercel's edge network for global static delivery. Cesium assets (~8 MB) would load slower for users far from the Render region. |
| **No preview deployments** | Render doesn't have Vercel's "every PR gets a unique URL" feature. For iterative development during SIH, preview URLs are very valuable. |
| **Coupling** | Frontend and backend on the same platform means a Render outage takes down everything. Splitting reduces risk. |
| **No framework detection** | Vercel auto-detects Vite and configures build settings. Render requires manual configuration. |

### What we chose: Vercel (frontend) + Render (backend)

| Concern | Vercel | Render |
|---|---|---|
| Static asset delivery | Edge CDN (fast globally) | Slower for static |
| SPA routing | Built-in (rewrites) | Works but less polished |
| Preview deployments | Every PR gets URL | Manual |
| Python server | Serverless (10-60s timeout, no disk) | Native Python + Docker |
| Persistent storage | No | Persistent disks (SSD) |

### Alternatives we considered

| Alternative | Why rejected |
|---|---|
| **Render for both** | Slower CDN, no preview deploys |
| **Vercel for both** | Vercel serverless can't run persistent Python with disk. 10-60s timeout too short for marching cubes. No persistent disk — SQLite/Zarr lost between invocations. Cold starts on every request. |
| **All on Railway** | No native Python runtime (Docker only). No Blueprint IaC. Smaller community. Usage-based pricing unpredictable. |
| **All on Fly.io** | Docker only. More complex setup. Free tier limited (shared CPU). No Blueprint. |
| **All on Heroku** | No free tier (ended 2022). More expensive than Render. Ephemeral filesystem (need S3). |
| **AWS (EC2 + S3 + CloudFront)** | Overkill for SIH demo. VPC, security groups, IAM — hours of setup. |
| **Vercel + Render** ✅ | Best of both: Vercel CDN for frontend, Render disk + Python for backend. |

### The verdict
**No single platform handles both frontend and backend well.** Vercel is best for
static/CDN, Render is best for Python+disk. Splitting is the natural choice.

---

## Shift 3: Paid ($9.50/mo) → Free ($0/mo)

### What we had: Render Starter + Persistent Disk

Originally planned:
- Vercel free (frontend) — $0
- Render Starter (backend) — $7/mo
- Render 10 GB persistent disk — $2.50/mo
- Total: $9.50/month

### Why it was bad

| Problem | Detail |
|---|---|
| **Cost** | User explicitly requested free tier only, no extra costs. $9.50/mo is not free. |
| **Persistent disk limits scaling** | A disk-attached service can only run one instance. No autoscaling. |
| **No zero-downtime deploy** | With a disk, Render can't do zero-downtime deploys. Brief downtime on each deploy. |
| **Disk can only grow** | Can increase size but never decrease. Pick wrong → wasted money. |
| **Single point of failure** | All data on one disk. If the instance dies, data is on the disk (safe) but the service is down. |

### What we chose: 100% Free Tier

| Service | Free Tier | What it does |
|---|---|---|
| Vercel | 100 GB bandwidth, unlimited static sites | Frontend CDN |
| Cloudflare R2 | 10 GB storage, **zero egress** | Zarr data (browser fetches directly) |
| Supabase | 500 MB Postgres | Argo/Glider metadata (browser queries directly) |
| Render | 750 hours/month, 512 MB RAM | Isosurface compute only |
| cron-job.org | Free cron | Keep Render warm |
| Cesium ion | Free terrain + imagery | Globe terrain |

**Total: $0/month**

### Alternatives we considered

| Alternative | Cost | Why rejected |
|---|---|---|
| **Render paid ($9.50/mo)** | $9.50/mo | Not free. User said no extra costs. |
| **Fly.io free** | $0 | Docker only, more complex, shared CPU may not handle xarray |
| **Railway** | $5/mo (usage-based) | Not free. Usage-based is unpredictable. |
| **Heroku** | $5/mo (eco) | Not free. No free tier anymore. |
| **AWS free tier** | $0 (12 months) | Free tier expires after 12 months. Complex setup. |
| **GCP free tier** | $0 (always free) | Complex setup. e2-micro instance too weak for xarray. |
| **Vercel + R2 + Supabase + Render free** ✅ | $0 | All permanent free tiers. No expiry. |

### The verdict
**The paid plan was unnecessary.** By moving data to R2 (zero egress) and Supabase
(direct browser access), we eliminated the need for a persistent backend disk. The
backend becomes compute-only (isosurface), which fits in Render's free 750 hours.

---

## Shift 4: Backend in Hot Path → No Backend in Hot Path

### What we had: Backend serves all data

Originally:
```
Browser → Render backend → Disk (Zarr + SQLite) → Backend → Browser
```

Every data request went through the backend:
- Zarr chunks: Browser → Backend → Disk → Backend → Browser
- Argo metadata: Browser → Backend → SQLite → Backend → Browser
- Isosurfaces: Browser → Backend → Marching cubes → Backend → Browser

### Why it was bad

| Problem | Detail |
|---|---|
| **Backend is a bottleneck** | Every chunk request goes through Python. 512 MB RAM on free tier can't handle many concurrent requests. |
| **Needs persistent disk** | Zarr + SQLite on disk = paid Render plan. Can't use free tier. |
| **Cold start penalty** | On free tier, backend spins down after 15 min. First request takes ~30s. Every data request is affected. |
| **Backend CPU bound** | Serving chunks is I/O bound but Python GIL limits parallelism. Many concurrent users → slow. |
| **Single point of failure** | Backend down = no data at all. |
| **Bandwidth costs** | All data flows through backend. Egress costs on paid Render. |

### What we chose: Direct browser-to-storage

```
Browser → R2 (Zarr chunks directly)     ← zero egress, ms latency, CDN
Browser → Supabase (metadata directly)   ← direct JS client, PostGIS
Browser → Render (only for isosurface)  ← occasional, cold start OK
```

### How this works

| Data | Before (backend proxy) | After (direct) |
|---|---|---|
| Zarr chunks | Browser → Backend → Disk → Browser | Browser → R2 (direct) |
| Argo metadata | Browser → Backend → SQLite → Browser | Browser → Supabase (direct) |
| Isosurfaces | Browser → Backend → Compute → Browser | Browser → Backend → Compute → Browser (same) |

### Alternatives we considered

| Alternative | Why rejected |
|---|---|
| **Keep backend proxy** | Needs paid disk. Backend is bottleneck. Cold start affects everything. |
| **Backend + CDN cache** | Still needs backend. CDN doesn't help with auth or dynamic queries. |
| **GraphQL gateway** | Still a backend. Same problems. |
| **Direct R2 + Supabase** ✅ | No backend in hot path. Faster. More scalable. Free. |

### The verdict
**The backend was solving a problem that doesn't exist.** R2 and Supabase are
designed for direct browser access. Adding a backend proxy in front of them adds
latency, cost, and a failure point for zero benefit.

---

## Shift 5: Blind Commit → De-Risk First

### What we had: Commit to zarr-cesium for all rendering

Originally planned to use zarr-cesium as a given:
- Use `ZarrLayerProvider` for SST/salinity/sea level
- Use `ZarrCubeProvider` for depth slices
- Use `ZarrCubeVelocityProvider` for currents (or cesium-wind-layer)
- Build the full platform on this assumption

### Why it was bad

| Problem | Detail |
|---|---|
| **zarr-cesium is v0.1.4** | Pre-1.0. API may change. Only 10 months old (created Nov 2025). |
| **Only 3 contributors** | Small team. If they abandon it, we're stuck. |
| **14 open issues** | Including projection bugs (EPSG3857). May affect our data. |
| **"Tested real data" only recently** | Release notes say "tested real data" in v0.1.2 (Nov 2025). Very little real-world usage. |
| **No fallback ready** | If we commit and it fails at Milestone 3, we lose weeks of work. |
| **cesium-wind-layer has compat issues** | Breaks with Cesium >= 1.127.0. Known Vite bundling bug. |

### What we chose: De-risk first (Phase 0)

**Phase 0 (1-2 days):** Build a minimal proof-of-concept:
1. Upload a small GLORYS Zarr to R2
2. Test `ZarrLayerProvider` — does SST render?
3. Test `ZarrCubeVelocityProvider` — do particles animate?
4. Test Supabase — do direct browser queries work?

**Decision tree:**
```
zarr-cesium works?
├── YES → Use it for everything (fastest path)
└── NO  → Fall back to custom ImageryProvider + zarrita.js (2-3 extra days)
```

### Alternatives we considered

| Alternative | Why rejected |
|---|---|
| **Commit to zarr-cesium blindly** | Too risky. v0.1.4, 14 issues, 3 contributors. Could waste weeks. |
| **Skip zarr-cesium, build custom** | May be unnecessary. zarr-cesium is designed for exactly our use case. Building custom first is over-engineering. |
| **Use cesium-wind-layer instead of zarr-cesium velocity** | Has known Cesium >= 1.127 compat bug. zarr-cesium's velocity provider may be better. |
| **De-risk first, then build** ✅ | 1-2 days to know if our primary library works. Fallbacks ready but not pre-built. |

### The verdict
**Blind commitment to a v0.1.4 library is irresponsible.** A 1-2 day proof-of-concept
is cheap insurance. If zarr-cesium works (likely — it's designed for this), we
proceed with confidence. If it fails, we catch it early and switch to the fallback.

---

## Decision Point 1: Data Format

### Choices we had

| Choice | Pros | Cons |
|---|---|---|
| **NetCDF direct** | Simple, standard in oceanography | File-level download, no chunk access, heavy, slow |
| **GRIB2** | Compact, used by weather | Hard to parse in browser, no JS library, sequential access |
| **OPeNDAP** | Subset access, standards | Server-mediated (needs backend), CPU bound, slower than Zarr |
| **Zarr** | Chunked, cloud-native, parallel reads, JS library (zarrita) | Needs conversion from NetCDF, chunking strategy matters |
| **HDF5** | Scientific standard | No browser library, server-mediated, no chunk streaming |
| **COG (Cloud Optimized GeoTIFF)** | Good for raster, browser support | 2D only, no time/depth dimensions, not for ocean volumes |

### What we chose: Zarr

### Why
- **40× faster** than OPeNDAP for time-series access (published benchmark)
- **zarrita.js** — solid TypeScript library (v0.7, well-maintained, FetchStore for HTTP)
- **S3-compatible** — works with R2, AWS, GCP
- **Chunked** — browser fetches only needed chunks (~100 KB each)
- **Multiscale** — ndpyramid generates LOD pyramids for zoom levels
- **Used by** Pangeo, nordicseas3d, zarr-cesium — proven in ocean viz

### Why not the others
- NetCDF/GRIB2/HDF5: No browser library, need backend to serve
- OPeNDAP: Needs backend, slower, CPU bound
- COG: 2D only, can't handle 4D ocean data (lat, lon, depth, time)

---

## Decision Point 2: Ocean Rendering Library

### Choices we had

| Choice | Pros | Cons |
|---|---|---|
| **zarr-cesium** | Purpose-built for Zarr + Cesium, 3 providers (scalar, cube, velocity), GPU rendering | v0.1.4, 10 months old, 14 issues, 3 contributors |
| **cesium-wind-layer** | GPU particles, 112 stars, active | Breaks with Cesium >= 1.127, only does wind/currents (not scalar) |
| **Custom ImageryProvider + zarrita** | Full control, no dependency | CPU-side rendering (Canvas 2D), slower, 2-3 days to build |
| **Custom Cesium Primitive + WebGL shader** | GPU rendering, full control | Most work (1-2 weeks), need to write GLSL shaders |
| **deck.gl + Zarr** | deck.gl is mature | Not a globe engine, needs Mapbox, 2D-focused |
| **earth.nullschool approach (D3 + Canvas)** | Proven, simple | 2D only, not 3D globe, CPU rendering, no depth |

### What we chose: zarr-cesium (with fallback to custom ImageryProvider)

### Why
- **Purpose-built** for exactly our use case (Zarr → Cesium)
- **Three providers** cover all our needs:
  - `ZarrLayerProvider` → SST, salinity, sea level
  - `ZarrCubeProvider` → depth slices, vertical sections
  - `ZarrCubeVelocityProvider` → current particles
- **GPU rendering** (WebGL, not Canvas 2D)
- **MIT licensed**, has demo, has docs
- **Developed by NOC** (National Oceanography Centre) — credible institution

### Why not the others
- cesium-wind-layer: Only does particles, not scalar fields. Has Cesium compat bug.
- Custom ImageryProvider: More work, CPU-side rendering. Good fallback but not first choice.
- Custom WebGL shader: Too much work (1-2 weeks) for the same result.
- deck.gl: Not a globe, needs Mapbox, 2D-focused.
- earth.nullschool: 2D Canvas, not 3D, no depth exploration.

### The fallback
If zarr-cesium fails in Phase 0, build a custom `ImageryProvider`:
1. Use `zarrita.js` FetchStore to read Zarr chunks from R2
2. Render to Canvas with d3-scale-chromatic colormap
3. Return Canvas as imagery tile to Cesium
4. ~2-3 days of work, CPU-side (slower but reliable)

---

## Decision Point 3: Database

### Choices we had

| Choice | Pros | Cons |
|---|---|---|
| **SQLite on Render disk** | Simple, file-based, no server | Needs paid disk, no direct browser access, needs backend |
| **Supabase (Postgres)** | Free 500 MB, PostGIS, direct browser access, JS client | Pauses after 1 week, 500 MB limit |
| **Render Postgres (free)** | Integrated with Render | Expires after 30 days, 1 GB, no PostGIS |
| **MongoDB Atlas (free)** | 512 MB, document store | No spatial index, overkill for tabular Argo data |
| **JSON files on R2** | Simple, free, no database | No spatial queries, slow for large datasets |
| **PlanetScale (free)** | MySQL, serverless | No PostGIS, no spatial index |

### What we chose: Supabase

### Why
- **Free 500 MB** Postgres — permanent, not 30-day expiry
- **PostGIS extension** — spatial R-tree index for bbox queries
- **Direct browser access** — `@supabase/supabase-js` queries from frontend, no backend
- **Auto REST API** — tables automatically exposed as REST endpoints
- **Auth built-in** — if we need user accounts later

### Why not the others
- SQLite: Needs paid disk, no browser access, needs backend proxy
- Render Postgres: Expires after 30 days (deletes data!) — unacceptable
- MongoDB: No spatial index, overkill for tabular data
- JSON on R2: No spatial queries, slow for 4000+ floats
- PlanetScale: No PostGIS

### Capacity check
- 4000 Argo floats × 100 profiles × (depth + temp + salinity arrays)
- As JSONB: ~480 MB — fits in 500 MB
- If tight: store only metadata in Supabase, profiles as JSON in R2

---

## Decision Point 4: Zarr Storage

### Choices we had

| Choice | Free Tier | Egress | S3-compatible | Why rejected/selected |
|---|---|---|---|---|
| **Render persistent disk** | No (paid) | N/A | No | Not free. Single instance only. |
| **Cloudflare R2** | 10 GB | **Zero** | Yes | ✅ Selected. Zero egress is critical. |
| **AWS S3** | 12 months only | $0.09/GB | Yes | Free tier expires. Egress costs. |
| **Google Cloud Storage** | 5 GB | $0.12/GB | Yes | Egress costs. Only 5 GB. |
| **Supabase Storage** | 1 GB | 5 GB included | No | Only 1 GB. Not S3-compatible. |
| **GitHub Releases** | 2 GB/file | Free | No | Good for static data, no API, no range requests. |
| **Backblaze B2** | 10 GB | $0.01/GB | Yes | Egress costs (not zero). |

### What we chose: Cloudflare R2

### Why
- **10 GB free** — enough for Indian Ocean GLORYS subset
- **Zero egress** — no bandwidth bills regardless of traffic (critical for a viz app that streams chunks)
- **S3-compatible** — zarrita.js FetchStore works directly, rclone/aws-cli for uploads
- **Public bucket** — browser fetches chunks directly via `https://pub-xxx.r2.dev/...`
- **CDN** — Cloudflare's edge network, fast globally

### Why not the others
- Render disk: Not free
- AWS S3/GCS: Egress costs (users loading chunks = bandwidth = money)
- Supabase Storage: Only 1 GB
- GitHub Releases: No range requests (Zarr needs byte-range requests for sharding)
- Backblaze B2: Egress costs (not zero)

---

## Decision Point 5: Frontend Hosting

### Choices we had

| Choice | Free Tier | CDN | Preview Deploys | Cesium Support |
|---|---|---|---|---|
| **Vercel** | 100 GB BW | Edge network | Every PR | Officially recommended by CesiumGS |
| **Render Static** | Yes | Good | No | Works |
| **Netlify** | 100 GB BW | Edge | Every PR | Works |
| **Cloudflare Pages** | Unlimited BW | Edge | Every PR | Works |
| **GitHub Pages** | 100 GB | GitHub CDN | No | Works but limited |

### What we chose: Vercel

### Why
- **CesiumGS officially recommends Vercel** (2025 tutorials: "Build a CesiumJS App with AI", "Build a Flight Simulator with CesiumJS")
- **Edge CDN** — fastest for Cesium's ~8 MB static assets
- **Preview deployments** — every PR gets a URL (critical for SIH iteration)
- **Vite framework detection** — auto-configures build
- **Free tier** — 100 GB bandwidth, unlimited static sites

### Why not the others
- Render Static: No preview deploys, slower CDN
- Netlify: Good but CesiumGS doesn't specifically recommend it
- Cloudflare Pages: Good but less documentation for Cesium
- GitHub Pages: No SPA routing support, limited

---

## Decision Point 6: Backend Hosting

### Choices we had

| Choice | Free Tier | Persistent Disk | Python | Always-on |
|---|---|---|---|---|
| **Render free** | 750 hrs/mo | No | Native + Docker | No (spins down 15 min) |
| **Fly.io free** | 3 VMs | Yes (volumes) | Docker only | No (spins down) |
| **Vercel serverless** | Yes | No | Python (serverless) | No (cold start every call) |
| **Railway** | $5 credit | Yes (volumes) | Docker only | Yes |
| **Heroku** | No | Yes (dynos) | Native + Docker | Yes (paid) |
| **AWS Lambda** | 1M calls | No | Python | No (cold start) |

### What we chose: Render free

### Why
- **750 free hours/month** — enough for keep-warm during working hours (310 hrs)
- **Native Python** — no Docker needed for basic FastAPI
- **Docker support** — if PyVista/VTK needs system deps
- **Health checks** — auto-restart on failure
- **Git-based** — push to GitHub → auto-deploy

### Why not the others
- Fly.io: Docker only, more complex, shared CPU may not handle xarray
- Vercel serverless: 10-60s timeout (too short for marching cubes), no disk, cold start every call
- Railway: Not free ($5 credit runs out)
- Heroku: No free tier
- AWS Lambda: No disk, cold start, 15 min timeout

### The limitation
Render free has no persistent disk. But we don't need one — the backend reads Zarr
from R2 (S3 API) and caches isosurfaces back to R2. No local storage needed.

---

## Decision Point 7: Current Visualization

### Choices we had

| Choice | Pros | Cons |
|---|---|---|
| **zarr-cesium ZarrCubeVelocityProvider** | Purpose-built for Zarr U/V, integrated with zarr-cesium | Same v0.1.4 risk as rest of zarr-cesium |
| **cesium-wind-layer** | 112 stars, GPU particles, active | Breaks with Cesium >= 1.127, only does particles |
| **Custom GPU particle shader** | Full control, no dependency | 1-2 weeks of GLSL work |
| **Custom Canvas 2D particles** | Simple, no dependency | CPU-side, slower, fewer particles |
| **Streamlines (static)** | Simple, no animation | Not animated, less engaging |

### What we chose: zarr-cesium velocity provider (fallback: cesium-wind-layer)

### Why
- **Integrated** with zarr-cesium — if zarr-cesium works for SST, velocity likely works too
- **Purpose-built** for Zarr U/V data — no data transformation needed
- **GPU rendering** — thousands of particles at 60fps

### Why not the others
- cesium-wind-layer: Known Cesium >= 1.127 compat bug (Vite alias fix exists but fragile)
- Custom GPU shader: 1-2 weeks of work, same result
- Canvas 2D: CPU-side, slower, fewer particles
- Static streamlines: Not animated, less engaging for demo

### Fallback chain
```
zarr-cesium velocity → cesium-wind-layer (with Vite fix) → custom GPU shader
```

---

## Summary: Every Choice, Every Alternative, Every Reason

| Decision | Chose | Rejected | Reason |
|---|---|---|---|
| Globe engine | CesiumJS | Three.js, MapboxGL, deck.gl, Google Maps | Geospatial accuracy, terrain, day/night, LOD |
| Data format | Zarr | NetCDF, GRIB2, HDF5, OPeNDAP, COG | Chunked, browser streaming, zarrita.js, 40× faster |
| Ocean rendering | zarr-cesium | cesium-wind-layer, custom shader, deck.gl, nullschool | Purpose-built, 3 providers, GPU rendering |
| Database | Supabase | SQLite, Render Postgres, MongoDB, PlanetScale | Free, PostGIS, direct browser access, no expiry |
| Zarr storage | Cloudflare R2 | Render disk, S3, GCS, B2, GitHub Releases | Free 10 GB, zero egress, S3-compatible |
| Frontend hosting | Vercel | Render, Netlify, Cloudflare Pages, GitHub Pages | CesiumGS recommended, edge CDN, preview deploys |
| Backend hosting | Render free | Fly.io, Vercel serverless, Railway, Heroku, Lambda | 750 free hrs, native Python, Docker support |
| Currents | zarr-cesium velocity | cesium-wind-layer, custom shader, Canvas 2D | Integrated, purpose-built, GPU rendering |
| Deployment cost | $0/mo (all free) | $9.50/mo (Render paid) | User requested free only |
| Architecture | No backend in hot path | Backend proxy for all data | R2 + Supabase direct, faster, scalable, free |
| Build strategy | De-risk first | Blind commit, build custom first | zarr-cesium v0.1.4 too new to trust blindly |

---

## What Made Each Previous Approach Bad

### Approach 1: Three.js globe (original)
**Bad because:** Wrong tool. Three.js is a 3D library, not a geospatial engine.
No terrain, no real day/night, no geospatial coordinates, no LOD, no imagery
streaming. Would take months to replicate what CesiumJS gives for free.

### Approach 2: Single platform (Render only)
**Bad because:** No single platform is best at both static CDN and Python+disk.
Render's CDN is slower than Vercel's. No preview deployments. Coupling frontend
and backend on one platform increases risk.

### Approach 3: Paid deployment ($9.50/mo)
**Bad because:** User explicitly requested free tier only. The paid disk was the
only reason for the cost — and we don't need it if data goes to R2 + Supabase.

### Approach 4: Backend in hot path
**Bad because:** Backend is a bottleneck (512 MB RAM, Python GIL). Needs paid
disk. Cold start affects every data request. Single point of failure. R2 and
Supabase are designed for direct browser access — proxying them adds cost and
latency for zero benefit.

### Approach 5: Blind commit to zarr-cesium
**Bad because:** zarr-cesium is v0.1.4, 10 months old, 3 contributors, 14 open
issues. Committing weeks of build time without testing first is irresponsible.
A 1-2 day proof-of-concept is cheap insurance.

---

## The Final Architecture (Why It's the Best)

```
Browser → Vercel (frontend, CDN, free)
Browser → R2 (Zarr chunks, zero egress, direct)
Browser → Supabase (metadata, PostGIS, direct)
Browser → Render (isosurface compute only, free, cold start OK)
```

**Why this is the best:**
1. **$0/month** — all permanent free tiers, no expiry
2. **No backend in hot path** — R2 + Supabase are direct, fast, scalable
3. **De-risked** — Phase 0 tests zarr-cesium before committing
4. **Each phase delivers something demoable** — early phases are strong SIH submission alone
5. **Fallbacks ready** — custom ImageryProvider, cesium-wind-layer, custom shader
6. **Scope discipline** — explicitly not doing OPeNDAP, full volume, glider/BGC, paid services
