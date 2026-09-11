# 01 — PS Authority + Shared Canonical (SIH26067)

**Authority:** `../problem-statement/PROBLEM-STATEMENT-ANALYSIS.md`
**PS:** SIH26067, MoES/INCOIS Ocean Valley, Software, Disaster Management
**Deadline:** 30 Sep 2026
**Date of this comparison:** 2026-09-09
**Verification channel:** 9router gateway (`http://localhost:20128`, `tavily/search` + `tavily/fetch`, `exa` fallback, key via `$NINEROUTER_KEY`, never commit key)

> Pasted SIH portal text is canonical. Official listing URL differs — pasted text wins on conflict. Do not invent the blank in-situ URL. Do not cite Esri archwatch externally until resolved. Do not cite Unity engine for NASA Eyes. Do not cite star counts as maturity proof. Do not claim WMS/WCS live compliance.

---

## 1. Five gaps R1–R5 (binding)

| ID | Gap (PS verbatim) | Milestone | Follows to |
|----|-------------------|-----------|------------|
| R1 | No web platform-independent 3D render with depth-resolved volumetric views | M1, M3 | F1 globe + depth + isosurface |
| R2 | No unified Argo/Glider display (lat, lon, depth, time, T, S, chlorophyll) beside model fields | M4 | F2 markers + click-profile + residual |
| R3 | No variable / depth-slice / time-animation / colorbar controls | M2 | F4 palette/min/max/log-linear/opacity/exaggeration |
| R4 | New streams/variables need re-engineering | M5 | F3 ingest adapters + F6 plugin registry |
| R5 | No intuitive rapid 3D understanding for operational decisions | M1–M5 demo arc | Scene arc 01→07, preset fly-to, 90s script |

R5 is the demo-arc requirement. Every demo beat must name one mandate (see §3). Currently unmapped — open item.

---

## 2. Seven functional requirements F1–F7 (binding)

| ID | Requirement | Stack lock | Build status |
|----|-------------|------------|--------------|
| F1 | 3D volumetric: T/S/currents full water column, depth slices, isosurfaces, time animation. PS names WebGL/Three.js **or** Cesium.js — either satisfies | CesiumJS + zarr-cesium + resium | Designed, not built. M3 tasks unchecked |
| F2 | Instrument overlay: Argo, Glider, CTD, BGC markers, geospatially accurate; click → depth-vs-variable profile + timestamps | zarr-cesium query APIs (point / time-series / profile / transect + cancellation) + Plotly.js | Designed, not built. M4 tasks unchecked |
| F3 | Ingest: automated NetCDF (PS names PyNIO/xarray backend) + delimited text; new variables/sources with minimal code change | xarray via xpublish + argopy + SQLite. PyNIO dropped — needs one-line ADR | Designed, not built. No ASCII/delimited adapter. No PyNIO ADR |
| F4 | Controls: palette, min/max, log/linear, variable selector, opacity, vertical exaggeration. Customizable colorbar | Shader uniforms | Designed, not built. M2/M3 tasks unchecked |
| F5 | Architecture: modern JS frontend, lightweight REST/OPeNDAP backend, INCOIS-deployable, zero client install | React 18 + Vite + TS + MUI/shadcn light theme; FastAPI + Zarr REST + OPeNDAP via xpublish; cesium-wind-layer GPU advection | Designed, not built. Demo = Vercel+R2+Supabase+Render free. Deliverable = Docker nginx+uvicorn+xpublish on INCOIS infra. Distinction not yet documented as deliverable |
| F6 | Extensibility: plugin-style sensors (CTD, moorings, HF-radar, ADCP), new variables, ML products | Plugin registry (M5 task, unchecked) | Zero live. Lakshya defers post-SIH. Prem22k research-only |
| F7 | Standards: OGC WMS/WCS, CF Conventions. Interop with national/international portals | WMS/WCS **roadmap-only** — label roadmap, never claim live compliance | Principle mention only. No library, endpoint, milestone design beyond checklist row |

