# D5 — Externals Resolved + Reuse Teardowns

Date: 2026-09-10. 5 agents + 3 closers. `$NINEROUTER_KEY` absent in tool shell, gateway skipped. Access date per URL. UNVERIFIED marked.

## 1. Esri 3D target — resolved

| Rank | Candidate | URL | Verdict |
|---|---|---|---|
| 1 | EMU Explorer | `https://livingatlas.arcgis.com/emu/` | CITE primary 3D ocean baseline + UX |
| 2 | Ocean basemap | `.../arcgis/rest/services/Ocean/World_Ocean_Base/MapServer` | CITE base layer only |
| 3 | 3D Ocean Explorer / Ocean Voxels | `https://labs.esri.com/ocean-explorer/` → canonical `.../ocean-voxels/` | DROP as dependency (code repo 404, license `For demo purposes only`); cite voxel prior art only |
| 4 | Living Atlas generic | `https://www.esri.com/en-us/arcgis/products/arcgis-living-atlas` | DROP as target; discovery portal at most |

EMU: JSAPI 4.24 SceneView + WebScene via portalItem; app item modified 2026-02-19; repo pushed 2023-08-19; code Apache-2.0. Ocean basemap: live, 17 LODs scales 591657527→9027, JPEG 256px EPSG:3857, item created 2014-02-24 modified 2026-05-26; attribution verbatim `Esri, Garmin, GEBCO, NOAA NGDC, and other contributors`; GEBCO no-navigation/safety-at-sea note. Reference service `.../Ocean/World_Ocean_Reference/MapServer` tileCache true.

Copy keys: `esri/views/SceneView`, `esri/WebScene`, `esri/Map`, `new WebScene({portalItem:{id}})`, `view.goTo({tilt:45})`, `basemap:"sat"`, `.../4.24/esri/themes/dark/main.css`, VoxelLayer docs `https://developers.arcgis.com/javascript/latest/api-reference/esri-layers-VoxelLayer.html` (description-level). EMU data keys: 37 units, 6 vars (temperature, salinity, dissolved oxygen, nitrate, phosphate, silicate), 1/4° mesh, 102 depth zones (counts description-level). Item IDs: `58526e3af88b46a3a1d1eb1738230ee3` (EMU Explorer), `1e126e7520f9466c9ca28b8f28b5e500` (Ocean Base), `a1ba51fed98144de83bb2cc287550e20` (Voxels), `6a16bb85e9ab47829aa626dced51edc6` (netCDF sample 2021-10-12). UNVERIFIED: EMU bundle portalItem IDs (`CONT_0001` inaccessible), voxel bundle internals, Living Atlas page license, USGS label + bands beyond item descriptions.

Cesium instead: SceneView/WebScene + tilt → `Viewer` + `camera.flyTo` pitch ~-45° presets in repo JSON, no portal dependency; VoxelLayer → pre-sliced EMU volumes + `clippingPlanes` + profile panel, never 52M points in browser; Ocean Base + Reference → two imagery layers with verbatim attribution + GEBCO note; `basemap:"sat"` → optional imagery toggle. Best: EMU cite + Ocean Base underneath + Sayre 2017 + USGS DOI. Lazier: tiles + EMU summary sheets, skip voxel build.

## 2. USGS EMU numbers — dual-sourced

| claim | value | sources 2026-09-10 |
|---|---|---|
| DOI | 10.5066/P9Q6ZSGN → ScienceBase `642c9bd0d34ee8d4add254c0` | doi.org 302 + ScienceBase JSON identifiers |
| units | 37 distinct volumetric regions | ScienceBase body + TOS abstract |
| 6 vars | temperature, salinity, dissolved oxygen, nitrate, phosphate, silicate | ScienceBase + TOS + USGS news |
| depth bands | epipelagic 0–200m, mesopelagic 200–1000m, bathypelagic 1000–4000m, abyssopelagic >4000m | ScienceBase + TOS + item description |
| 37-unit list | Appendix 1 (numbers, CMECS, names, codes) + Appendix 2 (descriptions + maps) | TOS supplements + ScienceBase webLinks |
| points | over / more than 52 million | ScienceBase + TOS + Esri overview + USGS news |
| zones | 102 depth zones (count only) | Esri overview + USGS news (102 knots to 3.5 miles) |
| climatology | 57-year, decadal means, WOA 2013 v2 | ScienceBase + TOS |
| split | 22 extensive = 99% volume, 15 coastal | ScienceBase + TOS + USGS news |
| item | `58526e3a…`, owner `esri_oceans`, CC BY 4.0 item-only | ArcGIS item JSON |
| repo | `Esri/ecological-marine-units-explorer`, master, created 2017-07-20, Apache-2.0 | GitHub API + README |
| data license | `http://www.usa.gov/publicdomain/label/1.0/` (URL confirmed; deed wording UNVERIFIED — redirects) | data.usgs.gov JSON + USGS news |

