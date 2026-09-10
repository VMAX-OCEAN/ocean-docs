# D2 — Chunk-Transfer Benchmark Protocol (GLORYS Zarr, free tier)

Date: 2026-09-10. Status: runnable protocol + harness — **no results**. Every result cell blank on purpose.
Companion to `benchmark-protocol.md` (render/FPS/markers). This doc owns data-layer numbers: chunk bytes, browser network bytes, GET count, wall ms, R2 Class A/B.
Methodology frame: Nguyen, Chazaro Cortes, Dunn, Shiklomanov (2023), *Impact of Chunk Size on Read Performance of Zarr Data in Cloud-based Object Stores*, doi:10.1002/essoar.10511054.2.

Claims under test (from `docs/research/d6-capacity.md` §3–4, `netcdf-to-zarr.md`, `optimization.md` §1): slice repeat p95 ≤ 750 ms; cold load ≤ 10 s; dual-rep `(30,50,108,216)` beats balanced `(1,10,540,1080)` for time-series point queries without losing the slice gate. All UNVERIFIED until a locked-laptop run exists.

## 0. Credentials, gateway guard, free-tier facts

Copernicus creds read from env by the Toolbox: `COPERNICUSMARINE_SERVICE_USERNAME`, `COPERNICUSMARINE_SERVICE_PASSWORD`. Never echo.

```bash
# length-only check, never print the value
if [ -n "$NINEROUTER_KEY" ]; then echo "gateway: present (len=${#NINEROUTER_KEY})"; else echo "gateway: absent — direct fetch only"; fi
```

R2 free (verified 2026-09-10, `https://developers.cloudflare.com/r2/pricing/` page updated 2026-08-07): 10 GB-month Standard; Class A 1,000,000 req/mo (mutate: PutObject, CopyObject, ListObjects, CreateMultipartUpload, UploadPart); Class B 10,000,000 req/mo (read: GetObject, HeadObject, HeadBucket, GetBucketLocation); DeleteObject free; egress free; free tier Standard only.

## 1. Environment record (fill verbatim every session)

| Field | Value |
|---|---|
| Date/time (local ISO) | |
| Machine model / OS + kernel | |
| CPU model + cores | |
| RAM (GB) | |
| GPU + driver | |
| Browser + exact version | |
| `navigator.hardwareConcurrency` | |
| `navigator.deviceMemory` | |
| `gl.getParameter(UNMASKED_RENDERER_WEBGL)` | |
| `devicePixelRatio` | |
| Network: interface + `effectiveType`/`downlink`/`rtt` | |
| Power: plugged in | |
| App/harness commit hash | |
| Toolbox `copernicusmarine --version` | |
| Python / xarray / zarr / numcodecs versions | |
| Subset window (start–end, bbox, depth, var) | |
| Subset NetCDF sha256 + bytes | |
| R2 endpoint / bucket / store prefix | |

Reference laptop locks after first full session (see `reference-laptop.md`); later benchmarks cite this table.

## 2. Step 1 — build the subset

```bash
python3 -m venv .venv-bench && . .venv-bench/bin/activate
pip install "copernicusmarine==2.4.1" "xarray" "zarr>=3.3" "numcodecs" "netcdf4" "dask"
export COPERNICUSMARINE_SERVICE_USERNAME='...'
export COPERNICUSMARINE_SERVICE_PASSWORD='...'   # never echo

copernicusmarine describe --contains "cmems_mod_glo_phy_my_0.083deg_P1D-m" --include-versions
mkdir -p data/raw data/zarr
copernicusmarine subset \
  --dataset-id cmems_mod_glo_phy_my_0.083deg_P1D-m \
  --variable thetao \
  --minimum-longitude 60 --maximum-longitude 100 \
  --minimum-latitude -5  --maximum-latitude 30 \
  --minimum-depth 0     --maximum-depth 6000 \
  --start-datetime 2026-05-01T00:00:00 --end-datetime 2026-05-30T00:00:00 \
  --file-format netcdf \
  --output-directory data/raw --output-filename glorys_io_thetao.nc --overwrite
sha256sum data/raw/glorys_io_thetao.nc | tee data/raw/glorys_io_thetao.sha256
```

