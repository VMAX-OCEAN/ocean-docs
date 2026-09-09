# System Architecture

High-level system architecture and data flow for the SIH-OCEAN platform.

---

## Design Principles

1. **Stream only what the camera needs** (Google Earth principle) — chunked data,
   on-demand fetch, LOD selection
2. **GPU for everything visual** — colormaps, lighting, particles are shader-side,
   instant changes with no re-fetch
3. **Standards-compliant** — OGC 3D Tiles, CF Conventions, OPeNDAP, WMS/WCS
4. **Extensible** — plugin architecture for new sensors and variables
5. **No client install** — pure browser, deployable on INCOIS infrastructure

---

## Three-Tier Architecture

### Tier 1: Data Layer (pre-processed)

```
Raw Data Sources
├── GLORYS12 (Copernicus) ── NetCDF ──► xarray ──► Zarr store (chunked)
├── Argo (ifremer FTP)    ── NetCDF ──► argopy ──► SQLite (metadata + profiles)
├── Glider (ifremer FTP)  ── NetCDF ──► xarray ──► SQLite
└── INCOIS LAS            ── NetCDF/OPeNDAP ──► Zarr store
```

**One-time conversion** (offline batch job):
- GLORYS NetCDF → Zarr with dual chunking (time-series + map access patterns)
- Argo/Glider NetCDF → SQLite with R-tree spatial index for marker queries
- Metadata extracted to JSON catalogs

### Tier 2: Backend (xpublish / FastAPI)

```
xpublish Server (FastAPI)
├── Zarr REST API          ──► browser streams chunks directly (ms latency)
├── OPeNDAP plugin         ──► standards-compliant access for INCOIS portals
├── /profile endpoint      ──► Argo/Glider depth profile (SQLite query, ~10 µs)
├── /isosurface endpoint   ──► marching cubes isosurface (cached, server compute)
├── /timeseries endpoint   ──► point time series query
└── /metadata endpoint     ──► dataset/variable metadata
```

**Key:** the heaviest data (volumetric 3D fields) bypasses server compute entirely —
the browser fetches only the Zarr chunks it needs, in parallel, with ms latency. The
server only does lightweight metadata/profile work and occasional isosurface compute
(which is cached).

### Tier 3: Frontend (React + CesiumJS)

```
React App
├── Cesium Viewer (globe + terrain + imagery + lighting + atmosphere)
├── Ocean Layer System
│   ├── ZarrLayerProvider      ──► 2D SST/salinity surface overlay
│   ├── ZarrCubeProvider       ──► 3D volumetric depth slices + isosurfaces
│   └── ZarrCubeVelocityProvider ──► GPU particle advection (cesium-wind-layer)
├── Instrument Overlay System
│   ├── Argo/Glider markers    ──► Cesium entities (billboards/points)
│   └── Profile chart          ──► Plotly depth-vs-variable on click
├── Control Panel (light theme)
│   ├── Colorbar editor        ──► palette, min/max, log/linear, opacity
│   ├── Variable selector      ──► temp/salinity/currents/SSH
│   ├── Depth slider           ──► select depth level for slices
│   ├── Time controls          ──► timeline slider + play/pause animation
│   ├── Vertical exaggeration  ──► slider for depth visibility
│   └── Day/night toggle       ──► enable/disable sun lighting
└── Plugin Registry            ──► extensible for new sensors (CTD, moorings, HF-radar, ADCP)
```

---

## Data Flow (Runtime)

### Surface SST Layer (2D overlay)

```
1. User opens app, globe loads with Cesium terrain + imagery
2. User selects "Temperature" variable, "Surface" depth
3. ZarrLayerProvider requests Zarr chunk for (t=current, depth=0, bbox=view)
4. zarrita.js fetches chunk (~100 KB) from xpublish Zarr REST ──► ms latency
5. Provider builds Cesium imagery layer, applies colormap LUT in shader
6. Globe renders with SST overlay, colorbar shown in panel
7. User scrubs time slider ──► next chunk fetched ──► re-texture ──► animation
8. User changes colormap ──► shader uniform update ──► instant recolor (no fetch)
```

### 3D Depth Slice

```
1. User selects "Temperature", depth = 500m
2. ZarrCubeProvider requests Zarr chunk for (t=current, depth=500m, bbox=view)
3. Chunk fetched ──► colored sheet rendered at 500m depth inside globe
4. Vertical exaggeration slider ──► sheet position scales (shader uniform)
5. User changes depth slider ──► new chunk ──► re-render
```

### Isosurface (thermocline)

```
1. User selects "Isosurface" mode, target = 20°C
2. Backend /isosurface endpoint runs marching cubes on Zarr data
3. Returns mesh (vertices + faces + depth colors)
4. Frontend renders as Cesium 3D primitive ──► shows 20°C isotherm depth surface
5. Result cached for subsequent requests at same (t, target)
```

### Current Particles (GPU advection)

```
1. User enables "Currents" layer
2. ZarrCubeVelocityProvider fetches u/v chunks for (t, depth, bbox)
3. cesium-wind-layer spawns 10,000 particles in GPU texture
4. Each frame: shader reads velocity at particle position, moves particle (semi-Lagrangian)
5. Particles drawn as fading line trails, colored by speed
6. Particles re-seed when time changes
```

### Argo Profile (instrument overlay)

```
1. Backend ingests Argo data via argopy ──► SQLite (lat, lon, time, float_id, profiles)
2. Frontend queries /argo/floats?bbox=... ──► returns markers in view
3. Cesium renders markers as entities (billboards)
4. User clicks marker ──► /profile?float_id=X&variable=temp ──► SQLite query (~10 µs)
5. Plotly renders depth-vs-temperature profile chart in side panel
6. Co-visualization: model field + instrument profile on same globe
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│  INCOIS Infrastructure                   │
│                                         │
│  ┌─────────────┐    ┌─────────────────┐ │
│  │ nginx       │    │ uvicorn         │ │
│  │ (frontend   │───►│ (xpublish       │ │
│  │  static)    │    │  FastAPI)       │ │
│  └─────────────┘    └────────┬────────┘ │
│                              │          │
│              ┌───────────────┴────────┐ │
│              │  Zarr store (HTTP/S3)   │ │
│              │  SQLite (metadata)     │ │
│              └────────────────────────┘ │
└─────────────────────────────────────────┘
        │
        ▼ (HTTPS, browser)
┌─────────────────────────────────────────┐
│  User Browser                           │
│  React + CesiumJS + zarrita.js          │
└─────────────────────────────────────────┘
```

**Docker Compose:**
- `frontend` service: nginx serving built React app
- `backend` service: uvicorn running xpublish
- `data` volume: Zarr store + SQLite
- Optional: `convert` one-shot service for NetCDF → Zarr conversion
