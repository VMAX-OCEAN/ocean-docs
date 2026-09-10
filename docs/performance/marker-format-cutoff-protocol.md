# D2 — Marker-Format Cutoff Protocol (GeoJSON vs Arrow vs FlatGeobuf vs R2-JSON)

Date: 2026-09-10. Protocol only, no results. Scope: Indian Argo subset — 2,421 floats, 354,696 profile files (`docs/data/argo.md`), Supabase free 500 MB / 5 GB egress (`docs/research/d6-capacity.md` §2), R2 free 10 GB / 1M A / 10M B / egress-free (`https://developers.cloudflare.com/r2/pricing/`, 2026-09-10). Ceiling: 5,000 markers.

## 0. Preconditions

| Gate | Value | Status |
|---|---|---|
| Gateway `$NINEROUTER_KEY` | length 0 | unavailable — direct curl used |
| Supabase free | 500 MB DB, 5 GB egress, 7-day pause | `https://supabase.com/docs/guides/platform/database-size` 2026-09-10 |
| R2 free | 10 GB, 1M A, 10M B, egress free | `https://developers.cloudflare.com/r2/platform/limits/` 2026-09-10 |
| Markers | 2,421 floats (Indian bbox 30–120E / 30S–30N) | `docs/data/argo.md` 2026-09-10 |
| Renderer | Cesium billboard/point entities | — |

## 1. Format comparison

Wire bytes = 5,000 point markers, 6 fields (`wmo,cycle,lat,lon,date,vars`). Arithmetic shown; row size UNVERIFIED until fixture built.

| Format | Encoding | Bytes @5k (est) | Parse | Dep | bbox server-filter | Source 1 | Source 2 |
|---|---|---|---|---|---|---|---|
| GeoJSON (R2 manifest) | UTF-8 JSON text | ~450–750 KB raw, ~150–250 KB gzip | `JSON.parse` main thread | none | no (full fetch) | spatialworkflow: 59,391 feat = 27 MB raw / 2.65 MB gzip; "few thousand fine, tens of thousands borderline" (`https://www.spatialworkflow.io/geojson-too-big-for-browser/`) | maplibre #106: 200 LineString ×4,500 coords → stringify ~200 ms, parse ~200 ms, main-thread block (`https://github.com/maplibre/maplibre-gl-js/issues/106`) |
| Arrow IPC (apache-arrow JS) | columnar binary | ~90–130 KB uncompressed (6 cols ≈19 B/row + framing) | `tableFromIPC` → typed arrays | `apache-arrow` ~100–200 KB | no (client filter; manifest pre-partitions) | arrow-to-json: ~20x faster than JS arrow+stringify; column form ~36% smaller (npm 403 bot-block — UNVERIFIED) | Medium 1M×4col: JSON 90–120 MB / 600–1200 ms parse vs Arrow IPC 35–65 MB / 120–300 ms (`https://medium.com/@hadiyolworld007/python-js-handshake-arrow-to-instant-charts-3942a04b674d`, 2025-10-10) |
| Arrow — JS caveats | — | — | `tableFromIPC` sync; no IPC body-compression in JS → gzip-only over HTTP | — | — | apache/arrow-js #109: "Record batch compression not implemented" (`https://github.com/apache/arrow-js/issues/109`) | Flechette: vs Arrow JS ref impl 1.3–1.6x value iter, 2–7x array extract, 7–11x row-object (`https://github.com/uwdata/flechette`) |
| FlatGeobuf (JS) | FlatBuffers + Hilbert R-tree | ~150–250 KB; index ~40 B/node | `flatgeobuf.deserialize` streaming | `flatgeobuf-geojson.min.js` | YES — HTTP Range, lazy index | flatgeobuf.org: Denmark 906,602 LineStrings vs Shapefile=1 — read full FGB 0.46 vs GeoJSON 15; w/ spatial filter FGB 0.71 vs GeoJSON 705; size FGB 0.77 vs GeoJSON 1.2 (`https://flatgeobuf.org/`) | brycemecum: 1M pts FGB 106.7 MB with index (~40 MB index), 64 MB without; streamed draw starts immediately index-less (`https://brycemecum.com/2022/04/04/flatgeobuf/`) |
| Supabase+PostGIS (baseline) | PostgREST JSON rows | ~750 KB raw / row ~150 B | PostgREST serialize + `JSON.parse` | Supabase JS | YES — PostGIS GiST | d6 §2: GiST +40–60 B/row UNVERIFIED; `pg_database_size` counts data+indexes | MDPI 2025 doi:10.3390/ijgi14090336 (403 bot-block, metadata via Exa): Leaflet/OpenLayers fastest ≤10,000 feat; 50,000+ → >1 s all libs |