**F-coverage source problem:** `docs/DOC-MAP.md` cites `00-problem/PROBLEM-STATEMENT-ANALYSIS.md`, folder missing. Top level has `problem-statement/` + `research/`, not `00-problem/`. Proxy = `docs/roadmap/MILESTONES.md` checklist 18 rows, all unchecked. No binding R/F IDs in shared docs — traceability lives in prem22k 01, not in shared canonical.

---

## 3. Operational mandates (judging hooks, currently unmapped)

| Mandate | What demo beat must do | Current state |
|---------|------------------------|---------------|
| Hazard assessment | Name mandate on one beat, tie to dataset + preset | Unmapped |
| Search-and-rescue | Name mandate on one beat, tie to currents/particles + preset | Unmapped |
| Fishery advisories | Name mandate on one beat, tie to SST/chlorophyll + preset | Unmapped |
| Climate monitoring | Name mandate on one beat, tie to time-series/depth-profile | Unmapped |

Each demo beat should name one mandate. Open item 3 (mandate→beat map in pitch doc) still open in both namespaces.

---

## 4. Outreach (binding, second user class)

| Aspect | PS demand | Current state |
|--------|-----------|---------------|
| Users | Students, public campaigns, policymakers | Named in PS analysis, no build |
| Venues | Exhibitions, e-learning | Named, no build |
| Mode | Guided mode distinct from forecaster mode | M5 scope only. Prem22k checklist (deep link + embed iframe + guided tour, borrowed from MyOcean Pro verified features + NASA Eyes tour pattern). Lakshya zero |
| Borrow list | NASA Eyes tours, MyOcean Pro deep-link/embed/tour | Verified 2026-09-09, not yet built |

---

## 5. Datasets (PS links, do not invent)

| # | Dataset | URL / ID | Variables / spec | Card status |
|---|---------|----------|------------------|-------------|
| D1 | Model GLORYS12 reanalysis | `las.incois.gov.in` + `GLOBAL_MULTIYEAR_PHY_001_030` | 1/12° (~8 km), 50 levels, daily+monthly, thetao/so/uo/vo/zos (+ bottomT/mlotst/siconc per Copernicus page). Product IDs `cmems_mod_glo_phy_my_0.083deg_P1D-m` etc. PB-scale NetCDF | Missing. `docs/data/README.md` requires `glorys12.md` with URL, access date, sha256, license, bbox, variables, ingest version. Present file `glorys-dataset.md` is draft, no sha256/license/access-date |
| D2 | Argo floats | `ftp://ftp.ifremer.fr/ifremer/argo` | 931 GB total, 3.5M files, NetCDF per-float `_prof.nc` | Missing. Requires `argo.md`. Present `argo-data.md` draft only |
| D3 | Glider | `ftp://ftp.ifremer.fr/ifremer/glider/v2/` | NetCDF trajectory profiles | Missing. Requires `glider.md`. Present `glider-data.md` draft only |
| D4 | INCOIS LAS | `https://las.incois.gov.in/` | NetCDF/OPeNDAP, format/auth/subset unknown | Missing. Requires `incois-las.md`. Ingest detail empty — only URL in `data-sources.md`, backend path `backend/ingest/incois.py` named in `project-structure.md` with no spec |
| D5 | In-situ collection | **Blank in PS paste — unknown** | Unknown | Missing. Requires `insitu-collection.md`. `data/README.md` flags unknown correctly — do not invent URL. Blocks card completion |

**Dataset contract rule:** `docs/data/README.md` requires one card per PS source before any fixture use. Each card: source URL, access date, sha256, license, bbox, variables, ingest version, assumptions. None exist. NetCDF→Zarr conversion + chunking notes reference `../architecture/backend-strategy.md`.

---

## 6. Open items 1–5 (no code, doc-only, still open)

