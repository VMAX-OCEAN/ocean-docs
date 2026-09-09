# Backend Strategy

Comparison of backend strategies and the recommendation for SIH-OCEAN.

---

## The Constraint That Decides Everything

### Dataset Reality Check

| Dataset | Size | Structure | Implication |
|---|---|---|---|
| GLORYS12 (Copernicus) | 1/12° grid (~8 km), 50 depth levels, 1993–2026 daily + monthly | One 3D var/timestep ≈ 4320×2160×50 × 4 bytes ≈ 1.86 GB uncompressed (~186 MB compressed). Decades of daily 3D fields = petabyte-scale | Cannot load-and-serve naively. Must subset + convert to chunked format + stream |
| Argo GDAC | 931 GB total, 423 GB dac, 3.5M NetCDF files, ~4000 active floats, 3M+ profiles, 100k profiles/yr | Per-float `_prof.nc` files (N_PROF × N_LEVELS) | Point/profile data — small per-float, huge in aggregate. Needs indexing, not bulk load |
| Glider (ifremer ftp) | Similar NetCDF profile structure | Trajectory profiles | Same handling as Argo |

**Conclusion:** Any backend that loads full NetCDF files into memory per request will
fail on GLORYS. The architecture must be chunk-streamed.

---

## Strategy Comparison

### A. Zarr Streaming (browser-direct)

**How:** Pre-convert NetCDF → Zarr once. Browser streams chunks directly via zarrita.js.
No server CPU per read.

| Criterion | Rating |
|---|---|
| Runtime latency (volumetric reads) | Best — ms chunk fetch, no server CPU per read, parallel |
| Cold start / first paint | Fast — tiny consolidated `.zmetadata`, then chunks stream |
| Concurrency scaling | Hundreds of parallel chunk reads |
| Standards compliance (OGC/OPeNDAP) | Zarr is OGC-standard-in-progress, not OPeNDAP |
| Preprocessing cost | One-time NetCDF→Zarr conversion |
| Proven for this problem | nordicseas3d, zarr-cesium |

### B. FastAPI + SQLite + 3D Tiles (DOVis pattern)

**How:** NetCDF → SQLite, server generates 3D tiles on demand.

| Criterion | Rating |
|---|---|
| Runtime latency | Server computes tiles per request (CPU-bound) |
| Cold start | SQLite open fast, but tile-gen adds latency |
| Concurrency scaling | Server CPU bottleneck under many users |
| Standards compliance | Custom REST, not standard |
| Preprocessing cost | One-time NetCDF→SQLite + on-demand tile gen |
| Proven for this problem | DOVis (Indian Ocean DO) |

### C. Full OPeNDAP (PyDAP/xpublish)

**How:** Standards-compliant OPeNDAP server.

| Criterion | Rating |
|---|---|
| Runtime latency | Server CPU/memory bound, slower than Zarr+S3 |
| Cold start | Depends; xpublish lazy-loads metadata |
| Concurrency scaling | OPeNDAP servers bottleneck (NCEI study) |
| Standards compliance | Best — native OPeNDAP/WCS interop with INCOIS portals |
| Preprocessing cost | Minimal (lazy) |
| Proven for this problem | OPeNDAP is the legacy standard |

---

## Recommendation: Hybrid — xpublish

Use `xpublish` (FastAPI under the hood). It serves xarray datasets via:

- A **Zarr-compatible REST API** (browser streams chunks directly via `zarrita.js` —
  millisecond latency, no per-read server CPU)
- An **OPeNDAP plugin** (`xpublish-opendap`) for standards compliance with INCOIS/national portals
- Custom FastAPI endpoints for profiles, isosurfaces, metadata (SQLite-backed for
  marker lookups at ~10 µs)

### Why This Wins on Runtime

The heaviest data (volumetric 3D fields) bypasses server compute entirely — the browser
fetches only the Zarr chunks it needs, in parallel, with ms latency. The server only
does lightweight metadata/profile work and the occasional isosurface (which can be
cached). OPeNDAP is still available for standards compliance without being the hot path.

### Data Flow

```
GLORYS NetCDF ──(one-time)──► Zarr store (chunked: time-series & map access patterns)
Argo/Glider NetCDF ──(argopy)──► SQLite (metadata + profiles index)
                    │
                    ▼
        xpublish (FastAPI)  ──► Zarr REST chunks ──► browser (zarrita.js) ──► zarr-cesium providers
                             ──► OPeNDAP endpoints (standards)
                             ──► /profile, /isosurface (server compute, cached)
```

---

## Chunking Strategy (the biggest runtime lever)

From the benchmark study (doi:10.1002/essoar.10511054.2):

- **Time-series access** favors large time chunks + small spatial chunks
- **Map/slice access** favors small time chunks + large spatial chunks
- Smaller chunks = more I/O operations + lookup overhead
- Larger chunks = more data transferred per read

**Recommendation:** Store two Zarr representations:
1. **Time-series optimized** — for point queries and time animation
2. **Map/slice optimized** — for depth slices and spatial views

Or pick a balanced chunk and accept the tradeoff. The chunking strategy must match
the access pattern.

---

## xpublish Setup (planned)

```python
from xpublish import Rest
from xpublish_opendap import OpenDapPlugin
import xarray as xr

# Load GLORYS data (lazy — only metadata in memory)
ds = xr.open_zarr('data/glorys_temp.zarr', chunks='auto')

# Create xpublish server with OPeNDAP plugin
rest = Rest(
    datasets={'glorys_temp': ds},
    plugins=[OpenDapPlugin]
)

# Serve
rest.serve(host='0.0.0.0', port=8000)
```

### Endpoints (automatic + custom)

| Endpoint | Purpose |
|---|---|
| `/glorys_temp/zarr/.zmetadata` | Zarr metadata (browser reads this first) |
| `/glorys_temp/zarr/var/0.0.0` | Zarr chunk (browser streams on demand) |
| `/glorys_temp/opendap/...` | OPeNDAP access (standards compliance) |
| `/glorys_temp/keys` | Variable keys |
| `/glorys_temp/info` | Dataset summary |
| `/argo/floats?bbox=...` | Custom: Argo markers in view (SQLite) |
| `/argo/profile?float_id=X&variable=temp` | Custom: depth profile (SQLite) |
| `/isosurface?variable=temp&value=20&t=...` | Custom: marching cubes isosurface (cached) |
