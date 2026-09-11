# 03 — Prem22k Product/Science Track (8 files)

**Namespace:** `../../individuals/prem22k/`
**Role:** Product + science. PS-fit audit, benchmark teardowns, design transfer, fly-to, toggle, synthesis.
**Date:** 2026-09-09. Verification: 9router tavily search + fetch (6 angles, 5 pages). Access date throughout.
**Self-correcting:** `07-deep-research-synthesis.md` audits 01–06, flags Unity/stars/#13092/Esri.

---

## 1. Namespace at a glance

| # | File | Role | Status | Serves |
|---|------|------|--------|--------|
| 0 | `README.md` | Index | NO-CLAIMS | Scope collision rules only, refs R1-R8/W1-W2 residual rule Zarr ADR |
| 1 | `01-ps-fit-and-win-analysis.md` | R/F audit + gaps + inventions + win moves + M0 fixture | STANDS per 07 | R1-R5, R6 partial, R7 partial, R8 weak, W1-W2 differentiator |
| 2 | `02-benchmarks-nullschool-esri.md` | Benchmark teardowns | SPLIT | nullschool CONFIRMED via about+EQUINOCT fork; Esri UNVERIFIED assumption; MyOcean Pro VERIFIED; NASA Eyes VERIFIED engine undisclosed |
| 3 | `03-design-transfer-and-scene-arc.md` | Film/camera + spaces + games + journalism + SaaS + Mapbox 4D + WebGPU limiter + scene arc 01-07 | PARTIAL CONFIRMED | WebGPU limiter CONFIRMED via Yu et al Appl Sci 15(5):2782; rest design judgment stands |
| 4 | `04-google-earth-fly-to.md` | Preset-first fly-to | STRENGTHENED CONFIRMED | MyOcean Pro NO geocoder verified — differentiation, outreach hook opening 12s |
| 5 | `05-3d-4d-toggle-nasa-myocean.md` | Toggle + budgets + order | STANDS CORRECTED | NASA Eyes/MyOcean/Nullschool verified; Unity claim fixed to undisclosed |
| 6 | `06-earth-3d-4d-toggle-9router.md` | Verified toggle + subsurface + zarr-cesium + scope rule | MOSTLY CONFIRMED | zarr-cesium + Cesium subsurface CONFIRMED; #13092 UNVERIFIED; stars STALE |
| 7 | `07-deep-research-synthesis.md` | Synthesis audit 01-06 verdicts | CONFIRMED audit | nullschool stack/pipeline/render, MyOcean 4D + NO geocoder, zarr-cesium, Cesium subsurface, NASA Eyes suite, WebGPU paper, Kiln streaming |

---

## 2. Per-file deep dive

### 2.0 `README.md` — index, no claims

Scope collision rules only. Refs R1-R8/W1-W2, residual rule, Zarr ADR. No R/F claim. No action.

### 2.1 `01-ps-fit-and-win-analysis.md` — PS-fit audit

**PS match table:**

| Req | Assessment | Detail |
|-----|------------|--------|
| R1 browser 3D water column | Keep | MapLibre + Three slice + curtain (predates Cesium lock — read as pattern, stack now Cesium) |
| R2 T/S/currents, depth/isosurface/time | Keep | M1/M4 |
| R3 Argo/Glider/CTD/BGC markers + click profile | Keep | M2/M3 |
| R4 NetCDF/xarray + delimited text, modular ingest | Adapters | PyNIO dead upstream — xarray choice needs one-line ADR |
| R5 palette/range/log-linear/opacity/exaggeration | Covered | Keep |
| R6 REST/OPeNDAP + no-install | Partial | REST defined, OPeNDAP facade missing |
| R7 OGC WMS/WCS + CF + plugin | Partial | CF strong, WMS/WCS roadmap only. Label roadmap, avoid compliance claim |
| R8 outreach + Disaster Management | Weak | Hazard, SAR, fishery, climate need demo beats |
| W1 residual/QC + W2 Zarr/benchmark | Differentiator | Keep |