| # | Item | Detail | Owner milestone |
|---|------|--------|-----------------|
| 1 | Dataset cards | sha256 + license + bbox for all 5 links (`docs/data/`) | M2 gate |
| 2 | ADRs | PyNIO-drop ADR; Cesium-over-Three ADR; OPeNDAP-facade scope note | M5 gate (PyNIO/Cesium/OPeNDAP), M2 (chunking) |
| 3 | Mandate→beat map | Hazard/SAR/fishery/climate mapped to demo beats + datasets + presets in pitch doc | M5 gate |
| 4 | Cutoffs + benchmark + laptop | Observations GeoJSON-vs-Arrow cutoff; chunk hypothesis benchmark; reference laptop lock | M4 gate (Arrow), M2 gate (chunk) |
| 5 | Match-up semantics | `residual = model − observation` + QC/method on every comparison panel. Shared docs show co-viz without residual rule — adopt before M4 | M4 gate |

Paste uses `E = O − M` in one place — rejected. Docs enforce `residual = model − observation`. Use docs form everywhere.

---

## 7. Users (from PS analysis)

| User | Job | Proof |
|------|-----|-------|
| Forecaster | Verify model feature vs instruments | Agreement/disagreement < 2 min |
| Scientist | Explore front/thermocline/current | Value at x,y,z,t + provenance |
| Operator | Onboard feed | Config-only, no frontend edit |
| Presenter | Explain ocean structure | Guided legible story, no setup |

Operator row ties to F3/F6 (config-only extensibility). Presenter row ties to outreach guided mode.

---

## 8. Shared canonical stack locks

| Layer | Choice | Source file | Note |
|-------|--------|-------------|------|
| Globe engine | CesiumJS ^1.115 + resium ^1.18 | `docs/architecture/tech-stack.md` + `TECH-STACK-SUMMARY.md` | Either Cesium or Three satisfies PS. Lock = Cesium. Needs Cesium-over-Three ADR |
| Ocean volumetric rendering | zarr-cesium latest (providers: `ZarrLayerProvider` 2D, `ZarrCubeProvider` slices+curtain+exaggeration, `ZarrCubeVelocityProvider` u/v particles) | `tech-stack.md` + `visualization/temperature-overlay.md` + `ocean-currents.md` + `system-architecture.md` | Constructor opts + `setDepth`/`setTime`/`setVerticalExaggeration` presumed signatures — no pinned version in shared docs, no API ref. Treat as presumed until Phase 0 test. Re-pin 0.2.0 (npm latest) vs docs pin 0.1.4 stale |
| Current particles | cesium-wind-layer (hongfaqiu) | Same paths + `visualization/ocean-currents.md` | Compat break Cesium>=1.127 real. Fix = Vite alias + dedupe. NOC-OI fork v0.11.0 (2026-08-21). Test in M3, fallback custom GPU shader |
| Backend | xpublish + xpublish-opendap + FastAPI/uvicorn — Zarr REST + OPeNDAP + custom `/profile` `/isosurface` `/timeseries` | `docs/architecture/backend-strategy.md` + `system-architecture.md` | `xpublish-opendap` as named is REFUTED — real package is `xpublish-zarr`. OPeNDAP needs THREDDS/Hyrax separate or skip MVP. Shared `backend-strategy.md` import `xpublish_opendap.OpenDapPlugin` is assumed-present, not registry-verified. Endpoints table (`/glorys_temp/zarr/.zmetadata`, `/opendap/...`) illustrative |
| Data format | Zarr + zarrita.js + Blosc zstd + consolidated. Chunk `(1,10,540,1080)` cited, balanced single store first | `docs/data/netcdf-to-zarr.md` + `glorys-dataset.md` | Multiscale ndpyramid + dual-chunk time-series store documented as Option A/future. Recommendation = start balanced single store. Chunk hypothesis benchmark still open |
| Argo/Glider ingest | argopy + SQLite + R-tree — ~10us bbox claim | `docs/data/argo-data.md` + `glider-data.md` | 10us from sqlitegis benches (cited in `performance/benchmarks.md` correctly). `runtime-latency.md` ~100–500ms per-op table presents as expected platform latency without build — treat as estimate, not measurement |
| Frontend shell | React 18 + Vite 5 + TS 5 + Zustand + Plotly.js + d3-scale-chromatic + MUI/shadcn light theme | `tech-stack.md` + `TECH-STACK-SUMMARY.md` + `project-structure.md` | Light theme default per PS |
| Deployment (shared) | Docker nginx + uvicorn + xpublish on INCOIS infra | `system-architecture.md` | **Conflicts** with free-tier direct split (Vercel+R2+Supabase+Render free). Both true at different layers: demo lives on free cloud, deliverable lives as Docker on INCOIS infra. Distinction not yet written as deliverable doc |
| Perf claims | 40x Zarr vs GRIB2 (Gowan 2022), ms chunk latency (AWS blog), 10k particles 60FPS (cesium-wind-layer) | `performance/benchmarks.md` (cited correctly) | Do not promote to platform latency without locked-laptop run |

