# GLORYS12 Dataset — Global Ocean Physics Reanalysis

The primary ocean model output dataset for SIH-OCEAN.

---

## Product Details

| Property | Value |
|---|---|
| Product ID | GLOBAL_MULTIYEAR_PHY_001_030 |
| Product name | GLORYS12V1 |
| Source | Copernicus Marine Service |
| Spatial extent | Global (180°E to 180°E; 89°S to 90°N) |
| Spatial resolution | 1/12° (≈8 km) equirectangular grid |
| Vertical levels | 50 standard levels |
| Temporal extent | 01/01/1993 to present (M-1) |
| Temporal resolution | Daily mean + Monthly mean + Monthly climatology |
| Format | NetCDF CF1.4 |
| Update frequency | Yearly |

**Link:** https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description

---

## Datasets (3 sub-datasets)

| Dataset ID | Description |
|---|---|
| `cmems_mod_glo_phy_my_0.083deg_P1D-m` | 3D daily mean fields (temp, salinity, currents) + 2D surface/bottom/ice |
| `cmems_mod_glo_phy_my_0.083deg_P1M-m` | Monthly mean fields |
| `cmems_mod_glo_phy_my_0.083deg-climatology_P1M-m` | Monthly climatology (1993-2016 average) |

---

## Variables

### 3D Variables (depth-resolved)

| Variable | CF name | Unit | Description |
|---|---|---|---|
| Temperature | `thetao` | °C | Sea water potential temperature |
| Salinity | `so` | PSU | Sea water salinity |
| Eastward current | `uo` | m/s | Eastward sea water velocity |
| Northward current | `vo` | m/s | Northward sea water velocity |

> No vertical-velocity variable exists in `GLOBAL_MULTIYEAR_PHY_001_030` (PUM Table 2, product metadata). Only `uo`/`vo`. True 3D particle trajectories need `w`, which this product does not provide — per `revised-master-plan.md` scope table.

### 2D Variables (surface)

| Variable | CF name | Unit | Description |
|---|---|---|---|
| Sea surface height | `zos` | m | Sea surface height above geoid |
| Bottom temperature | `bottomT` | °C | Sea water potential temperature at sea floor |
| Mixed layer depth | `mlotst` | m | Ocean mixed layer thickness |
| Sea ice fraction | `siconc` | — | Sea ice area fraction |
| Sea ice thickness | `sithick` | m | Sea ice thickness |
| Sea ice velocity | `usi`, `vsi` | m/s | Sea ice velocity |
| Sea floor depth | `bathymetry` | m | Sea floor depth below geoid |

---

## Size Estimation

### One 3D variable, one timestep

```
Grid: 4320 (lon) × 2160 (lat) × 50 (depth) × 4 bytes = 1,866,240,000 bytes
     ≈ 1.86 GB uncompressed
     ≈ 186 MB compressed (10:1 with zstd)
```

### Full daily dataset (all 3D vars, all time)

```
~5 3D variables × 1.86 GB × 12,000+ days ≈ 111 TB uncompressed
≈ 11 TB compressed
```

### Monthly dataset (smaller)

```
~5 3D variables × 1.86 GB × 400 months ≈ 3.7 TB uncompressed
```

**Conclusion:** Cannot load-and-serve naively. Must subset + convert to Zarr + stream.

---

## Conversion to Zarr

### One-time conversion

```python
import xarray as xr

# Open NetCDF (lazy — only metadata in memory)
ds = xr.open_dataset('glorys_daily_2026.nc', chunks='auto')

# Convert to Zarr with chunking
ds.to_zarr(
    'data/glorys/temp.zarr',
    mode='w',
    encoding={
        'thetao': {'chunks': (1, 10, 540, 1080)},  # (time, depth, lat, lon)
        'so':     {'chunks': (1, 10, 540, 1080)},
        'uo':     {'chunks': (1, 10, 540, 1080)},
        'vo':     {'chunks': (1, 10, 540, 1080)}
    }
)
```

### Chunking Strategy

See [`netcdf-to-zarr.md`](netcdf-to-zarr.md) for the dual-chunking strategy.

---

## Access via Copernicus

### Subset API (recommended for samples)

```python
import copernicusmarine

copernicusmarine.subset(
    dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
    variables=["thetao", "so", "uo", "vo"],
    minimum_longitude=60, maximum_longitude=100,  # Indian Ocean
    minimum_latitude=5, maximum_latitude=30,
    start_datetime="2026-01-01",
    end_datetime="2026-01-31",
    output_filename="glorys_indian_ocean_jan2026"
)
```

### OPeNDAP access

```
https://data.marine.copernicus.eu/thredds/dodsC/cmems_mod_glo_phy_my_0.083deg_P1D-m
```

---

## Indian Ocean Subset

For the SIH demo, focus on the Indian Ocean (INCOIS's domain):

| Bound | Value |
|---|---|
| Longitude | 60°E to 100°E |
| Latitude | 5°S to 30°N |
| Depth | 0 to 5000 m (all 50 levels) |
| Time | 2026 (recent year) |

This subset is much smaller and manageable for development.
