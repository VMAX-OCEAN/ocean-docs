# SIH26067 — Research Program Overview

Date: 2026-09-10. Authority: SIH26067, MoES/INCOIS Ocean Valley, Software, Disaster Management. Deadline 30 Sep 2026.
Rule: no gate passes without measured evidence + access date. Blank cell = gate open. UNVERIFIED is never a pass.

This file is the entry point to the completed research program. It records what was verified, what is still open, and where every artifact lives. Deep detail lives in the linked files; this file is the map.

---

## 1. What this program answers

Five questions decide whether the build is correct:

1. **Does the reference design exist and does it fit?** — dataset contracts, stack pins, capacity math.
2. **Is the stack the best free option, not just an option?** — best-of-best passes for every locked choice.
3. **What must be measured before any number is claimed?** — protocols with gates, not estimates.
4. **What is the demo spine and does it name the mandates?** — four beat cards with scripts + presets.
5. **What decisions are binding?** — ADRs with evidence tables.

---

## 2. Workstreams D1–D8

| # | Workstream | Status | Artifact |
|---|---|---|---|
| D1 | Dataset cards (5 PS sources) | **Done** | `data/glorys12.md`, `data/argo.md`, `data/glider.md`, `data/incois-las.md`, `data/insitu-collection.md` |
| D2 | Reference laptop + measured-run protocols | **Protocols done, runs open** | `performance/reference-laptop.md`, `performance/benchmark-protocol.md`, `performance/chunk-benchmark-protocol.md`, `performance/marker-format-cutoff-protocol.md`, `ocean-web/scripts/bench-harness.js` |
| D3 | ADRs | **Done (2 accepted-benchmark-pending)** | `architecture/adr/ADR-001..005` + `adr/README.md` |
| D4 | Phase-0 lib pins + best free picks | **Done** | `research/d4-lib-pins.md` |
| D5 | Externals resolved + reuse teardowns | **Done** | `research/d5-externals.md` |
| D6 | Capacity precise (R2 + Supabase + chunk/cache) | **Done** | `research/d6-capacity.md` |
| D7 | Mandate beats + 90s scripts | **Done** | `research/d7-mandate-beats.md` |
| D8 | Mermaid sign rewrite + open-question gates | **Open** | `research/d8-*.md` (owed) |

---

## 3. D1 — Dataset contracts

All five PS sources now have contract cards with source URL, access date, sha256 (where a sample was hashed), license, bbox, variables, ingest version, assumptions.

| Card | DOI / URL | License | Key fact |
|---|---|---|---|
| `glorys12.md` | `10.48670/moi-00021` | Copernicus Marine licence (free, attribution + DOI) | 4 3D + 7 2D + 8 static vars; 1/12°, 50 levels; 1993→M-1. **No vertical velocity** (`wmo` was a doc error, fixed) |
| `argo.md` | `10.17882/42182` | CC-BY 4.0 | FTP + HTTPS + s3/rsync/ERDDAP; Indian subset 354,696 files / 2,421 floats |
| `glider.md` | `10.17882/56509` | CC-BY-NC 4.0 (**NC — check**) | Indian coverage sparse+clustered: 11.7% deployments, 124/131 = one Mayotte array. Availability risk |
| `incois-las.md` | `las.incois.gov.in` / ERDDAP | ERDDAP boilerplate verbatim | 16 ERDDAP IDs, 13 LAS cats, 44 holdings rows; live APIs, sha NONE |
| `insitu-collection.md` | **blank — authority-side** | n/a | PS item d ends at colon. 8 candidates ranked. Fail closed; ask SIH/INCOIS |

Three source-doc bugs found and fixed: `glorys-dataset.md` false `wmo`; `argo-data.md` wrong `region()` arg order + dead `search_lat_lon`. All fixes verified against upstream docs.

---

## 4. D4 — Stack pins (best free)