Option names verified from source (`command_line_interface/group_subset.py` v2.4.1, `core_functions/models.py:13`: `--file-format` ∈ {netcdf,zarr,csv,parquet}). Depth 6000 covers GLORYS 50 levels (centers ~0.49–5727 m). Expected dims time=30 depth=50 lat=480 lon=420. Raw float32 = 30·50·480·420·4 = 1,209,600,000 B (1.2096 GB) — deterministic, not measured. Record actual download bytes as `data_transfer_size`.

## 3. Step 2 — build BOTH chunkings + on-disk chunk bytes

Write Zarr **v2** (`.zmetadata`) so zarrita.js opens via the verified v2 consolidated path. zarr-python 3 writes v3 by default — force `zarr_format=2`.

```python
#!/usr/bin/env python3
# scripts/build_chunkings.py
import json, statistics, hashlib
from pathlib import Path
import xarray as xr
from zarr.codecs.numcodecs import Blosc   # zarr 3.3

NC  = Path("data/raw/glorys_io_thetao.nc")
OUT = Path("data/zarr"); OUT.mkdir(parents=True, exist_ok=True)
COMP = Blosc(cname="zstd", clevel=3, shuffle=2)   # bitshuffle

BALANCED = (1, 10, 540, 1080)
TIMESER  = (30, 50, 108, 216)

ds = xr.open_dataset(NC)
depth_dim = "depth" if "depth" in ds.dims else ("elevation" if "elevation" in ds.dims else None)
assert depth_dim, f"no depth dim: {list(ds.dims)}"
assert ds["thetao"].dims == ("time", depth_dim, "latitude", "longitude"), ds["thetao"].dims

def build(name, chunks):
    enc = {"thetao": {"chunks": chunks, "compressor": COMP, "dtype": "float32"}}
    p = OUT / f"glorys-io-{name}.zarr"
    ds.to_zarr(p, mode="w", encoding=enc, zarr_format=2, consolidated=True, safe_chunks=True)
    return p

def chunk_stats(p):
    files = [f for f in p.rglob("*") if f.is_file()
             and f.name not in (".zmetadata", ".zarray", ".zattrs", ".zgroup", "zarr.json")]
    sizes = sorted(f.stat().st_size for f in files); n = len(sizes)
    return {"store": str(p), "n_chunk_files": n,
            "bytes_min": sizes[0] if n else 0,
            "bytes_median": int(statistics.median(sizes)) if n else 0,
            "bytes_mean": int(sum(sizes)/n) if n else 0,
            "bytes_max": sizes[-1] if n else 0, "bytes_total": sum(sizes)}

report = {}
for name, ch in (("balanced", BALANCED), ("timeseries", TIMESER)):
    p = build(name, ch); st = chunk_stats(p)
    st["declared_chunks"] = list(ch); st["array_shape"] = list(ds["thetao"].shape)
    st["effective_chunk"] = [min(c, s) for c, s in zip(ch, ds["thetao"].shape)]
    report[name] = st; print(json.dumps(st, indent=2))
Path("data/zarr/chunk-report.json").write_text(json.dumps(report, indent=2))
print("sha256(raw netcdf)", hashlib.sha256(NC.read_bytes()).hexdigest())
```

Effective balanced chunk on this subset = `(1,10,480,420)`; effective time chunk = `(30,50,108,216)`. Record both.

## 4. Step 3 — upload both stores to R2

```bash
npx wrangler r2 bucket create glorys-bench
export R2_ACCOUNT_ID='<accountid>'
aws s3 sync data/zarr/glorys-io-balanced.zarr   "s3://glorys-bench/glorys-io-balanced.zarr/" \
  --endpoint-url "https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com" --delete
aws s3 sync data/zarr/glorys-io-timeseries.zarr "s3://glorys-bench/glorys-io-timeseries.zarr/" \
  --endpoint-url "https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com" --delete
```

