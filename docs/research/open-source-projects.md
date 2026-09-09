# Open-Source Ocean/Weather Visualization Projects

Reference open-source projects that solve parts of the SIH-OCEAN problem. Study these
before building — several are exactly our problem statement.

---

## 1. DOVis (HungerBar/DOVis) — Closest Match

**GitHub:** https://github.com/HungerBar/DOVis

Interactive web visualization system for exploring dissolved oxygen (DO) variation
in the **Indian Ocean**. Combines a FastAPI scientific-data backend with a Vite, React,
and Cesium frontend.

### Stack
- **Backend:** FastAPI, Uvicorn, xarray, NumPy, SciPy, pandas, NetCDF4, scikit-image,
  trimesh, PyVista, VTK
- **Frontend:** Vite, React, Cesium
- **Package:** pnpm

### Features
- 3D dissolved oxygen visualization on a Cesium globe
- Dissolved oxygen isosurface generation and export (server-side)
- Vertical profile queries for inspecting oxygen changes with depth
- EOF analysis tools for studying dominant spatial-temporal patterns
- Hypoxia visualization for low-oxygen regions
- FastAPI endpoints for time, volume, profile, isosurface, EOF, hypoxia data

### Data Pipeline
NetCDF → SQLite database → API → 3D tiles → Cesium frontend

### Why it matters
Same ocean (Indian Ocean), same data formats (NetCDF), same volumetric requirements.
This is our blueprint. The 4D dataset is longitude, latitude, depth, time.

---

## 2. OceanStream globe-3d-viewer (OceanStreamIO)

**GitHub:** https://github.com/OceanStreamIO/globe-3d-viewer

Interactive 3D visualization of global ocean Essential Climate Variables (ECVs). Data
sourced from Copernicus Marine Service, updated daily.

### Features
- 3D Globe Visualization with smooth zooming from global to local scales
- 6 Ocean Variables: SST, Sea Ice, Sea Level, Chlorophyll, Water Clarity, True-Color
- Multi-layer Display with adjustable transparency
- Time Navigation: timeline slider, play animations, control playback speed
- Point Queries: click anywhere to see values, time series, climatological statistics
- Data Download: NetCDF, GeoTIFF, or CSV subsets
- Customizable Colors: scientific colormaps and adjustable value ranges

### Why it matters
Shows the exact UX the problem statement asks for (colorbar, time animation, point
queries, multi-layer). Built on Cesium + Copernicus data — same as our plan.

---

## 3. nordicseas3d — Best Three.js Reference

**GitHub:** https://github.com/nordicseas3d/nordicseas3d.github.io

Interactive browser viewer for Nordic Seas ocean fields. Reads a Zarr store directly
in the browser and renders on 3D bathymetry.

### Stack
- React 18, TypeScript, Vite, Plotly, Three.js
- `zarrita` for client-side Zarr access

### Features
- Horizontal 3D map slices at selected depth and time
- Zonal sections at selected latitude
- User-drawn transects between two map points
- 3D class clouds for value bands through the water column
- Isosurface mode for isothermal, isohaline, isopycnal depth sheets
- Particle tracking mode for 3D Lagrangian paths through U/V/W
- Eddy detection / eddy volume view
- Optional topography, wind-stress, sea-ice layers
- Depth-resolved ocean-current vectors (Plotly and Three renderers)
- Basin masking (North Atlantic, Greenland Sea, Iceland Sea, Norwegian Sea)

### Why it matters
Proves Three.js can do everything the PS asks — and the Zarr-in-browser pattern avoids
a heavy backend. The most complete open-source 3D ocean viewer.

---

## 4. zarr-cesium (NOC-OI) — Key Library

**GitHub:** https://github.com/NOC-OI/zarr-cesium

CesiumJS providers for interactive 2D and 3D visualization of environmental and
geospatial data stored in Zarr. Streamed directly from cloud object stores
(HTTP/S3/GCS) **without preprocessing, conversion, or a backend server**.

### Providers

| Provider | Purpose | Description |
|---|---|---|
| `ZarrLayerProvider` | 2D scalar fields | Renders single-level variables as Cesium imagery layers (temperature, chlorophyll) |
| `ZarrCubeProvider` | 3D volumetric fields | Renders volumetric cubes with horizontal and vertical slices (ocean temperature) |
| `ZarrCubeVelocityProvider` | 3D vector fields | Visualizes vector flow (u/v) using animated particle advection |

### Example
```js
const cube = new ZarrCubeProvider(viewer, {
  url: 'https://example.com/ocean_temp.zarr',
  variable: 'temperature',
  bounds: { west: -20, south: 30, east: 10, north: 60 },
  colormap: 'plasma',
  verticalExaggeration: 50
});
await cube.load();
```