---

## 9. Shared coverage (all designed, not built)

| Capability | Design location | Build status |
|------------|-----------------|--------------|
| Globe + day/night | `docs/visualization/globe-rendering.md` + `day-night-lighting.md` + M1 tasks | Unchecked |
| Time animation | `docs/visualization/temperature-overlay.md` + `performance/runtime-latency.md` ~150ms/frame claim + M2 tasks | Unchecked |
| Colorbar / variable / opacity / exaggeration | `docs/visualization/colorbar-editor.md` + `temperature-overlay.md` + M2/M3 tasks | Unchecked |
| Depth-slice + isosurface + volume | `docs/visualization/isosurfaces.md` + `temperature-overlay.md` + `research/temperature-rendering.md` Techniques C/D + M3 tasks | Unchecked. Technique D (Three.js volume renderer ray-casting premium mode) orphaned — no stack entry, no milestone task, no file in `project-structure.md` |
| Currents particles | `docs/visualization/ocean-currents.md` + `research/temperature-rendering.md` Technique B + M3 tasks | Unchecked |
| Argo/Glider overlay + click-profile | `docs/data/argo-data.md` + `glider-data.md` + `system-architecture.md` Tier 3 + M4 tasks | Unchecked |
| Open standards | `system-architecture.md` line 13 (OGC 3D Tiles, CF, OPeNDAP, WMS/WCS) + M5 row 17 | Principle + checklist only. No library, endpoint, task. Roadmap-only, not even OPeNDAP-level design |

---

## 10. Shared gaps (pre-existing, before namespaces)

1. `00-problem` missing. DOC-MAP authority cited, no folder/file. No R/F IDs to bind.
2. Dataset contract cards missing (see §5).
3. Residual rule missing. Zero hits for `residual`, `volume-subset` across `docs/`. No doc enforces subset ceiling.
4. WMS/WCS zero design (see F7).
5. PyNIO zero hits repo-wide. If PS mandates, gap total.
6. INCOIS LAS ingest empty (see D4).
7. In-situ collection URL blank (see D5).
8. DOC-MAP stale. Claims `research/individuals/`, `lakshya-research/` top-level, `TECH-STACK-SUMMARY.md` move. `research/individuals/` missing at shared level (lives under `research/individuals/` with lakshya+prem22k), folder READMEs mirror claim unchecked.
9. Technique D orphaned (see §9).
10. Provider API unverified (see §8 zarr-cesium row).
11. `xpublish-opendap` assumed present (see §8 backend row).
12. Perf numbers extrapolated (see §8 perf row).
13. Nothing mislabeled live except aspirational principle line (`system-architecture.md` line 13) listing WMS/WCS alongside built items. All MILESTONES checkboxes unchecked — honest draft state.