Cache headers are set at HTTP layer, not S3 sync — use custom domain + Cache Rule or Worker. Custom domain preferred (Cache, WAF, no r2.dev rate limit; `developers.cloudflare.com/r2/buckets/public-buckets/`). CORS (`.../r2/buckets/cors/`) must include harness origin:

```json
[
  {
    "AllowedOrigins": ["http://localhost:8000"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["*"],
    "ExposeHeaders": ["ETag", "Content-Length"],
    "MaxAgeSeconds": 3600
  }
]
```

CORS headers appear only when request carries `Origin`; `curl` without `Origin` shows none.

```bash
STORE=https://<your-domain>/glorys-io-balanced.zarr
curl -sI -H 'Origin: http://localhost:8000' "$STORE/.zmetadata" | grep -iE 'HTTP/|access-control|content-length|cache-control'
curl -sI -H 'Origin: http://localhost:8000' "$STORE/thetao/0.0.0.0" | grep -iE 'HTTP/|access-control|content-length'
```

## 5. Measurement harness

### 5a. Local validator — `scripts/local_query_bench.py`

```python
#!/usr/bin/env python3
import time, json
from pathlib import Path
import xarray as xr, numpy as np

STORES = {"balanced": "data/zarr/glorys-io-balanced.zarr",
          "timeseries": "data/zarr/glorys-io-timeseries.zarr"}

def run(store, kind, t=15, d=25, i=240, j=210):
    ds = xr.open_zarr(store, consolidated=True)
    depth = "depth" if "depth" in ds.dims else "elevation"
    da = ds["thetao"]
    sel = (da.isel(time=slice(t, t+1), **{depth: slice(d, d+1)}) if kind == "slice"
           else da.isel(**{depth: slice(d, d+1)}, latitude=slice(i, i+1), longitude=slice(j, j+1)))
    t0 = time.perf_counter(); arr = sel.load().values
    return {"store": store, "kind": kind, "wall_ms": (time.perf_counter()-t0)*1000,
            "decoded_bytes": int(arr.size * arr.dtype.itemsize),
            "chunksizes": {k: list(v) for k, v in sel.chunksizes.items()}}

out = []
for s in STORES:
    for k in ("slice", "point"):
        r = run(STORES[s], k); out.append(r); print(json.dumps(r))
Path("data/zarr/local-query-report.json").write_text(json.dumps(out, indent=2))
```

Run 20×, report p50/p95/max. Local reads hit page cache after run 1 — informational, not the free-tier gate.

### 5b. Browser harness — `bench/chunk-bench.html` (single file)

```html
<!doctype html><meta charset="utf-8"><title>chunk-bench</title>
<pre id="out"></pre>
<script type="module">
import * as zarr from "https://esm.sh/zarrita@0.7.5";
const OUT = document.getElementById("out"); const log = [];
let storeURL = new URLSearchParams(location.search).get("store");

function wrapFetch(cold) {
  return async (input, init) => {
    const url = typeof input === "string" ? input : input.url;
    const t0 = performance.now();
    const res = await fetch(input, cold ? { ...(init || {}), cache: "no-store" } : init);
    const buf = await res.clone().arrayBuffer();
    log.push({ url, status: res.status, bytes: buf.byteLength, ms: performance.now() - t0 });
    return res;
  };
}
function summarize() {
  return { gets: log.length, bytes: log.reduce((a, r) => a + r.bytes, 0) };
}
window.__CHUNKBENCH = {
  async open(cold) {
    let store = new zarr.FetchStore(storeURL, { fetch: wrapFetch(cold) });
    store = await zarr.withConsolidatedMetadata(store);
    window.__ARR = await zarr.open(store, { kind: "array" });
    return window.__ARR;
  },
  async query(kind, { t = 15, d = 25, i = 240, j = 210 } = {}) {
    const arr = window.__ARR;
    const sel = kind === "slice"
      ? [zarr.slice(t, t + 1), zarr.slice(d, d + 1), null, null]
      : [null, zarr.slice(d, d + 1), zarr.slice(i, i + 1), zarr.slice(j, j + 1)];
    log.length = 0;
    const t0 = performance.now();
    const res = await zarr.get(arr, sel);
    return { kind, wall_ms: performance.now() - t0,
             decoded_bytes: res.data.length * res.data.BYTES_PER_ELEMENT, ...summarize() };
  },
  info() {
    const gl = document.createElement("canvas").getContext("webgl");
    const ext = gl && gl.getExtension("WEBGL_debug_renderer_info");
    const c = navigator.connection || {};
    return { ua: navigator.userAgent, cores: navigator.hardwareConcurrency,
             deviceMemory: navigator.deviceMemory, dpr: devicePixelRatio,
             gpu: ext ? gl.getParameter(ext.UNMASKED_RENDERER_WEBGL) : null,
             effectiveType: c.effectiveType, downlink: c.downlink, rtt: c.rtt };
  }
};
OUT.textContent = "harness ready. run __CHUNKBENCH.info()";
</script>
```

