# Deep-research synthesis — all prem22k docs (2026-09-09)

9router tavily search (6 angles) + tavily fetch (5 pages). Verified each doc claim.
Access date 2026-09-09 throughout.

## 1. Verified CONFIRMED

- nullschool data stack: GFS weather, OSCAR v2.0 currents, CMEMS analysis/forecast
  (DOI 10.48670/moi-00016), OI SST v2.1, OSTIA, RTGSST, WAVEWATCH III.
  Source: [about page](https://earth.nullschool.net/about).
- nullschool pipeline: grib2json (netcdf-java) offline → static JSON → S3/Cloudflare.
  No runtime server. Source: [EQUINOCT fork](https://github.com/EQUINOCT/earth-nullschool).
- nullschool render: D3 projection + Canvas 2D. 2D only, no depth axis.
  Source: [about page](https://earth.nullschool.net/about).
- MyOcean Pro is 4D (lon/lat/depth/time): catalogue hybrid search, multi-variable,
  zoom ~150 m, EPSG:4326 + polar, date-time + depth selection, point query,
  time-series, depth-profile, line/polygon section + trajectory, histogram,
  export `.nc`/`.CSV`, palettes SEQUENTIAL/DISCRETE/DIVERGING, LINEAR/LOG,
  layer opacity, deep link, embed iframe, guided tour.
  Source: [main features](https://help.marine.copernicus.eu/en/articles/4794675-main-features-of-myocean-pro-viewer).
- MyOcean Pro has NO geographical location search bar (❌ in UX table).
  Our fly-to is a real differentiator, not parity. Same source.
- zarr-cesium: MIT, Zarr v2+v3, multiscale (ndpyramid/GeoZarr), Icechunk stores,
  EPSG:4326/3857, on-demand streaming, GPU colormap, 3 providers
  (`ZarrLayerProvider` 2D / `ZarrCubeProvider` volumetric slices + exaggeration /
  `ZarrCubeVelocityProvider` u/v particles via cesium-wind-layer fork),
  point/time-series/profile/transect query APIs with cancellation,
  CesiumJS 1.119+ incl 1.142+. Source: [GitHub](https://github.com/NOC-OI/zarr-cesium).
- Cesium subsurface: globe transparency + `enableCollisionDetection = false` +
  `translucencyEnabled` + `frontFaceAlphaByDistance`, Sandcastle demos
  (Globe Translucency / Interior / Underground Color).
  Sources: [blog](https://cesium.com/blog/2020/06/16/visualizing-underground/),
  [forum test thread](https://community.cesium.com/t/help-us-test-the-new-underground-features-in-cesiumjs/9581).
- NASA Eyes: suite of 3D viz apps over real NASA data/imagery, browser-run,
  click-and-zoom-to, temporal nav.
  Source: [NASA Eyes](https://science.nasa.gov/eyes).
- WebGPU volume paper exists: Yu et al, Appl Sci 15(5):2782 — ray casting +
  early termination + adaptive sampling, Babylon.js + WebGPU, regular + irregular
  grids. Validates slices/curtain/isosurface-first limiter cited in 03.
  Source: [MDPI](https://www.mdpi.com/2076-3417/15/5/2782).
- Kiln (WebGPU out-of-core, bricked storage, LRU streaming, ~2 GB in browser,
  few-hundred-ms first render) confirms chunked-streaming direction.
  Source: [forum](https://forum.image.sc/t/kiln-a-webgpu-native-out-of-core-rendering-system-for-virtualized-volumetric-data/120375).

## 2. Corrections to prem22k docs

- 05 §NASA Eyes "Unity → WebGL export": UNSOURCED. NASA page says browser-run
  but names no engine. Soften to "engine undisclosed; treat as closed showcase".
  Fix in 05 before citing externally.
- 06 §5 "48 stars": STALE. Mirror shows 39 stars, updated 2025/12/23.
  Source: [mirror](https://threejs3d.com/cesium-projects/projects/noc-oi-zarr-cesium).
  Fix number or drop it (stars rot fast — prefer version/API facts).
- 06 §4 "issue #13092 camera jump since 1.136": NOT re-verified this session
  (no fetch). Keep as risk with "unverified 2026-09-09" tag until checked.
- 02 "Esri archwatch": still ambiguous, no search run (assumed Living Atlas/EMU).
  Flag stays.

## 3. New win-relevant findings

- MyOcean Pro lacks geocoder → fly-to + presets is differentiation, keep in pitch.
- MyOcean Pro deep-link + embed + guided tour = outreach-mode checklist items.
  Add to 03 scene arc / M5.
- zarr-cesium query APIs (profile/transect + cancellation) already cover F2
  click-profile plumbing. Cite in stack ADR.
- Cesium 1.119+ support incl 1.142+ gives version-pin floor. Pin ≥1.119, test
  translucency camera behavior at pin.
- Kiln LRU + bricked streaming vocabulary backs Zarr chunking ADR language.

## 4. Per-doc verdict

| Doc | Verdict |
|---|---|
| 01 ps-fit | stands; no external claim needed re-verification |
| 02 benchmarks | nullschool half CONFIRMED via about+fork; Esri half still assumption |
| 03 design-transfer | WebGPU limiter CONFIRMED via paper; rest is design judgment, stands |
| 04 fly-to | strengthened: MyOcean ❌ geocoder confirms gap; presets-first order stands |
| 05 toggle | stands except Unity + stars fixes above |
| 06 9router toggle | stands except stars number; #13092 needs verification tag |

## 5. Follow-ups (doc-only, no code)

1. Fix Unity + stars lines in 05/06.
2. Verify Cesium #13092 status before version pin ADR.
3. Resolve Esri archwatch target or drop assumption.
4. Dataset cards + mandate→beat map still open (from 01).
