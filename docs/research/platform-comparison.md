# Platform Comparison

Comparison of all relevant weather/ocean visualization platforms against our SIH
problem statement requirements.

---

## Comparison Matrix

| Platform | Rendering | Temperature method | 3D/Depth | Data source | Open source? | Relevance to PS |
|---|---|---|---|---|---|---|
| **earth.nullschool.net** | D3 + Canvas 2D (fake 3D globe) | 2D colormap overlay + particle advection | No depth (2D only) | GFS GRIB2, RTG-SST, OSTIA | Partial (old repo) | Surface SST + currents reference. Not the 3D model viz we need |
| **Windy.com** | MapLibre + WebGL | 2D scalar overlay + particles | No ocean depth | GFS, ECMWF, ICON | Closed | UX reference for controls/timeline; not 3D ocean |
| **Ventusky** | WebGL (InMeteo) | 2D scalar overlay, temp anomaly | No depth | GFS, ICON, DWD | Closed | Temperature anomaly colormap reference |
| **zoom.earth** | Mapbox + satellite | True-color satellite + radar | No depth | GOES/Himawari/MODIS | Closed | Satellite imagery reference, not model data |
| **Google Earth** | C++→WASM + WebGL | Universal Texture + 3D Tiles | Terrain only (no ocean volume) | Google tile servers | 3D Tiles standard is open | Globe quality benchmark; can load its 3D Tiles into Cesium |
| **OceanStream globe-3d-viewer** | CesiumJS | 2D SST overlay, multi-layer | Surface only | Copernicus | Closed | Closest UX to our PS (6 vars, timeline, point queries, colorbar) |
| **DOVis** | React + Cesium | 3D volumetric DO, isosurfaces, profiles | Full 3D + depth | NetCDF (Indian Ocean) | MIT | Closest architecture — same ocean, same formats, same 3D req |
| **nordicseas3d** | React + Three.js + Plotly | 3D slices, isosurfaces, particles, class clouds | Full 3D + depth | Zarr (browser-direct) | Open | Best Three.js 3D reference — proves all techniques in browser |
| **zarr-cesium** | CesiumJS providers | 2D layers + 3D cubes + velocity particles | 3D cubes | Zarr (no backend) | Open | Our rendering core — drop-in Cesium providers |
| **i4Ocean** (paper) | Custom ray casting | Volumetric transfer functions | True volume | NetCDF | Paper | Academic algorithm reference for ray casting |
| **WebGPU ocean volume** (MDPI 2025) | Babylon.js + WebGPU | Ray casting + early termination | True volume | NetCDF | Paper | Cutting-edge perf reference |
| **Atlas** (prior SIH INCOIS) | — | Argo profiles | Profiles only | Argo | Open | Prior SIH Argo project — study what judges liked |
| **IMOS Live** (AODN Australia) | Mapbox + WebGL | SST mosaic, SST anomaly, marine heatwaves, particles | Surface + mooring depth profiles | IMOS ocean data | Open | Excellent reference: SST + anomaly + particles + mooring profiles |
| **Globe Viz** (engineered.at) | 3D globe | NASA OISST SST + anomaly, time scrubbing | Surface | AWS S3 | MIT | Simple open SST anomaly globe — good starting template |
| **DeepSwitch** | Vite + Three.js | Space-time cube, slices, isocontours | Full 3D (depth or time as 3rd dim) | Cloud storage | Open | Non-expert UX reference (matches public outreach requirement) |
| **netcdf-three** | Three.js + netcdfjs | Volume rendering, 3D texture, 1D colormaps | True volume | NetCDF (browser) | Open | Pure-frontend NetCDF→volume pipeline reference |

---

## Detailed Notes

### earth.nullschool.net
- **Strength:** Beautiful, fast, runs everywhere, particle advection is iconic
- **Weakness:** 2D only, no depth, closed-source modern version, Canvas-based (CPU heavy)
- **Take:** Colormap LUT approach + particle advection concept. Use GPU versions.

### Windy.com
- **Strength:** Best-in-class UX for weather controls, timeline, layer management
- **Weakness:** No ocean depth, closed-source, not 3D volumetric
- **Take:** UX patterns for controls, timeline slider, layer panel

### Google Earth
- **Strength:** The "perfect globe" — real terrain, atmosphere, day/night, 3D buildings
- **Weakness:** No ocean volumetric data, C++/WASM (we can't replicate), closed data
- **Take:** Globe quality benchmark. Can load its Photorealistic 3D Tiles into Cesium.
- **Take:** Day/night lighting via Cesium's built-in `enableLighting`.

### DOVis
- **Strength:** Exact same problem (Indian Ocean, NetCDF, 3D volumetric, Cesium)
- **Weakness:** Specific to dissolved oxygen, SQLite-based (not Zarr streaming)
- **Take:** This is our blueprint. Study the FastAPI + Cesium + isosurface architecture.

### nordicseas3d
- **Strength:** All 3D techniques in Three.js, Zarr-in-browser (no backend)
- **Weakness:** Regional (Nordic Seas), Plotly can be slow
- **Take:** Zarr-in-browser pattern, isosurface mode, particle tracking

### zarr-cesium
- **Strength:** Drop-in Cesium providers for Zarr — exactly what we need
- **Weakness:** Newer library, less battle-tested
- **Take:** This is our rendering core. `ZarrLayerProvider` + `ZarrCubeProvider` +
  `ZarrCubeVelocityProvider`.

---

## What No Single Platform Does (Our Opportunity)

The PS explicitly states these gaps. No existing platform combines ALL of:

1. **Web-based 3D volumetric ocean model rendering** with depth-resolved views
   - DOVis does this (but only for dissolved oxygen)
   - nordicseas3d does this (but regional, Three.js not Cesium)

2. **Unified display of Argo/Glider profiles alongside model fields**
   - Atlas does Argo only (no model fields)
   - DOVis does model only (no Argo overlay)
   - None co-visualize both

3. **Interactive controls** (variable selection, depth-slice, time animation, colorbar)
   - OceanStream has most of this (but 2D surface only)
   - nordicseas3d has most (but regional)

4. **Extensible plugin architecture** for new sensors
   - None have this explicitly

5. **Open standards** (OGC WMS/WCS, CF Conventions, OPeNDAP)
   - Most use custom APIs
   - OPeNDAP is legacy but PS requires it

**Our differentiation:** Co-visualization of model fields + instrument profiles on a
single Cesium globe, with full 3D depth, time animation, and extensible plugin
architecture — using open standards.