```bash
cd bench && python3 -m http.server 8000
# http://localhost:8000/chunk-bench.html?store=https://<domain>/glorys-io-balanced.zarr
```

```js
const arr = await __CHUNKBENCH.open(false);
const warm = [];
for (let k = 0; k < 20; k++) warm.push(await __CHUNKBENCH.query("slice"));
copy(JSON.stringify({ env: __CHUNKBENCH.info(), warm }, null, 2));
```

Cold = fresh profile (`--user-data-dir`) + `open(true)` (cache: no-store), single query. Only valid cold number.

### 5c. R2 dashboard Class A/B

Dashboard → R2 → `glorys-bench` → Metrics → Operations. Record baseline before/after; delta = after − before. Class B delta should equal (harness `gets` + 1 metadata HEAD) per cold open; Class A ≈ 0 for reads. Aggregates hourly with lag — if stale use R2 GraphQL `r2OperationsAdaptiveGroups` or note "dashboard pending". Never substitute an estimate.

## 6. Protocol A — slice query

Selection: `thetao[time=15, depth=25, lat all, lon all]`.

| Run id | Store | Cache | Network | i | Release (ms) | Done (ms) | wall_ms | GETs | bytes | decoded bytes |
|---|---|---|---|---|---|---|---|---|---|---|
| A-warm-bal-01 | balanced | warm | none | 1 | | | | | | |
| … | balanced | warm | none | 20 | | | | | | |
| A-warm-ts-01 | timeseries | warm | none | 1 | | | | | | |
| … | timeseries | warm | none | 20 | | | | | | |
| A-cold-bal-01 | balanced | cold | none | 1 | | | | | | |
| A-cold-ts-01 | timeseries | cold | none | 1 | | | | | | |
| A-cold3g-bal-01 | balanced | cold | Fast 3G | 1 | | | | | | |
| A-cold3g-ts-01 | timeseries | cold | Fast 3G | 1 | | | | | | |
| A-repeat-bal | balanced | warm (2nd identical) | none | 1 | | | | | | |

| Store | wall p50 | wall p95 | wall max | GETs med | bytes med | Pass G1 (warm p95 ≤ 750 ms) |
|---|---|---|---|---|---|---|
| balanced | | | | | | |
| timeseries | | | | | | |

Cold (single): wall, GETs, bytes, first-chunk HTTP status; Gate G2 ≤ 10 s.

## 7. Protocol B — time-series point query

Selection: `thetao[time all, depth=25, lat=240, lon=210]`.

| Run id | Store | Cache | i | wall_ms | GETs | bytes | decoded bytes | heap delta |
|---|---|---|---|---|---|---|---|---|
| B-warm-bal-01 | balanced | warm | 1 | | | | | |
| … | balanced | warm | 20 | | | | | |
| B-warm-ts-01 | timeseries | warm | 1 | | | | | |
| … | timeseries | warm | 20 | | | | | |
| B-cold-bal-01 | balanced | cold | 1 | | | | | |
| B-cold-ts-01 | timeseries | cold | 1 | | | | | |

