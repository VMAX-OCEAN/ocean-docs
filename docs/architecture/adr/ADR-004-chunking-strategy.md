# ADR-004 — Chunking Strategy for GLORYS12 Zarr on Object Storage

**Status:** Proposed — pending benchmark. Provisional until the measured-run gate (`../performance/chunk-benchmark-protocol.md` §9) produces a locked-laptop result. No gate passes on UNVERIFIED or blank cells.

**Date:** 2026-09-10

**Decision owner:** Data layer. Inputs: `../../research/d6-capacity.md` §1/§3, `../../performance/chunk-benchmark-protocol.md`, `../../performance/optimization.md` §1, `../../data/netcdf-to-zarr.md`, `../../data/glorys12.md`.

---

## Context

GLORYS12 (`GLOBAL_MULTIYEAR_PHY_001_030`, doi:10.48670/moi-00021) is 1/12° reanalysis on a 4320 × 2041 global grid, 50 levels, 4 3D vars (`thetao`, `so`, `uo`, `vo`) + 2D (`zos`). Product grid/resolution/levels verified in `glorys12.md` (accessed 2026-09-10). The platform serves the Indian-Ocean subset (lon 60–100E, lat 5S–30N) as Zarr over HTTP from R2 free tier.

Two access patterns compete:

- **Slice / spatial view** — one depth-time slice, all lat/lon. Favours small time chunks, large spatial chunks.
- **Time-series / point query** — one point, all time. Favours large time chunks, small spatial chunks.

Two candidate chunkings (`optimization.md` §1, `netcdf-to-zarr.md`; from the chunk-size study doi:10.1002/essoar.10511054.2):

- Balanced single-store `(1,10,540,1080)` — slice-optimized, one store.
- Dual-rep time-series `(30,50,108,216)` — time-optimized, second store (dual = both stores).

Binding constraint is R2 free tier, cap 10 GB Standard, 1M Class A / 10M Class B req/mo, egress free (`https://developers.cloudflare.com/r2/pricing/`, accessed 2026-09-10). R2 byte math (`d6-capacity.md` §1): default scope (daily surface + daily 5-depths rolling 12 mo + monthly full-50 24 mo) ≈ **1.2 GB** at 10:1 — holds with headroom. Dual-rep roughly doubles GB. Ratio caveat: 10:1 is an optimistic lossless float32 ceiling; measured ocean zstd is ~1.35x–3.06x, so real scope may shrink, not grow. Compression is not the lever here — chunk share of the 10 GB is.

Per-chunk arithmetic (`d6-capacity.md` §3; deterministic, not measured):

| Store | Declared chunk | Elems | Raw | @10:1 | vs 100KB–2MB sweet spot |
|---|---|---|---|---|---|
| balanced | (1,10,540,1080) | 5,832,000 | 23.33 MB | ~2.33 MB | slightly over |
| timeseries | (30,50,108,216) | 34,992,000 | 139.97 MB | ~14.0 MB | far over (UNVERIFIED outside doc) |

Effective chunks on the benchmark subset differ: balanced `(1,10,480,420)`, time `(30,50,108,216)` (`chunk-benchmark-protocol.md` §3). The claimed ~40x time-series gain is from `optimization.md`/`netcdf-to-zarr.md`; the chunk study corroborates the *direction* with a 713–1405x worst-case tradeoff, but the exact 40x is UNVERIFIED. So dual-rep is a hypothesis, not a default.

## Decision

**Adopt the balanced single-store chunking `(1,10,540,1080)` as the default now.** Defer every additional representation.

1. **Default = one Zarr store, balanced `(1,10,540,1080)`.** Holds the free tier (default scope ~1.2 GB), gives the smallest cold payload (~2.33 MB/chunk), and is a single artifact to build, upload, cache, and reason about. Recommended as Option B in `netcdf-to-zarr.md`; selected in `d6-capacity.md` §3.
2. **Dual-rep `(30,50,108,216)` is gated, not adopted.** Build/adopt the second time-series store **only if the chunk bench passes all of G5 ∧ G6 ∧ G7** (time-series GETs and wall beat balanced; slice wall not lost) **on top of G1 ∧ G2 ∧ G9** — per the decision rule in `chunk-benchmark-protocol.md` §9. Simpler store wins ties: balanced-only iff G1 ∧ G2 ∧ G9 but ¬(G5 ∧ G6 ∧ G7).
3. **Pyramid (ndpyramid multiscale) deferred.** Not now. ×1.14 3D / ×1.33 2D GB multiplier (`d6-capacity.md` §3, 2x coarsen assumed) competes with the same 10 GB cap; revisit only after dual-rep is settled and only if zoomed-out fetch cost is a measured problem (G9-style budget check, §9).
4. **Cache layer is part of the decision, not an add-on.** Browser `Cache-Control: max-age=86400` + server `lru_cache(maxsize=1000)` for isosurfaces; no pyramid; KTX2 only on the 3D Tiles path. Winner combo in `d6-capacity.md` §3.
5. **Evidence before lock.** Status stays *Proposed* until a full session fills `chunk-benchmark-protocol.md` §10 (env table, Table A chunk bytes, Protocol A/B, R2 Class B delta, verdict). Gate G8 records balanced chunk bytes against 100KB–2MB (record-only, no hard gate).

## Consequences

**Positive**
- Free tier held with ~8.8 GB headroom at default scope; no dual-store duplication.
- Smallest cold payload and GET count for the primary (slice/map) access pattern.
- One build path, one bucket prefix, one cache story — least operational surface.
- Cold-start ≤ 10 s target is most likely met by the smallest chunk option, pending G2.

