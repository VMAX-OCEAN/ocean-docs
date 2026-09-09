# 3D earth + 4D toggle — research (2026-09-09)

Plan: NASA-type 3D earth + Google-earth toggle for 3D, location-scoped 4D toggle.
Sources via 9router (tavily search, tavily/exa fetch). Accessed 2026-09-09.

## 1. NASA Eyes — borrow interaction, not stack

- Eyes suite: browser-native 3D apps over real NASA data/imagery, exploration + temporal nav.
  Sources: [NASA Eyes](https://science.nasa.gov/eyes), [Eyes on Earth](https://eyes.nasa.gov/apps/earth), [Eyes on Solar System](https://eyes.nasa.gov/apps/solar-system).
- Not open source as a reusable ocean engine. Closest open work: community clones
  ([Planetarium](https://github.com/rijulpaul/Planetarium)), Three.js photoreal demos
  ([showcase thread](https://discourse.threejs.org/t/photorealistic-real-time-solar-system-in-three-js-3dsolarsystem-online/91545)).
- Open globe engine available: [CesiumJS](https://cesium.com/platform/cesiumjs).
- Borrow: cinematic fly-to, telemetry labels, time controls, layer toggles, guided vs free explore.
- Skip: planetary ephemeris, mission sim, custom engine. No value for SIH26067.

## 2. MyOcean Pro — analysis tools yes, 2D layout no

Fetched: [main features doc](https://help.marine.copernicus.eu/en/articles/4794675-main-features-of-myocean-pro-viewer).
MyOcean Pro calls itself 4D (lon, lat, depth, time) and ships:

- Catalogue hybrid search, multi-variable/layer display, zoom ~150 m, EPSG:4326 + polar grids.
- Date-time selection across layers, depth selection, point value query.
- Time-series graphs, depth-profile graphs, line/polygon section + trajectory profiles,
  histograms, interactive movable graphs, export `.nc`/`.csv`, measure tools.
- Entry: [viewer](https://data.marine.copernicus.eu/viewer), [intro](https://help.marine.copernicus.eu/en/articles/6482737-introduction-to-myocean-pro-viewer).

Why it feels 2D: map-centric equirectangular view; depth/time exposed as selectors and
graphs, not as navigable volume. Confirmed gap vs F1 depth-resolved volumetric views.

Borrow the toolset (profile, section, time-series, subset/export), rebuild inside 3D volume.
Reference product for data: [GLOBAL_MULTIYEAR_PHY_001_030](https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description).

## 3. 4D toggle — definition + scope rule

4D = 3D space (lon, lat, depth) + time controls. No simultaneous 4-axis render exists;
"4D view" means scoped volume with time scrub/play.

Modes (one Cesium viewer, not two engines):

| Mode | Camera | Content | Time |
|---|---|---|---|
| Globe | global | imagery + bathymetry + markers | lighting clock only |
| 3D location | scoped bbox | slice, curtain, isosurface, currents, exaggeration | fixed timestep |
| 4D location | scoped bbox | same volume + trajectory + model/profile compare | scrub + play, particles re-seed |

Scope rule: entering 3D/4D requires bbox + depth range + timestep. No unbounded volume fetch.
Lazier alternative: preset locations replace geocoder (same demo effect, fewer deps).

## 4. Cesium subsurface — the enabling APIs

- [Underground & Undersea](https://cesium.com/use-cases/underground-undersea/): bathymetry base
  ([World Bathymetry](https://cesium.com/platform/cesium-ion/content/cesium-world-bathymetry/)),
  transparent water/earth to reveal sub-surface data, per-region translucency tuning.
- [Visualizing underground](https://cesium.com/blog/2020/06/16/visualizing-underground/):
  `screenSpaceCameraController.enableCollisionDetection = false` lets camera go below surface;
  ground-hidden-near-camera for interior walk; opaque-until-close for context.
- [GlobeTranslucency](https://cesium.com/learn/cesiumjs/ref-doc/GlobeTranslucency.html),
  [camera guide](https://cesium.com/learn/cesiumjs-learn/cesiumjs-camera).
- Known risk: camera jump with translucency since 1.136
  ([issue #13092](https://github.com/CesiumGS/cesium/issues/13092) — UNVERIFIED 2026-09-09, no fetch this session). Pin ≥1.119 (zarr-cesium floor), test translucency behavior at pin before ADR.
- Prior art: Terradepth seabed/wrecks on Cesium; Camptocamp boreholes/seismic.

## 5. zarr-cesium — rendering core confirmed

Repo: [NOC-OI/zarr-cesium](https://github.com/NOC-OI/zarr-cesium) (MIT, TS, demo
[site](https://noc-oi.github.io/zarr-cesium/), docs
[site](https://noc-oi.github.io/zarr-cesium/docs)). v2+v3, multiscale (ndpyramid),
EPSG:4326/3857, on-demand streaming, GPU color mapping.
Fetched README 2026-09-09 adds: Icechunk/custom Zarrita stores, private HTTP
(`requestOverrides`/`transformRequest`/`onAuthError`), point/time-series/
profile/transect query APIs with cancellation, CesiumJS 1.119+ incl 1.142+.
Query APIs cover F2 click-profile plumbing — cite in stack ADR.

| Provider | Role in toggle |
|---|---|
| `ZarrLayerProvider` | Globe mode SST/surface overlay |
| `ZarrCubeProvider` | 3D/4D slices (horizontal + vertical curtain), exaggeration |
| `ZarrCubeVelocityProvider` | currents particles, depth + time bound |

Peer 4D references: [DOVis](https://github.com/HungerBar/DOVis) (FastAPI + Cesium, Indian Ocean),
[nordicseas3d](https://github.com/nordicseas3d/nordicseas3d.github.io) (Zarr-in-browser slices/sections),
[DeepSwitch](https://github.com/19Chris98H/DeepSwitch) (space-time cube for non-experts),
[OceanBrowser paper](https://www.vliz.be/imisdocs/publications/ocrd/296600.pdf).

## 6. PS fit

- F1 volumetric + slices + isosurface + time: 3D/4D location modes. Keep.
- F2 markers + click profiles: globe + scoped modes. Keep.
- F4 controls: palette/range/log-linear/opacity/exaggeration as shader uniforms. Keep.
- F5/F7: xpublish REST + OPeNDAP plugin; WMS/WCS roadmap-only until live.
- Mandates (hazard, SAR, fishery, climate): map one demo beat each. Open.

## 7. Kill risks

- Full-cube fetch kills memory. Enforce bbox + depth + time chunk requests, abort stale, downsample-while-drag.
- Isosurface server-side/precomputed + cached first; browser volume deferred.
- Every sample: dataset, variable, units, UTC time, QC/mode, transform version.
- `residual = model − observation`; anomaly only with stated baseline.
- Pre-warm offline demo assets; recorded backup after live attempt.
- In-situ collection URL unknown — do not invent.

## Open threads

- Verify Cesium #13092 status, then pin version (floor ≥1.119) + ADR.
- Resolve Esri "archwatch" target or drop assumption.
- Observations GeoJSON-vs-Arrow cutoff; chunk hypothesis benchmark; reference laptop lock.
- Geocoder vs presets decision (presets first).