UNVERIFIED: interval breakdown 5/25/50/100m to 5,500m (Exa-only, PDF redirect); mesh nuance (1/4° T/S, 1° others); deed text. `ponytail:` Esri "1/4° + 102 zones" simplified — upgrade path full Sayre 2017 PDF.

Cite-ready:
- Sayre, R., 2023, EMUs: USGS data release, `https://doi.org/10.5066/P9Q6ZSGN`. Accessed 2026-09-10.
- Sayre et al., 2017, A Three-Dimensional Mapping of the Ocean Based on Environmental Data: Oceanography 30(1), 90–103, `https://doi.org/10.5670/oceanog.2017.116`. Accessed 2026-09-10.
- Esri, Ecological Marine Units overview. Accessed 2026-09-10.
- USGS, Mapping the World's Ocean Ecosystems, 2017-04-24. Accessed 2026-09-10.
- ArcGIS item `58526e3af88b46a3a1d1eb1738230ee3`, `https://livingatlas.arcgis.com/emu`. Accessed 2026-09-10.
- GitHub `Esri/ecological-marine-units-explorer`, Apache-2.0. Accessed 2026-09-10.

## 3. INCOIS — resolved, card written

Holdings `https://incois.gov.in/site/dataholdings.jsp` HTTP 200, 44 rows. ERDDAP `https://erddap.incois.gov.in/erddap/` live, 16 datasets (`info/index.csv` — bare path 302, `-L` required): AMSRE_MONTHLY_GLOBAL, ascat_daily/mnt, NOAA_AVHRR_AMSR, incois_argo 10day/mnt McCreary + 10d VAM, argo_sst_weekly, oceansat2, quickscat daily/mnt, tmi_3day, valueadded, IRS_chlorophyll, Indian_ARGO_Floats. Per-dataset griddap `.das/.dds/.csv/.nc/.graph` + FGDC/ISO19115 + RSS; tabledap `Indian_ARGO_Floats` `.subset/.csv/.graph`. LAS `https://las.incois.gov.in/las` GWT app: `getCategories.do` 13 cats (ARGO, ASCAT, GODAS, IGORA, MaMetAtTIO, MICROWAVE, NIO climatology, NOAA SST, Ocean Carbonate, OCEAN COLOUR, Oscat, QUICKSCAT, Tropflux 1940-2025); `getDatasets.do?catid=` works (endpoint ignores catid, md5-identical 52-dataset dump; SST cat ~17MB latin-1). ESSDP `https://incois.gov.in/essdp/` HTTP 200, 16 metadata links; "1047 datasets" string NOT found — claim UNVERIFIED. THREDDS `.../thredds/catalog.html` HTTP 200 but single DatasetScan "Data form LAS", no per-dataset listing — OPeNDAP path UNVERIFIED, do not code. TLS needs `-k` (missing intermediate).

Key `.das` bbox/time: NOAA SST lon 20.125–139.875 lat -29.875–29.875 (0.25°), time ends 2011-10-04 (regional, not global); VAM lon 30.5–119.5 lat ±29.5, ends 2026-07-30; floats 2002-10-24–2025-04-23. 11 unfetched `.das` = index summaries only. License verbatim (ERDDAP `.das` boilerplate): "The data may be used and redistributed for free but is not intended for legal use, since it may contain inaccuracies. Neither the data Contributor, ERD, NOAA, nor the United States Government … makes any warranty … or assumes any legal liability …". Holdings tiers exact wording + counts; ~15 blank cells unknown.

Copyable (200s, 2026-09-10):

