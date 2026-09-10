# ADR-005 — Marker transport format and cutoff (Argo/Glider float markers, ≤5,000)

## Status

**Proposed — pending benchmark.** Provisional. Locked only after §4 harness of
`docs/performance/marker-format-cutoff-protocol.md` runs and `N_LOCK` is measured. Any
statement below marked HYPOTHESIS/UNVERIFIED is a prediction, not a result.

## Date

2026-09-10

## Context

- Scope: Indian Ocean Argo subset — **2,421 floats**, 354,696 profile files, bbox lon
  30–120 E / lat 30 S–30 N (`docs/data/argo.md`). Ceiling **5,000 markers**.
- Free-only hosting: Supabase free 500 MB DB / 5 GB egress / 7-day pause
  (`docs/research/d6-capacity.md` §2); Cloudflare R2 free 10 GB / 1M Class A / 10M
  Class B / egress-free.
- Renderer: Cesium billboard/point entities. At 5,000 resident the render path, not the
  wire format, is the likely ceiling.
- Candidate transports: Supabase PostgREST + PostGIS bbox (baseline), R2 static GeoJSON,
  R2 Arrow IPC, R2 FlatGeobuf.
- Marker row: 6 fields `wmo,cycle,lat,lon,date,vars`.
- Metadata-only Supabase fit is ~7 MB at 800 floats × 104 cycles (`d6-capacity.md` §2) —
  **≤60 MB** for the metadata/latest subset, well inside the 500 MB cap. This is why the
  small-N baseline is viable at all; full profile data does not fit (700×100 ≈ 527 MB, over cap).

## Decision

Tiered, size-gated. Rendering stays format-agnostic (all four arms feed the same Cesium path).

| N | Transport | Rationale |
|---|---|---|
| `N < N_LOCK` | **Supabase PostgREST bbox** (`GET /rest/v1/floats?select=...&geom=cs.{...}`; PostGIS GiST), JSON rows | Metadata subset ≤60 MB fits free DB; server-side bbox; no new dep; smallest diff. |
| `N >= N_LOCK` | **R2 static object** (GeoJSON by default) | Egress-free; no backend hot path; `JSON.parse` needs zero new deps. |
| `N >= N_LOCK` **and** measured `parse_ms` at chosen N **> 50 ms** | **R2 Arrow IPC** | Columnar decode is the binding bottleneck; `tableFromIPC` → typed arrays. |
| `N >= N_LOCK` **and** bbox-from-one-object **without a DB** is required | **R2 FlatGeobuf** | HTTP Range + Hilbert R-tree gives server-filter from a single static object. |

`N_LOCK` is defined by **`marker-format-cutoff-protocol.md` §7**:

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
```

If no condition trips through N = 5,000, lock reads: "Supabase holds through 5,000;
Arrow deferred until render FPS forces R2" (§7). Render ceiling dominates at 5,000 — if
`fps_3s < 30`, fix the render path (PointPrimitiveCollection / GPU layer), not the format.

Free-tier crossovers, both drivers independent:
1. Latency/parse crossover ≈ N 1,000–2,000 (HYPOTHESIS, §5).
2. Supabase egress: 5 GB/mo ÷ (5,000 × ~150 B gzip ≈ 0.75 MB) ≈ **6,700 bbox loads/mo
   (~220/day)**; R2 egress-free removes the cap.

Caveat carried from protocol §1: **Arrow JS has no IPC body-compression** — record-batch
compression not implemented in apache/arrow-js (`apache/arrow-js#109`). Arrow over HTTP is
gzip-only; do not budget IPC-level compression in JS.

## Consequences

- Small-N path reuses Supabase already provisioned; no new service, no new dep, zero
  frontend changes beyond the query.
- Large-N path is a static R2 object: no hot backend, egress-free, but bbox filtering moves
  client-side (GeoJSON/Arrow) unless FlatGeobuf is chosen.
- Two code paths to maintain once `N_LOCK` is crossed; the cutoff is a single constant, so
  the switch is one branch, not a refactor.
- Choosing Arrow adds `apache-arrow` (~100–200 KB) and a binary manifest; choosing
  FlatGeobuf adds `flatgeobuf-geojson.min.js`. GeoJSON avoids both.
- Provisional status: no ingest, fixture, or benchmark exists yet; all numeric claims are
  arithmetic or cited, not measured on our data.

## Alternatives

| Alternative | Why not (now) |
|---|---|
| Supabase everywhere, incl. N ≥ N_LOCK | Egress cap (~6,700 bbox loads/mo) and `d6-capacity.md` §2 fallback (size >400 MB / egress >4 GB/mo) bind before 5,000. |
| R2 GeoJSON everywhere (even N < N_LOCK) | Works and is laziest, but loses server-side bbox and re-ships the full object for a small query; Supabase already provisioned. Revisit if `N_LOCK` never trips. |
| R2 Arrow everywhere | Adds dep + binary toolchain for no measured gain below crossover; JS path gzip-only (`#109`). |
| R2 FlatGeobuf everywhere | Heaviest toolchain (ogr2ogr build step); only justified when bbox-from-one-static-object w/o DB is a hard requirement. |
| JSONB one row per profile | Worse than normalized: ~3–5 KB/row + TOAST (`d6-capacity.md` §2). |
| SQLite-wasm + full download | Ranked 2nd in `d6-capacity.md` §2 alt ranking; full-download cost, client index. |