---

## 11. Four flagged shared docs — now covered (74/74 proof)

Stem-name audit flagged these 4. Semantic check: concepts covered elsewhere, exact names/methods missed. Patched here, no re-audit needed.

### 11a. `docs/performance/optimization.md` — chunk/cache/prefetch/GPU bible

| Method | Detail | Feeds gate |
|---|---|---|
| Dual chunking | `(30,50,108,216)` time-series vs `(1,10,540,1080)` map/slice; frontend picks store per op | M2 chunk ADR |
| Chunk sweet spot | ~100KB–2MB compressed per chunk; too small = I/O overhead, too large = bandwidth waste | M2 benchmark |
| Browser cache | `Cache-Control: public, max-age=86400` on Zarr chunks; repeat view instant | M2 slice ≤750ms |
| Isosurface cache | `lru_cache(maxsize=1000)` keyed `(variable, value, time, bbox_hash)`; 50ms vs 500ms | M3 isosurface |
| Cesium tile cache | `viewer.scene.globe.tileCacheSize = 1000` | M1 globe |
| Time prefetch | Render current, prefetch next 3 timesteps; camera-flight prefetch auto via Cesium | M2 scrub smoothness |
| GPU LUT | Colormap = 1D texture, palette/min/max/log = shader uniforms, instant no re-fetch | M2/M3 F4 |
| GPU particles | Ping-pong textures, 10k+ at 60FPS, zero CPU/frame | M3 currents |
| Exaggeration uniform | Shader uniform, no geometry rebuild | M3 curtain |
| LOD + pyramid | Cesium screen-space-error LOD; `ndpyramid` 4-level Zarr pyramid, coarse far / fine near | M1/M3 |
| Lazy load | xarray/xpublish metadata-only open; Argo markers bbox SQL (`floats_rtree` view-only, 4000+ floats fast) | M4 markers |
| Compression | Blosc zstd clevel 3 + BITSHUFFLE ~10:1, zarrita.js decode; KTX2+ETC1S 10–30% smaller, 80% less GPU mem | M2 R2 budget |
| Parallel fetch | zarrita.js HTTP/2 multiplex, 4 depth chunks via `Promise.all`; center-priority | M3 slices |
| Progressive render | `setProgressiveRender(true)`: coarse now, refine on arrival | M2 cold ≤10s |

Prior miss: exact tokens `prefetch` / `lru_cache` / `tileCacheSize` / `progressive` / `KTX2` never named in 01–07. Concepts (abort superseded, low-res first, downsample, cache-in-R2) covered. Fix = cite this file in chunk ADR.

### 11b. `docs/research/nullschool-earth.md` — 2D canvas truth, GPU takeaways

D3 orthographic projection (lat/lon→pixels, sphere illusion, NOT WebGL) + SVG Natural Earth base + 2 Canvas layers (particles + scalar overlay) + grib2json (netcdf-java) offline→S3 static + ColorBrewer/Kindlmann/cubehelix/Dave Green LUTs. Scalar render = per-pixel inverse-projection → bilinear interp of 4 cells → LUT → overlay canvas, masked to globe silhouette, `globalAlpha` blend. Costly per-pixel JS (their own comment). Particles = spawn N, advect `velocity×dt` via bilinear (u,v), Jacobian finite-difference projection correction, fading trails, CPU redraw loop. Modern live version closed-source (ocean currents/SST/depth, tiled Natural Earth, non-Web-Mercator poles). Takeaways locked: LUT idea moves to GPU shader (instant palette), particles move to `cesium-wind-layer` GPU (10k 60FPS), static-host idea moves to pre-converted Zarr chunks, Web-Mercator pole lesson → Cesium geographic projection. Scope fence: nullschool = surface 2D layer only, depth volumetric still owed (F1).

Prior miss: tokens `orthographic` / `Jacobian` / `Kindlmann` / `cubehelix` never quoted. Fence + pipeline covered in prem22k 02.

