# D2 — Render-Latency + Marker Benchmark Protocol

Date: 2026-09-10. Status: **runnable protocol + harness — no results**. Every
result cell below is blank on purpose. Do not fill from estimates; the numbers
in `runtime-latency.md` are architecture expectations, not measurements.
Doc references: `d6-capacity.md` §3 step 3, §4 (open: slice ≤750 ms, cold
≤10 s, 30 FPS + 5000 markers, terrain bytes + ion quota 20-reload, offline);
`d4-lib-pins.md` §9 (terrain bytes/load, quota headroom, airplane-mode reload).

Free-only: DevTools (Chrome/Edge/Firefox), `performance` API,
PerformanceResourceTiming, `npx vite preview`. No paid tooling, no new deps.
Optionally Playwright (free, MIT) for the automated runner. A gateway lookup is
only ever authorized by checking `$NINEROUTER_KEY` has non-zero length — never
print the key, never paste it into the harness or a recorded artifact.

Harness: `ocean-web/scripts/bench-harness.js`.

---

## 0. What does NOT exist yet (must be built before (a) can pass)

The current app is globe-only. Confirmed by reading source:

- No slice/scrub UI, no `updateSlices`, no Zarr provider mounted.
  `CesiumViewer.tsx` → `createOptimizedViewer` → `addCloudLayer` only.
- No markers — no entity/PointPrimitive code anywhere in `src/`.
- `window.__VIEWER__` is not exposed. Harness can't attach until patched.
- Viewer is created with `terrain: undefined`, then
  `Cesium.Terrain.fromWorldTerrain({ requestVertexNormals: true })` attached
  async (`config.ts:131-149`). Rotating SSE 4 → 2 after `readyEvent` + 1500 ms.
  Base imagery is NASA GIBS `BlueMarble_NextGeneration` via a custom GIBS
  tiling scheme (`base-imagery.ts`), **not** Bing. This is the first layer for
  (b) and (d).

So (a) and (c) are BLOCKED on instrumentation + the slice/marker features. This
protocol defines the exact hooks so results are apples-to-apples once built.

### Instrumentation patch (smallest required)

1. `CesiumViewer.tsx`, in the `onReady` path (after `viewerRef.current = viewer`):
   `window.__VIEWER__ = viewer;`
   `ponytail:` dev-only exposure; gate behind `import.meta.env.DEV || __BENCH__`
   when a prod build must not leak the viewer.
2. Slice/scrub control: call `window.__BENCH.markScrubRelease()` in the
   pointerup / `onChange`-release handler (the moment the user lets go).
3. Data-layer `ImageryProvider.requestImage(x,y,level).then(img => ...)`:
   call `window.__BENCH.markSliceTileRendered()` **after decode**, in the same
   `.then` that returns the ready image to Cesium. This is "first rendered
   tile" without depending on `postRender` internals.
4. Cold load: `__BENCH.attach()` fires `globeReady` on first `postRender`;
   call `__BENCH.waitTilesIdle()` once after the first data layer is added to
   stamp `tilesSettled`.

If (a)/(c) ship later, only steps 2–3 are new; harness already supports them.

---

## 1. Environment (record verbatim, every run)

| Field | Value |
|---|---|
| Date/time (local, ISO) | |
| Machine / OS | |
| CPU model + cores (`navigator.hardwareConcurrency`) | |
| GPU / renderer (chrome://gpu or `gl.getParameter(UNMASKED_RENDERER_WEBGL)`) | |
| RAM (`navigator.deviceMemory`) | |
| Browser + exact version | |
| Profile | clean (new) / existing |
| Display scale (`devicePixelRatio`) | |
| Network (Ethernet / Wi-Fi band) | |
| App commit / build hash | |
| `cesium` exact version from lockfile | |
| `zarr-cesium` version (if slice path active) | |
| Dev mode: `vite preview` (must be preview, not dev) | |
| Extensions | none |
| Power: plugged in | |

**Reason `vite preview` not `vite dev`:** dev serves unbundled ESM + HMR client;
cold-load numbers from dev are meaningless. Build once: `npm run build &&
npx vite preview --port 4173`.

---

## 2. DevTools setup — exact steps

Run each protocol block 3× (report median of the 3); for jitter-sensitive
numbers also keep min/max.

### 2.1 Clean-cache / cold-cache start

1. DevTools open **before** navigating (else you miss early entries).
2. `F12` → Console. Check **"Preserve log"**.
3. Cold cache — pick one, state which:
   - **C1 Hard reload:** DevTools → Network → check **"Disable cache"**, then
     `Ctrl+Shift+R`. Does NOT clear the on-disk HTTP cache, only bypasses it
     for this reload. Use for "cold-ish".
   - **C2 True clean profile:** close all windows → relaunch with a fresh
     `--user-data-dir` (`chrome --user-data-dir=/tmp/bench-<runid>`), or
     Firefox `about:profiles` → new profile. This is the real cold load. Use
     for (b) and (d) cold.
4. Warm cache = C1 reload #2 with "Disable cache" **unchecked** (repeat visit,
   same profile, no clearing between).