**Negative / risks**
- Time animation and point queries may be slower: balanced scans ~30 GETs (one per time step) for a full time series vs the time store's ~1 chunk (`chunk-benchmark-protocol.md` §7, hypothesis).
- Single chunk ~2.33 MB sits slightly over the 100KB–2MB sweet spot; may need tuning.
- Compression ratio caveat (10:1 optimistic) means real byte budget may shrink; fallback order `d6-capacity.md` §1: drop uo/vo → cut rolling months → coarser chunks → float16/quantized (quality UNVERIFIED).
- Provisional: if G1/G2 fail, diagnose per §9 (chunk > 2 MB, missing `Cache-Control`, no HTTP/2, cold missing cache/Range) before changing chunking.

## Alternatives considered

| Alternative | Shape | Why not now |
|---|---|---|
| **Balanced single-store (chosen)** | `(1,10,540,1080)`, one store | Default. Holds free tier, smallest cold, simplest. Recommended in `netcdf-to-zarr.md`. |
| **Dual-rep time-series** | balanced + `(30,50,108,216)` | ~2x GB; exact 40x gain UNVERIFIED. Gate on measured G5/G6/G7 (see Decision 2). Adopt only if time animation dominates and gates pass. |
| **Pyramid (ndpyramid)** | 4-level multiscale | ×1.14/×1.33 GB; competes with 10 GB cap. Defer until dual-rep settled + zoomed-out cost measured. |
| **Single-large chunk** | e.g. one chunk/var/level/month `(30,480,420)` | Fewest objects, but a single fetch is many MB — blows the 2 MB sweet spot and cold target. Daily-per-step chunks also explode Class A ops (free 1M A/mo covers bulk ingest only coarse). Rejected. |

## Evidence

| Claim | Value | Source | Verification |
|---|---|---|---|
| R2 free cap | 10 GB-mo Standard; Class A 1M, Class B 10M req/mo; egress free | `https://developers.cloudflare.com/r2/pricing/` (page updated 2026-08-07) | Accessed 2026-09-10, HTTP 200 |
| Default scope bytes | ~1.2 GB (daily surface + 5-depths 12 mo + monthly full-50 24 mo) | `../../research/d6-capacity.md` §1 | Deterministic arithmetic |
| Balanced chunk @10:1 | ~2.33 MB (23.33 MB raw) | `../../research/d6-capacity.md` §3 | Deterministic arithmetic |
| Time chunk @10:1 | ~14.0 MB (139.97 MB raw) | `../../research/d6-capacity.md` §3 | Deterministic arithmetic |
| Sweet spot | 100 KB – 2 MB compressed | `../../performance/optimization.md` §1 | Doc-stated |
| Chunk-size → read perf | large-time/small-space vs small-time/large-space tradeoff | Nguyen, Chazaro Cortes, Dunn, Shiklomanov (2023), doi:10.1002/essoar.10511054.2 | Crossref metadata verified 2026-09-10 (posted 2023-03-09); DOI landing 403 (publisher blocks curl) → **UNVERIFIED** at landing, metadata confirmed |
| ~40x time-series gain | claimed | `optimization.md` §1, `netcdf-to-zarr.md` | **UNVERIFIED** — corroborated only in direction (713–1405x worst-case, chunk study) |
| Multiscale pyramid | ndpyramid builds 4-level Zarr; zarr-cesium auto-selects | `netcdf-to-zarr.md`; `https://github.com/carbonplan/ndpyramid` | Repo accessed 2026-09-10, HTTP 200; "A small utility for generating ND array pyramids using Xarray and Zarr." |
| Slices/gates G1–G9 | thresholds defined; all cells blank | `../../performance/chunk-benchmark-protocol.md` §9 | **No measured run** — provisional |

## References

- `../../research/d6-capacity.md` §1 (R2 byte math), §3 (chunk + cache combo, winner/runner-up) — accessed 2026-09-10.
- `../../performance/chunk-benchmark-protocol.md` §9 (pass/fail gates G1–G9, decision rule; measured-run gate), §10 (result record) — accessed 2026-09-10.
- `../../performance/optimization.md` §1 (dual chunking, chunk size tuning) — accessed 2026-09-10.
- `../../data/netcdf-to-zarr.md` (Option A dual vs Option B balanced; recommendation Option B) — accessed 2026-09-10.
- `../../data/glorys12.md` (grid, variables, DOI, dataset IDs) — accessed 2026-09-10.
- Nguyen, D. M. T., Chazaro Cortes, J., Dunn, M. M., Shiklomanov, A. N. (2023). *Impact of Chunk Size on Read Performance of Zarr Data in Cloud-based Object Stores.* doi:10.1002/essoar.10511054.2. Metadata via `https://api.crossref.org/works/10.1002/essoar.10511054.2` (accessed 2026-09-10, HTTP 200); DOI landing 403 → UNVERIFIED.
- ndpyramid — `https://github.com/carbonplan/ndpyramid` (accessed 2026-09-10, HTTP 200).
- Zarr performance guide — `https://zarr.readthedocs.io/en/stable/user-guide/performance.html` (accessed 2026-09-10, HTTP 200).
- R2 pricing/limits — `https://developers.cloudflare.com/r2/pricing/` (accessed 2026-09-10, HTTP 200).

### Verification / gateway note

Gateway guard run length-only, value never printed:
`if [ -n "$NINEROUTER_KEY" ]; then echo "gateway: present (len=${#NINEROUTER_KEY})"; else echo "gateway: absent — direct fetch only"; fi`

Result this run: **gateway absent** — all fetches direct curl. Re-verify via gateway before ADR sign-off if policy requires. Exa MCP was rate-limited (free tier).
