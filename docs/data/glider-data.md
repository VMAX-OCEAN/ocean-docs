# Glider Data

Underwater glider profile data — high-resolution transects of temperature, salinity,
and biogeochemical variables.

---

## Source

**FTP:** ftp://ftp.ifremer.fr/ifremer/glider/v2/

Glider data has a similar structure to Argo (NetCDF profile files) but with key
differences:

| Property | Argo | Glider |
|---|---|---|
| Platform | Free-drifting profiling floats | Piloted underwater gliders |
| Sampling | Vertical profiles at fixed locations | Transects (moving along a path) |
| Depth | 0-2000 m | 0-1000 m (typical) |
| Resolution | ~10 m vertical | ~1 m vertical (higher resolution) |
| Variables | Temp, sal, (BGC) | Temp, sal, O2, Chl, CDOM, etc. |
| Feature type | trajectoryProfile | trajectoryProfile |

---

## Data Structure (NetCDF)

Glider NetCDF files follow CF conventions with `featureType = trajectoryProfile`:

```
Dimensions:
  trajectory:  1
  profile:     N    (number of profiles in transect)
  obs:         M    (total observations across all profiles)

Variables:
  trajectory (trajectory)
  profile_id (profile)
  latitude (obs)
  longitude (obs)
  time (obs)
  depth (obs)
  temperature (obs)
  salinity (obs)
  oxygen (obs)
  chlorophyll (obs)
```

---

## Ingestion Pipeline

```
ifremer FTP (glider NetCDF files)
   │
   ▼ xarray
Glider metadata + profiles
   │
   ├──► SQLite: gliders table (glider_id, lat, lon, date, variables)
   │    + R-tree spatial index
   │
   └──► SQLite: glider_profiles table (glider_id, profile_id, depth, temp, sal, ...)
        indexed by (glider_id, profile_id)
```

### Python ingestion

```python
import xarray as xr
import sqlite3

def ingest_glider(filepath, db):
    ds = xr.open_dataset(filepath)

    for profile_id in ds.profile.values:
        prof = ds.sel(profile=profile_id)
        lat = prof.latitude.mean().values
        lon = prof.longitude.mean().values
        date = prof.time.mean().values

        # Insert into gliders table
        db.execute(
            "INSERT INTO gliders VALUES (?, ?, ?, ?, ?)",
            (ds.trajectory, profile_id, lat, lon, str(date))
        )

        # Insert profile data
        for i in range(len(prof.depth)):
            db.execute(
                "INSERT INTO glider_profiles VALUES (?, ?, ?, ?, ?, ?)",
                (ds.trajectory, profile_id, float(prof.depth[i]),
                 float(prof.temperature[i]), float(prof.salinity[i]),
                 float(prof.oxygen[i]) if 'oxygen' in prof else None)
            )
```

---

## Visualization

Glider data is visualized similarly to Argo:

1. **Markers** on Cesium globe showing glider transect positions
2. **Click** marker → depth-vs-variable profile chart (Plotly)
3. **Transect view** (optional) — show the glider's path as a line on the globe,
   colored by a variable (e.g., temperature along the transect)

### Transect rendering

```js
// Glider transect as a Cesium polyline
const transect = viewer.entities.add({
  polyline: {
    positions: gliderPositions,  // [lon, lat] array
    material: Cesium.Color.fromCssColorString('#ff6600'),
    width: 2,
    clampToGround: true
  }
});
```

---

## For SIH-OCEAN

Glider handling mirrors Argo (same SQLite schema, same profile chart UX). The
ingestion is via xarray (not argopy, which is Argo-specific). The co-visualization
with model fields works the same way — glider markers overlay the model temperature
field, and clicking shows the observed profile vs the model profile at that location.
