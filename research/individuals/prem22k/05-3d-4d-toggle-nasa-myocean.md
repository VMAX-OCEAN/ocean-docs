# 3D globe + 4D location toggle (2026-09-09)

Links to `problem-statement/PROBLEM-STATEMENT-ANALYSIS.md` F1–F7. No shared edits.

## Plan under test

Google-earth 3D globe default. NASA-Eyes-style object focus. MyOceanPro-style depth/time controls. Toggle: 3D view / 4D view for selected location.

## NASA Eyes teardown

- Apps: Eyes on Earth, Solar System, Exoplanets. Real mission data, free explore, temporal nav.
- Stack: Unity game engine → WebGL export, not hand-rolled Three.js. Curated datasets, scripted tours.
- Borrow: camera language (approach → orbit → focus), object as query (click satellite/dataset → panels), time scrub tied to scene.
- Limit: no NetCDF ingest, no Argo QC, no model–obs residual, no OPeNDAP/CF pipeline. Showcase, not analysis backend.
- Lesson: globe polish comes from curated base + lighting + tours. Copy tours as guided outreach mode (F-outreach), not science core.

## MyOceanPro teardown

- Viewer: Copernicus Marine viewer. Layers, depth slider, time slider, profile extraction, subset download.
- Why feels 2D: map-first projection, depth = slider value not volume, weak direct manipulation, panels dominate canvas.
- Borrow: depth/time control pattern, profile extraction UX, bbox subset flow, variable comparison.
- Limit: no volumetric depth perception, no float-as-anchor interaction, no residual field.
- Lesson: keep its controls, replace its canvas with Cesium globe + depth curtain.

## Nullschool fresh (about page, 2026-09-09)

- Data: GFS weather, OSCAR v2.0 currents, CMEMS global physics analysis/forecast, OI SST v2.1, OSTIA, RTGSST, WAVEWATCH III.
- Pipeline: grib2json (netcdf-java) offline → S3/Cloudflare static. No runtime server.
- Render: D3 projection + Canvas 2D overlay + particle layer. 2D only, no depth axis.
- Borrow: particle advection for u,v; instant scrub feel; static precompute pattern matches Zarr chunk preload.
- Limit: no profiles, no QC, no match-up.

## Toggle design

- One switch: `2D map / 3D globe / 4D location`.
- Search → bbox, not point. Catalogue query filters datasets by bbox. Empty bbox = blocked view with message, never blank globe.
- 3D mode: Cesium globe, terrain + bathymetry, SST overlay, currents particles, markers.
- 4D mode: bounded location volume. Small bbox + 3–5 depths + 3–5 timesteps + 1 variable + nearby markers. Depth slider, curtain, time scrub, profile click.
- Same F4 controls all modes: palette, min/max, log/linear, opacity, exaggeration. Exaggeration factor labeled beside view.
- Progressive: globe → location → float → profile → residual. Residual gated on QC/method, `residual = model − observation`.

## Budgets / risks

- Never full water column. `24×40×500×500 ≈ 0.96 GB` float32 never ships whole. Subset API + Arrow/binary only.
- Fly races fetch → jank. Preload low-res slice first, abort superseded, preset buttons before live geocoder.
- Geocoder land/no-data kills demo. Presets: Bay Bengal eddy, Arabian Sea. Offline pre-warm mandatory.
- Unlabeled field blocked: units + standard_name + missing-value rule + source version + ETag required.

## Order

M1 globe + presets → M2 surface + time → M3 depth + currents → M4 markers + profiles → 4D toggle last, bounded bbox.

## Sources (2026-09-09)

- https://eyes.nasa.gov/ (JS-heavy, generic shell fetched; app detail from cutoff knowledge)
- https://earth.nullschool.net/about (scraped: OSCAR v2.0, CMEMS, OI SST, OSTIA, D3 + Canvas)
- https://data.marine.copernicus.eu/viewer (JS shell only; control pattern from shared docs)
- https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description
- Shared: `docs/architecture/tech-stack.md` (CesiumJS + zarr-cesium lock)

`ponytail:` geocoder + live 4D volumes deferred; presets + bounded subsets ceiling now, upgrade when M1–M4 proven.