### 2.2 Network throttling

Network panel → **"No throttling"** dropdown:

- (a) warm slice, (b) unthrottled baseline, (c) FPS: **No throttling**.
- (a) cold slice + (b) cold load: **Fast 3G** preset (1.6 Mbps down / 750 Kbps
  up / 562.5 ms RTT in Chrome; record exact preset values). Run both unthrottled
  and Fast-3G; label rows.
- Do not use "Slow 3G" for pass/fail — informational only.

### 2.3 Network panel filters (record GETs + bytes)

Network panel filter box, one at a time:

| Purpose | Filter string |
|---|---|
| ion terrain (+ any ion) | `assets.ion.cesium.com` |
| GIBS imagery | `gibs.earthdata.nasa.gov` |
| Zarr chunks | `r2.dev` or your R2 custom domain |
| Cloud texture | `clouds.matteason.co.uk` |
| All fetch/XHR only | type filter `Fetch/XHR` |
| All images only | type filter `Img` |

For each filtered run record: **# requests, transfer size, transferred vs
resource size** (bottom status bar), and check **"Disable cache"** state.
Sort by **Time** descending to isolate the tail; sort by **Size** to find the
biggest tile.

Hover any row → **Timing** tab: note Queueing/Stalled and Content Download.
Cross-origin rows show `(from disk cache)` / `(from ServiceWorker)` — record,
and confirm repeat-view = `304` or disk-cache (d6 §3 step 4: repeat same slice
must show 0 new Class-B / disk cache hit).

`performance.getEntriesByType('resource')` in the harness mirrors this panel
and is the machine-readable copy — dump `__BENCH.report()` at the end. If a
host lacks `Timing-Allow-Origin`, `transferSize` is 0 → harness flags
`taoMissing: true`; in that case the Network panel's own size column is the
only byte source (record it by hand).

### 2.4 Performance panel (frame timing cross-check)

Performance panel → Record (`Ctrl+E`) for the FPS window → Frames track. Read
**FPS** and **dropped frames**. This is the independent cross-check for the
harness rAF numbers. Also enable **Rendering → Frame Rendering Stats** in the
Rendering drawer for a live on-canvas FPS/GPU readout (free, built-in).

### 2.5 Device profiler (Android, free option)

Android Chrome via `chrome://inspect` over USB, or DevTools → **Performance
Monitor** → CPU/GPU/JS heap. For the ≤5000-marker phone claim: record device
model + Chrome version + whether `rendererString` is the phone GPU (not
SwiftShader), else the row is INVALID.

---

## 3. Metric definitions (exact)

| Metric | Definition | Instrumentation |
|---|---|---|
| `sliceLatency` | `markSliceTileRendered − markScrubRelease` (ms). First slice tile decoded+handed to Cesium after release. | `__BENCH.sliceLatencyMs()` |
| `sliceLatency (p95)` | 95th percentile over N=20 scrubs | sort samples |
| `coldLoad.globeReady` | `firstScene.postRender.startTime − navigationStart` (ms). Globe canvas painting. | attach auto-mark |
| `coldLoad.tilesSettled` | `tileLoadProgressEvent` first hits 0 after having been >0, minus `navigationStart` (ms). | `__BENCH.waitTilesIdle()` |
| `frame.fps` | `1000 / mean(rAF intervals)` over 10 s steady window, camera static then during a fixed pan | `__BENCH.startFrames(10000)` / `stopFrames()` |
| `frame.p95Ms` | 95th percentile rAF interval; must be ≤ 33.3 ms for 30 FPS headroom | `stopFrames()` |
| `frame.pctOver33` | % of frames with interval > 33.3 ms; target ≤ 5% | `stopFrames()` |
| `markers.atTarget` | marker count at which fps ≥ 30 fails for the first time | sweep |
| `terrain.transferBytes` | sum `transferSize` host `assets.ion.cesium.com` for one cold load | `__BENCH.terrainBytes()` |
| `layer.firstBytes` | sum `transferSize` for first imagery layer (GIBS) one cold load | `__BENCH.gibsBytes()` |
| `quota.20reloadBytes` | 20 × per-reload streamed bytes (ion); compare to 15 GB/mo streaming budget | 20 reload loop |
| `quota.headroom` | `budget − 20reloadBytes` (bytes and % of budget) | arithmetic |
| `offline.behavior` | pass = ellipsoid/basemap renders + no unhandled throw; fail = blank canvas / uncaught error | airplane-mode reload |

