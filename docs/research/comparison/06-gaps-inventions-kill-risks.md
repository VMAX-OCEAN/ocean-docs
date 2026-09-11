# 06 — Gaps, Inventions, Kill Risks (Shared + Per-Namespace)

**Date:** 2026-09-09
**Rule:** gaps = binding requirement with zero coverage. Inventions = unsourced/assumed cited as fact. Kills = failure modes that end demo or build.

---

## 1. Shared gaps (both namespaces, 13)

| # | Gap | Binds to | Evidence of absence | Gate that fixes it |
|---|-----|----------|---------------------|--------------------|
| G1 | Dataset cards sha256/license/bbox for all 5 PS links absent | F1/F2 data proof, 01 win move1, open item 1 | `docs/data/README.md` placeholder only. Present files drafts, no sha256/license/access-date: `data-sources.md`, `glorys-dataset.md`, `argo-data.md`, `glider-data.md`, `netcdf-to-zarr.md` | M2 gate: cards required before fixture use |
| G2 | Mandate→beat map absent | R5 demo arc, open item 3 | PS analysis §mandates "currently unmapped". Both namespaces flag open, neither writes map | M5 gate: mandate-mapped 90s script |
| G3 | Reference laptop lock absent | Chunk benchmark, slice≤750ms, cold≤10s, 30FPS+5000 markers claims | Prem22k workload fixed (256×256/40/24/2vars/1000 markers) no device. Lakshya no workload at all | M2 gate: lock device, run, record |
| G4 | Chunk hypothesis benchmark absent | F1 time scrub + slice latency | Lakshya notes risk only. Prem22k threshold open. `backend-strategy.md` dual-rep vs balanced unmeasured | M2 gate: chunk ADR with device + sizes |
| G5 | GeoJSON-vs-Arrow cutoff absent | F2 markers at scale | Prem22k suggests <500, Lakshya silent. Neither measures Supabase bbox + R2 JSON fallback | M4 gate: Arrow cutoff ADR |
| G6 | Residual=model−obs implementation absent | R2 match-up, open item 5 | Prem22k defines rule, Lakshya omits rule entirely. Zero panels built | M4 gate: residual + QC/method required on every compare panel |
| G7 | QC/method labels enforcement absent | R2 trust | Prem22k gates in prose, Lakshya silent. No UI enforcement built | M4 gate with G6 |
| G8 | F6 plugin live absent (CTD/moorings/HF-radar/ADCP/ML) | F6, R4 | Lakshya defers post-SIH. Prem22k research-only. M5 registry task unchecked | M5 gate: registry + one added sensor proof |
| G9 | F7 WMS/WCS live absent | F7 | Lakshya skips MVP. Prem22k labels roadmap-only (correct). No endpoint design | M5 gate: facade scope note, never claim live |
| G10 | F3 delimited ingest + minimal-code extensibility live absent | F3, R4 | xarray only. PyNIO-drop ADR missing both | M5 gate: delimited adapter + PyNIO ADR |
| G11 | Outreach guided mode live absent | Outreach binding, R5 | Prem22k checklist only. Lakshya zero. M5 tasks unchecked | M5 gate: deep-link + embed + tour |
| G12 | INCOIS-deployable proof absent | F5 | Public-cloud demo vs F5 on-prem tension unresolved both. Shared `system-architecture.md` Docker good but conflicts free-tier split | M5 gate: compose proof + demo≠deliverable doc |
| G13 | OPeNDAP-facade scope + Cesium-over-Three ADR missing | F5/F7/F1, open item 2 | Per PROBLEM-STATEMENT-ANALYSIS open items. Neither namespace writes them | M5 gate |

---

## 2. Lakshya-only gaps (12)

| # | Gap | Location | Fix from prem22k |
|---|-----|----------|------------------|
| L-G1 | F1 partial: isosurface only, full volume deferred | revised-master-plan §Not doing | Import scope rule — bounded volumes, not full |
| L-G2 | F2 zero beyond Argo: Glider/CTD/BGC/moorings skipped | revised-master-plan §Not doing, Phase5 Argo only | Import residual rule + marker spec |
| L-G3 | F3 zero ASCII/delimited adapter | free-tier + revised-master Phase0.2 (NetCDF→Zarr + argopy only) | Import adapter task |
| L-G4 | F3/R4 zero minimal-code/config-only proof | No adapter interface, no registry demo | Import M0 fixture + operator proof |
| L-G5 | F6 zero plugin registry | No registry in Phase0-6, M5 deferred | Import registry task |
| L-G6 | F7 zero live, OPeNDAP skipped, WMS/WCS vague | revised-master §Not doing, cross-check Decision9 | Import roadmap-only label + facade note |
| L-G7 | F4 partial: palette/min/max/opacity, missing log/linear | revised-master Phase2 | Import full F4 set as shader uniforms |
| L-G8 | F5 zero INCOIS on-prem path | Vercel+R2+Supabase only | Write demo≠deliverable doc |
| L-G9 | Outreach zero: no tour/embed/deep-link/presenter | No M5 outreach | Import checklist + scene arc |
| L-G10 | Mandate beats zero | Unmapped | Import beat map |
| L-G11 | Cards zero | No sha256/license/bbox | Import card gate |
| L-G12 | Residual/QC/Arrow/chunk-benchmark/laptop zero | Silent or notes-only | Import all three gates |

