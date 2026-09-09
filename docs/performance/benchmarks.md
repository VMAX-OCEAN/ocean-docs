# Performance Benchmarks

Research-backed performance data that informed our architecture decisions.

---

## Zarr vs OPeNDAP vs NetCDF

### Source: "Big Arrays, Fast: Profiling Cloud Storage Read Throughput" (doi:10.1002/essoar.10508824.2)

| Protocol | Throughput | Scaling | Notes |
|---|---|---|---|
| Zarr over HTTP + S3 | Highest | Hundreds of parallel reads | Cloud-object-storage optimized |
| NetCDF over HTTP (h5py) | Moderate | Limited by file structure | Multiple chunks per file |
| OPeNDAP | Lower | Server CPU/memory bound | Established but slower |

**Key finding:** Zarr over HTTP, coupled with cloud object storage, shows favorable
scaling up to hundreds of parallel processes.

---

## Zarr Chunk Latency

### Source: AWS Public Sector Blog — "Decrease geospatial query latency from minutes to seconds using Zarr on Amazon S3"

> "Using Zarr with Amazon S3 enables chunk access with **millisecond latency**.
> Chunk reads and writes can run in parallel and be scaled as needed."

- ERA5 dataset (hourly, 31 km grid, multiple altitudes): Zarr queries for 1-13 years
  of historical data completed in **seconds** vs minutes for file-based access

---

## Zarr vs GRIB2

### Source: Gowan et al. 2022 (referenced in chunk-size study)

> "Zarr was significantly more efficient (e.g., **40× faster time-series access**)
> than GRIB2 on both smaller and high-performance computing nodes."

---

## Chunk Size Impact

### Source: "Impact of Chunk Size on Read Performance of Zarr Data" (doi:10.1002/essoar.10511054.2)

| Access pattern | Optimal chunking | Why |
|---|---|---|
| Time-series (point query) | Large time chunks, small spatial | Fewer I/O ops per time step |
| Map/slice (spatial view) | Small time chunks, large spatial | Fewer I/O ops per spatial region |
| Smaller chunks | More I/O operations + lookup overhead | Slower per access |
| Larger chunks | More data transferred per read | Faster per access, more bandwidth |

**Conclusion:** Chunking strategy must match the access pattern. Store two Zarr
representations if both access patterns are common.

---

## OPeNDAP Server Performance

### Source: NCEI "Gridded Environmental Data in the Cloud" (doi:10.6084/m9.figshare.14983956.v1)

> "Traditional OPeNDAP servers may be less efficient tools for data dissemination
> than Zarr in S3, especially when used with Dask."

> "CPU and memory limitations of Fargate containers in EKS may bottleneck OPeNDAP
> server performance."

| Server | Performance | Notes |
|---|---|---|
| THREDDS | CPU/memory bound | Well-established, on-premises |
| Hyrax | CPU/memory bound | Java-based |
| ERDDAP | CPU/memory bound | Popular for ocean data |
| ZarrDAP (NCEI custom) | Better | Python/Flask, handles Zarr in S3 |

---

## Cesium 3D Tiles Performance

### Source: Cesium blog — "Up to 10x Faster 3D Tiles Streaming"

| Metric | Improvement |
|---|---|
| Load speed | 2× to 10× faster (CesiumJS 1.57+) |
| Tiles loaded | 27% to 53% fewer tiles on average |
| Priority system | Visually significant tiles load first |
| Camera flight preload | Tiles ready by the time camera arrives |

### 3D Tiles generation cost

| Source data | Tiling time | Tileset size | Avg load time |
|---|---|---|---|
| AGI HQ (small) | 0:52 | 61 MB | 2.54s |
| Osaka (medium) | 26:08 | 1.74 GB | 3.97s |
| Space Shuttle (large) | 1:31:39 | 1.61 GB | 2.37s |

**Note:** zarr-cesium streams on-demand with **no preprocessing/conversion** — avoids
this tiling cost entirely.

---

## SQLite Spatial Query Performance

### Source: sqlitegis benchmarks (LucaCappelletti94/sqlitegis)

| Workload | sqlitegis | SpatiaLite | Ratio |
|---|---|---|---|
| ST_Intersects (bulk, unindexed) | 5.53 ms | 8.95 ms | 1.62× |
| ST_Intersects (window, R-tree) | **10.69 µs** | 13.10 µs | 1.23× |
| ST_Contains (window, R-tree) | 10.83 µs | 13.07 µs | 1.21× |
| ST_DWithin (bulk) | 31.10 ms | 39.07 ms | 1.26× |

**Key:** R-tree-prefiltered spatial queries are ~10 µs — excellent for marker lookups.

---

## Google Earth Threading Performance

### Source: Google Earth blog — "Performance of WebAssembly: A thread on threading"

> "Fetching and decompressing data on background threads allows the main rendering
> loop to execute much faster, resulting in higher average framerate."

- With threads: significantly higher average framerate
- With threads: much less frame dropping
- Without threads: severe frame dropping during camera movement

**Lesson:** Background-thread decode is essential for smooth streaming. Our browser
fetch + zarrita.js decode happens off the main render loop (async fetch).

---

## Summary: Why Our Architecture Is Fast

| Our choice | Performance reason | Source |
|---|---|---|
| Zarr (not NetCDF direct) | 40× faster time-series access, ms chunk latency | Gowan 2022, AWS blog |
| Zarr (not OPeNDAP-only) | OPeNDAP is CPU/memory bound; Zarr streams direct | NCEI study |
| zarr-cesium (not 3D Tiles) | No preprocessing; on-demand streaming | Cesium blog |
| SQLite + R-tree (for markers) | 10 µs spatial queries | sqlitegis benchmarks |
| GPU shaders (for colormaps) | Instant changes, no re-fetch | nullschool/Cesium |
| GPU particle advection (for currents) | 10k+ particles at 60 FPS | cesium-wind-layer |
| Dual chunking (time + map) | Optimal for both access patterns | Chunk-size study |
