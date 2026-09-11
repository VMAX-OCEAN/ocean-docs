# 08 — Mermaid Design/Science Track (Third Namespace, origin/main ad5c121)

**Date:** 2026-09-09
**Source:** `ocean-docs` commit `ad5c121` (author prajwal), 15 files, 403 lines. Pulled from `origin/main`, fast-forward `26bb71f..ad5c121`, tree clean.
**Diff proof:** `26bb71f..ad5c121` touches mermaid files only. Lakshya + prem22k + shared unchanged. Files 01–07 still valid for those namespaces. This file adds the missing namespace. Cross-file patches appended to 04/05/06/07 + README.
**Lens:** rate against binding R/F IDs first, never namespace-vs-namespace first.

---

## 1. What landed (all 15 files)

| # | File | Lines | Kind | One-line content |
|---|------|-------|------|------------------|
| 1 | `research/individuals/mermaid/README.md` | 18 | Index | Thesis ocean-as-interface + 7-question reference rule |
| 2 | `research/individuals/mermaid/deep-dive-analysis.md` | 79 | Synthesis | 4D environment thesis, analytics engine, 5 interaction patterns, hybrid arch, validation questions |
| 3 | `research/individuals/mermaid/00-overview/research-map.md` | 28 | Map | 12-section map (01 problem → 12 references) + core research question |
| 4 | `research/individuals/mermaid/01-problem-space/requirements.md` | 34 | Requirements | Data list, lon×lat×depth×time, variables, MODEL+OBSERVATION baseline + 6-step extension, 5 user questions |
| 5 | `research/individuals/mermaid/02-existing-ocean-platforms/README.md` | 33 | Benchmark | MyOcean Pro, Argovis, ODV, Esri 3D, Nullschool, INCOIS + benchmark conclusion |
| 6 | `research/individuals/mermaid/03-design-inspiration/README.md` | 35 | Inspiration | Awwwards, Godly, NASA Eyes, Mapbox, Pudding, games + borrow-principles-not-decoration |
| 7 | `research/individuals/mermaid/04-interaction-patterns/pattern-library.md` | 12 | Patterns | 10 patterns: canvas, camera-as-scale, observation-as-query, morph, residual-first, uncertainty physics, feature-as-object, temporal tracking, contextual panels, progressive disclosure |
| 8 | `research/individuals/mermaid/05-visual-language/design-system.md` | 26 | Design language | Composition, editorial/telemetry type, semantic color, motion semantics, animation test |
| 9 | `research/individuals/mermaid/06-scientific-analytics/analytics.md` | 25 | Methods | Residual, anomaly, uncertainty, feature extraction, trajectory, temporal tracking, AI policy |
| 10 | `research/individuals/mermaid/07-data-and-standards/data.md` | 18 | Pipeline | Formats, CF, OGC, coords/units/calendars, raw→viz pipeline, traceability rule |
| 11 | `research/individuals/mermaid/08-rendering-and-performance/README.md` | 26 | Rendering | WebGPU paper link, ray casting/LOD/chunks/GPU analytics, 8 metrics |
| 12 | `research/individuals/mermaid/09-system-architecture/architecture.md` | 20 | Arch options | Pipeline sources→GPU, frontend/3D/GPU/scientific/backend option lists, division-of-labor principle |
| 13 | `research/individuals/mermaid/10-prototypes-and-experiments/experiments.md` | 13 | Prototype ladder | P0–P7 + record fields (goal/hypothesis/implementation/dataset/result/performance/what-changed) |
| 14 | `research/individuals/mermaid/11-research-questions/questions.md` | 14 | Open questions | 12 questions: UX, co-location, uncertainty, features, residuals, GPU-vs-server, contribution class |
| 15 | `research/individuals/mermaid/12-references/README.md` | 22 | References | 11 URLs in 3 classes + citation discipline rule |

Thesis: **DATA → SPATIOTEMPORAL ALIGNMENT → INTERACTION → COMPARISON → DISCOVERY → INSIGHT**. Ocean itself the interface. Baseline MODEL + OBSERVATION + 3D RENDERING, extension adds co-location → residual → uncertainty → features → tracking → contextual interaction.