**Gaps (5):**

| # | Gap | Fix |
|---|-----|-----|
| 1 | `sources.md` lacks 5 PS dataset links | Add las.incois, GLOBAL_MULTIYEAR_PHY_001_030, ifremer Argo, ifremer glider v2, blank in-situ |
| 2 | `data-contract-and-pipeline.md` uses synthetic `incois-demo-hycom-YYYYMMDD` | Need dataset cards + sha256 + license + bbox |
| 3 | `system-design.md` observations endpoint lacks GeoJSON-vs-Arrow cutoff | Suggest `<500 features GeoJSON` |
| 4 | Benchmark workload fixed (`256×256`, 40 depths, 24 steps, 2 vars, 1000 markers) but reference laptop absent | Lock device, run, record |
| 5 | HYCOM/GODAS context in problem-statement = assumption, not official | Label it |

**Win moves, ordered:**

| # | Move | Maps to |
|---|------|---------|
| 1 | Lock M0 fixture: one model cube + Argo profiles, Indian Ocean bbox, event date, manifest checksums | Dataset/ADR gate |
| 2 | Prove M1-M3 live: slice controls, marker click, profile + matchup residual with method + QC | M4 residual gate |
| 3 | M4 depth cue: curtain + exaggeration + currents; isosurface server/precomputed first | M3 scope rule |
| 4 | M5 harden: shareable view, outreach mode, clean-browser reload, compose deploy | M5 gate |
| 5 | Paper trail: dataset cards, ADRs (Cesium/PyNIO/OPeNDAP/chunking), OpenAPI client, benchmark record, known limits | All gates |
| 6 | Pitch dry-run: mandate-mapped 90s script, fallback quality mode | M5 gate |

**Kill risks (4):** full 4D fetch 0.96GB → subset API + downsample-while-drag; unlabeled field → block render without units + missing-value rule + source version + ETag; invented resolution → mark assumptions; net-dependent demo → pre-warm + recorded backup after live attempt.

**Assumptions flagged honestly:** HYCOM/GODAS not official; pasted PS canonical over listing URL; PyNIO-drop ADR owed; sources.md lacks 5 links; data-contract synthetic fixture needs cards.

**Status per 07:** STANDS. No external claim needed re-verification. Old paths referenced (`sources.md`, `data-contract-and-pipeline.md`, `system-design.md` pre-date current `docs/` layout — resolve names before citing).

### 2.2 `02-benchmarks-nullschool-esri.md` — benchmark teardowns

**earth.nullschool.net — CONFIRMED 2026-09-09:**

