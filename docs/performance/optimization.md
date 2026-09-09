# Optimization Strategies

Strategies to keep the SIH-OCEAN platform fast at runtime.

---

## 1. Chunking Strategy (biggest lever)

### Dual chunking
Store two Zarr representations matching the two access patterns:

```python
# Time-series optimized (point queries, time animation)
chunks: (30, 50, 108, 216)  # large time, small space

# Map/slice optimized (depth slices, spatial views)
chunks: (1, 10, 540, 1080)  # small time, large space
```

The frontend uses the appropriate store based on the current operation.

### Chunk size tuning
- Too small: more I/O operations + lookup overhead
- Too large: more bandwidth per read
- Sweet spot: ~100 KB - 2 MB per chunk (compressed)

---

## 2. Caching

### Browser cache (HTTP)
Zarr chunks are served with `Cache-Control` headers. The browser caches them
automatically. Revisiting the same time/depth/region is instant.

```python
# xpublish / FastAPI cache headers
@app.get("/zarr/{var}/{chunk}")
async def get_chunk(var, chunk):
    response = Response(content=chunk_data)
    response.headers["Cache-Control"] = "public, max-age=86400"  # 24h
    return response
```

### Server-side isosurface cache
Marching cubes is expensive. Cache results by `(variable, value, time, bbox)`:

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def compute_isosurface(variable, value, time, bbox_hash):
    # Expensive marching cubes computation
    return mesh_data
```

### Cesium tile cache
CesiumJS caches terrain + imagery tiles in memory and (optionally) on disk.
Configure the cache size:

```js
viewer.scene.globe.tileCacheSize = 1000;  // tiles in memory
```

---

## 3. Prefetch

### Time animation prefetch
When playing a time animation, prefetch the next few time chunks while rendering
the current one:

```js
function animateTime() {
  if (!isPlaying) return;

  // Render current time
  sstLayer.setTime(currentTime);

  // Prefetch next 3 timesteps
  for (let i = 1; i <= 3; i++) {
    prefetchChunk(currentTime + i * timeStep);
  }

  setTimeout(animateTime, 200);
}
```

### Camera flight prefetch
When the camera is flying to a new location, prefetch tiles for the destination
(Cesium does this automatically).

---

## 4. GPU Optimization

### Colormap as LUT (not per-pixel JS)
The colormap is a 1D texture (LUT) sampled in the fragment shader. Changing
palette/min/max/log is a shader uniform update — instant, no re-fetch.

### Particle advection on GPU
Current particles are computed entirely on GPU (ping-pong textures). No CPU
overhead per frame. 10,000+ particles at 60 FPS.

### Vertical exaggeration as shader uniform
Changing vertical exaggeration is a shader uniform — no geometry re-build.

---

## 5. Level of Detail (LOD)

### Cesium terrain/imagery LOD
CesiumJS automatically selects the appropriate LOD based on camera distance
(Screen-Space Error). Far views use coarse tiles; zoomed views use fine tiles.

### Zarr multiscale (ndpyramid)
For ocean data, generate a multiscale Zarr pyramid:

```python
from ndpyramid import PyramidFactory
factory = PyramidFactory(levels=4)
pyramid = factory.build(ds, levels=4)
pyramid.to_zarr('data/glorys/temp_pyramid.zarr')
```

zarr-cesium supports multiscale datasets with automatic resolution selection —
coarse data when zoomed out, fine data when zoomed in.

---

## 6. Lazy Loading

### Zarr metadata only on startup
xarray/xpublish opens Zarr lazily — only metadata is loaded, not data. Data is
fetched on-demand when a chunk is requested.

### Argo markers in view only
Only query SQLite for markers in the current view bbox:

```sql
SELECT * FROM floats_rtree
WHERE min_lat >= :south AND max_lat <= :north
  AND min_lon >= :west AND max_lon <= :east;
```

This returns only visible markers — fast even with 4000+ floats globally.

---

## 7. Compression

### Zarr chunk compression
Use Blosc with zstd (good ratio + speed):

```python
compressor = zarr.Blosc(cname='zstd', clevel=3, shuffle=zarr.Blosc.BITSHUFFLE)
```

- Ratio: ~10:1 for ocean data
- Decompression: fast (browser-side via zarrita.js)

### KTX2 for textures (if using 3D Tiles)
Cesium supports KTX2 + ETC1S compression for textures:
- 10-30% smaller
- 30% faster loading
- 80% less GPU memory

---

## 8. Request Batching

### Parallel chunk fetches
zarrita.js fetches chunks in parallel (browser handles HTTP/2 multiplexing):

```js
// Fetch 4 depth chunks in parallel
const chunks = await Promise.all([
  fetchChunk(depth=0),
  fetchChunk(depth=100),
  fetchChunk(depth=500),
  fetchChunk(depth=1000)
]);
```

### Request prioritization
Prioritize chunks for the center of the screen over edges (Cesium does this
automatically for terrain/imagery).

---

## 9. Progressive Rendering

### Render available data first
Don't wait for all chunks before rendering. Render with available data, then
update as chunks arrive:

```js
sstLayer.setProgressiveRender(true);
// Shows coarse data immediately, refines as chunks load
```

---

## Summary

| Strategy | Impact | Effort |
|---|---|---|
| Dual chunking | High (40× for time-series) | Medium |
| Browser cache | High (instant repeat access) | Low |
| Isosurface cache | High (50ms vs 500ms) | Low |
| Time prefetch | Medium (smooth animation) | Low |
| GPU shaders (colormap) | High (instant changes) | Low |
| GPU particles | High (60 FPS vs 5 FPS) | Medium |
| Multiscale Zarr | Medium (zoom-dependent) | Medium |
| Lazy loading | High (fast startup) | Low |
| Compression | High (10:1 ratio) | Low |
| Parallel fetches | Medium (HTTP/2) | Low |
