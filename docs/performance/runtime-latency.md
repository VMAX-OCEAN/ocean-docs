# Runtime Latency

Expected runtime latency for each operation in the SIH-OCEAN platform.

---

## Operation Latency Table

| Operation | Latency | Why |
|---|---|---|
| Globe render (terrain/imagery) | 60 FPS | Cesium LOD streaming — only visible tiles fetched |
| Day/night terminator | 0 cost | Shader calculation, no data fetch |
| Atmosphere | 0 cost | Shader calculation |
| Sun/moon position | 0 cost | Astronomy calc in Cesium |
| SST overlay load (first) | ~200ms | One Zarr chunk for view bbox (~100 KB) |
| SST overlay load (cached) | instant | Browser cache hit |
| Depth slice change | ~100ms | One Zarr chunk for new depth |
| Time step animation (per frame) | ~150ms | One Zarr time chunk, re-texture |
| Colormap change | **instant** | Shader uniform, no re-fetch |
| Opacity change | **instant** | Shader uniform |
| Vertical exaggeration change | **instant** | Shader uniform |
| Variable change (e.g., temp to salinity) | ~200ms | New Zarr store, first chunk |
| Current particles (render) | 60 FPS | GPU ping-pong textures, no CPU |
| Current particles (init) | ~300ms | Upload velocity textures to GPU |
| Isosurface (first request) | ~500ms | Server marching cubes + transfer |
| Isosurface (cached) | ~50ms | Cache hit |
| Argo marker query (bbox) | ~10ms | SQLite R-tree query |
| Argo profile (click marker) | ~10ms | SQLite indexed lookup |
| Profile chart render (Plotly) | ~50ms | Plotly render |

---

## Cold Start (first page load)

| Step | Time | Notes |
|---|---|---|
| HTML + JS bundle | ~500ms | Vite-optimized bundle |
| CesiumJS init | ~300ms | Library initialization |
| Terrain provider | ~200ms | Connect to Cesium ion |
| First terrain tiles | ~500ms | Initial view tiles |
| First imagery tiles | ~500ms | Initial view imagery |
| Zarr metadata | ~100ms | Consolidated .zmetadata (small) |
| First SST chunk | ~200ms | View bbox chunk |
| **Total to first paint** | **~2-3s** | Acceptable for a data viz platform |

After first paint, all subsequent operations are fast (chunk streaming + shader updates).

---

## Concurrency Scaling

| Users | Performance | Bottleneck |
|---|---|---|
| 1-10 | Excellent | None — browser fetches chunks directly |
| 10-100 | Excellent | Zarr chunks served as static files (nginx/CDN) |
| 100-1000 | Good | May need CDN for Zarr chunks |
| 1000+ | Scale with infrastructure | Add S3/CDN for Zarr storage |

**Key:** Because Zarr chunks are served as static files (via xpublish Zarr REST or
directly from S3/CDN), they scale horizontally without server CPU bottleneck. This is
unlike OPeNDAP, where every request hits server CPU.

---

## Bandwidth Estimation

| Operation | Data transferred | Notes |
|---|---|---|
| SST chunk (one timestep, view bbox) | ~100 KB | Compressed Zarr chunk |
| 3D temp chunk (one depth, view bbox) | ~100 KB | One slice of the cube |
| Full 3D cube (all depths, view bbox) | ~2 MB | 50 depth levels x 100 KB |
| Current u/v chunks | ~200 KB | Two variables |
| Argo markers (view bbox) | ~10 KB | JSON metadata |
| Argo profile (one float) | ~5 KB | Depth + temp array |
| Isosurface mesh | ~500 KB | Vertices + faces |

**Per-frame during animation:** ~100-300 KB (one or two chunks) — very lightweight.

---

## Comparison: Our Approach vs Alternatives

| Approach | First load | Animation | Colormap change | Concurrency |
|---|---|---|---|---|
| **Our (Zarr + GPU shaders)** | 2-3s | 150ms/frame | instant | 100s of users |
| OPeNDAP-only | 5-10s | 500ms+ (server CPU) | instant | limited by server |
| Full NetCDF download | 30s+ (GB download) | instant (local) | instant | 1 user |
| 3D Tiles (pre-baked) | 2-5s | instant (cached) | instant | 100s (static files) |

Our approach matches 3D Tiles performance for static data while being far more
flexible (any subset, any time, any variable — no preprocessing).