| Aspect | Finding | Source |
|--------|---------|--------|
| Data | GFS weather, OSCAR v2.0 currents, CMEMS global physics analysis/forecast DOI 10.48670/moi-00016, OI SST v2.1, OSTIA, RTGSST, WAVEWATCH III | [about](https://earth.nullschool.net/about) |
| Pipeline | grib2json (netcdf-java) offline → static JSON → S3/Cloudflare. No runtime server | [EQUINOCT fork](https://github.com/EQUINOCT/earth-nullschool) |
| Code | `github.com/cambecc/earth`. D3 + canvas. Projection + particle integrator reusable. 2D only, no depth | about + code |
| Interaction | Drag rotate, scroll zoom, click values, time scrub. Minimal chrome | about |
| Borrow | Current trails for u,v. Instant scrub feel. Location readout. Particles for surface currents in M4 | judgment — keep |
| Limit | No depth axis. No Argo profiles. No QC. No match-up. No NetCDF ingest | gap vs F1/F2 |
| Lesson | Science stays separate from particles | scope |

**Esri 3D Ocean Explorer — UNVERIFIED, assumption only:**

| Aspect | Finding |
|--------|---------|
| Target | "archwatch" ambiguous; no search run 2026-09-09. Assumed Living Atlas/EMU stack |
| Assumed stack | ArcGIS JS API WebScene + hosted bathymetry tiles + popups. Globe fly-to built-in |
| Borrow | Preset fly-to. Bathymetry base. Storytelling for outreach |
| Limit | Vendor lock. No NetCDF/Zarr pipeline. No residual/QC. INCOIS hosting unclear |
| Rule | **Do not cite externally until resolved** |

**Peers table:**

| Peer | Pattern to borrow | Verified |
|------|-------------------|----------|
| MyOcean Pro | 4D nav, depth/time controls, time-series, depth-profile, section + trajectory, histogram, `.nc`/`.CSV` export, palettes LINEAR/LOG, deep link, guided tour. **NO geocoder (❌) — our fly-to = differentiation** | 2026-09-09 [features](https://help.marine.copernicus.eu/en/articles/4794675-main-features-of-myocean-pro-viewer) |
| Argovis | Trajectory + profile + QC query (space/time/depth/parameter/quality/platform/year) | pattern ref |
| webODV | No-install flow profile → context → trajectory → comparison | flow ref |
| HUB Ocean | Region select → retrieval → viz workspace | workflow ref |
| NASA Eyes | Suite browser-run 3D, real NASA data, click-and-zoom-to, temporal nav. Engine undisclosed — closed showcase, not stack | 2026-09-09 [Eyes](https://science.nasa.gov/eyes) |
| Mapbox Globe | Camera/globe/terrain precedent. Fly-to proof | pattern ref |
| INCOIS holdings + training | Judge baseline (xarray, Cartopy, Plotly, 3D, anomaly, profiles, vectors). Missing from sources.md, add next | open |

**Status per 07:** nullschool half CONFIRMED via about+fork; Esri half still assumption.

### 2.3 `03-design-transfer-and-scene-arc.md` — design transfer

**Transfers (keep principles, cut decoration):**

| Source | Transfer | Constraint |
|--------|----------|------------|
| Film camera language | GLOBAL → INDIAN → ARABIAN → THERMOCLINE → FLOAT → PROFILE. Maps to 90s arc + presets | Keep |
| Architecture spaces | Exploration/comparison/observation/analysis/data = progressive disclosure | Keep |
| Games | Float-as-anchor, contextual controls. Observation-as-query | Keep anchor, require method labels |
| Journalism | Direct labels + nearby units beside phenomenon | Matches provenance rule, keep |
| SaaS disclosure | OCEAN → FLOAT → PROFILE → MODEL VS OBS → RESIDUAL. Matches M1→M2→M3 order | Gate last step on QC/method |
| Mapbox 4D canvas | lat×lon×depth×time matches canonical grid | Keep |
| WebGPU volume framework | Yu et al, Appl Sci 15(5):2782 — ray casting + early termination + adaptive sampling, Babylon.js + WebGPU, regular + irregular grids. **Validates slices/curtain/isosurface-first, full volume stretch.** Verified via [MDPI](https://www.mdpi.com/2076-3417/15/5/2782) | Cite as limiter |

**Visual system:** dark base (volume occupies space, not theme). Editorial headline + tiny telemetry. Semantic color: base deep blue/cyan, observation white/mint, model blue, residual orange/red, uncertainty translucency, feature accent. Constrain by R5 palette/range/log-linear/opacity/exaggeration + units on every plot.

**Motion vocabulary (selective):** camera = scale change. Morph = transform. Pulse = live. Trail = history. Fade = relevance. Split = compare. Scrub = causality. **Drop expansion = uncertainty until method exists.**

**Scene arc 01→07:** Enter → Approach → Reality → Grab → Compare → Divergence → Investigate. Matches pitch beats 0–90s.

**Sign fix:** paste uses `E = O − M`. Docs enforce `residual = model − observation`. Use docs form.

**Constraint:** point divergence now, volume divergence deferred. Sparse floats cannot form dense volume without interpolation assumptions. Require pre-warmed presets + abort superseded fetches + low-res first.

**Outreach checklist (from 07 MyOcean verified):** deep link incl layers/objects/plots, embed iframe, guided tour for beginners. Add to M5 outreach mode alongside NASA Eyes tour pattern.

**Thesis:** `Ocean you can interrogate` works as pitch line atop R1-R8 completion, not replacement. Judges score compliance first.

**Status per 07:** WebGPU limiter CONFIRMED via paper; rest design judgment, stands.

### 2.4 `04-google-earth-fly-to.md` — fly-to

Idea: search location → fly-to → zoom 3D → relevant filters. Verified: MyOcean Pro has NO geocoder (❌ UX table) — fly-to = differentiation, not parity, keep in pitch.

| Aspect | Detail |
|--------|--------|
| Fit | Strong hook for outreach + opening 12s. PS wants rapid intuitive understanding. Cheap with MapLibre flyTo, easier globe with Cesium |
| Risk 1 | Stack lacks globe+geocoder. True globe needs Cesium or MapLibre globe mode + ADR (PS names Cesium) |
| Risk 2 | Geocoder returns place, not feature. Needs bbox → catalogue query (`/v1/catalog/datasets?bbox=`), else empty view |
| Risk 3 | Fly animation races chunk fetch → jank. Need abort + preload low-res slice first |
| Risk 4 | Offline judging kills tiles + geocoder. Need pre-warmed demo locations |
| Lazier path | Preset flyTo buttons (Bay Bengal eddy 2026-08-10, Arabian Sea, …) replace geocoder + globe. Same demo effect, one config line, no dep |
| Order | Presets now. Cesium globe + search only after M1-M3 proven, behind ADR |
| Open thresholds | Observations GeoJSON vs Arrow cutoff. Chunk benchmark + reference device. Cold ≤10s / slice ≤750ms / 30FPS + ≤5000 markers on locked laptop |

**Status per 07:** STRENGTHENED. MyOcean ❌ geocoder confirms gap; presets-first order stands.

### 2.5 `05-3d-4d-toggle-nasa-myocean.md` — toggle

Plan: Google-earth 3D globe default. NASA-Eyes-style object focus. MyOceanPro-style depth/time controls. Toggle 3D / 4D for selected location.

**NASA Eyes teardown:** Eyes on Earth, Solar System, Exoplanets. Real NASA data, browser-run, free explore, temporal nav. Engine undisclosed — closed showcase, not reusable stack. Borrow camera language (approach → orbit → focus), object-as-query (click → panels), time scrub tied to scene. Limit: no NetCDF ingest, no Argo QC, no residual, no OPeNDAP/CF. Lesson: globe polish = curated base + lighting + tours. Copy tours as guided outreach mode, not science core.

**MyOceanPro teardown — VERIFIED:** full 4D toolset (catalogue hybrid search, multi-variable, ~150m zoom, EPSG:4326+polar, date-time + depth selection, point query, time-series, depth-profile, line/polygon section + trajectory, histogram, `.nc`/`.CSV` export, palettes LINEAR/LOG, opacity, deep link, embed, guided tour). No geocoder. Why feels 2D: map-first projection, depth = slider value not volume, weak direct manipulation, panels dominate canvas. Borrow depth/time control pattern, profile extraction UX, bbox subset flow, variable comparison. Limit: no volumetric depth perception, no float-as-anchor, no residual field. Lesson: keep its controls, replace canvas with Cesium globe + depth curtain.

**Nullschool fresh — CONFIRMED:** data + pipeline + render per §2.2. Borrow particle advection for u,v; instant scrub feel; static precompute = Zarr chunk preload pattern. Limit: no profiles, no QC, no match-up.

**Toggle design:**

| Element | Rule |
|---------|------|
| Switch | `2D map / 3D globe / 4D location` |
| Search | → bbox, not point. Catalogue query filters datasets by bbox. Empty bbox = blocked view with message, never blank globe |
| 3D mode | Cesium globe, terrain + bathymetry, SST overlay, currents particles, markers |
| 4D mode | Bounded location volume. Small bbox + 3–5 depths + 3–5 timesteps + 1 variable + nearby markers. Depth slider, curtain, time scrub, profile click |
| F4 controls | Same all modes: palette, min/max, log/linear, opacity, exaggeration. Exaggeration factor labeled beside view |
| Progressive | Globe → location → float → profile → residual. Residual gated on QC/method, `residual = model − observation` |

**Budgets/risks:** never full water column (`24×40×500×500 ≈ 0.96GB` float32 never ships whole — subset API + Arrow/binary only). Fly races fetch → preload low-res first, abort superseded, presets before live geocoder. Geocoder land/no-data kills demo — presets Bay Bengal eddy + Arabian Sea, offline pre-warm mandatory. Unlabeled field blocked: units + standard_name + missing-value rule + source version + ETag required.

**Order:** M1 globe + presets → M2 surface + time → M3 depth + currents → M4 markers + profiles → 4D toggle last, bounded bbox.

`ponytail:` geocoder + live 4D volumes deferred; presets + bounded subsets ceiling now, upgrade when M1–M4 proven.

**Status per 07:** stands except Unity + stars fixes (engine → undisclosed, fixed in live file).

### 2.6 `06-earth-3d-4d-toggle-9router.md` — verified toggle (highest-rated prem22k)

**4D definition + scope rule:** 4D = 3D space (lon, lat, depth) + time controls. No simultaneous 4-axis render exists; "4D view" = scoped volume with time scrub/play.

| Mode | Camera | Content | Time |
|------|--------|---------|------|
| Globe | global | imagery + bathymetry + markers | lighting clock only |
| 3D location | scoped bbox | slice, curtain, isosurface, currents, exaggeration | fixed timestep |
| 4D location | scoped bbox | same volume + trajectory + model/profile compare | scrub + play, particles re-seed |

Scope rule: entering 3D/4D requires bbox + depth range + timestep. No unbounded volume fetch. Lazier alternative: preset locations replace geocoder.

**Cesium subsurface — enabling APIs:**

| API | Source |
|-----|--------|
| Underground & Undersea use case: bathymetry base (World Bathymetry), transparent water/earth, per-region translucency | [use-cases](https://cesium.com/use-cases/underground-undersea/) |
| `screenSpaceCameraController.enableCollisionDetection = false` lets camera go below surface; ground-hidden-near-camera; opaque-until-close | [blog 2020-06-16](https://cesium.com/blog/2020/06/16/visualizing-underground/) |
| `GlobeTranslucency`, camera guide | [ref-doc](https://cesium.com/learn/cesiumjs/ref-doc/GlobeTranslucency.html) |
| Known risk: camera jump with translucency since 1.136 ([issue #13092](https://github.com/CesiumGS/cesium/issues/13092) — UNVERIFIED 2026-09-09, no fetch this session). Pin ≥1.119 (zarr-cesium floor), test at pin before ADR | risk tag |
| Prior art: Terradepth seabed/wrecks on Cesium; Camptocamp boreholes/seismic | context |

**zarr-cesium — rendering core confirmed:** [NOC-OI/zarr-cesium](https://github.com/NOC-OI/zarr-cesium) (MIT, TS, [demo](https://noc-oi.github.io/zarr-cesium/), [docs](https://noc-oi.github.io/zarr-cesium/docs)). v2+v3, multiscale (ndpyramid), EPSG:4326/3857, on-demand streaming, GPU color mapping. Fetched README 2026-09-09 adds: Icechunk/custom Zarrita stores, private HTTP (`requestOverrides`/`transformRequest`/`onAuthError`), point/time-series/profile/transect query APIs with cancellation, CesiumJS 1.119+ incl 1.142+. **Query APIs cover F2 click-profile plumbing — cite in stack ADR.**

| Provider | Role in toggle |
|----------|----------------|
| `ZarrLayerProvider` | Globe mode SST/surface overlay |
| `ZarrCubeProvider` | 3D/4D slices (horizontal + vertical curtain), exaggeration |
| `ZarrCubeVelocityProvider` | Currents particles, depth + time bound |

Peer 4D refs: [DOVis](https://github.com/HungerBar/DOVis) (FastAPI + Cesium, Indian Ocean), [nordicseas3d](https://github.com/nordicseas3d/nordicseas3d.github.io) (Zarr-in-browser slices/sections), [DeepSwitch](https://github.com/19Chris98H/DeepSwitch) (space-time cube for non-experts), [OceanBrowser paper](https://www.vliz.be/imisdocs/publications/ocrd/296600.pdf).

**PS fit:** F1 volumetric + slices + isosurface + time (3D/4D location modes). F2 markers + click profiles (globe + scoped). F4 controls as shader uniforms. F5/F7 xpublish REST + OPeNDAP plugin, WMS/WCS roadmap-only. Mandates map open.

**Kill risks:** full-cube fetch → bbox + depth + time chunk requests, abort stale, downsample-while-drag. Isosurface server-side/precomputed + cached first; browser volume deferred. Every sample: dataset, variable, units, UTC time, QC/mode, transform version. `residual = model − observation`; anomaly only with stated baseline. Pre-warm offline assets; recorded backup after live attempt. In-situ URL unknown — do not invent.

**Open threads:** verify #13092 then pin (floor ≥1.119) + ADR. Resolve Esri archwatch or drop. Arrow cutoff; chunk benchmark; laptop lock. Geocoder vs presets (presets first).

**Assumptions flagged:** 48 stars STALE vs 39 mirror 2025/12/23 (dropped from live file, prefer version/API facts). #13092 UNVERIFIED. Esri unresolved. In-situ unknown.

**Status per 07:** MOSTLY CONFIRMED — zarr-cesium + Cesium subsurface CONFIRMED, #13092 UNVERIFIED.

### 2.7 `07-deep-research-synthesis.md` — synthesis audit

9router tavily search (6 angles) + fetch (5 pages). Access date 2026-09-09 throughout.

**Verified CONFIRMED (11):** nullschool data stack; nullschool pipeline; nullschool render D3+Canvas 2D-only; MyOcean Pro 4D toolset (palettes SEQUENTIAL/DISCRETE/DIVERGING, LINEAR/LOG, opacity, deep link, embed, tour); MyOcean NO geocoder; zarr-cesium (MIT, v2+v3, multiscale, Icechunk, EPSG, streaming, GPU colormap, 3 providers, query APIs + cancellation, 1.119+ incl 1.142+); Cesium subsurface (transparency + enableCollisionDetection=false + translucency + frontFaceAlphaByDistance, Sandcastle demos); NASA Eyes suite (browser-run, real data, click-zoom-to, temporal nav); WebGPU paper Yu et al; Kiln (WebGPU out-of-core, bricked storage, LRU streaming, ~2GB in browser, few-hundred-ms first render — backs chunking ADR language).

**Corrections to prem22k docs (4):**

| # | Doc | Error | Fix |
|---|-----|-------|-----|
| 1 | 05 NASA Eyes "Unity → WebGL export" | UNSOURCED | Soften to "engine undisclosed; closed showcase" |
| 2 | 06 "48 stars" | STALE (mirror 39, 2025/12/23) | Fix number or drop; stars rot fast, prefer version/API facts |
| 3 | 06 "#13092 camera jump since 1.136" | NOT re-verified this session | Keep as risk with "unverified 2026-09-09" tag |
| 4 | 02 "Esri archwatch" | Ambiguous, no search run | Flag stays |

**New win-relevant findings (5):** MyOcean lacks geocoder → fly-to differentiation, keep in pitch. MyOcean deep-link + embed + tour = outreach checklist, add to 03/M5. zarr-cesium query APIs cover F2 plumbing, cite in stack ADR. Cesium 1.119+ incl 1.142+ = pin floor, test translucency at pin. Kiln LRU + bricked streaming vocabulary backs Zarr chunking ADR.

**Per-doc verdicts:** 01 stands; 02 nullschool CONFIRMED / Esri assumption; 03 WebGPU CONFIRMED / rest judgment stands; 04 strengthened; 05 stands except Unity+stars; 06 stands except stars/#13092 tag.

**Follow-ups (doc-only):** fix Unity + stars in 05/06. Verify #13092 before pin ADR. Resolve Esri or drop. Dataset cards + mandate→beat map still open (from 01).

---

## 3. Prem22k kills (ranked)

| # | Kill | Mechanism | Mitigation (in-docs) |
|---|------|-----------|----------------------|
| 1 | Full-cube 0.96GB fetch | 24×40×500×500 float32 never ships whole | Scope rule bbox+depth+time + abort/downsample (01 kills, 06 budgets) |
| 2 | Offline judging net-dependence | Tiles+geocoder+chunks all net | Pre-warm + recorded backup, not yet built (04 risks, 06 kill risks) |
| 3 | Fly-vs-fetch race | Fly animation races chunk fetch → jank | Preload low-res first + abort superseded (04 risks, 06 budgets) |
| 4 | Geocoder empty-bbox | Place not feature, needs bbox→catalog query else empty view | Presets-first mitigates (04 risks/order, 06 toggle) |
| 5 | zarr-cesium v0.1.4 churn + #13092 translucency jump | Pin ≥1.119 floor, test at pin before ADR | 06 §4/open threads |
| 6 | INCOIS-deployable vs public-cloud tension | F5 on-prem vs demo cloud, no compose proof, judging Q&A risk | Open — defers to shared docs |
| 7 | R2 10GB / Supabase 480-500MB / Render 512MB caps | Inherited from shared arch | Subset discipline only mitigation, toggle defers to shared docs |

---

## 4. Prem22k inventions (flag, don't cite externally)

| # | Claim | Files | Fix |
|---|-------|-------|-----|
| 1 | Esri archwatch ambiguous, assumed Living Atlas/EMU stack | 02, 07 §2/§5 | Resolve or drop; no search 2026-09-09 |
| 2 | HYCOM/GODAS context assumption, not official PS text | 01 gaps item5 | Labeled but still reused — keep label everywhere reused |
| 3 | NASA Eyes Unity→WebGL export UNSOURCED | 07 §2, fix in 05 | Corrected to engine undisclosed closed showcase |
| 4 | 48 stars STALE, mirror 39 updated 2025/12/23, stars rot | 07 §2, fix 05/06 | Dropped from live file; prefer version/API facts |
| 5 | Official listing URL differs from pasted portal text | 01 inventions | Pasted text canonical |
| 6 | Resolution claims without cards: MyOcean ~150m / EPSG4326+polar / GLOBAL_MULTIYEAR_PHY_001_030 1/12° as our resolution | 05/06 | Needs dataset card before reuse as our spec |
| 7 | Bay Bengal eddy 2026-08-10 / Arabian Sea presets + M0 event date synthetic fixture | 04 lazier path, 01 win move1 | Labeled synthetic — do not cite as data |
| 8 | `incois-demo-hycom-YYYYMMDD` synthetic fixture name | 01 | Labeled synthetic, invented if cited as data |
| 9 | Cesium #13092 camera jump since 1.136 UNVERIFIED no fetch | 06 §4, 07 §2 | Keep risk tag until checked |

## 5. Shared research library link (prem22k benchmark base)

`docs/research/nullschool-earth.md`: D3 orthographic illusion + 2×Canvas + grib2json→S3 + Kindlmann/cubehelix LUTs + bilinear per-pixel + Jacobian particle correction. Takeaway = GPU LUT + GPU particles + Zarr preload. Detail: `01-ps-authority-and-shared-canonical.md` §11b.

`docs/research/open-source-projects.md`: 14-entry library. DOVis blueprint + OceanStream UX mirror + nordicseas3d Three.js proof + DeepSwitch outreach + netcdf-three zero-backend + IMOS moorings + GlobeViz starter + Atlas/OceanEye prior SIH. Detail: §11c.

`docs/research/platform-comparison.md`: 17-row matrix. Windy/Ventusky controls ref, zoom.earth satellite ref, Google Earth globe benchmark. Verdict: none combine volumetric + co-viz + controls + plugins + standards. Differentiation locked. Detail: §11d.

Next: `04-head-to-head-comparison.md`.