| Store | wall p50 | wall p95 | GETs med | bytes med | decoded bytes med |
|---|---|---|---|---|---|
| balanced | | | | | |
| timeseries | | | | | |

Expected shape (hypothesis, DOI): balanced ~30 GETs (one per time step); time-store ~1 GET but decodes whole effective chunk. Pass/fail comparative in §9 — no invented absolute ms.

## 8. Metric definitions (exact)

| Metric | Definition | Instrument |
|---|---|---|
| `wall_ms` | `performance.now()` delta around `await zarr.get(...)`, fetch+decode | harness |
| `gets` | HTTP requests issued during query window | fetch wrapper |
| `bytes` | Σ `arrayBuffer.byteLength` received (post content-encoding, exact on-wire) | fetch wrapper |
| `taobytes` | Σ `PerformanceResourceTiming.transferSize` for store host; **0 when Timing-Allow-Origin absent** → Network panel is only byte source | Resource Timing |
| `decoded_bytes` | `data.length * BYTES_PER_ELEMENT` from zarrita | harness |
| `heap_delta` | `performance.memory.usedJSHeapSize` delta (Chromium only) | harness |
| `chunk_bytes_{min,median,mean,max}` | on-disk chunk file sizes per store | `chunk_stats()` |
| `effective_chunk` | `min(declared_chunk, array_shape)` per dim | build script |
| `p95` | 95th percentile n=20, nearest-rank | arithmetic |
| `cold` | fresh profile + `cache:"no-store"` | harness |
| `warm` | same profile, cache enabled, query run once | harness |
| `repeat` | identical query 2nd time, warm, expect 0 new GETs | harness |
| `ClassB_delta` | R2 dashboard GetObject/HeadObject after − before | dashboard |

All wall-clock `performance.now()`. `vite preview`/`http.server`, not dev servers. Cache state recorded on every row.

## 9. Pass/fail rules

| Gate | Threshold | Source |
|---|---|---|
| G1 slice warm repeat p95 | ≤ 750 ms, unthrottled | d6 §4 |
| G2 cold first query | ≤ 10,000 ms, fresh profile | d6 §4 |
| G3 cold Fast-3G | informational only | `benchmark-protocol.md` §2.2 |
| G4 repeat view | 2nd identical warm query = 0 new store GETs / Class B | d6 §3 step 4 |
| G5 time-series GETs | timeseries GETs < balanced GETs | DOI tradeoff |
| G6 time-series wall | timeseries p95 < balanced p95 | DOI tradeoff |
| G7 slice wall | balanced p95 ≤ timeseries p95 | DOI tradeoff |
| G8 chunk bytes | balanced chunk within 100 KB–2 MB (record, no hard gate) | `optimization.md` §1 |
| G9 free tier | Class A ≤ 1M AND Class B ≤ 10M AND storage ≤ 10 GB Standard | R2 pricing 2026-09-10 |

Decision:
- **Dual-rep adopted** iff G1 ∧ G2 ∧ G5 ∧ G6 ∧ G7 ∧ G9.
- **Balanced-only** iff G1 ∧ G2 ∧ G9 but ¬(G5 ∧ G6 ∧ G7). Simpler store wins ties.
- **Fail G1/G2** → diagnose: chunk > 2 MB (G8), missing `Cache-Control`, no HTTP/2 multiplex, cold missing cache/Range; then reduce chunk, add `max-age=86400`, verify custom domain.
- **Fail G9** → drop dual or pyramid; re-measure.
- UNVERIFIED ⇒ not a pass. Blank cell ⇒ gate open. Never backfill from `runtime-latency.md`.

## 10. Result record (one block per full session)