JSONB one-row-per-profile ~3–5 KB + TOAST worse than normalized (d6 §2). Arrow/FGB not carried in the Supabase DB.

## 2. Test matrix

Vary N ∈ {100, 500, 1000, 2000, 5000} (fixed seed, same 5,000-feature pool sampled without replacement → nested sets). 10 runs/arm, discard first (warmup), report p50 + IQR.

| Arm | Source | Transport | Client decode |
|---|---|---|---|
| A1 | Supabase PostgREST | `GET /rest/v1/floats?select=...&geom=cs.{...}` | `res.json()` |
| A2 | Supabase RPC | PostGIS `ST_Intersects` function, GeoJSON out | `res.json()` |
| B | R2 `manifest_geojson` | `GET` full object | `JSON.parse` |
| C | R2 `markers.arrow` | `GET` ArrayBuffer | `tableFromIPC` |
| D | R2 `markers.fgb` | `GET` (index) + Range bbox | `flatgeobuf.deserialize` |

Control: same N, local `file://` (removes network) — isolates parse vs wire.

## 3. Metrics (exact units)

Per run: `ttfb_ms` (`responseStart − requestStart`); `bytes` (`content-length` compressed + decoded; **R2 Class B ops** from dashboard delta); `server_ms` (Supabase only: `curl -w %{time_total}` minus TTFB; plus `EXPLAIN (ANALYZE, BUFFERS)` planner ms); `parse_ms` (`performance.now()` around parse); `prep_ms` (feature→Entity/PointPrimitive build); `first_frame_ms` (fetch start → `scene.postRender` first); `fps_3s` (frames/3 s with 5,000 resident); `egress_bytes_month` (projected `bytes_gzip × queries_per_month`; flag if >4 GB = 80% of 5 GB).

## 4. Harness (stdlib + CDN only)

Fixture generator (Python, stdlib):

```python
# gen_fixtures.py — emits geojson/arrow/fgb/sql for N in 100..5000
import json, random
random.seed(42)
# FLOATS from ar_index parse: (wmo, cycle, lat, lon, date, vars)
# ...build N nested features, write markers_N.geojson
```

```bash
ogr2ogr -f FlatGeobuf markers_5000.fgb markers_5000.geojson                       # index ON
ogr2ogr -f FlatGeobuf markers_5000_noidx.fgb markers_5000.geojson -lco SPATIAL_INDEX=NO
python -c "import pyarrow.json as pj,pyarrow.feather as pf; pf.write_feather(pj.read_json('markers_5000.geojson'),'markers_5000.arrow',compression='uncompressed')"
```

Browser harness (one file, no framework):

```html
<script type="module">
import { tableFromIPC } from 'https://cdn.jsdelivr.net/npm/apache-arrow@21/+esm';
const t0 = performance.now();
const buf = await (await fetch(URL)).arrayBuffer();
const t1 = performance.now();
const table = tableFromIPC(new Uint8Array(buf));
const t2 = performance.now();
window.__m = { fetch: t1-t0, parse: t2-t1, bytes: buf.byteLength };
</script>
```

FlatGeobuf: `https://unpkg.com/flatgeobuf/dist/flatgeobuf-geojson.min.js` → global `flatgeobuf`; `deserialize(url, bbox)`.

```bash
curl -s -o /dev/null -w "%{time_total}\n" "$SUPABASE_URL/rest/v1/rpc/floats_in_bbox?..." -H "apikey: $ANON"
psql "$DB" -c '\timing on' -c "EXPLAIN (ANALYZE, BUFFERS) SELECT wmo,cycle,lat,lon,date,vars FROM floats WHERE geom && ST_MakeEnvelope(30,-30,120,30,4326);"
```

## 5. Expected crossover (HYPOTHESIS — UNVERIFIED, to be measured)

| N | Fastest (expected) | Basis |
|---|---|---|
| 100 | Supabase ≈ R2-JSON | 15–30 KB both; PostgREST round-trip ~30–60 ms dominates; Arrow/FGB init 50–150 ms one-time hurts small N |
| 500 | Supabase (warm) | PostgREST ~75 KB; GiST ~1–3 ms; same wire class |
| 1000 | tie | ~150 KB; GeoJSON parse ~10–25 ms; Arrow ~20 KB, decode <10 ms |
| 2000 | **crossover region** | Supabase ~300 KB + serialize; Arrow ~40 KB + R2 TTFB 20–50 ms → Arrow edges out |
| 5000 | R2-Arrow (bytes/parse); render-bound | 5,000 Cesium billboards vs 33 ms frame budget — render, not format, is the ceiling |