| Layer | Pick | Why | Detail |
|---|---|---|---|
| Globe | `cesium@1.142.0` exact | 101d soak; avoids 1.145 ClippingPolygons freeze + 1.119 age | `d4-lib-pins.md` §3 |
| Zarr render | `zarr-cesium@0.2.0` exact (+ custom ImageryProvider A-arm) | Triple-confirmed latest; providers unchanged | §2, §5 |
| Particles | NOC fork `cesium-wind-layer` v0.11.1 via provider | Provider wraps it — cannot drop | §4 |
| Host | Cloudflare Pages | Unlimited BW; 25 MiB/file bind → chunks to R2 | §8 |
| Base | GIBS Blue Marble + ion World Bathymetry | $0 + true depth | §9 |
| ion | Community tier | 10 GB storage / 15 GB/mo / 1000 sessions | §7 |

Every pick has a best-of-best rationale + a fallback + an open measurement.

---

## 5. D5 — Externals + reuse

- **Esri resolved**: EMU Explorer (cite, Apache-2.0) + Ocean Ocean basemap (cite base-only). Voxels dropped (code 404, demo-only licence).
- **INCOIS resolved**: prior fetch fail fixed; ERDDAP + LAS + holdings all live; copyable curl.
- **Mapbox**: APIs verified; official pricing captured (adds $2.50 tier 1M–5M).
- **gods-eye-view**: useful as reference architecture, **not** a fork. 12 ranked copies (renderGovernor, layer manager, sharelink, map stacks). MIT with NC/ODbL carve-outs.
- **NASA Eyes**: engine undisclosed; 10-step M5 tour.

---

## 6. D6 — Capacity (precise)

- **R2 default ~1.2 GB**: daily surface + 5-depths rolling 12 mo + monthly full-50 24 mo. 10:1 compression is a ceiling; at 3x full-50 daily ≈ 6 mo.
- **Supabase**: 4000×100 claim false (≈3 GB, 6x over). Latest-10 cycles + metadata ≈ 60 MB fits; R2 JSON holds full history egress-free.
- **Chunk winner**: single balanced `(1,10,540,1080)` + `max-age=86400` + `lru_cache(1000)`; dual-rep only if benchmark proves it.

---

## 7. D7 — Demo spine

Four mandate beats, each naming its mandate aloud in the first 15s:

| Beat | Mandate | Datasets | Preset |
|---|---|---|---|
| Cyclone/storm-surge (Fani 2019) | Hazard assessment | ASCAT + VAP + VAM + GLORYS + floats | Bay 80–95E / 5–22N, 4 steps |
| SAR drift (Konkan) | Search-and-rescue | GLORYS uo/vo + GDP CC0 + SARAT + HF (registered) | 68–74E / 12–20N, 5 daily |
| Fishery PFZ | Fishery advisories | NOAA SST + IRS chlorophyll + PFZ row | 60–104E / 0–25N, 2005-01-15 |
| Basin warming | Climate monitoring | GLORYS monthly + climatology + OISST + Argo | 60–100E / −5–30N, 12 monthly |

Running order: hazard → SAR → fishery → climate. Residual canonical `model − observation` on every compare panel.

---

## 8. D8 — Open

- Rewrite mermaid flipped sign to canonical in 3 files (working tree already shows `M − O` — unexplained, verify before attributing).
- Q7 gate: one-feature proof before detection claims.
- Q9 gate: GPU-vs-server split benchmark before committing GPU ops.
- Q10 gate: random-access path proven before volume claims.

---

## 9. Reading order

1. `RESEARCH-PROGRAM.md` (this file)
2. `research/README.md` — research index
3. `data/*.md` — the 5 cards
4. `research/d4..d7` — pins, externals, capacity, beats
5. `architecture/adr/` — binding decisions
6. `performance/*protocol*` — what to measure
7. `research/verification-ledger.md` — every claim + source

---

## 10. What is still genuinely open

| Open item | Blocks | Owner |
|---|---|---|
| Locked-laptop benchmark runs (slice/cold/FPS/markers/chunk/Arrow) | M2/M4 pass | D2 protocols |
| ADR-002 pin applied in `ocean-web/package.json` (`^1.127.0` → `1.142.0`) | Version ADR | build |
| `insitu-collection` PS item-d URL | D1 card completeness | SIH/INCOIS contact |
| Mermaid sign rewrite + Q7/Q9/Q10 | M4 panels | D8 |
| Live subset wiring + pitch doc assembly | M5 | build |
