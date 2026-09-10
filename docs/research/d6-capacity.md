# D6 — Capacity Precise (Free Tier)

Date: 2026-09-10. 3 agents. Exact arithmetic shown. Ratio/overhead caveats marked. Access date per URL.

## 1. R2 byte math (cap 10 GB Standard)

Grid: GLORYS 1/12° = 0.083°/cell. Bbox lon 60–100E × lat 5S–30N = 40° × 35° = 480 × 420 = 201,600 cells/slice. float32 slice = 806,400 B = 0.806 MB. Vars: thetao/so/uo/vo 3D + zos 2D → full step = 4×50+1 = 201 slices = 162.086 MB uncompressed. Surface-only (5 slices) = 4.032 MB. 5-depths (21 slices) = 16.934 MB.

Per stored month @10:1: monthly 1-step surface 0.403 MB / 5-depths 1.693 MB / full-50 16.209 MB; daily ~30.44 steps surface 12.273 MB / 5-depths 51.548 MB / full-50 493.390 MB. Fit 10,000 MB: monthly surface 24,801 / 5-depths 5,905 / full-50 617; daily surface 815 (~68 yr) / 5-depths 194 (~16 yr) / full-50 20.3 (~1.7 yr). ×1.074 if GiB counting (daily full-50 = 21.8 mo).

Ratio caveat: 10:1 optimistic ceiling for pure lossless float32. Measured: CESM ocean zstd 1.35x, earth cube Blosc ~3.06x. 10:1 needs smooth-field + shuffle/bitshuffle or lossy/quantized path. At 3x, divide months-fit ×0.3 (daily full-50 ≈ 6 mo).

Chunk rule: one chunk per var-level per month (time=30, x=480, y=420). Daily-per-step chunks explode Class A ops (free 1M A/mo covers bulk ingest only coarse). Chunk overhead ~0.5–2% UNVERIFIED. Isosurface cache ~1–10 MB/mesh UNVERIFIED (12 cached ≈ 50 MB) — keep local/IndexedDB LRU, out of R2.

Default scope locked: daily surface + daily 5-depths rolling 12 mo (~766 MB) + monthly full-50 24 mo (~389 MB) = ~1.2 GB. Full-50 daily fits ~20 mo zero headroom — avoid default. Fallback order: drop uo/vo → cut months (rolling window) → coarser chunks → float16/quantized (quality UNVERIFIED). Broader IO 40–120E/30S–30N = ×3.43 cells (grid-ratio arithmetic UNVERIFIED).

Sources: `https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description`, `https://developers.cloudflare.com/r2/pricing/`, CESM study purl 10428975, arxiv 2604.06221, Lexcube 10.1109/mcg.2023.3321989 (all 2026-09-10).

## 2. Supabase fit (cap 500 MB + 7d pause)

Schema: `docs/data/argo-data.md`. PG row math (MAXALIGN 8, 24B header + 4B item ptr; `https://www.postgresql.org/docs/18/storage-page-layout.html`): floats row ~84B (wmo/cycle int4, lat/lon float8, date text 10B, variables ~12B); profiles row ~76B (wmo/cycle int4 + depth/temp/sal/oxygen float8). Geography point 32B (`ST_MemSize` ref). GiST +40–60B/row UNVERIFIED.

MB table (heap only, no indexes/TOAST/WAL):

| scope | float-rows | floats MB | level-rows | profiles MB | total | fits |
|---|---|---|---|---|---|---|
| 700 × 100 cycles | 70,000 | 5.9 | 6,860,000 | 521 | 527 | no |
| 800 × 104 | 83,200 | 7.0 | 8,153,600 | 620 | 627 | no |
| 900 × 100 | 90,000 | 7.6 | 8,820,000 | 670 | 678 | no |
| 800 × 10 recent | 8,000 | 0.7 | 784,000 | 60 | 60 | yes |
| 800 × 1 latest | 800 | 0.07 | 78,400 | 6.0 | 6.1 | yes |
| metadata only 800×104 | 83,200 | 7.0 | 0 | 0 | 7.0 | yes |

4000×100 claim FALSE: 39.2M rows × 76B ≈ 3 GB heap, 6x over before indexes. Overhead UNVERIFIED: btree (wmo,cycle) +130–260 MB, GiST +3–5 MB, fill/WAL pushes disk > DB size (quota counts data+indexes: `https://supabase.com/docs/guides/platform/database-size`). Plain lat/lon + btree beats PostGIS (saves ~20 MB). R-tree SQLite-only — do not port. JSONB worse (one row/profile ~3–5 KB + TOAST, worse depth filter) — normalized wins.