---

## 3. Prem22k-only gaps (12, all live-zero, rules-defined)

| # | Gap | Rule defined | Live missing |
|---|-----|--------------|--------------|
| P-G1 | F6 plugin live zero | Need named | No registry/contract/code (01 win moves, 06 §PS fit open) |
| P-G2 | F7 live zero | Roadmap-only correctly labeled | No live endpoint (01 R7, 06 §PS fit) |
| P-G3 | F3 live zero | Delimited adapter + PyNIO ADR noted | No adapter built (01 gaps+R4) |
| P-G4 | F2 live partial | Markers + click profile defined | No live markers beyond research (01 R3, 06 toggle) |
| P-G5 | Outreach live zero | Deep-link/embed/tour checklist (03/07) | No mode built (03 checklist) |
| P-G6 | Mandate beats live zero | Need beats | Still open (01 gaps, 06 §PS fit) |
| P-G7 | Cards live zero | Flagged open | No cards (01 gaps items1-2) |
| P-G8 | Residual live zero | Rule defined | No panel built (03 sign fix, 06 budgets) |
| P-G9 | QC/method live zero | Gate defined | No UI enforcement (06 toggle, 07 follow-ups) |
| P-G10 | Arrow cutoff live zero | <500 suggested | No decision/run (01 item3, 04 thresholds) |
| P-G11 | Chunk benchmark + laptop live zero | Workload fixed, no device | No run (01 item4, 04 thresholds) |
| P-G12 | F5 INCOIS live zero | REST+OPeNDAP named | No compose proof (06 §PS fit) |

Pattern: prem22k defines rules, builds nothing. Lakshya builds, defines few rules. Merge = Lakshya build + prem22k rules.

---

## 4. Shared inventions (7, flag don't cite)

| # | Invention | Truth | Rule |
|---|-----------|-------|------|
| I1 | HYCOM/GODAS as official context | Assumption not in pasted PS text | Label everywhere reused |
| I2 | Resolution claims (1/12° / 50 levels / ~150m zoom) reused without card | No sha256/bbox provenance | Needs card before reuse as our spec |
| I3 | Listing URL vs pasted portal text conflict | Pasted text canonical | Cite pasted text, note conflict |
| I4 | Star-count rot (48 vs 39 / 112) without access date | Rot fast | Prefer version/API facts |
| I5 | Unity engine for NASA Eyes | Unsourced | Use engine undisclosed |
| I6 | Esri archwatch target ambiguous (Living Atlas/EMU) | No search 2026-09-09 | Resolve or drop, never cite |
| I7 | Perf claims (40x / ms / ~100KB / 60FPS / 10k) without benchmark/device | Cited correctly in `benchmarks.md`, extrapolated in `runtime-latency.md` | Keep claims discipline per 01 |

---

## 5. Lakshya inventions (11)

| # | Claim | File | Fix |
|---|-------|------|-----|
| LI1 | 48 stars / 5 forks / 3 contrib, no date; stale vs 39 mirror | cross-check D2 | Re-date 2026-09-09 (~49/5/~4 issues, pushed 2026-09-08) or drop |
| LI2 | 112 stars / 31 forks / 205 downloads, no date | cross-check D3 | Date or drop |
| LI3 | 40x faster, no source | approach, change-log, cross-check D4 | Cite Gowan 2022 / essoar.10511054.2 or mark estimate |
| LI4 | ~100KB / ms / ~200ms / 60FPS / 10k, no device | free-tier, cesium-deployment | Mark estimate until laptop run |
| LI5 | CesiumGS recommends Vercel (2025 tutorials), no URL | approach D5, cross-check D8 | Add URLs or soften |
| LI6 | R2 10GB fits 5 vars × IO × 1-2mo, no byte math | free-tier | Add byte math in chunk ADR |
| LI7 | Supabase 500MB fits 4000×100 ~480MB JSONB, unproven | cross-check D6 | Measure; R2 JSON fallback ready |
| LI8 | `xpublish-opendap` exists | render-blueprint, change-log | **CORRECTED 2026-09-10: TRUE.** v0.2.0 BSD-3 on PyPI. Earlier false claim wrong (ADR-003) |
| LI9 | GLORYS12 IDs + res as primary, no card | change-log, render-deployment | Needs card |
| LI10 | Ion free sufficient, unspecified | cesium-deployment | Specify or mark assumption |
| LI11 | Render 750hrs/512MB/0.1CPU/15min/30s, no date | free-tier, pricing | CONFIRMED 2026-09-09 — add date |