## Evidence table

| Claim | Value | Basis | Status |
|---|---|---|---|
| Indian subset | 2,421 floats / 354,696 profiles, 30–120 E / 30 S–30 N | `docs/data/argo.md` (live index parse 2026-09-10) | VERIFIED |
| Supabase free | 500 MB DB, 5 GB egress, 7-day pause | `https://supabase.com/docs/guides/platform/database-size` (2026-09-10) | VERIFIED |
| Metadata fit | ≤60 MB (800×104 metadata ~7 MB) | `d6-capacity.md` §2 | VERIFIED (arithmetic) |
| R2 free | 10 GB, 1M A, 10M B, egress free | `https://developers.cloudflare.com/r2/pricing/` (2026-09-10) | VERIFIED |
| `N_LOCK` definition | min N tripping (a)(b)(c) | `marker-format-cutoff-protocol.md` §7 | LOCKED RULE |
| Supabase egress crossover | ~6,700 bbox loads/mo (~220/day) | protocol §5 | HYPOTHESIS |
| Arrow JS no IPC compression | record-batch compression not implemented | `https://github.com/apache/arrow-js/issues/109` (2026-09-10) | VERIFIED |
| Arrow size @5k | ~90–130 KB uncompressed (6 cols ≈19 B/row) | protocol §1 | UNVERIFIED (arithmetic) |
| GeoJSON size @5k | ~450–750 KB raw / ~150–250 KB gzip | protocol §1 | UNVERIFIED (arithmetic) |
| FlatGeobuf size @5k | ~150–250 KB; index ~40 B/node | `https://flatgeobuf.org/`, `https://brycemecum.com/2022/04/04/flatgeobuf/` (2026-09-10) | VERIFIED (external) |
| Supabase baseline size @5k | ~750 KB raw / row ~150 B | protocol §1 | UNVERIFIED (arithmetic) |
| Parse crossover | N 1,000–2,000 | protocol §5 | HYPOTHESIS |
| MDPI 10k-feat guidance | fastest libs ≤10,000 feat; 50,000+ >1 s all | `https://doi.org/10.3390/ijgi14090336` | 403 bot-block; metadata via Exa — PARTIAL |
| Render ceiling @5k | billboards vs 33 ms frame budget | protocol §5 | HYPOTHESIS |
| Gateway | `$NINEROUTER_KEY` length 0 → gateway unavailable this run | local length check (never printed) | VERIFIED |

## References

Access date 2026-09-10 per URL. Gateway unavailable this run (`$NINEROUTER_KEY` length
checked only, never printed); all fetches direct curl/urllib.

| URL | HTTP | Used for |
|---|---|---|
| `docs/performance/marker-format-cutoff-protocol.md` | local | §7 `N_LOCK` rule, §1 format table, §5 crossover, §6 template |
| `docs/research/d6-capacity.md` §2 | local | Supabase fit, metadata ~7 MB / ≤60 MB, JSONB penalty, egress trigger |
| `docs/data/argo.md` | local | subset 2,421 floats / 354,696 profiles, bbox, CC-BY 4.0 |
| `https://github.com/apache/arrow-js/issues/109` | 200 | Arrow JS no IPC compression |
| `https://flatgeobuf.org/` | 200 | FGB vs Shapefile/GeoJSON perf + size |
| `https://github.com/flatgeobuf/flatgeobuf` | 200 | same table |
| `https://brycemecum.com/2022/04/04/flatgeobuf/` | 200 | 1M pts, index ~40 B/node |
| `https://developers.cloudflare.com/r2/pricing/` | 200 | R2 free tier |
| `https://developers.cloudflare.com/r2/platform/limits/` | 200 | R2 limits |
| `https://supabase.com/docs/guides/platform/database-size` | 200 | quota counts data+indexes |
| `https://supabase.com/docs/guides/platform/free-project-pausing` | UNVERIFIED (not re-fetched) | 7-day pause trigger |
| `https://github.com/maplibre/maplibre-gl-js/issues/106` | 200 | JSON parse main-thread block |
| `https://www.spatialworkflow.io/geojson-too-big-for-browser/` | 200 | 59,391 feat = 2.65 MB gzip |
| `https://github.com/uwdata/flechette` | 200 | vs Arrow JS ref impl |
| `https://arrow.apache.org/js/main/functions/Arrow.dom.tableFromIPC.html` | 200 | API |
| `https://doi.org/10.3390/ijgi14090336` | 403 | MDPI bot-block; metadata via Exa — UNVERIFIED |
| `https://www.npmjs.com/package/arrow-to-json` | 403 | npm bot-block; 20x claim UNVERIFIED |
