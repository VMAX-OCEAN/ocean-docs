# Tech Stack Summary

Condensed reference of the complete tech stack for the SIH-OCEAN platform.

---

## Frontend

| Component | Technology | Version | Purpose |
|---|---|---|---|
| Framework | React | 18 | UI component model |
| Build tool | Vite | 5+ | Fast dev server + build |
| Language | TypeScript | 5+ | Type safety |
| 3D globe | CesiumJS | latest | Globe, terrain, imagery, lighting, atmosphere |
| Cesium React bindings | resium | latest | React wrapper for Cesium |
| Ocean rendering | zarr-cesium | latest | ZarrLayerProvider, ZarrCubeProvider, ZarrCubeVelocityProvider |
| Current particles | cesium-wind-layer | latest | GPU particle advection |
| Zarr client | zarrita.js | latest | Browser-side Zarr chunk fetching |
| Charts | Plotly.js | latest | Depth-vs-variable profile charts |
| Colormaps | d3-scale-chromatic | latest | Scientific colormap LUTs |
| State | Zustand | latest | Lightweight state management |
| UI components | Material UI / shadcn | latest | Light theme controls |
| HTTP client | fetch / axios | — | API calls |

---

## Backend

| Component | Technology | Version | Purpose |
|---|---|---|---|
| Framework | FastAPI | latest | REST API |
| xarray server | xpublish | latest | Zarr REST + OPeNDAP + custom endpoints |
| OPeNDAP | xpublish-opendap | latest | Standards-compliant OPeNDAP |
| Data arrays | xarray | latest | NetCDF/Zarr handling |
| NetCDF I/O | netCDF4 | latest | NetCDF file reading |
| Argo data | argopy | latest | Argo float data access |
| Scientific | NumPy, SciPy, pandas | latest | Data processing |
| Isosurface | PyVista, VTK | latest | Marching cubes |
| Database | SQLite | built-in | Argo/Glider metadata + profiles |
| Server | uvicorn | latest | ASGI server |

---

## Data

| Component | Format | Purpose |
|---|---|---|
| Ocean model (GLORYS) | NetCDF → Zarr | 3D temp/salinity/currents |
| Argo floats | NetCDF → SQLite | Instrument profiles |
| Glider data | NetCDF → SQLite | Instrument transects |
| Bathymetry | GEBCO (via Cesium) | Seafloor relief |
| Imagery | Bing/MapTiler (via Cesium) | Satellite base layer |
| Coastlines | Natural Earth (via Cesium) | Map outlines |

---

## Deployment

| Component | Technology | Purpose |
|---|---|---|
| Frontend | nginx | Static file serving |
| Backend | uvicorn | ASGI server |
| Containerization | Docker | Reproducible deployment |
| Orchestration | docker-compose | Multi-service management |

---

## Key Libraries (npm)

```json
{
  "dependencies": {
    "react": "^18",
    "react-dom": "^18",
    "cesium": "^1.115",
    "resium": "^1.18",
    "zarr-cesium": "latest",
    "cesium-wind-layer": "latest",
    "zarrita": "latest",
    "plotly.js-dist-min": "latest",
    "d3-scale-chromatic": "latest",
    "zustand": "latest",
    "@mui/material": "^5",
    "axios": "latest"
  },
  "devDependencies": {
    "vite": "^5",
    "typescript": "^5",
    "@types/react": "^18",
    "vite-plugin-cesium": "latest"
  }
}
```

---

## Key Libraries (pip)

```
# requirements.txt
fastapi
uvicorn[standard]
xpublish
xpublish-opendap
xarray
netCDF4
argopy
numpy
scipy
pandas
pyvista
vtk
zarr
blosc
```
