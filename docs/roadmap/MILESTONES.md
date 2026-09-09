# Milestone Plan

The implementation roadmap for the SIH-OCEAN platform, broken into 5 milestones.

---

## Milestone 1 — Perfect Light-Theme Globe (1-2 days)

**Goal:** A Google-Earth-quality globe with accurate day/night, light theme, and UI shell.

### Tasks
- [ ] Set up React + Vite + TypeScript project
- [ ] Install CesiumJS + resium
- [ ] Configure Cesium viewer with light theme
- [ ] Add Cesium World Terrain + GEBCO bathymetry
- [ ] Add satellite imagery (Bing/MapTiler/Blue Marble)
- [ ] Enable day/night lighting (`enableLighting`, `dynamicAtmosphereLighting`)
- [ ] Enable atmosphere + sun/moon discs
- [ ] Set up light theme (white background, no starfield, light UI chrome)
- [ ] Build basic UI shell (control panel placeholder, time slider placeholder)
- [ ] Camera controls (zoom, pan, rotate)

### Deliverable
A polished, light-theme 3D globe with real terrain, bathymetry, satellite imagery,
and accurate day/night terminator. No data yet — visual foundation.

### Verification
- Globe renders at 60 FPS
- Day/night terminator moves when scrubbing time
- Atmosphere glows correctly at terminator
- Light theme (no black background)
- Zoom reveals more detail (LOD streaming)

---

## Milestone 2 — Temperature Surface Layer (2-3 days)

**Goal:** End-to-end pipeline — ingest one GLORYS variable, render as SST overlay,
animate over time.

### Tasks
- [ ] Set up FastAPI + xpublish backend
- [ ] Download GLORYS sample (Indian Ocean subset, 1 month)
- [ ] Convert NetCDF → Zarr (one-time script)
- [ ] Serve Zarr via xpublish REST API
- [ ] Install zarr-cesium + zarrita.js in frontend
- [ ] Implement `ZarrLayerProvider` for SST surface overlay
- [ ] Build colorbar editor (palette, min/max, log/linear, opacity)
- [ ] Build variable selector (temp/salinity/SSH)
- [ ] Build time slider + play/pause animation
- [ ] Test colormap changes are instant (no re-fetch)

### Deliverable
Globe with animated SST overlay, customizable colorbar, time animation. Proves the
full pipeline: ingest → convert → stream → render → animate.

### Verification
- SST overlay renders on globe
- Time animation smooth (~5 FPS, ~200ms per frame)
- Colormap changes instant
- Opacity slider works
- Colorbar displays with correct labels

---

## Milestone 3 — 3D Depth + Currents (3-4 days)

**Goal:** The headline 3D volumetric requirement — depth slices, isosurfaces,
and animated currents.

### Tasks
- [ ] Implement `ZarrCubeProvider` for 3D temperature field
- [ ] Build depth slider (select depth level)
- [ ] Build vertical exaggeration slider
- [ ] Implement isosurface mode (server-side marching cubes, cached)
- [ ] Implement `ZarrCubeVelocityProvider` for ocean currents
- [ ] Integrate `cesium-wind-layer` for GPU particle advection
- [ ] Add sea surface height (SLA) overlay
- [ ] Test depth slice at various levels (0m, 100m, 500m, 1000m)
- [ ] Test isosurface (20°C isotherm)

### Deliverable
Full 3D ocean visualization: depth slices, thermocline isosurfaces, animated
currents, sea level. The core PS requirement.

### Verification
- Depth slice renders at selected depth inside globe
- Vertical exaggeration makes ocean layer visible
- Isosurface shows thermocline depth
- Current particles animate smoothly (10k+ particles, 60 FPS)
- All layers can co-exist (multi-layer with opacity)

---

## Milestone 4 — Instrument Overlay (2-3 days)

**Goal:** Argo/Glider markers with click-to-view profile charts. Co-visualization
of model fields + instruments.

### Tasks
- [ ] Set up argopy for Argo data ingestion
- [ ] Build SQLite database (floats + profiles tables + R-tree index)
- [ ] Add Argo marker endpoints (`/argo/floats`, `/argo/profile`)
- [ ] Render Argo markers on globe (Cesium entities)
- [ ] Render Glider markers
- [ ] Implement click → Plotly depth-vs-temperature profile chart
- [ ] Co-visualize: model field + instrument profile on same globe
- [ ] Add marker filtering (by date, variable, region)

### Deliverable
Argo/Glider markers overlay the model temperature field. Click any marker →
depth-vs-temperature profile chart. The headline co-visualization requirement.

### Verification
- Markers render at correct lat/lon
- Click marker → profile chart appears in side panel
- Profile shows depth on Y-axis, temperature on X-axis
- Model field visible behind markers (co-visualization)
- Marker query is fast (<10ms)

---

## Milestone 5 — Polish + Extensibility (2 days)

**Goal:** Plugin architecture, OPeNDAP, light theme refinement, demo prep.

### Tasks
- [ ] Build plugin registry for future sensors (CTD, moorings, HF-radar, ADCP)
- [ ] Add OPeNDAP endpoints (xpublish-opendap plugin)
- [ ] Refine light theme (panels, controls, colorbar)
- [ ] Mobile responsiveness
- [ ] Performance optimization (chunk prefetch, caching)
- [ ] Demo data prep (curated datasets for presentation)
- [ ] Documentation (README, deployment guide)
- [ ] Docker setup (frontend + backend)

### Deliverable
A polished, extensible, deployable platform with all PS requirements met.

### Verification
- All PS requirements checked (see checklist below)
- Plugin system can add a new sensor with minimal code
- OPeNDAP endpoints work (test with external client)
- Deployable via Docker
- Demo runs smoothly

---

## PS Requirements Checklist

| Requirement | Milestone | Status |
|---|---|---|
| 3D volumetric rendering (temp/salinity/currents) | 3 | ☐ |
| Depth-slice views | 3 | ☐ |
| Isosurface extraction | 3 | ☐ |
| Time-step animation | 2 | ☐ |
| Instrument data overlay (Argo/Glider/CTD/BGC) | 4 | ☐ |
| Click instrument → depth-vs-variable profile | 4 | ☐ |
| Multi-format data ingestion (NetCDF, ASCII) | 2, 4 | ☐ |
| Modular/extensible architecture | 5 | ☐ |
| Customizable colorbar (palette, min/max, log/linear) | 2 | ☐ |
| Variable selector | 2 | ☐ |
| Layer opacity controls | 2 | ☐ |
| Vertical exaggeration slider | 3 | ☐ |
| Web-based (browser, no install) | 1 | ☐ |
| Scalable architecture | 5 | ☐ |
| Open standards (OGC WMS/WCS, CF, OPeNDAP) | 5 | ☐ |
| Plugin-style for future sensors | 5 | ☐ |

---

## Total Estimate

~10-14 days of focused development for a complete, demoable platform.

| Milestone | Days | Cumulative |
|---|---|---|
| 1. Perfect globe | 1-2 | 2 |
| 2. Temperature layer | 2-3 | 5 |
| 3. 3D depth + currents | 3-4 | 9 |
| 4. Instrument overlay | 2-3 | 12 |
| 5. Polish + extensibility | 2 | 14 |