---

## 2. Web verification 2026-09-09 (mermaid reference claims)

| Claim in mermaid files | Check | Verdict |
|---|---|---|
| MyOcean Pro 4D map + layers + depth/time + profiles + trajectories + histograms + exports + in-situ + particles | Fetched intro article: v7, Data Store embed, Add-to-map, depth/date controls, opacity/colormap/min-max, subset download | **CONFIRMED** (viewer exists, v7 current, updated this week) |
| MyOcean intro URL second link | Fetched `6482737` intro article, live | **CONFIRMED** |
| Argovis trajectories/profiles/metadata/filtering + FLOAT→trajectory→model→residual question | Fetched `argovis.colorado.edu`: Argo Core/BGC/Deep, WOCE, GO-SHIP, drifters, cyclones, API key, 91-day range, colocate datasets | **CONFIRMED** (platform real, colocate framing real) |
| ODV profiles/trajectories analysis + webODV Explore zero-install | Fetched `odv.awi.de`: ODV 5.8.6 Jun 13 2026, webODV Explore live, Argo collections online, OPeNDAP remote NetCDF, 135k users | **CONFIRMED** |
| webODV Explore dataset tree | Fetched `explore.webodv.awi.de`: GLODAP, SOCAT, GEOTRACES, WOCE, SeaDataCloud collections live | **CONFIRMED** |
| INCOIS operational context + formats | Fetch `incois.gov.in` failed (unknown error) | **UNVERIFIED**, cite link only, no stack claims |
| Mapbox globe/camera/fly-to | Docs host live, page body thin on fetch | Link real, **no feature claims verified** beyond mermaid's own words |
| NASA Eyes / Pudding / Awwwards / Godly as inspiration | Not fetched, mermaid's own rule says inspiration ≠ evidence | **Inspiration-only**, never cite for science claims |
| WebGPU ocean volume rendering paper `mdpi.com/2076-3417/15/5/2782` | Same DOI prem22k verified earlier (Yu et al, ray casting, early termination, adaptive sampling) | **CONFIRMED** (prior baseline) |
| Esri 3D listed as study target | No URL, no version, same open thread as prem22k | **UNVERIFIED**, do not cite externally |

---

## 3. R/F coverage matrix (mermaid vs binding IDs)

| Req | Mermaid coverage | Live built | Verdict |
|---|---|---|---|
| F1 volumetric/slices/isosurface/time | Rendering study (ray casting, LOD, chunks, isosurfaces, particles) + arch options, no provider choice, no code | Zero | Concept only. Lakshya providers + prem22k scope rule still the build path |
| F2 markers/click-profile | Observation-as-query + trajectory sampling `M(x(t),y(t),z(t),t)` vs `O(t)` + residual-first mode. Strongest mermaid contribution | Zero | **Keep concept**, enforce canonical sign (see §4) |
| F3 ingest | Pipeline raw→validation→metadata→normalize→chunk→colocate→API→GPU + formats list (NetCDF/HDF5/CSV/GeoJSON/CF) | Zero | Pipeline shape useful, no adapter. M5 adapter task unchanged |
| F4 controls | Semantic color (base/model/obs/±residual/uncertainty/selected) + motion semantics + no-rainbow rule + animation test | Zero | **Keep as design gate** for M2/M3 shader uniforms |
| F5 arch/deploy | Hybrid split (server heavy interp/extraction, browser interaction/render/light analytics) + option lists incl. Next.js/Three/Babylon | Zero runnable, no pins, no deploy target | Direction matches free-tier split, engine options diverge (see §5) |
| F6 plugins | Feature-as-object + temporal tracking + P5 detect-and-track-one-feature | Zero | **Keep as M5 differentiator**, gate on robust-detection question Q7 |
| F7 standards | CF + OGC + traceability rule (source/variable/timestamp/depth/method/uncertainty) | Zero live | Traceability rule strengthens cards/ADRs. Never claim compliance |
| R1 3D volumetric | Camera-as-scale + ocean-as-canvas | Zero | Complements scene arc, builds nothing |
| R2 model+obs fusion | Co-location + residual + uncertainty + trajectory. Core thesis | Zero panels | Concepts feed M4, sign must flip to canonical |
| R3 controls | Full pattern + design language | Zero widgets | Design spec, not implementation |
| R4 extensibility | Nothing (no adapter/registry) | Zero | Gap stays open |
| R5 rapid intuitive 3D | Progressive disclosure + contextual panels + P0–P7 ladder | Zero | **Keep process**, feeds M1/M5 |
| Mandates hazard/SAR/fishery/climate | Zero mapping | Zero | Gap stays open, beat map still owed |
| Outreach students/public/policymakers/exhibitions/e-learning | Scrollytelling (Pudding) + tour patterns + progressive disclosure | Zero modes | Checklist stays prem22k's, mermaid adds narrative sequencing |
| Dataset cards | Traceability rule only, no cards | Zero | Gate unchanged |