All wall-clock uses `performance.now()` (monotonic, sub-ms). `navigationStart`
from `performance.getEntriesByType('navigation')[0]`.

`ponytail:` rAF intervals measure presented frames only on a compositor-driven
page; Cesium requests renders on demand (`requestRender`), so for a *static*
camera rAF may throttle. FPS rows must therefore be taken DURING a continuous
camera pan/rotate, or with `viewer.scene.requestRenderMode = false`. State
which was used. Upgrade path: `scene.postRender` deltas if rAF proves noisy.

---

## 4. Protocol (a) — slice load ≤ 750 ms

**Claim under test (d6 §4):** scrub-release → first rendered tiles ≤ 750 ms.

1. Load app (W1 warm: same profile, slice fetched once already). Settle globe.
2. Paste harness. Confirm `__BENCH.selftest()` PASS (checks the stats path).
3. Ensure first layer is loaded. Set camera to a fixed view; record it.
4. For i in 1..20:
   a. `__BENCH.markScrubRelease()` is auto-fired by the scrub control on release.
   b. Move scrubber to a **new** depth/time, release.
   c. Provider `.then` fires `markSliceTileRendered`.
   d. Read `__BENCH.sliceLatencyMs()`; append to table.
5. Repeat step 4 as **W2 warm** (same scrub positions, second visit → cache hit)
   and **C cold** (Disable cache / new profile → first fetch of those chunks,
   Fast-3G once + unthrottled once).
6. Take p50/p95/max.

Required artifact: Network filter `r2.dev` (or domain) filtered to one scrub —
record # chunks, bytes, whether any Range/206, cache headers seen.

### Table (a) — slice latency

| Run | Cache | Network | i | Release mark (ms) | Tile mark (ms) | sliceLatency (ms) |
|---|---|---|---|---|---|---|
| a-01 | warm | none | 1 | | | |
| a-02 | warm | none | 2 | | | |
| … | warm | none | 20 | | | |
| a-cold-01 | cold | none | 1 | | | |
| a-cold-02 | cold | Fast 3G | 1 | | | |

| Aggregate | p50 | p95 | max | n | Pass (p95 ≤ 750 ms, warm) |
|---|---|---|---|---|---|
| warm W1 | | | | | |
| warm W2 (repeat) | | | | | |
| cold (unthrottled) | | | | | |
| cold (Fast 3G) | | | | | |

**Pass:** warm p95 ≤ 750 ms. Cold is informational (no pass gate in d6;
report as-is).
**Fail →** record chunk count + bytes per scrub + whether pyramid/dual-store
was active; candidate causes: chunk > 2 MB (optimization.md sweet spot),
no `Cache-Control`, cold missing `Range`/206.

---

## 5. Protocol (b) — cold load ≤ 10 s

**Claim under test:** clean-browser load → usable globe + first layer ≤ 10 s.

1. **C2 clean profile** (or new `--user-data-dir`). DevTools already open.
2. Network **No throttling**. Navigate to `http://localhost:4173`.
3. Harness auto-attaches when `window.__VIEWER__` appears; `globeReady` = first
   `postRender`. After first imagery layer added, run
   `__BENCH.waitTilesIdle()` (the slice/marker build calls it; if layer not yet
   built, stamp manually).
4. At end: `copy(JSON.stringify(__BENCH.report()))` → paste into the table.
5. Repeat for **Fast 3G** (label the row).
6. Repeat 3×, keep median.

### Table (b) — cold load

| Run | Network | navStart | DOMContentLoaded (ms) | loadEvent (ms) | globeReady (ms) | tilesSettled (ms) | first-paint (ms) | first-contentful-paint (ms) | Pass (tilesSettled ≤ 10000, unthrottled) |
|---|---|---|---|---|---|---|---|---|---|
| b-01 | none | 0 | | | | | | | |
| b-02 | none | 0 | | | | | | | |
| b-03 | none | 0 | | | | | | | |
| b-3G | Fast 3G | 0 | | | | | | | |

Byte breakdown for the same runs (Network panel filtered; harness copies):

| Host | # requests | transferSize | encodedBodySize | decodedBodySize | TAO present? |
|---|---|---|---|---|---|
| localhost:4173 (HTML/JS/CSS) | | | | | |
| assets.ion.cesium.com (terrain) | | | | | |
| gibs.earthdata.nasa.gov (imagery) | | | | | |
| clouds.matteason.co.uk | | | | | |
| R2 / zarr host | | | | | |
| **total** | | | | | |