Counts: global active ~4000 (`https://argo.ucsd.edu/about/status/`); India-only 73–75 active (AST25 report) / 122 claimed May 2026 LinkedIn; Indian Ocean all-nations 700–900 UNVERIFIED (3×3° target estimate, no public tally). Profiles/float: schema N_PROF 104 × N_LEVELS 98; use 100–104 recent, 150 lifetime max UNVERIFIED.

Pause exact (`https://supabase.com/docs/guides/platform/free-project-pausing`, `.../pricing`): 7d low-activity trigger; warning email ~1wk before + confirmation after; dashboard Resume; data retained, 1-yr restore; 2 active projects; 500 MB then read-only; 5 GB egress; 1 GB storage. Wake latency 1–3 min UNVERIFIED. Keep-warm: docs prescribe "few user requests each day" — no anti-ping clause found; trivial `SELECT 1` sufficiency UNVERIFIED, use real queries. Plan: daily Action/cron `GET /rest/v1/floats?select=wmo&limit=1` + one bounded bbox query 2–3×/day; alert on warning email; monitor `pg_database_size()` weekly. Fallback trigger: size >400 MB or level-rows >5M or egress >4 GB/mo → strict subset (metadata + latest 10, ~60 MB).

R2 JSON fallback (wins full history, egress-free: 10 GB-mo + 1M A + 10M B/mo, `https://developers.cloudflare.com/r2/pricing/`): `r2://argo-indian/{wmo}/{cycle}.json` `{wmo,cycle,lat,lon,date,levels:[[pres,temp,psal,doxy]…]}` + `manifest.json` bbox list; frontend direct, no backend hot path. Alt ranking: R2 JSON > SQLite-wasm (zero backend, full download/client) > Supabase strict subset (hot path only). Lazier: skip Supabase entirely, R2 JSON + client index.

## 3. Chunk + cache combo (methods: `docs/performance/optimization.md`)

Winner: single balanced `(1,10,540,1080)` + browser `max-age=86400` + `lru_cache(maxsize=1000)` + no pyramid + KTX2 only 3D Tiles. Holds free tier, smallest cold (~2.33 MB/chunk). Runner-up dual-rep +`(30,50,108,216)` only if time-animation dominant (~2x GB).

Per-chunk @10:1: slice store 5,832,000 elems = 23.33 MB raw ≈ 2.33 MB; time store 34,992,000 elems = 139.97 MB raw ≈ 14.0 MB. Sweet spot 100KB–2MB (doc): slice slightly over, time far over — UNVERIFIED outside doc. Dual 40x time-series gain claimed in doc; corroboration 713–1405x worst-case tradeoff (ESSOAr chunk study); exact 40x UNVERIFIED. Pyramid ×1.14 3D / ×1.33 2D (2x coarsen assumed). R2 free 10 GB / 1M A / 10M B / egress free (`.../r2/pricing/`, `.../r2/platform/limits/`). Repeat-view: second load 0 Class B (hit rate workload-dependent, no % invented). Cold: metadata JSON KBs (lazy open) + first chunks; ≤10s UNVERIFIED until measured. Isosurface `lru_cache` 50 vs 500 ms per doc (functools semantics corroborated); R2-precompute-vs-lru UNVERIFIED — lru wins free (0 R2 cost, process-local), precompute wins multi-user repeat. KTX2 10–30% smaller / 30% faster / 80% less GPU mem per doc; Khronos artist guide corroborates ~78–82% GPU saving — use only 3D Tiles path.

Benchmark steps (record network panel + R2 dashboard): 1. build one var both chunkings, record compressed bytes (`ls -l`, `zarr.info`); 2. cold slice (clear cache: GETs + bytes + wall) + time-series point query, single vs dual; 3. cold start throttled Fast-3G + unthrottled (metadata bytes, time-to-first-slice; pass slice ≤750 ms repeat unthrottled, cold ≤10 s); 4. repeat same slice twice, confirm 0 Class B / disk-cache / 304; 5. isosurface cold vs lru hit ×10 runs each vs R2 precomputed fetch; 6. pyramid 4-level GB multiplier + zoomed-out GETs/bytes with/without; 7. sum GB vs 10 GB + Class A/B vs 1M/10M monthly — fail → drop dual or pyramid.

Sources: R2 pricing + calculator + limits; doi:10.1002/essoar.10511054.2 + zarr performance guide; spatialworkflow + EOPF chunking; Khronos KTX + artist guide; ndpyramid README + functools docs; MDN Cache-Control (semantics only). All 2026-09-10.

## 4. Locked decisions

R2 default scope ~1.2 GB (§1). Supabase latest-10 + metadata ~60 MB + R2 JSON history (§2). Chunk single balanced default (§3). Still open: laptop runs (slice ≤750 ms, cold ≤10 s, 30 FPS + 5000 markers, Arrow cutoff, §3 steps 1–7).
