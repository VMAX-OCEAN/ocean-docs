# 04 — Head-to-Head Comparison: Lakshya vs Prem22k

**Date:** 2026-09-09
**Lens:** rate against binding R/F IDs first, never against each other first.
**Tracks:** Lakshya = deployment/execution. Prem22k = product/science.

---

## 1. Dimension matrix (12 axes)

| # | Dimension | Lakshya (execution) | Prem22k (science) | Winner + why |
|---|-----------|---------------------|-------------------|--------------|
| 1 | PS traceability R1-R5 F1-F7 | No R/F IDs. Serves F1/F5 + demo cost. Misses residual/QC, bbox rule, cards, ADRs, mandate beats | Full R/F audit (01). Residual rule defined. Bbox scope rule defined. Cards/ADRs flagged open. Mandates flagged open | **Prem22k.** Only track with R/F map |
| 2 | Globe + 3D volumetric (F1) | zarr-cesium 3 providers mapped exactly to SST/slice/particles. Phase 0 gates + decision tree prevent blind v0.1.4 commit | Toggle design (globe / 3D location / 4D location) + scope rule (bbox + depth + time required). Subsurface APIs verified. Query APIs cited for F2 plumbing | **Tie.** Lakshya = how to render. Prem22k = when/what to render |
| 3 | Markers + profiles + residual (F2) | Argo only. Phase 5 markers + Plotly. No residual, no QC/method, no Glider/CTD/BGC | Markers + click-profile defined. `residual = model − observation` gated on QC/method. Point divergence now, volume divergence deferred (sparse floats can't form dense volume) | **Prem22k.** Residual rule exists only here |
| 4 | Ingest + extensibility (F3/F6) | NetCDF→Zarr via xarray + argopy→Supabase. No ASCII adapter. No registry. Glider/CTD/BGC skipped post-SIH | Adapters noted. PyNIO-drop ADR noted, not written. Plugin need named, no registry/contract/code | **Tie (both zero live).** Prem22k slightly ahead on paper trail |
| 5 | Controls (F4) | Phase 2 palette/min/max/opacity. Missing log/linear | Full set: palette/range/log-linear/opacity/exaggeration as shader uniforms, all modes. Exaggeration labeled beside view | **Prem22k.** Complete control set |
| 6 | Architecture + deploy (F5) | **Strongest asset.** Vercel + R2 direct + Supabase direct + Render compute-only. Runnable vite config + R2 upload + PostGIS schema + keep-warm cron. $0 | xpublish REST + OPeNDAP named. No compose/on-prem proof. Defers to shared docs | **Lakshya.** Only runnable deploy |
| 7 | Standards (F7) | OPeNDAP skipped MVP. WMS/WCS vague. CORRECTED: `xpublish-opendap` real (BSD-3 v0.2.0), distinct from `xpublish-zarr` (Apache-2.0) | WMS/WCS roadmap-only correctly labeled. OPeNDAP facade scope noted. Same package confusion inherited | **Prem22k (narrow).** Correct roadmap label |
| 8 | Outreach + mandates | Zero guided mode. Zero mandate beats. No Docker vs demo distinction | Checklist: deep-link + embed + tour (MyOcean verified) + NASA Eyes tour pattern. Scene arc 01-07. Mandates flagged open with beat mapping owed | **Prem22k.** Checklist exists |
| 9 | Risk honesty | Honest risk matrix + fallbacks (ImageryProvider, wind-layer, custom shader). Scope discipline table. Self-corrects OPeNDAP | Self-correcting 07 synthesis (Unity/stars/#13092/Esri). Kill-ranked lists. Memory math (0.96GB) blocks full-cube fetch | **Tie.** Both honest. Lakshya = lib risks. Prem22k = demo/science risks |
| 10 | Executability | Phase 0 gates runnable. Copy-paste R2/Supabase/Vercel code. 20-26d timeline | No runnable configs. Thresholds without locked laptop run. Workload fixed (256×256/40/24/2vars/1000 markers) but no device | **Lakshya.** Only track that builds |
| 11 | Evidence quality | Pins + capacity math, but stars rot, no dates, CORRECTED: `xpublish-opendap` exists (prior false claim); perf without device | 9router verified teardowns with sources + dates. Self-flagged stale (Unity, stars, #13092, Esri) | **Prem22k.** Sourced + dated + self-corrected |
| 12 | Win / judging | Early phases alone = strong submission. Cost $0 | Preset-first fly-to differentiation (MyOcean no-geocoder). 90s arc. M0 fixture. Claims discipline | **Prem22k (pitch), Lakshya (demo).** Need both |

**Tally:** Prem22k 6, Lakshya 2, Tie 3, Split 1. Prem22k wins product/science. Lakshya wins execution. Neither ships alone.

---

## 2. F1–F7 coverage head-to-head

| Req | Lakshya | Prem22k | Merged take |
|-----|---------|---------|-------------|
| F1 volumetric/slices/isosurface/time | Partial. Isosurface only, full volume deferred. 3 providers mapped | 3D/4D location modes + scope rule + subsurface APIs + server/precomputed isosurface first | Lakshya providers + prem22k scope rule + isosurface-cached-first |
| F2 markers/click-profile | Argo only, co-viz only, no residual | Markers + profiles + residual gated QC/method | Prem22k residual rule mandatory on every compare panel |
| F3 ingest | NetCDF→Zarr + argopy only. No delimited adapter | Adapter + PyNIO ADR noted, not built | xarray netCDF4 backend ADR + delimited adapter task in M5 |
| F4 controls | Palette/min/max/opacity. No log/linear | Full set + labeled exaggeration | Prem22k set as shader uniforms (M2/M3 gate) |
| F5 arch/deploy | $0 split runnable. No INCOIS compose | REST/OPeNDAP named. No compose | Demo = free cloud. Deliverable = Docker on INCOIS. Write distinction doc |
| F6 plugins | Deferred post-SIH | Research-only | Registry task in M5 with CTD/moorings/HF-radar/ADCP contract |
| F7 standards | Skip MVP, vague | Roadmap-only label correct | Roadmap-only until live. Never claim compliance. Facade scope note M5 |

---

## 3. R1–R5 gap coverage head-to-head

| Gap | Lakshya | Prem22k |
|-----|---------|---------|
| R1 3D volumetric | Providers + phases | Toggle + scope + subsurface verify |
| R2 Argo/Glider beside model | Argo only, no unified T/S/chlorophyll | Markers + profiles + residual defined, Glider/CTD/BGC still open |
| R3 controls | Partial set | Full set |
| R4 new streams no re-engineering | Zero (no adapter/registry proof) | Zero live (adapter/ADR noted) |
| R5 rapid intuitive 3D | Working globe fast (Phase 1 stakeholder demo) | Scene arc + presets + 90s script |

---

## 4. Pros / cons (condensed from synthesis)

### Lakshya pros (6)

1. Phase 0 de-risk gates + decision tree prevent blind v0.1.4 commit
2. Free-tier hot-path split R2+Supabase direct kills backend bottleneck + $0
3. zarr-cesium 3 providers mapped exactly to SST/slice/particles
4. Runnable checklists + vite cesium config + R2/Supabase SQL + keep-warm cron
5. Honest risk matrix + fallbacks ImageryProvider + wind-layer + custom shader
6. Scope discipline table cuts OPeNDAP/full-volume/glider/paid

### Lakshya cons (6)

1. No R/F ID trace, misses residual/QC + bbox scope rule
2. Misses dataset cards + ADRs PyNIO/Cesium/OPeNDAP/chunking
3. Stale paid docs remain without banner (render-deployment, pricing, blueprint superseded)
4. OPeNDAP confusion CORRECTED: `xpublish-opendap` exists (BSD-3); earlier nonexistent claim wrong
5. Supabase 500MB tight, no Arrow cutoff locked
6. No mandate beats + outreach thin + no INCOIS Docker vs demo distinction

### Prem22k pros (6)

1. PS-fit audit to R/F IDs + gaps + inventions + kill risks
2. Verified teardowns nullschool/MyOcean/NASA/Eyes with sources + dates
3. Residual rule model-observation gated on QC/method
4. Scoped bbox+depth+time toggle + memory math blocks full-cube fetch
5. Preset-first fly-to differentiation vs MyOcean no-geocoder
6. Scene arc 01-07 + outreach deep-link/embed/tour + self-correcting 07 synthesis

### Prem22k cons (6)

1. No runnable configs, thresholds without locked laptop run
2. Esri archwatch unresolved assumption, must not cite externally
3. Stale Unity-engine claim + star counts, self-flagged in 07 needs fix
4. Geocoder vs presets leaves search infra open
5. WMS/WCS roadmap label needs code enforcement
6. HYCOM/GODAS context assumption needs label everywhere reused

---

## 5. Keep / drop (merged)

### Keep (10)

| # | Keep | Source |
|---|------|--------|
| 1 | Phase 0 de-risk gates + decision tree | revised-master-plan |
| 2 | No-backend-hot-path split: Vercel + R2 direct + Supabase direct + Render compute-only | free-tier-deployment |
| 3 | zarr-cesium 3 providers mapping + zarrita fallback sketch + pinned versions (re-pin 0.2.0) | revised-master-plan + 06 |
| 4 | Vercel vite-plugin-cesium config + R2 upload + Supabase PostGIS schema + keep-warm cron | vercel/cesium/free-tier |
| 5 | R/F IDs + F1-F7 traceability | PROBLEM-STATEMENT-ANALYSIS + 01 |
| 6 | `residual = model − observation` gated on QC/method on every compare panel | 03/05/06 |
| 7 | Scoped bbox+depth+time rule, no unbounded volume fetch, abort superseded + low-res first | 04/05/06 |
| 8 | Preset-first fly-to Bay Bengal eddy + Arabian Sea, geocoder deferred | 04 + 06 |
| 9 | Scene arc 01-07 + mandate beats + outreach deep-link/embed/tour | 03 + 07 |
| 10 | Dataset cards sha256+license+bbox + ADRs Cesium/PyNIO/OPeNDAP/chunking + benchmark record | 01 + data/README |

### Drop (8)

| # | Drop | Reason |
|---|------|--------|
| 1 | `render-deployment.md` paid Starter+disk path | Superseded by free-tier + revised-master-plan |
| 2 | `pricing-analysis.md` $9.50 prod | Contradicts free-only constraint |
| 3 | `render-blueprint.md` paid render.yaml disk Starter | Stale + bad dep name |
| 4 | `deployment-architecture.md` paid Render hot-path flow | Superseded, bottleneck |
| 5 | `render-vs-alternatives.md` $9.50 conclusion | Keep matrix only |
| 6 | Full water-column fetch 24×40×500×500 ~0.96GB float32 | Never ship whole |
| 7 | Live geocoder before presets, Esri archwatch, Unity-engine claim, star counts | Risk / unsourced / rot |
| 8 | `TECH-STACK-SUMMARY.md` latest pins + SQLite-only | Stale vs master plan, fix or drop (xpublish-opendap real, not a defect) |

---

## 6. One-line verdict

Lakshya builds it. Prem22k makes it correct + winnable. Mermaid makes it explorable (observation-as-query + residual-first + feature-as-object), pending sign rewrite to canonical `residual = model − observation`.

## 7. Third-namespace addendum (mermaid, ad5c121)

Three-way deltas, sign conflict, engine evaluate-only verdict: see `08-mermaid-design-science-track.md` §4/§5/§7. Keep additions K11–K17 feed M4/M5 design. Kills K10–K12 added (sign propagation, engine churn, detection overclaim).

## 8. Coverage note (74/74)

4 flagged shared docs now closed in `01-ps-authority-and-shared-canonical.md` §11: optimization dual-chunk/prefetch/lru/tileCache/KTX2/progressive, nullschool orthographic/Jacobian/Kindlmann/cubehelix, open-source OceanStream/netcdf-three/IMOS/GlobeViz/three-globe/OceanEye, platform Windy/Ventusky/zoom.earth. No head-to-head change.

Next: `05-ratings-and-leaderboard.md`.