**Pass:** unthrottled `tilesSettled ≤ 10 000 ms`. Fast-3G informational.
**Fail →** split the waterfall; the dominant contributor is whichever host owns
the largest `Content Download`, and terrain requests are deliberately
async/off critical path (`config.ts` Fix 2) so a terrain stall should not fail
this gate — verify globeReady fired before terrain `readyEvent`.

---

## 6. Protocol (c) — 30 FPS with ≤ 5000 markers

**Claim under test:** 30 FPS sustained at 5000 markers (d6 §4, d4 §4/§5 — no
FPS numbers exist yet; do not import the "10k @ 60 FPS" marketing figure).

Two marker backend arms (d4 §5 render-path A/B):
- `entity` = `viewer.entities.add({ billboard })` — per-entity overhead.
- `point` = `Cesium.PointPrimitiveCollection` — GPU point batch, cheap.

1. Fixed camera, `requestRenderMode = false` for the sample window, then run a
   **continuous camera pan** during sampling. State pan speed.
2. For each arm, run `await __BENCH.markerSweep([arm], [500,1000,2000,3000,4000,5000], 10000)`.
   Each step: clear → add N random points → settle 2 s → sample 10 s → teardown.
3. Cross-check each step in the Performance panel (Frames → FPS, dropped).
4. On a phone (2.5) repeat the 5000 row only.

### Table (c) — marker sweep (entity arm)

| N markers | mean ms | fps | p50 ms | p95 ms | p99 ms | max ms | % frames >33.3 ms | dropped (Perf panel) | fps ≥30? |
|---|---|---|---|---|---|---|---|---|---|
| 500 | | | | | | | | | |
| 1000 | | | | | | | | | |
| 2000 | | | | | | | | | |
| 3000 | | | | | | | | | |
| 4000 | | | | | | | | | |
| 5000 | | | | | | | | | |

### Table (c) — marker sweep (PointPrimitive arm)

| N markers | mean ms | fps | p50 ms | p95 ms | p99 ms | max ms | % frames >33.3 ms | dropped | fps ≥30? |
|---|---|---|---|---|---|---|---|---|---|
| 500 | | | | | | | | | |
| 1000 | | | | | | | | | |
| 2000 | | | | | | | | | |
| 3000 | | | | | | | | | |
| 4000 | | | | | | | | | |
| 5000 | | | | | | | | | |

| Device | arm | max N with fps ≥30 | fps at 5000 | pass (≥30 FPS @ ≤5000) |
|---|---|---|---|---|
| laptop | entity | | | |
| laptop | point | | | |
| phone | point | | | |

**Pass:** any arm sustains mean fps ≥ 30 AND pct frames >33.3 ms ≤ 5% at
N = 5000, laptop. Pick the winning arm; promote it.
**Fail →** report `markers.atTarget` (largest N passing) and the failing arm;
candidate fixes: cluster, viewport cull, PointPrimitive over entity,
`disableDepthTestDistance` off if depth test is affordable.

---

## 7. Protocol (d) — terrain bytes, ion quota 20-reload, offline

### d-1 terrain + layer bytes per load

| Reload # | cache | ion requests | ion transferSize | ion decoded | GIBS requests | GIBS transferSize | zarr requests | zarr transferSize | tilesSettled ms |
|---|---|---|---|---|---|---|---|---|---|
| 1 | cold | | | | | | | | |
| 2 | warm | | | | | | | | |
| 3 | warm | | | | | | | | |
| 4 | hard-reload (cache disabled) | | | | | | | | |
| 5 | warm | | | | | | | | |

Extract with filtered Network panel + `__BENCH.terrainBytes()` /
`__BENCH.gibsBytes()`. Note whether ion 3D Tiles/bathymetry surfaces use
`Content-Encoding` (gzip/br) — record `encodedBodySize` vs `transferSize`.

### d-2 ion quota 20-reload headroom

Budget: **15 GB/mo streaming** (d4 §7; source-only tiled-excluded; Community
tier). Streamed bytes per reload = ion `transferSize`(cold) for reload 1 +
`transferSize`(warm) for reloads 2..20. Warm reloads that hit browser cache
contribute 0 to ion streaming — measure that explicitly.

