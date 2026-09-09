# Tech Stack

Complete technology stack for the SIH-OCEAN platform, with rationale for each choice
based on the research.

---

## Decision Summary

| Layer | Choice | Why |
|---|---|---|
| Globe engine | **CesiumJS** (with `resium` React bindings) | Geospatial accuracy for Argo/Glider overlay; OGC standards; built-in day/night lighting, atmosphere, terrain; proven by DOVis/OceanStream/zarr-cesium |
| Ocean volumetric rendering | **zarr-cesium** providers | Drop-in Cesium providers for 2D layers, 3D cubes, velocity particles. Solves depth slices, vertical exaggeration, U/V advection |
| Current particle animation | **cesium-wind-layer** (hongfaqiu) | GPU-accelerated particle advection, 10k+ particles at 60 FPS, terrain occlusion. Same lib zarr-cesium uses |
| Backend | **xpublish** (FastAPI + Zarr REST + OPeNDAP) | Single server serves Zarr chunks (ms-latency browser streaming) + OPeNDAP (standards compliance) + custom endpoints |
| Data format | **Zarr** (chunked, cloud-streamed) | 40× faster access than GRIB2, parallel reads, scales to hundreds of clients, ms chunk latency |
| Argo/Glider data | **argopy** + SQLite | argopy eliminates Argo parsing pain; SQLite for metadata/marker queries (~10 µs with R-tree) |
| Frontend framework | **React 18 + Vite + TypeScript** | Used by DOVis, nordicseas3d, OceanStream, zarr-cesium. Component model fits plugin-style extensibility |
| UI components | **Material UI** or **shadcn/ui** (light theme) | Light theme default; component library for controls, colorbar editor, panels |
| Profile charts | **Plotly.js** | nordicseas3d uses Plotly for depth profiles. Click float → depth-vs-variable chart |
| Colormaps | **d3-scale-chromatic** / `cesium-color-maps` | Scientific colormaps (plasma, viridis, turbo, RdBu) as GPU LUT |
| State management | **Zustand** | Lightweight, fits React + Cesium |
| Deployment | **Docker** (nginx + uvicorn) | Deployable on INCOIS infrastructure, no client install (PS requirement) |
| Testing | **Vitest** + **Playwright** | Unit + E2E for interactive globe |

---

## Why CesiumJS (not hand-rolled Three.js)

Our current `realistic-earth-globe.html` is a hand-rolled Three.js sphere with a CDN
texture. For a "perfect" Google-Earth-quality globe with accurate day/night,
temperature, and water levels, we use CesiumJS instead.

| What we want | Hand-rolled Three.js | CesiumJS |
|---|---|---|
| Accurate day/night terminator | Must write shader (sun position math + dot product + smoothstep — error-prone) | Built-in: `scene.globe.enableLighting = true` — sun position auto-derived from clock |
| Realistic atmosphere | Cheap additive fresnel approximation | Built-in atmospheric scattering (Rayleigh + Mie, single-scatter volumetric ray casting) |
| Real terrain/bathymetry | Flat sphere, no elevation | Streams Cesium World Terrain + GEBCO bathymetry (real seafloor relief) |
| Real imagery | One static NASA Blue Marble JPG | Streams Bing/ArcGIS/MapTiler satellite imagery at any zoom |
| Geospatial accuracy | Sphere geometry, wrong for Argo/Glider overlay | WGS84 ellipsoid + hybrid log-depth buffer (no z-fighting at planet scale) |
| Light theme | Hardcoded black background | Default is light; fully themeable |
| Performance | Fine for demo, no LOD streaming | Quadtree LOD + Screen-Space Error tile selection (Google Earth principle) |

**The day/night terminator** — in CesiumJS it's literally:
```js
viewer.scene.globe.enableLighting = true;
viewer.scene.globe.dynamicAtmosphereLighting = true;
viewer.scene.globe.dynamicAtmosphereLightingFromSun = true;
viewer.clock.currentTime = Cesium.JulianDate.fromIso8601("2026-09-09T12:00:00Z");
```
The sun position is computed from clock time using real astronomy. The terminator is
a Lambert diffuse shading calculation in the globe fragment shader, with a
`lightingFade` based on camera distance. The atmosphere uses the sun direction for
dynamic scattering. We get the accurate light/dark side **for free**.

---

## Why Zarr (not NetCDF direct or OPeNDAP-only)

### Performance data (from research)

- **Zarr over HTTP + object storage:** scales to hundreds of parallel reads; 40× faster
  time-series access than GRIB2; millisecond chunk latency on S3
- **OPeNDAP servers** (THREDDS/Hyrax/ERDDAP): CPU/memory bound, "less efficient than
  Zarr in S3 especially with Dask"
- **Cesium 3D Tiles:** generation is expensive (Osaka 4.3 GB → 26 min tiling); zarr-cesium
  streams on-demand with no preprocessing

### Chunking strategy (from benchmark study)

Store **two Zarr representations** — one chunked for time-series access (large time,
small space) and one for map/slice access (small time, large space) — or pick a
balanced chunk and accept the tradeoff. This is the single biggest runtime lever.

---

## Why xpublish (not raw FastAPI or full OPeNDAP)

`xpublish` is a FastAPI-based server that serves xarray datasets via:

- A **Zarr-compatible REST API** (browser streams chunks directly via `zarrita.js` —
  millisecond latency, no per-read server CPU)
- An **OPeNDAP plugin** (`xpublish-opendap`) for standards compliance with INCOIS/national portals
- Custom FastAPI endpoints for profiles, isosurfaces, metadata (SQLite-backed for
  marker lookups at ~10 µs)

This satisfies "no user delay" **and** the PS's explicit OPeNDAP/OGC requirement in
one server.

---

## Complete Stack Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  BROWSER (React + Vite + TypeScript + CesiumJS)            │
│                                                            │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐     │
│  │ Cesium Globe│  │ Ocean Layers │  │ Instrument     │     │
│  │ (terrain +  │  │ (zarr-cesium)│  │ Overlays       │     │
│  │  imagery +  │  │              │  │ (Argo/Glider)  │     │
│  │  lighting + │  │ - SST surface│  │                │     │
│  │  atmosphere)│  │ - Depth slice│  │ - Markers      │     │
│  │             │  │ - Isosurface │  │ - Profile chart│     │
│  │             │  │ - Currents   │  │   (Plotly)     │     │
│  └─────────────┘  └──────────────┘  └────────────────┘     │
│         │                │                   │             │
│         └────────────────┴───────────────────┘             │
│                          │                                 │
│              ┌───────────┴───────────┐                     │
│              │  Controls (light theme)│                     │
│              │  - Colorbar editor     │                     │
│              │  - Variable selector  │                     │
│              │  - Depth slider       │                     │
│              │  - Time animation     │                     │
│              │  - Day/night toggle   │                     │
│              └───────────────────────┘                     │
└──────────────────────────┬──────────────────────────────────┘
                           │ (Zarr chunks streamed on demand, ms latency)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  BACKEND (xpublish / FastAPI)                              │
│  - Zarr REST API (browser streams chunks directly)         │
│  - OPeNDAP endpoints (standards compliance)                │
│  - /profile, /isosurface (cached server compute)           │
│  - argopy for Argo data → SQLite metadata index            │
└──────────────────────────┬──────────────────────────────────┘
                           │ (one-time conversion)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  DATA (pre-converted)                                     │
│  - GLORYS NetCDF → Zarr (temp/salinity/u/v, 50 levels)      │
│  - Argo/Glider → SQLite (metadata + profile index)         │
└─────────────────────────────────────────────────────────────┘
```