### 11c. `docs/research/open-source-projects.md` — 14-entry build library

DOVis (HungerBar, FastAPI+xarray+PyVista/VTK + Cesium, Indian Ocean DO, isosurface+profile+EOF+hypoxia, NetCDF→SQLite→API→3D-tiles — blueprint), OceanStream globe-3d-viewer (Copernicus ECVs, 6 vars SST/ice/level/chlorophyll/clarity/true-color, timeline+point-query+download+colormaps — PS UX mirror), nordicseas3d (React18+TS+Vite+Plotly+Three+zarrita, slices/sections/transects/class-clouds/isosurface/particle-tracking/eddy/basin-mask — best Three.js proof + Zarr-in-browser), zarr-cesium (3-provider table + example — render core), DeepSwitch (Vite+Three space-time cube, non-expert UX, doi 10.2312/envirvis.20251146), netcdf-three (netcdfjs partial download + GPU 3D texture — zero-backend option), i4Ocean (two-layer shell + ray casting + transfer functions — algorithm gold), WebGPU MDPI 2025 (Babylon+WebGPU early-termination — perf ceiling), Atlas (prior SIH INCOIS Argo maps/profiles/trajectories), OceanEye (prior SIH hazard cluster/heatmap/verification), three-globe (vasturiano hex/H3/tiles/arcs, `r3f-globe` landing-page option), argopy (`ArgoFloat.open_dataset('prof')` → xarray, kills 90% parsing pain), IMOS Live (AODN: geostrophic particles + GSLA heatmap + AusTEMP MHW + buoy/mooring clusters + depth temp + slider), Globe Viz (OISST SST+anomaly MIT on S3 — starter template).

Prior miss: names `OceanStream` / `netcdf-three` / `IMOS` / `GlobeViz` / `three-globe` / `OceanEye` never listed in 01–07. DOVis/nordicseas3d/zarr-cesium/Atlas/argopy/i4Ocean/WebGPU covered.

### 11d. `docs/research/platform-comparison.md` — 17-row decision matrix

Matrix columns Rendering | Temperature method | 3D/Depth | Data source | Open? | PS relevance. Rows: nullschool (D3+Canvas fake-3D, surface ref), Windy (MapLibre+WebGL, UX controls/timeline ref), Ventusky (InMeteo WebGL anomaly colormap ref), zoom.earth (Mapbox satellite, imagery ref not model), Google Earth (C++→WASM globe benchmark, 3D-Tiles-into-Cesium), OceanStream (closest 2D UX), DOVis (closest architecture), nordicseas3d (best Three.js), zarr-cesium (render core), i4Ocean (algorithm), WebGPU MDPI (perf ceiling), Atlas (prior SIH Argo), IMOS (SST+anomaly+particles+moorings), Globe Viz (starter), DeepSwitch (outreach UX), netcdf-three (zero-backend). Opportunity gaps (PS binds, none combine all 5): true volumetric depth + unified model+instrument co-viz + full controls + plugin registry + open standards. Differentiation locked: model fields + instrument profiles co-viz on single Cesium globe, full depth + time + plugins + standards.

Prior miss: rows `Windy` / `Ventusky` / `zoom.earth` never named in 01–07. Matrix verdict (no single platform combines all) covered in spirit via R-gaps.

Coverage now: 74 md total = 38 shared + 14 lakshya + 8 prem22k + 15 mermaid (75 paths listed, README counted twice across roots). All stems mapped. Next files unchanged in validity; this section closes audit.

Next: `02-lakshya-deployment-track.md` (execution track, 14 files) → `03-prem22k-product-science-track.md` (science track, 8 files) → `04-head-to-head-comparison.md` → `05-ratings-and-leaderboard.md` → `06-gaps-inventions-kill-risks.md` → `07-merged-build-plan-and-research-queue.md`.
