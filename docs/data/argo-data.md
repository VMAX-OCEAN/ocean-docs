# Argo Float Data

Argo profiling float data — temperature and salinity profiles from the upper 2000 m
of the global ocean.

---

## Program Overview

| Property | Value |
|---|---|
| Active floats | ~4,000 (as of 2025) |
| Total profiles | 3+ million (since 1999) |
| Profiles per year | ~100,000 |
| Depth range | 0 to 2000 m |
| Variables | Temperature, salinity (core); oxygen, chlorophyll, etc. (BGC) |
| Data latency | 94% shared within 24 hours |
| Format | NetCDF (CF-1.6, Argo-3.1 conventions) |
| Total GDAC size | 931 GB (3.5M NetCDF files) |

**Source:** ftp://ftp.ifremer.fr/ifremer/argo

---

## Data Structure

### Per-float files

Each float has multiple NetCDF files:

| File | Contents |
|---|---|
| `<WMO>_prof.nc` | All profiles for this float (N_PROF × N_LEVELS) |
| `<WMO>_Rtraj.nc` | Trajectory data |
| `<WMO>_meta.nc` | Metadata |
| `<WMO>_tech.nc` | Technical data |
| `<WMO>_Sprof.nc` | Synthetic profiles (BGC) |

### Profile file dimensions

```
Dimensions:
  N_PROF:    104    (number of profiles)
  N_PARAM:   3      (parameters: temp, sal, pressure)
  N_LEVELS:  98     (depth levels)
  N_CALIB:   1
  N_HISTORY: 0
```

### Key variables

| Variable | Description |
|---|---|
| `LATITUDE` | Float latitude per profile |
| `LONGITUDE` | Float longitude per profile |
| `JULD` | Julian day of profile |
| `PRES` | Pressure (depth proxy, 1 dbar ≈ 1 m) |
| `TEMP` | Temperature (°C) |
| `PSAL` | Practical salinity |
| `DOXY` | Dissolved oxygen (BGC floats) |
| `CYCLE_NUMBER` | Profile cycle number |

---

## Ingestion with argopy

argopy is a Python library purpose-built for Argo data access and manipulation.

### Load a float's profiles

```python
from argopy import ArgoFloat

# Load all profiles for a float
ds = ArgoFloat(6901254).open_dataset('prof')
# → xarray.Dataset with N_PROF × N_LEVELS
```

### Fetch by region/time

```python
from argopy import DataFetcher

# Fetch Argo data for Indian Ocean, 2026
ds = DataFetcher().region(
    [-90, 30, 180, 90,        # lon_min, lat_min, lon_max, lat_max
     '2026-01-01', '2026-12-31']
).to_xarray()
```

### List floats in a region

```python
from argopy import ArgoIndex

# Get index of floats in Indian Ocean
idx = ArgoIndex().search_lat_lon([-90, 30, 180, 90])
df = idx.to_dataframe()
# → DataFrame with float WMO, lat, lon, date, profile count
```

---

## Ingestion Pipeline

```
ifremer FTP (3.5M NetCDF files)
   │
   ▼ argopy
ArgoIndex (float metadata: WMO, lat, lon, date)
   │
   ├──► SQLite: floats table (WMO, lat, lon, date, cycle, variables)
   │    + R-tree spatial index for fast bbox queries
   │
   └──► SQLite: profiles table (WMO, cycle, depth, temp, sal, doxy)
        indexed by (WMO, cycle) for fast profile lookup
```

### SQLite Schema

```sql
-- Floats metadata (for marker rendering)
CREATE TABLE floats (
  wmo INTEGER,
  cycle INTEGER,
  latitude REAL,
  longitude REAL,
  date TEXT,
  variables TEXT  -- 'temp,sal,doxy'
);

-- R-tree spatial index for bbox queries
CREATE VIRTUAL TABLE floats_rtree USING rtree(
  wmo, min_lat, max_lat, min_lon, max_lon
);

-- Profiles (for depth-vs-variable charts)
CREATE TABLE profiles (
  wmo INTEGER,
  cycle INTEGER,
  depth REAL,
  temperature REAL,
  salinity REAL,
  oxygen REAL
);
CREATE INDEX idx_profiles ON profiles(wmo, cycle);
```

### Query performance

- `ST_Intersects` bbox query with R-tree: ~10 µs
- Profile lookup by (wmo, cycle): ~10 µs

---

## BGC-Argo

Biogeochemical Argo floats add:
- Dissolved oxygen (`DOXY`)
- Chlorophyll-a (`CHLA`)
- Nitrate (`NITRATE`)
- pH
- Particulate backscattering (`BBP700`)

BGC snapshot tarball: ~50 GB (vs 931 GB for full GDAC)

---

## INCOIS Argo DAC

INCOIS is one of the Argo Data Assembly Centers:
- 70 BGC-Argo floats managed by INCOIS
- 12,736 BGC files from INCOIS

INCOIS Argo data is available via their portal and the GDAC.

---

## For SIH-OCEAN

1. **Ingest** Argo data via argopy → SQLite (one-time, or scheduled)
2. **Render** float markers on Cesium globe (Cesium entities)
3. **Click** marker → query SQLite for that float's profile → Plotly depth-vs-temp chart
4. **Co-visualize** with model fields (the headline PS requirement)