---

## 4. Critical conflict — residual sign (binding)

| Source | Formula | Status |
|---|---|---|
| `problem-statement/PROBLEM-STATEMENT-ANALYSIS.md:70` | `residual = model − observation` | **Canonical. Wins.** |
| mermaid `06/analytics.md` | `E(x,y,z,t) = O(x,y,z,t) − M(x,y,z,t)` | **Rejected.** Do not implement |
| mermaid `04/pattern-library.md` item 5 | `E = Observation − Model` | **Rejected.** Do not implement |
| mermaid `deep-dive-analysis.md` §2 | `E = Observation - Model` | **Rejected.** Do not implement |

Three mermaid files used the flipped sign consistently (systematic, not typo). **RESOLVED 2026-09-10 (observed in working tree): all three now read canonical `M − O`.** Rewrite verified against `PROBLEM-STATEMENT-ANALYSIS.md:70`. Attribution of the edit unknown (not this session). Merged rule: residual-first mode UI (mermaid's interaction idea) + canonical sign (PS authority). Never average the two.

---

## 5. Stack divergence — evaluate-only, no commit

| Mermaid proposes | Locked stack | Decision |
|---|---|---|
| Three.js / WebGPU / Babylon.js primary, CesiumJS one option among three | CesiumJS + zarr-cesium locked (F1 build path, Phase-0 gates) | **Cesium lock stands.** Mermaid engine list = evaluate-only |
| React/Next.js frontend | React18 + Vite + TS locked (vite-plugin-cesium config runnable) | Vite stands. Next.js evaluate-only |
| FastAPI + xarray + Dask + Zarr + object storage backend | xpublish + xpublish-zarr + argopy + SQLite/Supabase | Compatible at Python/xarray/Zarr layer. Dask evaluate-only. OPeNDAP via THREDDS/Hyrax, never `xpublish-opendap` |
| GPU real-time numerical ops | Server/precomputed isosurface first, browser volume deferred | prem22k scope rule stands. GPU ops need benchmark before commit |
| P6 benchmark WebGL/WebGPU + server/client split | Chunk ADR + locked-laptop benchmark open | **Merge:** mermaid's 8 metrics (FPS, memory, GPU mem, first render, interaction latency, slice time, residual time) become the benchmark record fields |

---

## 6. Ratings — mermaid files (same 6 axes, 1–5)

Axes: PS-align | Evid | Exec | Risk | Win | Fresh = Total.

| File | PS | Ev | Ex | Ri | Wi | Fr | Total | Note |
|---|---|---|---|---|---|---|---|---|
| `mermaid/deep-dive-analysis.md` | 4 | 2 | 2 | 3 | 4 | 5 | **20** | Best synthesis, AI policy good, sign error costs Risk |
| `mermaid/04-interaction-patterns/pattern-library.md` | 4 | 1 | 2 | 3 | 5 | 5 | **20** | Highest Win in namespace, observation-as-query + residual-first |
| `mermaid/08-rendering-and-performance/README.md` | 3 | 3 | 2 | 3 | 3 | 5 | **19** | Paper link real, metrics list adoptable |
| `mermaid/06-scientific-analytics/analytics.md` | 4 | 2 | 2 | 3 | 3 | 5 | **19** | Strong methods; sign fixed 2026-09-10 |
| `mermaid/09-system-architecture/architecture.md` | 3 | 2 | 2 | 3 | 3 | 5 | **18** | Division-of-labor matches split, options unevaluated |
| `mermaid/02-existing-ocean-platforms/README.md` | 3 | 3 | 1 | 3 | 3 | 5 | **18** | URLs real, conclusion honest, Esri/INCOIS unverified |
| `mermaid/05-visual-language/design-system.md` | 3 | 1 | 2 | 3 | 4 | 5 | **18** | Semantic color + motion test adoptable |
| `mermaid/10-prototypes-and-experiments/experiments.md` | 3 | 1 | 3 | 3 | 3 | 5 | **18** | P0–P7 ladder best process artifact |
| `mermaid/README.md` | 3 | 1 | 2 | 3 | 4 | 5 | **18** | Thesis pitchable, 7-question rule good hygiene |
| `mermaid/07-data-and-standards/data.md` | 3 | 2 | 2 | 3 | 2 | 5 | **17** | Traceability rule good, no cards |
| `mermaid/03-design-inspiration/README.md` | 2 | 2 | 1 | 4 | 3 | 5 | **17** | Borrow-not-decoration discipline best Risk in namespace |
| `mermaid/12-references/README.md` | 2 | 3 | 1 | 4 | 1 | 5 | **16** | Citation classes good, content-free by design |
| `mermaid/11-research-questions/questions.md` | 3 | 1 | 1 | 4 | 2 | 5 | **16** | Scope honesty, Q7/Q9/Q10 gate real work |
| `mermaid/00-overview/research-map.md` | 2 | 1 | 2 | 2 | 2 | 5 | **14** | Map only |
| `mermaid/01-problem-space/requirements.md` | 3 | 1 | 1 | 2 | 2 | 5 | **14** | Restates baseline, no sources |

Namespace track rating: PS 3 | Ev 2 | Ex 2 | Ri 3 | Wi 4 | Fr 5 = **19**. Design/science concept track. Top-3 (29/27/26) and bottom-3 (7/8/9) unchanged — mermaid best 20 sits Tier B, mermaid floor 14 above Tier C.

---

## 7. Three-way head-to-head deltas

| Dimension | Lakshya (execution) | Prem22k (product/science) | Mermaid (design/science) | Merged take |
|---|---|---|---|---|
| PS traceability | No R/F IDs | Full R/F audit | No R/F IDs, concepts map loosely | Prem22k audit still only map |
| F1 volumetric | Providers + gates, builds | Scope + subsurface verify | Rendering study, no provider | Lakshya builds, mermaid metrics record the benchmark |
| F2 fusion | Argo only, no residual | Residual rule canonical | Observation-as-query + trajectory + residual-first UI, sign now canonical | Mermaid interaction + canonical sign |
| F4 controls | Partial set | Full uniform set | Semantic color + motion test | Prem22k uniforms + mermaid gates (no rainbow, animation must communicate) |
| F5 arch | Runnable $0 split | REST/OPeNDAP named | Hybrid split + option lists | Lakshya split stands, mermaid options evaluate-only |
| Outreach | Zero | Checklist + scene arc | Narrative sequencing + progressive disclosure | Prem22k checklist + mermaid disclosure order |
| Risk honesty | Lib fallbacks | Self-correcting synthesis | AI policy + borrow-discipline + open questions, sign error open | Keep policies, fix sign |
| Executability | Only runnable track | Thresholds no device | P0–P7 ladder no code | Lakshya builds, mermaid ladder orders prototypes |
| Evidence | Pins no dates | Sourced + dated | URLs mostly real, no dates/versions | Prem22k bar stands, mermaid refs need dates |

Tally unchanged in structure: prem22k product/science, Lakshya execution, mermaid design. Neither of three ships alone.

---

## 8. Gaps / inventions / kills deltas from mermaid

New shared gaps mermaid fills (concept only, live still zero): observation-as-query pattern, residual-first UI pattern, feature-as-object + temporal tracking, trajectory sampling method, prototype ladder, benchmark metric list, citation classes, motion semantics, traceability pipeline wording. None close a live gate. All feed M4/M5 design.

New inventions flagged (do not cite): residual sign flip (was systematic, now fixed §4), engine-switch implication (options read as recommendation), Next.js implication, Dask-at-scale implication, Esri 3D study claim without URL, INCOIS formats claim without fetch, Mapbox feature claims beyond link, Awwwards/Godly as anything beyond inspiration.

New kill risks: K10 sign-flip propagation (any panel built from mermaid docs computes wrong residual — mitigate: rewrite 3 files to canonical before M4), K11 engine-churn (Three/WebGPU rewrite discards Phase-0 Cesium gates — mitigate: evaluate-only label, gate decides), K12 feature-detection overclaim (eddies/fronts robust detection unverified — mitigate: Q7 gate, P5 one-feature proof before M5 claims).

---

## 9. Merged plan additions (Keep 10 + 7)

Prior Keep 1–10 stand. Add:

| # | Keep | Source | Gate |
|---|---|---|---|
| 11 | Observation-as-query: FLOAT→trajectory→local model volume→prediction→observation→residual (canonical sign) | mermaid 02/04 | M4 interaction |
| 12 | Residual-first mode UI + model→obs→residual morph | mermaid 04 | M4, blocked until sign rewrite |
| 13 | Feature-as-object + temporal tracking, one-feature proof (eddy/front) first | mermaid 04/06/10 | M5, Q7 gate |
| 14 | Trajectory sampling method note `M(x(t),y(t),z(t),t)` vs `O(t)` | mermaid 06 | M4 method label |
| 15 | P0–P7 prototype ladder + record fields | mermaid 10 | Process, immediate |
| 16 | Motion semantics + animation test (remove if only cool) | mermaid 05 | M5 polish gate |
| 17 | Citation classes (benchmark/inspiration/implementation/method/validation) | mermaid 12 | Evidence hygiene, immediate |

Reject/defer: flipped sign (REWRITE DONE 2026-09-10), engine switch (evaluate-only), Next.js (evaluate-only), Dask (evaluate-only), AI classification/forecasting (post-SIH, policy kept), Esri/INCOIS/Mapbox claims beyond verified links.

Deep-research queue adds Q9: re-verify residual sign rewrite in 3 mermaid files + confirm no panel code uses `O − M` before M4 pass.

`ponytail:` mermaid concepts ceiling now (design input), upgrade to implementation only through Phase-0/M4 gates.
→ skipped: engine rewrite, Next.js move, Dask scale-out, AI features, live feature detection beyond one-feature proof. Add when gates pass.

---

## 10. Actual-impact verdict (binding)

Mermaid impact = design-only, zero live gates closed.

| Question | Answer |
|---|---|
| Closes M1-M5 gate live? | No. Zero panels, zero providers, zero cards, zero benchmarks built |
| Changes stack lock? | No. CesiumJS+Vite+xpublish stands. Three/WebGPU/Babylon + Next.js + Dask = evaluate-only, rejected for build |
| Changes residual rule? | No. Mermaid sign was flipped in 3 files (rejected). Canonical `model − observation` wins. **Rewrite DONE 2026-09-10 — 3 files now canonical.** M4 unblocked on sign |
| Adoptable now, zero cost? | Yes. Keep 11-17: observation-as-query, residual-first UI (canonical sign), feature-as-object + one-feature proof, trajectory method note, P0-P7 ladder, motion test, citation classes |
| Kills added? | K10 sign propagation (rewrite 3 files pre-M4), K11 engine churn (evaluate-only label), K12 detection overclaim (Q7 gate) |
| Research depth added? | Yes. MyOcean/Argovis/ODV/webODV CONFIRMED links, 8-metric benchmark fields, traceability wording, AI policy |
| Bottom line | Mermaid makes it explorable, builds nothing. Adopt concepts, reject sign + engine switch. Tier B, above stale Tier C, below top-3 |

Coverage: 74 md total mapped. 01 §11 closes 4 flagged shared docs (optimization prefetch/lru/tileCache/KTX2/progressive, nullschool orthographic/Jacobian/Kindlmann/cubehelix, open-source OceanStream/netcdf-three/IMOS/GlobeViz/three-globe/OceanEye, platform Windy/Ventusky/zoom.earth). 02 §5 + 03 §5 link them. No re-audit needed.