```bash
curl -k "https://erddap.incois.gov.in/erddap/griddap/NOAA_AVHRR_AMSR_datasets.csv?sst%5B(2010-01-01T00:00:00Z):1:(2010-01-02T00:00:00Z)%5D%5B(0.0):1:(0.0)%5D%5B(10):1:(12)%5D%5B(60):1:(62)%5D"
# → time,zlev,latitude,longitude,sst rows e.g. 2010-01-01T00:00:00Z,0.0,10.125,60.125,27.31
curl -k "https://erddap.incois.gov.in/erddap/tabledap/Indian_ARGO_Floats.csv?PLATFORM_NUMBER,latitude,longitude,time&time%3E=2020-01-01T00:00:00Z&time%3C=2020-02-01T00:00:00Z&orderBy(%22time%22)"
curl -k "https://las.incois.gov.in/las/getCategories.do"
curl -k "https://las.incois.gov.in/las/getDatasets.do?catid=0F031264DFBA634FEC1F23F7240DBFB3"
```

Ingest order: ERDDAP first (`.das` axes → griddap `.nc` slices, tabledap `.csv` points) → LAS catalog second → holdings static ref only (viz-only rows need requisition form). Full card: `docs/data/incois-las.md` (10.8K, 8 assumptions, sha NONE explicit — live APIs). Verdict: cite-with-links.

## 4. Mapbox — verified + official pricing

Globe: `new mapboxgl.Map({container, projection:'globe'})`, `setProjection/getProjection`, enum `albers|equalEarth|equirectangular|globe|lambertConformalConic|mercator|naturalEarth|winkelTripel`; default style v12 `globe`; needs v2.9+; terrain/fog/FreeCamera globe-only. Camera: `easeTo` (offset [0,0], duration 500, defaultEasing), `flyTo`, `jumpTo`; `CameraOptions` center/zoom/bearing/pitch/fov[0.01,60]/around/padding/retainPadding/minZoom/maxZoom; `AnimationOptions` duration/easing/offset/animate/essential/preloadOnly/curve 1.42/minZoom/speed 1.2/maxDuration/linear. `essential:true` overrides `prefers-reduced-motion`. Terrain: `addSource raster-dem mapbox://mapbox.terrain-rgb` + `setTerrain({source, exaggeration 0-1000 default 1})`, globe|mercator, SDK ≥2.0. Fog: `setFog/getFog`, color/high-color/horizon-blend/range/space-color/star-intensity/vertical-range, gates ≥2.3/2.9/3.0. Sources: projections/globe guides, camera API + raw `camera.ts`, terrain/fog spec, flyto example (all 2026-09-10).

Model verified: per Map Load, unlimited tiles per session, 12h max then new load, v2+ per-map billing, email-only overage. Official pricing (`https://www.mapbox.com/pricing`, 2026-09-10 — prior provisional corrected, adds $2.50 tier): Map Loads 50k free then $5/$4/$3/$2.50 per 1k; Directions 100k then $2/$1.60/$1.20; Temp Geocoding 100k then $0.75/$0.60/$0.45; Static 50k then $1/$0.80/$0.60; Mobile MAU 25k then $4/$3.20/$2.40. PROVISIONAL dropped.

Cesium equivalents: `camera.flyTo` (destination/orientation/duration/maximumHeight/pitchAdjustHeight/flyOverLongitude/easingFunction/complete/cancel) + `flyToBoundingSphere` + `flyHome(3)`; `EasingFunction.*`; `CesiumTerrainProvider.fromIonAssetId/fromUrl`; `screenSpaceCameraController`; atmosphere via `skyAtmosphere`/`atmosphere`/`skyBox` not `setFog`. Dropped: `CameraFlightPath` (404), `setView` + `FreeCameraOptions` (unverified). Cesium always globe — no `setProjection` needed.

## 5. gods-eye-view — useful YES, reference not fork

`bilawalsidhu/gods-eye-view`: browser spy-satellite simulator on photorealistic 3D Earth. CesiumJS-only (`cesium ^1.124.0`, vanilla JS, vite 6, `vite-plugin-cesium ^1.2.23`, `satellite.js ^6.0.2`, `@mapbox/vector-tile`, `pbf`, `mgrs`, `egm96-universal`). No Three/MapLibre/deck/zarr/netcdf/particles. Globe yes (Google tiles direct+ion, Esri keyless, OSM, Re:Earth terrain). Fly-to yes (presets, POIs, search). Particles no (traffic dots = PointPrimitives lerp). Markers yes (5000+ billboards, PointPrimitiveCollection, CLAMP ellipses). Profiles no. Time partial (live poll + SGP4, no slider). Data: JSON APIs via Vite `/api/*` proxies + governors (OpenSky TTL+429+stale, TomTom 40000/day, `.gev-cache/`). Counts dated 2026-09-10: stars 22311, forks 4744, issues 148, pushed 2026-09-05 (Exa 541 stale rejected). License: code MIT with third-party carve-out (GitHub API NOASSERTION) — TeleGeography CC BY-NC-SA (delete for commercial/gov), OSM/Overpass/adsb.lol ODbL share-alike, OpenSky non-commercial, TomTom/Google BYOK.

