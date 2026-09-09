# NetCDF to Zarr Conversion

The one-time data conversion pipeline and chunking strategy that enables fast
runtime streaming.

---

## Why Convert to Zarr

### Performance comparison (from research)

| Format | Access pattern | Performance |
|---|---|---|
| NetCDF4 | File-level download | Heavy download volumes, no parallel chunk access |
| OPeNDAP | Server-mediated subset | CPU/memory bound, slower than Zarr+S3 |
| Zarr over HTTP | Direct chunk access | 40× faster time-series access, ms latency, parallel reads |

Zarr stores each chunk as a separate object, enabling:
- **Direct chunk access** — fetch only the chunks you need
- **Parallel reads** — hundreds of concurrent chunk fetches
- **Millisecond latency** on HTTP/S3
- **Cloud-native** — no file system needed

---

## Conversion Pipeline

### One-time conversion script

```python
import xarray as xr
import zarr

def convert_glorys_to_zarr(netcdf_path, zarr_path):
    """Convert GLORYS NetCDF to Zarr with optimal chunking."""
    ds = xr.open_dataset(netcdf_path, chunks='auto')

    # Define chunking for each variable
    encoding = {
        'thetao': {'chunks': (1, 10, 540, 1080), 'compressor': zarr.Blosc('zstd', 3)},
        'so':     {'chunks': (1, 10, 540, 1080), 'compressor': zarr.Blosc('zstd', 3)},
        'uo':     {'chunks': (1, 10, 540, 1080), 'compressor': zarr.Blosc('zstd', 3)},
        'vo':     {'chunks': (1, 10, 540, 1080), 'compressor': zarr.Blosc('zstd', 3)},
        'zos':    {'chunks': (1, 540, 1080),     'compressor': zarr.Blosc('zstd', 3)},
    }

    ds.to_zarr(zarr_path, mode='w', encoding=encoding, consolidated=True)
    print(f"Converted {netcdf_path} → {zarr_path}")
```

### Chunk dimensions explained

For a 3D variable `temp[time, depth, lat, lon]`:

```
chunks: (1, 10, 540, 1080)
         │   │    │     │
         │   │    │     └── 1080 lon points (1/4 of global 4320)
         │   │    └────── 540 lat points (1/4 of global 2160)
         │   └────────── 10 depth levels (of 50)
         └────────────── 1 time step
```

One chunk ≈ 1 × 10 × 540 × 1080 × 4 bytes ≈ 23 MB uncompressed ≈ 2.3 MB compressed

---

## Dual Chunking Strategy

From the benchmark study (doi:10.1002/essoar.10511054.2):

- **Time-series access** (point queries, time animation) favors large time chunks +
  small spatial chunks
- **Map/slice access** (depth slices, spatial views) favors small time chunks +
  large spatial chunks

### Option A: Two Zarr stores

```python
# Time-series optimized (for point queries and animation)
ds.to_zarr('data/glorys/temp_ts.zarr', encoding={
    'thetao': {'chunks': (30, 50, 108, 216)}  # large time, small space
})

# Map/slice optimized (for depth slices and spatial views)
ds.to_zarr('data/glorys/temp_map.zarr', encoding={
    'thetao': {'chunks': (1, 10, 540, 1080)}  # small time, large space
})
```

### Option B: Balanced chunk (simpler)

```python
# Balanced — acceptable for both access patterns
ds.to_zarr('data/glorys/temp.zarr', encoding={
    'thetao': {'chunks': (1, 10, 540, 1080)}  # single time, moderate space
})
```

**Recommendation:** Start with Option B (balanced). If time animation is slow,
add Option A's time-series store.

---

## Multiscale (ndpyramid)

For zoom-dependent resolution, generate a multiscale Zarr pyramid using `ndpyramid`:

```python
from ndpyramid import PyramidFactory

factory = PyramidFactory(levels=4)
pyramid = factory.build(ds, levels=4)
pyramid.to_zarr('data/glorys/temp_pyramid.zarr')
```

This creates 4 zoom levels — the browser fetches coarser data when zoomed out,
finer data when zoomed in (like map tiles). zarr-cesium supports multiscale datasets
with automatic resolution selection.

---

## Consolidated Metadata

Always use `consolidated=True`:

```python
ds.to_zarr('data/glorys/temp.zarr', mode='w', consolidated=True)
```

This writes a single `.zmetadata` file with all metadata consolidated. The browser
reads this one small file first, then fetches only the chunks it needs — fast cold start.

---

## Compression

Use Blosc with zstd (good ratio + speed):

```python
import zarr
compressor = zarr.Blosc(cname='zstd', clevel=3, shuffle=zarr.Blosc.BITSHUFFLE)
```

| Compressor | Ratio | Speed | Use |
|---|---|---|---|
| zstd (level 3) | ~10:1 | Fast | Default |
| blosc-lz4 | ~5:1 | Very fast | If speed > ratio |
| gzip | ~10:1 | Slow | Avoid |

---

## Serving via xpublish

Once converted, serve via xpublish (which provides a Zarr REST API):

```python
from xpublish import Rest

ds = xr.open_zarr('data/glorys/temp.zarr', chunks='auto')
rest = Rest(datasets={'glorys_temp': ds})
rest.serve(host='0.0.0.0', port=8000)
```

The browser accesses chunks via:
```
GET /glorys_temp/zarr/thetao/0.1.2.3  →  binary chunk (2.3 MB)
```

zarrita.js in the browser handles the fetching and decoding.

---

## Conversion Script (full)

```python
#!/usr/bin/env python3
"""One-time conversion: GLORYS NetCDF → Zarr"""
import xarray as xr
import zarr
from pathlib import Path

NETCDF_DIR = Path('data/raw/glorys')
ZARR_DIR = Path('data/zarr/glorys')

compressor = zarr.Blosc(cname='zstd', clevel=3, shuffle=zarr.Blosc.BITSHUFFLE)

variables_3d = ['thetao', 'so', 'uo', 'vo']
variables_2d = ['zos', 'bottomT', 'mlotst']

for nc_file in sorted(NETCDF_DIR.glob('*.nc')):
    ds = xr.open_dataset(nc_file, chunks='auto')

    encoding = {}
    for var in variables_3d:
        if var in ds:
            encoding[var] = {'chunks': (1, 10, 540, 1080), 'compressor': compressor}
    for var in variables_2d:
        if var in ds:
            encoding[var] = {'chunks': (1, 540, 1080), 'compressor': compressor}

    zarr_path = ZARR_DIR / nc_file.stem
    ds.to_zarr(zarr_path, mode='w', encoding=encoding, consolidated=True)
    print(f"✓ {nc_file.name} → {zarr_path}")
```

Run once (or on schedule for new data). The Zarr store is then served by xpublish
and streamed by the browser.