Two independent drivers decide "Supabase stops being best": (1) latency/parse crossover ≈ N 1,000–2,000; (2) free-tier egress crossover earlier in use — Supabase 5 GB/mo ÷ (5,000 × ~150 B gzip ≈ 0.75 MB) ≈ **6,700 bbox loads/mo (~220/day)**; R2 egress-free removes cap.

Lazy recommendation pending measurement: R2 GeoJSON manifest needs zero new deps and no Supabase hot path; add Arrow only if measured `parse_ms` at chosen N exceeds 50 ms. FGB only if bbox from one static R2 object w/o DB is required.

## 6. Measurement template (fill after run)

| N | Arm | ttfb_ms p50 | bytes gz | parse_ms p50 | prep_ms | first_frame_ms | fps_3s | planner_ms | Class B | proj GB/mo |
|---|---|---|---|---|---|---|---|---|---|---|
| 100 | A1 | | | | | | | | — | |
| 100 | B | | | | | | | | | |
| 100 | C | | | | | | | | | |
| 100 | D | | | | | | | | | |
| 500 | A1..D | | | | | | | | | |
| 1000 | A1..D | | | | | | | | | |
| 2000 | A1..D | | | | | | | | | |
| 5000 | A1..D | | | | | | | | | |

Budgets: parse+prep ≤ 50 ms; first frame ≤ 150 ms; steady 30 FPS with 5,000 resident; Supabase egress <4 GB/mo; R2 Class B <10M/mo.

## 7. Decision rule (lock)

```
N_LOCK = min N ∈ {100,500,1000,2000,5000} where ANY holds:
  (a) p50_e2e(Supabase) > p50_e2e(R2-Arrow) × 1.20, IQRs non-overlapping
  (b) projected Supabase egress(month) > 4 GB
  (c) p95(parse+prep) > 50 ms OR p95(first_frame) > 150 ms

N <  N_LOCK → Supabase PostgREST bbox (A1), GeoJSON rows.
N >= N_LOCK → R2 static object:
              Arrow IPC  if batch decode is the bottleneck (C)
              FlatGeobuf if bbox-from-one-object w/o DB is required (D)
              GeoJSON    if N_LOCK > 2000 (no dep, zero backend)
Render ceiling dominates at 5,000 → if fps_3s < 30, fix render path
(PointPrimitiveCollection / GPU layer), not wire format.
```

Report `N_LOCK`, winning arm, binding condition. If none trips, lock = "Supabase holds through 5,000; Arrow deferred until render FPS forces R2".

## 8. Source ledger (2026-09-10 unless noted)

| URL | HTTP | Note |
|---|---|---|
| `https://flatgeobuf.org/` | 200 | official perf table |
| `https://github.com/flatgeobuf/flatgeobuf` | 200 | same table |
| `https://brycemecum.com/2022/04/04/flatgeobuf/` | 200 | 1M pts, index 40 B/node |
| `https://github.com/apache/arrow-js/issues/109` | 200 | JS no IPC compression |
| `https://github.com/uwdata/flechette` | 200 | vs Arrow JS ref impl |
| `https://arrow.apache.org/js/main/functions/Arrow.dom.tableFromIPC.html` | 200 | API |
| `https://github.com/maplibre/maplibre-gl-js/issues/106` | 200 | JSON parse ~200 ms block |
| `https://www.spatialworkflow.io/geojson-too-big-for-browser/` | 200 | 59,391 feat = 2.65 MB gzip |
| `https://doi.org/10.3390/ijgi14090336` | 403 | MDPI bot-block; metadata via Exa |
| `https://www.npmjs.com/package/arrow-to-json` | 403 | npm bot-block; 20x claim UNVERIFIED |
| `https://developers.cloudflare.com/r2/pricing/` | 200 | free tier |
| `https://developers.cloudflare.com/r2/platform/limits/` | 200 | limits |
| `https://supabase.com/docs/guides/platform/database-size` | 200 | quota counts data+indexes |
| `https://www.postgresql.org/docs/18/storage-page-layout.html` | 200 | row math |

Gateway unavailable (`$NINEROUTER_KEY` len 0) — all direct curl. No results here; run §4 and fill §6.