```
Session id:
Date:
Env table filled? yes/no
Harness versions (toolbox/python/zarr/xarray/zarrita):
Subset: window / bbox / var / sha256 / bytes
Table A — chunk bytes: balanced & timeseries: declared/effective/n/min/median/mean/max/total
Table A — compression ratio (raw/compressed) per store:
Protocol A slice — warm p95 / cold / warm GETs / warm bytes / G1 / G2:
Protocol B point — warm p95 / cold / GETs / bytes / G5/G6/G7:
G4 repeat-view new GETs:
R2 Class B delta / Class A delta / dashboard timestamp:
Verdict: dual-rep | balanced-only | fail
Open anomalies / retries:
Artifacts: chunk-report.json / local-query-report.json / HAR (scrubbed)
```

Scrub `Authorization`, `Cookie`, credential headers before saving HAR.

## 11. Exact command list

```bash
[ -n "$NINEROUTER_KEY" ] && echo "gateway present (len=${#NINEROUTER_KEY})" || echo "gateway absent"
python3 -m venv .venv-bench && . .venv-bench/bin/activate
pip install "copernicusmarine==2.4.1" xarray "zarr>=3.3" numcodecs netcdf4 dask
copernicusmarine subset --dataset-id cmems_mod_glo_phy_my_0.083deg_P1D-m \
  --variable thetao --minimum-longitude 60 --maximum-longitude 100 \
  --minimum-latitude -5 --maximum-latitude 30 --minimum-depth 0 --maximum-depth 6000 \
  --start-datetime 2026-05-01T00:00:00 --end-datetime 2026-05-30T00:00:00 \
  --file-format netcdf --output-directory data/raw --output-filename glorys_io_thetao.nc --overwrite
sha256sum data/raw/glorys_io_thetao.nc
python3 scripts/build_chunkings.py
python3 scripts/local_query_bench.py
npx wrangler r2 bucket create glorys-bench
aws s3 sync data/zarr/glorys-io-balanced.zarr   s3://glorys-bench/glorys-io-balanced.zarr/   --endpoint-url "https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com" --delete
aws s3 sync data/zarr/glorys-io-timeseries.zarr s3://glorys-bench/glorys-io-timeseries.zarr/ --endpoint-url "https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com" --delete
curl -sI -H 'Origin: http://localhost:8000' "https://<domain>/glorys-io-balanced.zarr/.zmetadata"
cd bench && python3 -m http.server 8000
# run §6/§7 console snippets, 20× warm + fresh-profile cold; then R2 dashboard delta
```

## 12. Verification notes

Verified 2026-09-10: `copernicusmarine` latest 2.4.1 (PyPI, 2026-05-11), option names from `group_subset.py`, `FileFormat` from `core_functions/models.py:13`, creds env names from `core_functions/credentials_utils.py`; `zarr` 3.3.0 `Blosc`/`BloscShuffle`; xarray `to_zarr` `consolidated`/`zarr_format`/`safe_chunks`; `zarrita` 0.7.5 `FetchStore` custom fetch + `withConsolidatedMetadata` v2 `.zmetadata` default (use Zarr v2 for browser; v3 untested with zarr-cesium); R2 free tier numbers + op classification.

Deterministic arithmetic (not measured): subset raw = 1.2096 GB; effective balanced chunk `(1,10,480,420)` = 8.064 MB raw (0.806 MB @10:1, 2.688 MB @3:1); effective time chunk `(30,50,108,216)` = 139.968 MB raw (13.997 MB @10:1). Expectations only; tables blank until measured.

UNVERIFIED: R2 `Timing-Allow-Origin` on public/custom-domain responses (fallback Network panel); dashboard metric lag; balanced `.zmetadata` + chunk GETs under HTTP/2 without Range stalls; actual cold ≤10 s and slice ≤750 ms on locked laptop. `glorys12.md` ingest v0 sha NONE — §2 subset hash becomes first real hash for that card.

Gateway not used this run: `$NINEROUTER_KEY` absent (length 0, never printed). All fetches direct curl/exa. Re-verify via gateway before D2 sign-off if policy requires. Skipped: Playwright runner, pyramid, isosurface/marker rows (owned by `benchmark-protocol.md`).