| Quantity | Value |
|---|---|
| cold-reload ion streamed bytes | |
| warm-reload ion streamed bytes (×19) | |
| `quota.20reloadBytes` (sum) | |
| monthly budget (15 GB = 15,000,000,000 B) | 15000000000 |
| `quota.headroom` (bytes) | |
| `quota.headroom` (% of budget) | |
| # reloads to exhaust budget (`budget / per-reload`) | |
| Pass (20 reloads fit within budget with ≥ headroom) | |

Also open the Cesium ion **Usage Dashboard** (free, web) and record the same
day's streamed-bytes figure to cross-check the DevTools number. If dashboard
and DevTools disagree > 20%, trust the dashboard (server-authoritative) and
note the discrepancy.

**Pass:** `20reloadBytes` < budget AND the 20-reload run leaves headroom for
the rest of the month's demos. Report the implied reloads/month ceiling. Fail →
reduce: Sentinel-2, higher SSE, lower `resolutionScale`, fewer layers (d4 §7).

### d-3 airplane-mode / offline reload

1. Load once normally; settle.
2. DevTools → Network → **Offline** (or OS airplane mode). Do **not** clear cache.
3. Reload.
4. Record which of these render: ellipsoid globe, GIBS basemap (cached tiles),
   terrain (cached tiles), clouds, slice layer.
5. Console: any uncaught errors? Network: failed requests (# , which hosts).
6. Restore online.

| Check | Result | Notes |
|---|---|---|
| Ellipsoid globe renders | pass / fail | |
| GIBS basemap tiles (cached) render | pass / fail | |
| Terrain (cached) renders | pass / fail | |
| Cloud layer renders or cleanly absent | pass / fail | |
| Slice layer renders or cleanly absent | pass / fail | |
| Uncaught console errors | # | |
| Error UI shown (`onError` path) | yes / no | |
| Reviewable without network | yes / no | |

**Pass:** no blank canvas and no uncaught exception; missing layers degrade
silently or show the error overlay. **Fail →** capture the exact console string
and request URLs.

---

## 8. Result record (one block per full session)

```
Session id:
Date:
Env table (§1) filled?  yes/no
Harness version:
Harness selftest: PASS/FAIL
(a) slice warm p95 (ms):
    cold p95 (ms):
    verdict:
(b) tilesSettled median (ms, unthrottled):
    verdict:
(c) winning arm / fps @5000 / max N:
    verdict:
(d) ion bytes/reload cold/warm:
    20-reload total / headroom:
    offline verdict:
Open anomalies / retries:
Artifacts (screenshots, HAR, report JSON path):
```

Export a HAR for the cold load once (Network panel → right-click → "Save all
as HAR") as the raw evidence file; do not commit secrets from headers — scrub
`Authorization` / `Cookie` before saving.

---

## 9. Pass/fail summary gates

| Gate | Threshold | Source | Verdict |
|---|---|---|---|
| (a) slice load, warm p95 | ≤ 750 ms | d6 §4 | |
| (b) cold load, tilesSettled | ≤ 10 000 ms unthrottled | d6 §4 + §3 step 3 | |
| (c) 30 FPS @ 5000 markers | fps ≥ 30 and >33.3 ms frames ≤ 5% | d6 §4 + d4 §4/§5 | |
| (d1) terrain bytes/load | recorded (no threshold) | d4 §9 | |
| (d2) ion 20-reload headroom | 20 reloads < 15 GB/mo budget | d4 §7 | |
| (d3) airplane-mode reload | no blank canvas, no uncaught error | d4 §9 | |

No gate passes without a measured number. UNVERIFIED ⇒ not a pass.

---

## 10. Automation (optional, free)

`bench-run.mjs` (Playwright, MIT) can loop protocols with a fresh
`userDataDir` per run and CDP throttling:

- `context = await chromium.launchPersistentContext(tmpProfile, { args: ['--disable-gpu-vsync'] })`
- `page.context().clearCookies(); await page.evaluate(() => caches.keys().then(k => Promise.all(k.map(x => caches.delete(x)))))`
- `const cdp = await context.newCDPSession(page); await cdp.send('Network.emulateNetworkConditions', { offline:false, latency:562.5, downloadThroughput: 1.6*1024*1024/8, uploadThroughput: 750*1024/8 })`
- `Network.setCacheDisabled({ cacheDisabled: true })` for cold runs; leave false for warm.
- Inject harness via `page.addScriptTag({ path: 'scripts/bench-harness.js' })`, then
  `page.waitForFunction(() => window.__VIEWER__)`, drive `__BENCH.*`, collect
  `page.evaluate(() => __BENCH.report())`.
- Save HAR: `recordHar` context option.

`ponytail:` manual DevTools path above is sufficient for one pass and adds zero
deps; add Playwright only when repeated (3×) runs must be scripted/reproducible.
