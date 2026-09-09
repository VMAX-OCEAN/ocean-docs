# 3D globe + 4D location toggle (2026-09-09)

Links to `problem-statement/PROBLEM-STATEMENT-ANALYSIS.md` F1–F7. No shared edits.

## Plan under test

Google-earth 3D globe default. NASA-Eyes-style object focus. MyOceanPro-style depth/time controls. Toggle: 3D view / 4D view for selected location.

## NASA Eyes teardown

- Apps: Eyes on Earth, Solar System, Exoplanets. Real NASA data/imagery, browser-run, free explore, temporal nav. Engine undisclosed — treat as closed showcase, not reusable stack. Verified 2026-09-09 via [NASA Eyes](https://science.nasa.gov/eyes).
- Borrow: camera language (approach → orbit → focus), object as query (click satellite/dataset → panels), time scrub tied to scene.
- Limit: no NetCDF ingest, no Argo QC, no model–obs residual, no OPeNDAP/CF pipeline. Showcase, not analysis backend.
- Lesson: globe polish comes from curated base + lighting + tours. Copy tours as guided outreach mode (F-outreach), not science core.

## MyOceanPro teardown — VERIFIED 2026-09-09

- Viewer: Copernicus Marine MyOcean Pro, self-described 4D (lon/lat/depth/time). Full toolset per [features doc](https://help.marine.copernicus.eu/en/articles/4794675-main-features-of-myocean-pro-viewer): catalogue hybrid search, multi-variable, zoom ~150 m, EPSG:4326 + polar, date-time + depth selection, point query, time-series, depth-profile, line/polygon section + trajectory, histogram, `.nc`/`.CSV` export, palettes, LINEAR/LOG, opacity, deep link, embed, guided tour. No geocoder (❌).
- Why feels 2D: map-first projection, depth = slider value not volume, weak direct manipulation, panels dominate canvas.
- Borrow: depth/time control pattern, profile extraction UX, bbox subset flow, variable comparison.
- Limit: no volumetric depth perception, no float-as-anchor interaction, no residual field.
- Lesson: keep its controls, replace its canvas with Cesium globe + depth curtain.

## Nullschool fresh — CONFIRMED 2026-09-09

- Data: GFS weather, OSCAR v2.0 currents, CMEMS global physics analysis/forecast (DOI 10.48670/moi-00016), OI SST v2.1, OSTIA, RTGSST, WAVEWATCH III. Source: [about](https://earth.nullschool.net/about).
- Pipeline: grib2json (netcdf-java) offline → static JSON → S3/Cloudflare. No runtime server. Source: [EQUINOCT fork](https://github.com/EQUINOCT/earth-nullschool).
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

## Sources (2026-09-09, verified via 9router tavily fetch)

- https://science.nasa.gov/eyes (Eyes suite: browser-run 3D, real data, engine undisclosed)
- https://earth.nullschool.net/about (fetched: OSCAR v2.0, CMEMS DOI 10.48670/moi-00016, OI SST, OSTIA, D3 + Canvas)
- https://github.com/EQUINOCT/earth-nullschool (pipeline: grib2json offline → static)
- https://help.marine.copernicus.eu/en/articles/4794675-main-features-of-myocean-pro-viewer (fetched: full 4D toolset, no geocoder)
- https://data.marine.copernicus.eu/viewer (JS shell only; control pattern from shared docs)
- https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description
- Shared: `docs/architecture/tech-stack.md` (CesiumJS + zarr-cesium lock)

`ponytail:` geocoder + live 4D volumes deferred; presets + bounded subsets ceiling now, upgrade when M1–M4 proven.
