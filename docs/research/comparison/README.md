# Research Comparison — SIH26067 Ocean Viz

Date: 2026-09-09. Authority: SIH26067, MoES/INCOIS Ocean Valley, Software, Disaster Management. Deadline 30 Sep 2026.

Lakshya namespace = deployment/execution track. 14 files.
Prem22k namespace = product/science track. 8 files.
Mermaid namespace = design/science track. 15 files, 403 lines (origin/main ad5c121, prajwal).
Shared canonical = stack + milestones, designed not built.

## File map

| # | File | Owns |
|---|---|---|
| 01 | `01-ps-authority-and-shared-canonical.md` | R1-R5, F1-F7, mandates, datasets, open items, shared stack locks, coverage gaps |
| 02 | `02-lakshya-deployment-track.md` | All 14 lakshya files, serves/stale/assumptions/risks, verdicts |
| 03 | `03-prem22k-product-science-track.md` | All 8 prem22k files, status, assumptions, risks, corrections |
| 04 | `04-head-to-head-comparison.md` | Dimension tables, keep/drop, pros/cons |
| 05 | `05-ratings-and-leaderboard.md` | 27 docs rated 1-5 x6 axes, top-3 bottom-3 (+ mermaid 15-file addendum, 42 total) |
| 06 | `06-gaps-inventions-kill-risks.md` | Shared + per-namespace gaps, inventions, kills with mitigations |
| 07 | `07-merged-build-plan-and-research-queue.md` | Phase 0 → M1-M5 gates, dataset/ADR gates, deep-research queue |
| 08 | `08-mermaid-design-science-track.md` | Third namespace: file inventory, web verification, R/F matrix, residual-sign conflict, ratings, three-way deltas, Keep 11–17 |

## Rating axes

PS-align | Evid | Exec | Risk | Win | Fresh. Each 1-5. Total = sum.

## Top-3

1. `problem-statement/PROBLEM-STATEMENT-ANALYSIS.md` — 29
2. `research/individuals/prem22k/06-earth-3d-4d-toggle-9router.md` — 27
3. `research/individuals/lakshya/free-tier-deployment.md` — 26

## Bottom-3

- `pricing-analysis.md` — 7, $9.50 paid contradicts free-only
- `render-blueprint.md` — 8, paid disk yaml stale
- `render-deployment.md` — 9, paid backend hot-path stale

## Stack lock

CesiumJS + zarr-cesium + xpublish + argopy + SQLite. F-coverage designed, not built. M1-M5 unchecked. WMS/WCS roadmap-only. PyNIO dropped, ADR owed.

## Coverage

74 md mapped: 38 shared + 14 lakshya + 8 prem22k + 15 mermaid (README double-counted across roots = 75 paths). 4 flagged shared docs closed in 01 §11 (optimization/nullschool/open-source/platform). Mermaid impact = design-only, zero live gates; Keep 11-17 adoptable, sign rewrite blocks M4. Detail: `08-mermaid-design-science-track.md` §10.

## Verification baseline

Web verification via 9router gateway 2026-09-09. zarr-cesium CONFIRMED, re-pin 0.2.0 (docs pin 0.1.4 stale). cesium-wind-layer compat issue real, NOC-OI fork v0.11.0. R2 10GB zero-egress CONFIRMED. Supabase 500MB + 1wk pause CONFIRMED. Render free 512MB/750hrs/spin-down CONFIRMED. CORRECTED 2026-09-10: `xpublish-opendap` v0.2.0 EXISTS on PyPI (BSD-3), distinct from `xpublish-zarr` v0.1.0 (Apache-2.0) — earlier 'REFUTED' claim was wrong (ADR-003). MyOcean Pro 4D toolset + no-geocoder CONFIRMED. nullschool stack/pipeline CONFIRMED. NASA Eyes suite CONFIRMED, engine undisclosed. Cesium subsurface CONFIRMED, #13092 UNVERIFIED. GLORYS vars/resolution CONFIRMED.