---

## 6. Prem22k inventions (9)

| # | Claim | Files | Fix |
|---|-------|-------|-----|
| PI1 | Esri archwatch assumed stack | 02, 07 | Resolve or drop |
| PI2 | HYCOM/GODAS context reused | 01 | Keep label |
| PI3 | NASA Eyes Unity→WebGL UNSOURCED | 07→05 | **Fixed** to undisclosed |
| PI4 | 48 stars STALE | 07→05/06 | **Fixed** (dropped, prefer version/API) |
| PI5 | Listing URL vs pasted text | 01 | Pasted canonical |
| PI6 | Resolution without cards | 05/06 | Needs card |
| PI7 | Bay Bengal eddy 2026-08-10 / Arabian Sea presets + M0 date synthetic | 04, 01 | Labeled synthetic, do not cite as data |
| PI8 | `incois-demo-hycom-YYYYMMDD` synthetic | 01 | Labeled synthetic |
| PI9 | #13092 since 1.136 UNVERIFIED | 06, 07 | Keep risk tag |

---

## 7. Kill risks ranked (merged, 9)

| Rank | Kill | Hit | Mechanism | Mitigation | Owner |
|------|------|-----|-----------|------------|-------|
| K1 | Full-cube 0.96GB fetch OOM | H×H | 24×40×500×500 float32 ships whole | Subset API + bbox+3-5 depths+3-5 steps+1var + abort superseded + downsample-while-drag + low-res first | M2/M3 gate |
| K2 | Offline judging net-death | H×H | Vercel+R2+Supabase+ion all net | Pre-warm presets + offline assets + recorded backup after live attempt | M1/M5 gate |
| K3 | zarr-cesium churn + #13092 jump | M×H | v0.1.4→0.2.0 API drift, EPSG3857 issues, translucency camera jump | Pin 0.2.0 + Cesium ≥1.119, test #13092 at pin before ADR, zarrita fallback ready | Phase 0 gate |
| K4 | Render 512MB PyVista OOM | H×H | Marching cubes on 0.1CPU/512MB | scikit-image marching cubes, cache in R2, test early | M3/Phase 0 |
| K5 | Supabase 480/500MB + 1wk pause | H×H | Overflow + wake latency kills M4 | Metadata PG + profiles R2 JSON, keep-warm ping | M4 gate |
| K6 | Fly-vs-fetch race jank | H×M | Fly animation races chunk fetch | Preload low-res slice first, abort superseded | M1/M3 |
| K7 | Geocoder empty-bbox blank globe | M×H | Place not feature, no bbox→catalog | Presets-first, empty bbox = blocked message never blank | M1 |
| K8 | INCOIS vs public-cloud tension | M×H | F5 on-prem vs demo cloud, judging Q&A | Demo≠deliverable doc + compose proof | M5 |
| K9 | R2 10GB overflow | M×H | Subset + isosurface cache growth | IO subset only, monthly only, aggressive compression | M2 |

H=high severity, M=medium severity/probability. K1+K2 kill demo day. K3+K4 kill build week. Rest degrade.

---

## 8. Residual + provenance enforcement (G6/G7 detail)

| Rule | Text | Enforce where |
|------|------|---------------|
| Sign | `residual = model − observation` (reject paste `E = O − M`) | Every compare panel, code + docs |
| Gate | No residual render without QC + method labels | Panel blocked message if missing |
| Provenance | Every sample: dataset, variable, units, UTC time, QC/mode, transform version | Point query, profile, transect, section APIs |
| Unlabeled block | Missing units + standard_name + missing-value rule + source version + ETag → blocked view | Same enforcement as empty bbox |
| Anomaly | Only with stated baseline | Divergence step of scene arc |
| Volume | Point divergence now, volume divergence deferred (sparse floats can't form dense volume without interpolation) | Scope rule doc |

## 9. Mermaid addendum (ad5c121)

Concept gaps mermaid fills (design only, live zero): observation-as-query, residual-first UI, feature-as-object + tracking, trajectory method, P0–P7 ladder, metric list, citation classes, motion test, traceability wording. New inventions: sign flip (was systematic 3 files, RESOLVED 2026-09-10), engine/Next/Dask implications, Esri/INCOIS/Mapbox claims beyond links. New kills: K10 sign propagation (CLOSED — 3 files rewritten canonical 2026-09-10), K11 engine churn, K12 detection overclaim. Detail: see `08-mermaid-design-science-track.md` §8.

## 10. Coverage note (74/74)

4 flagged shared docs closed in `01-ps-authority-and-shared-canonical.md` §11. No new gaps/kills: optimization prefetch/lru/tileCache/KTX2/progressive feed existing G4/K1 mitigations, nullschool canvas truth already fenced, open-source names map to existing F1/F2/F5 coverage, Windy/Ventusky/zoom.earth rows are UX refs not gaps.

Next: `07-merged-build-plan-and-research-queue.md`.
