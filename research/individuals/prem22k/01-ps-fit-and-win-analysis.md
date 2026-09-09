# PS fit + win analysis (2026-09-09)

Source: pasted SIH26067 PS text vs 8 existing docs (`vmax-ocean-docs/`).

## PS match

- R1 browser 3D water column: MapLibre + Three slice + curtain. Keep.
- R2 T/S/currents, depth/isosurface/time: M1/M4. Keep.
- R3 Argo/Glider/CTD/BGC markers + click profile: M2/M3. Keep.
- R4 NetCDF/xarray + delimited text, modular ingest: adapters. Note PyNIO dead upstream, xarray choice needs one-line ADR.
- R5 palette/range/log-linear/opacity/exaggeration: covered. Keep.
- R6 REST/OPeNDAP + no-install: partial. REST defined, OPeNDAP facade missing.
- R7 OGC WMS/WCS + CF + plugin: partial. CF strong, WMS/WCS roadmap only. Label roadmap, avoid compliance claim.
- R8 outreach + Disaster Management: weak. Hazard, SAR, fishery, climate need demo beats.
- W1 residual/QC + W2 Zarr/benchmark: differentiator. Keep.

## Gaps

1. `sources.md` lacks 5 PS dataset links (las.incois.gov.in, GLOBAL_MULTIYEAR_PHY_001_030, ifremer Argo, ifremer glider v2, blank in-situ collection).
2. `data-contract-and-pipeline.md` uses synthetic `incois-demo-hycom-YYYYMMDD`. Need dataset cards + sha256 + license + bbox.
3. `system-design.md` observations endpoint lacks GeoJSON-vs-Arrow cutoff (suggest `<500 features GeoJSON`).
4. Benchmark workload fixed (`256×256`, 40 depths, 24 steps, 2 vars, 1000 markers) but reference laptop absent.
5. HYCOM/GODAS context in problem-statement = assumption, not official. Label it.

## Inventions to fix

- Official listing URL differs from pasted portal text. Pasted text canonical.
- No fake perf numbers found. Good. Keep claims discipline.

## Win moves, ordered

1. Lock M0 fixture: one model cube + Argo profiles, Indian Ocean bbox, event date, manifest checksums.
2. Prove M1-M3 live: slice controls, marker click, profile + matchup residual with method + QC.
3. M4 depth cue: curtain + exaggeration + currents; isosurface server/precomputed first.
4. M5 harden: shareable view, outreach mode, clean-browser reload, compose deploy.
5. Paper trail: dataset cards, ADRs (Cesium/PyNIO/OPeNDAP/chunking), OpenAPI client, benchmark record, known limits.
6. Pitch dry-run: mandate-mapped 90s script, fallback quality mode.

## Kill risks

- Full 4D fetch kills memory (`24×40×500×500 ≈ 0.96 GB`). Enforce subset API + downsample-while-drag.
- Unlabeled field kills credibility. Block render without units + missing-value rule + source version + ETag.
- Invented resolution kills trust. Mark assumptions.
- Net-dependent demo kills judging. Pre-warm + recorded backup after live attempt.