### Why it matters
Drop-in Cesium providers that solve volumetric + vector rendering + multiscale. This
is our rendering core.

---

## 5. DeepSwitch (19Chris98H)

**GitHub:** https://github.com/19Chris98H/DeepSwitch

Web-based tool for introducing students and non-experts to visual analysis of
spatiotemporal processes in oceanographic data.

### Stack
- Vite + Three.js, Docker preprocessing

### Features
- Interactive 3D visualization in standard browsers
- Space-time cube paradigm — switch 3rd dimension between depth and time
- Slices, isocontours, color mapping
- Aimed at non-experts (matches our "public outreach" requirement)

### Paper
doi.org/10.2312/envirvis.20251146

---

## 6. netcdf-three (umrlastig)

**GitHub:** https://github.com/umrlastig/netcdf-three

ThreeJS visualization of NetCDF datasets. Promise-based partial NetCDF download,
GPU 3D texture, sampling + volume rendering materials with 1D colormaps.

### Stack
- Three.js + `netcdfjs` (browser NetCDF v3 reader) + dat.gui

### Why it matters
Pure-frontend NetCDF→volume pipeline if we want zero backend.

---

## 7. i4Ocean (paper)

**DOI:** 10.1080/17538947.2021.1886355

Ocean visualization framework with:
- Two-layer spherical shell as ocean data proxy geometry
- Improved ray casting for heterogeneous multisection ocean volume data
- Adaptive sampling + preintegrated transfer functions for temp/salinity anomalies
- Interactive transfer function for analyzing 3D structure

### Why it matters
Academic gold standard for the rendering algorithm.

---

## 8. WebGPU Volume Rendering (MDPI 2025)

**DOI:** 10.3390/app15052782

WebGPU-based volume rendering framework for ocean scalar data. Babylon.js + WebGPU,
ray casting with early termination + adaptive sampling. Cutting-edge performance
reference.

---

## 9. Atlas (s9swata) — Prior SIH INCOIS Project

**GitHub:** https://github.com/s9swata/Atlas

Argo Data Visualization Platform developed for INCOIS under SIH. Features:
- Interactive Argo float maps (deployments and trajectories)
- Oceanographic profiles (temperature, salinity)
- Trajectory analysis with time-based filtering
- Multi-parameter charts

### Why it matters
Prior SIH INCOIS project — study what judges liked.

---

## 10. OceanEye (iamdipayandutta) — Prior SIH INCOIS Project

**GitHub:** https://github.com/iamdipayandutta/OceanEye

Citizen science ocean hazard monitoring platform for INCOIS. Features:
- Real-time hazard maps (cluster + heatmap visualization)
- Interactive map view with severity color coding
- Verification workflow for admin tools

### Why it matters
Another prior SIH INCOIS project — study architecture and what judges liked.

---

## 11. three-globe (vasturiano)

**GitHub:** https://github.com/vasturiano/three-globe

WebGL Globe Data Visualization as a ThreeJS reusable 3D object. Supports:
- `globeImageUrl`, `bumpImageUrl` (NASA Blue Marble + topography bump map)
- `showAtmosphere` — atmosphere halo
- Hex binning (H3), tiles, points, arcs, custom layers
- React bindings: `r3f-globe`

### Why it matters
If we want a pure-Three.js hero globe for the landing page, use this instead of
hand-rolling. Far more polished than our current `realistic-earth-globe.html`.

---

## 12. argopy

**Docs:** https://argopy.readthedocs.io

Python library purpose-built for Argo data access/manipulation.

```python
from argopy import ArgoFloat
ds = ArgoFloat(6901254).open_dataset('prof')  # → xarray Dataset
```

Eliminates 90% of Argo parsing pain. Handles GDAC netcdf files, metadata, profiles,
trajectories, plotting.

---

## 13. IMOS Live (AODN, Australia)

**GitHub:** https://github.com/aodn/imos-live-frontend

Interactive marine data visualization for Australia's Integrated Marine Observing System.

### Features
- WebGL-accelerated particle animation showing ocean geostrophic current direction/speed
- GSLA sea level anomaly WebGL heatmap overlay
- AusTEMP marine-heatwave overlays: SST mosaic, SST-anomaly mosaic, categorical MHW layer
- Wave buoy and mooring data with clustered map points and time-series charts
- Per-depth temperature for moorings
- Temporal date slider

### Why it matters
Excellent reference: SST + anomaly + particles + mooring profiles — very close to our
requirements.

---

## 14. Globe Viz (engineered.at)

3D globe visualizing NASA OISST daily sea-surface temperatures as absolute values and
temperature anomalies, with time controls. Open source (MIT), data on AWS S3.

### Why it matters
Simple open SST anomaly globe — good starting template.
