# Project Structure

Repository and code organization for the SIH-OCEAN platform.

---

## Repository Layout

```
sih-ocean/
├── README.md
├── docs/                           # This documentation
│   ├── research/
│   ├── architecture/
│   ├── visualization/
│   ├── data/
│   ├── roadmap/
│   ├── performance/
│   └── references/
├── frontend/                       # React + Vite + TypeScript + CesiumJS
│   ├── src/
│   │   ├── main.tsx                # App entry
│   │   ├── App.tsx                 # Root component
│   │   ├── globe/                  # Cesium viewer, terrain, imagery, lighting
│   │   │   ├── CesiumViewer.tsx
│   │   │   ├── GlobeConfig.ts      # Lighting, atmosphere, day/night settings
│   │   │   └── TerrainProviders.ts # Cesium World Terrain + GEBCO bathymetry
│   │   ├── layers/                 # Ocean data layers
│   │   │   ├── SurfaceLayer.tsx    # 2D SST/salinity overlay (ZarrLayerProvider)
│   │   │   ├── VolumetricLayer.tsx # 3D depth slices (ZarrCubeProvider)
│   │   │   ├── IsosurfaceLayer.tsx # Thermocline isosurfaces
│   │   │   ├── CurrentLayer.tsx    # GPU particle advection (cesium-wind-layer)
│   │   │   └── LayerManager.tsx    # Multi-layer opacity/ordering
│   │   ├── instruments/            # Argo/Glider overlay
│   │   │   ├── ArgoMarkers.tsx     # Cesium entities for floats
│   │   │   ├── GliderMarkers.tsx
│   │   │   └── ProfileChart.tsx     # Plotly depth-vs-variable
│   │   ├── controls/               # UI control panel (light theme)
│   │   │   ├── ControlPanel.tsx
│   │   │   ├── ColorbarEditor.tsx  # Palette, min/max, log/linear, opacity
│   │   │   ├── VariableSelector.tsx
│   │   │   ├── DepthSlider.tsx
│   │   │   ├── TimeControls.tsx    # Timeline slider + play/pause
│   │   │   ├── ExaggerationSlider.tsx
│   │   │   └── DayNightToggle.tsx
│   │   ├── plugins/                # Extensible sensor modules
│   │   │   ├── PluginRegistry.ts
│   │   │   ├── CTDPlugin.ts
│   │   │   ├── MooringsPlugin.ts
│   │   │   ├── HFRadarPlugin.ts
│   │   │   └── ADCPPlugin.ts
│   │   ├── api/                    # Backend API client
│   │   │   ├── zarrClient.ts       # zarrita.js wrapper
│   │   │   ├── restClient.ts       # xpublish REST + custom endpoints
│   │   │   └── opendapClient.ts    # OPeNDAP access
│   │   ├── state/                  # Zustand stores
│   │   │   ├── globeStore.ts
│   │   │   ├── layerStore.ts
│   │   │   ├── timeStore.ts
│   │   │   └── controlStore.ts
│   │   ├── theme/                  # Light theme config
│   │   │   └── theme.ts
│   │   └── utils/
│   │       ├── colormaps.ts        # d3-scale-chromatic LUTs
│   │       ├── geo.ts              # Geo coordinate utils
│   │       └── time.ts             # Time animation utils
│   ├── public/
│   │   └── textures/               # Blue marble, bathymetry, bump maps (fallback)
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── package.json
├── backend/                        # FastAPI + xpublish
│   ├── main.py                     # xpublish server entry
│   ├── api/
│   │   ├── routes.py               # Custom REST endpoints
│   │   ├── opendap.py               # OPeNDAP plugin config
│   │   └── profiles.py             # Argo/Glider profile endpoints
│   ├── ingest/
│   │   ├── glorys.py               # GLORYS NetCDF → Zarr
│   │   ├── argo.py                 # Argo via argopy → SQLite
│   │   ├── glider.py               # Glider NetCDF → SQLite
│   │   └── incois.py               # INCOIS LAS ingestion
│   ├── convert/
│   │   ├── netcdf_to_zarr.py        # One-time conversion
│   │   └── chunking.py             # Dual chunking strategy
│   ├── compute/
│   │   ├── isosurface.py            # Marching cubes (cached)
│   │   └── timeseries.py            # Point time series
│   ├── db/
│   │   ├── database.py              # SQLite connection
│   │   └── schema.sql              # Tables + R-tree index
│   ├── config.py
│   └── requirements.txt
├── data/                           # Sample datasets (gitignored, large)
│   ├── glorys/
│   ├── argo/
│   └── glider/
├── docker/
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   └── docker-compose.yml
├── scripts/
│   ├── convert_data.py             # One-time NetCDF → Zarr + SQLite
│   └── download_samples.py         # Download sample datasets
└── .gitignore
```

---

## Key Directories Explained

### `frontend/src/globe/`
The Cesium viewer and globe configuration. Handles terrain, imagery, lighting,
atmosphere, and day/night. This is where the "perfect globe" lives.

### `frontend/src/layers/`
Ocean data rendering layers using zarr-cesium providers. Each layer type (surface,
volumetric, isosurface, currents) is a separate component for the plugin-style
extensibility the PS requires.

### `frontend/src/instruments/`
Argo/Glider marker overlays and profile charts. The co-visualization of model fields
+ instrument profiles happens here — the headline PS requirement.

### `frontend/src/controls/`
The light-theme UI control panel. Colorbar editor, variable selector, depth slider,
time controls. All changes are instant (shader uniforms) where possible.

### `frontend/src/plugins/`
Plugin registry for future sensors (CTD, moorings, HF-radar, ADCP). Each plugin
registers its data source, marker type, and profile format.

### `backend/ingest/`
Data ingestion modules. GLORYS → Zarr, Argo → SQLite (via argopy), Glider → SQLite,
INCOIS LAS → Zarr. Run once (or on schedule) to build the data stores.

### `backend/compute/`
Server-side computation for expensive operations (isosurfaces via marching cubes,
point time series). Results are cached.

---

## Gitignore (key entries)

```
data/              # Large datasets, not committed
node_modules/
__pycache__/
*.pyc
.env
dist/
build/
*.zarr             # Zarr stores (too large)
*.sqlite           # SQLite databases
*.nc               # NetCDF files
```