Ranked copies (exact paths + keys): 1. `src/renderGovernor.js` (`installRenderGovernor`, `holdContinuousRender`, `releaseContinuousRender`, `governorRequestRender`, `maximumRenderTimeChange = Infinity`) — idle-GPU fix. 2. `src/data/manager.js` (`DataLayerManager`, `layerFeedState`, nominal/loading/degraded/stale/fallback/unavailable, `init/enable/disable/update/destroy/getStats`). 3. `src/sharelink.js` (`ShareLinkManager`, lat/lon/alt/heading/pitch/style/bloom hash, `encodeLayerStateParams/decodeLayerStateParams`). 4. `src/mapStackController.js` + `src/mapStartup.js` (`MAP_STACKS`, `ESRI_WORLD_IMAGERY_URL`, `REEARTH_TERRAIN_URL`, `selectMapStartupRoute`, `loadPhotorealisticTileset`). 5. `src/data/earthquakes.js` + `src/data/localGeojson.js` (`depthColor`, 32.4→1.4ms static-ellipse note, `LOCAL_OVERLAY_COHORT_LIMIT`, `GROUND_SAMPLE_MAX_ARMED_RETRIES`). 6. `src/data/satellites.js` (SGP4 `twoline2satrec/propagate/gstime/eciToGeodetic`, `ORBIT_PATH_STEPS 180`, `POSITION_UPDATE_MS 1000`). 7. `src/data/trailRenderer.js` (`TRAIL_ALPHA 0.85`, occluded 0.4, `depthFailMaterial`, `gev-trail:` namespace). 8. `src/data/flights.js` header pattern only (262KB — billboard batching, `alignedAxis`, dead-reckoning + 1s lerp, click-track in place). 9. `src/camera.js` + `src/locations.js` (`CAMERA_PRESETS`, `CUBIC_IN_OUT`, `CITY_POIS`, `flyToGlobeView`). 10. `vite.config.js` proxy governors (extract per-route). 11. `src/data/dataCredits.js` + `DATA_SOURCES.md` (attribution lightbox). 12. `src/scenes/director.js` (cinematic recipes — demo-video only).

Implement in ocean-web: governor holds in `config.ts`; TS-lite layer manager with honest `KEY REQUIRED`/`STALE` chips; extend `base-imagery.ts` (Esri keyless default + ion/Google optional, Re:Earth fallback); hash share links in viewer/App; billboard+trail vessel/Argo layers (static geometry, no per-frame CallbackProperty); server proxies in ocean-api (TTL + budget + serve-stale). Drop: voice/OpenAI, CCTV, radio, bikeshare, traffic sim, cockpit, detection overlays, TeleGeography bundle. UNVERIFIED: `src/iconOrientation.js` root (real module under `src/data/`), `src/styles/` listing, voice tool count 28.

## 6. NASA Eyes — engine undisclosed, inspiration-only

Copy: object-as-query (click → fly + panel, Home reset); orbit/zoom/double-click focus, ride-along, Draw Mission path; LIVE + 1950–2050 scrub + speed (Cesium timeline native suffices); trails/orbits/labels/icons toggles + type filters; full-DB search + curated lists + Browse Destinations; next-5 watchlist + countdown; Vital Signs animate (SST, chlorophyll, sea level, …); Learn scrolly. M5 10-step tour: home+search+LIVE → object click → time scrub → Draw Mission → filters → vital-sign animate → watchlist → scrolly 3 stops → compare overlay → home reset. Sources: `https://science.nasa.gov/eyes/` + apps + tutorials + 2026-04-30 trajectory post + FAQ (2026-09-10; exoplanets direct 403, tutorial instead).

## 7. Open items

USGS full-PDF methods + deed text (redirects); Mapbox none (closed official); INCOIS per-dataset DAS remaining 11 + LAS catid mapping + ESSDP 1047 string; gods-eye port Vera? No — ports scheduled at build time per §5 mapping.
