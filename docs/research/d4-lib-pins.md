# D4 — Phase 0 Library Pins + Best Free Picks

Date: 2026-09-10. Verified + re-verified second pass (5 + 5 agents).
Method: exa + npm registry + GitHub API + raw + vendor docs curl. `$NINEROUTER_KEY` absent in tool shell, gateway skipped. Access date per URL. UNVERIFIED marked, never cited as fact.

## 1. Verdict table

| Item | Winner | Evidence | Still open |
|---|---|---|---|
| Zarr render lib | `zarr-cesium@0.2.0` exact | Registry triple-confirmed, tag sha match | Build retest on R2 URL |
| Custom render path | Custom ImageryProvider + zarrita + Canvas + d3 (A-arm), zarr-cesium B-arm | Smallest bundle, deps present | FPS/chunk-ms bench |
| Cesium pin | `cesium@1.142.0` exact, fallback `1.138.0` | 101d soak, peer ok | Laptop matrix test |
| Particles | NOC fork v0.11.1 via provider | Wrapper proof, upstream second | Particle FPS bench |
| Static host | Cloudflare Pages | Unlimited BW+requests | `dist` size check + deploy A/B |
| Globe base | GIBS Blue Marble + ion World Bathymetry | $0, true depth | Terrain bytes + quota 20-reload |
| Vercel numbers | 100 GB Fast Data Transfer + 10 GB Origin + 1M Edge | Dual-sourced docs | Patch 3 lakshya-side stale rows (recorded §6, not edited — foreign namespace) |
| ion quotas | Community, conditional pass | Dual-sourced docs | Measured demo bytes |

## 2. zarr-cesium 0.2.0 (latest confirmed)

Registry `https://registry.npmjs.org/zarr-cesium`: `dist-tags.latest 0.2.0`, `time.0.2.0 2026-08-21T14:32:01.298Z`, `modified ...01.660Z`. GitHub releases API: `v0.2.0 2026-08-21T14:32:02Z`. Tags sha `1e5f18daccbb164ab3084edd8d2d09253a255b96` matches npm `gitHead`. npm versions: `0.1.0, 0.1.1, 0.1.3, 0.1.4, 0.1.6, 0.2.0`. Tag-only no-publish: `0.1.2, 0.1.5, 0.1.7`. Traps: npmjs page stale shows 0.1.4, releases page misses 0.2.0 — registry wins. (One re-verify run read registry latest 0.1.4 — stale read, rejected by triple-confirm.)

Providers unchanged (`https://noc-oi.github.io/zarr-cesium/docs/` + raw `v0.2.0/README.md` + src list): `ZarrLayerProvider` / `ZarrCubeProvider` / `ZarrCubeVelocityProvider`. `ZarrImageryLayer` exists in 0.2.0 exports (prior absent claim corrected). Standalone npm `cesium-zarr` / `ZarrTileProvider` / `ZarrImageryLayer` 404.

`url` optional + `store` alt (raw `v0.2.0/src/types.ts` lines 39-42, 71-74, 98-101 + README 26-27, 129-134 + release body Icechunk line). Old url-only calls work. Peer exact `>=1.119.0 <2` (registry `zarr-cesium/0.2.0` + raw `v0.2.0/package.json`). Tested `cesium 1.142.0` (npm devDeps + raw package.json + `https://registry.npmjs.org/cesium/1.142.0`). Deps exact: `zarrita ^0.7.4`, `zarr-maps-tiling ^0.2.0`, `zarr-maps-colormap ^0.2.0`, NOC fork `cesium-wind-layer-0.11.1.tgz` release URL. zarrita latest `0.7.5` (2026-09-01T14:50:09Z) — `^0.7.4` allows it, combo untested, hold.

Breaking 0.1.4→0.2.0: peer `*`→range; deps 0→4 (needs GitHub tarball access); tiling/colormap migrated to Zarr Maps packages, types from `zarr-maps-tiling`, old deep imports (`webgl-utils`/`jsColormaps`/`zarr-utils`/`shaders`) break risk — use root; velocity uses NOC fork; payload `~12MB`→`314649`, files 29→6. Additive: `store/stores`, auth trio `requestOverrides/transformRequest/onAuthError`, queries `queryData/getTimeSeries/getVerticalProfile/getTransect`, GeoZarr multiscale, `CesiumHost = Viewer | CesiumWidget`.

R2 public = plain `url`, needs CORS + Range (`https://developers.cloudflare.com/r2/buckets/cors/`, `.../public-buckets/` — r2.dev rate-limited, prod custom domain; `https://zarrita.dev/packages/storage.html`, `https://jsr.io/@zarrita/storage/doc`). R2-specific Range failure mode UNVERIFIED. FetchStore keys: `new FetchStore(url, {fetch, overrides deprecated, useSuffixRequest})`; transforming URL must preserve Range via `new Request(newUrl, request)`.

Pin: `zarr-cesium@0.2.0` + `cesium@1.142.0` + `zarrita@^0.7.4`, exact pre-1.0, no float.

## 3. Cesium pin matrix

| ver | published | size/files | #13092 | wind | breaking |
|---|---|---|---|---|---|
| 1.119.0 | 2024-07-01 | 68.7MB/1047 | predates bug | fork ok; upstream `^1.127.0` FAILS | `CircleGeometry.unpack`, BaseLayerPicker, wgs84 deprecations |
| 1.138.0 | 2026-02-02 | 74.7MB/1086 | timeline-strong, changelog-weak | both ok | none (fixes + EXT_textureInfo only) |
| 1.142.0 | 2026-06-01 | 77.8MB/1090 | same gap | both ok | `boundingVolume` world-space (#13477) |
| 1.145.0 = npm latest | 2026-09-01 | 79.4MB/1090 | same gap | both ok | `ClippingPolygons` freeze (#13665) |

#13092: closed completed 2026-02-02T17:31:28Z by ggetz; fix PR #13098 merged 17:31:03Z commit `7c3a70c` (mzschwartz5); release 1.138 published 20:10:48Z; compare 1.137...1.138 contains fix then release commit. Strength: timeline strong, changelog-text weak (raw 1.138 CHANGES line 11 names only #13083; grep `13092|13098` zero on 1.138/1.139/1.142/1.145/main — link via PR body + close comment only). 1.136 introduced (pickAsync #12983 + terrain quadtrees #8481; bisect blames fast-picking #9961); 1.137 broken (only #12949 #13042); 1.138+ fixed retained, zero re-reports; 1.145 tag 2026-09-01T18:51:41Z. Followup #13180 not blocking. `enableCollisionDetection=false` invalid (default true; disables min/max zoom + tiles collision + CLAMP; 1.139.1 crash #13078; #12999 throttle laggy). `frontFaceAlphaByDistance` valid fade API, not fix. Floor `>=1.119` unsafe (includes 1.136–1.137).

Winner: `cesium@1.142.0` exact — 101d soak beats 9d 1.145 churn, avoids ClippingPolygons freeze + 1.119 age/upstream peer fail. Fallback `1.138.0` exact (zero breaking, smallest). ADR:

```
# ADR: pin cesium 1.142.0 for SIH demo
Date 2026-09-10. Pin exact cesium@1.142.0.
Why: 101d soak, zarr-cesium 0.2.0 peer ok, fork wind-layer ok,
avoids 1.145 ClippingPolygon freeze, avoids 1.119 staleness.
#13092 fix-version UNVERIFIED in CHANGES, needs laptop matrix test.
Revisit after matrix test or 1.145 +30d soak. Never float latest.
```

Matrix test (laptop, per version 1.119/1.138/1.142/1.145): translucency camera jump repro, Sentinel-2 imagery, CWB terrain/WMS pick, wind particles, zarr-cesium load, console errors, bundle parse. Promote only tested cell.

## 4. Velocity particles

Wrapper CONFIRMED, cannot drop: raw `main/src/zarr-cube-velocity-provider.ts` line 2 imports `WindLayer` runtime; class stores `WindLayer[]` per elevation slice; depth+time bound through it. Fork latest v0.11.1 (`a1fcc4c`; v0.11.0 `6ec553c`, both 21 Aug, 13:57 vs 11:58). Upstream 0.10.1 (2026-04-26, peer `^1.127.0`, dev `^1.136.0`). ≥1.127 break REAL: engine 15 vs widgets-requires-16, dual ContextLimits singletons, `DeveloperError: Width must be less than or equal to the maximum texture size (0)`. Fix VALID docs-only: Vite alias + dedupe + upgrade past 1.129 or pnpm overrides (PR #18 merged 2026-04-26 `80f6939`, released 0.10.1 via #19):

```ts
resolve: {
  alias: { '@cesium/engine': cesiumEngineAlias },
  dedupe: ['cesium', '@cesium/engine', '@cesium/widgets'],
}
```

Cesium 2019 wind blog `https://cesium.com/blog/2019/04/29/gpu-powered-wind/` LIVE 2026-09-10 (prior dead claim false). 0.2.0→v0.11.1 tarball pin: one run saw npm 0.1.4 + libraries.io fork v0.11.0 — registry triple-confirm wins. Fallback: fork v0.11.1 primary → upstream 0.10.1 + alias second → vendored shader last. RaymanNg `3D-Wind-Field` dropped (NetCDF v3 only, single timestep, pins cesium 1.125.0, MIT 155 commits latest 2025-06-18). Particle FPS bench still owed — no FPS numbers without source+device.

## 5. Render path best (free)

Winner: custom ImageryProvider + zarrita FetchStore + Canvas + d3-scale-chromatic (A-arm). Smallest added bundle, deps present, full depth+time control. zarr-cesium B-arm only. Load-bearing signatures (tarball): `requestImage(x, y, level, _request?)`, `zarrVersion?: 2 | 3`, `updateSelectors(selectors)`, `updateSlices({latIndex, lonIndex, elevationIndex})`. Zero `TimeDynamic|JulianDate|Clock` hits in dist — time/depth via updateSelectors + updateSlices + query APIs. nordicseas3d: no Cesium, vertex-colored BufferGeometry mesh (no Data3DTexture), gsZarr loader reusable, grid [73,72,312,320], last commit 543f090 2026-06-26. netcdf-three dropped: no npm package, v1.0.1, stale 2024-03-22, Three-only, v3-only (netcdfjs 4.0.0 unpacked 65797, three 0.186.0 unpacked 20443175). FPS scrub + chunk ms missing all paths — Phase 0 A/B bench owed, no invented numbers.

## 6. Vercel numbers (dual-sourced curl+exa)

Hobby current: 100 GB Fast Data Transfer + up to 10 GB Fast Origin + 1M Edge Requests (`https://vercel.com/docs/limits` updated 2026-09-03, `.../fair-use-guidelines`, `.../plans/hobby` 2026-08-31, `.../pricing`, `.../manage-cdn-usage` 2026-08-11). Number correct, label stale (`Bandwidth`→`Fast Data Transfer`). Function invocations first 1M; Active CPU 4 CPU-hrs; Provisioned mem 360 GB-hrs. Builds Basic 2vCPU/8GB/32GB (`.../changelog/basic-build-machines` 2026-09-03), 45 min/deploy, 1 concurrent, 100/day, routes 2048, projects 200, domains 50. 6000 build bucket stale — drop (`pricing` yaml `build_minutes hobby: not_available`). Extra stale: `Static sites Unlimited`→200, `Custom domains 1`→50. Apr 2026 cut UNVERIFIED. Real Apr changes: Turbo price cut 2026-04-15, Hobby 30-day retention 2026-04-27. vercel.json valid (`.../project-configuration/vercel-json` 2026-08-14, `.../routing/rewrites` 2026-08-11; filesystem before rewrites; `/cesium/*` bypasses SPA). Caveat: `/cesium/(.*)` 1yr immutable needs `dist/cesium/` match — default `cesium()` plugin, dist UNVERIFIED without build.

Stale rows live in `research/individuals/lakshya/` (foreign namespace — recorded here, not edited): `free-tier-deployment.md:78-80` (bandwidth 100 GB + build minutes 6000), `vercel-deployment.md:21,279-285`, `cross-check-verification.md:227`. Patch: rename to Fast Data Transfer + Origin + Edge rows, drop 6000 row, add Basic build caps row.

## 7. ion quotas (dual-sourced)

Community (live pricing page curl 2026-09-10 — storage says **10 GB**, older 5 GB snippets stale): storage 10 GB source-only tiled-excluded; streaming 15 GB/mo ex-Bing; Global Imagery 1000 sessions/mo (Bing+Google+Azure); Google Photorealistic 1000 root tiles/mo (= sessions per staff `https://community.cesium.com/t/cesium-ion-google-3d-tiles-api-limit/29307`); geocodes 50000/mo widget-only no REST; clips 10/mo (25 km² Depot, 200 km² own); Reality 20 gigapixels / Analysis 5 hrs single-source. Sources: `.../platform/cesium-ion/pricing/`, `.../learn/ion/optimizing-quotas/`, `.../cesium-world-bathymetry/`, `.../sentinel-2-imagery/`, `.../ion-access-tokens/`, `.../rest-api/`.

Bing burn per `Viewer` load confirmed (+ `Viewer.html`: `baseLayer:false` valid only if `baseLayerPicker:false`); `removeAll()` still burns; covering doubles. Fix: `baseLayer:false, baseLayerPicker:false` + Sentinel-2 assetId 3954 (10m global, data-quota, cached refresh). Token: `Authorization: Bearer`, dashboard tokens never expire vs OAuth monthly (`.../ion-oauth2/`) — different types. Bathymetry assetId 2426648 = GEBCO 2023 Grid doi:10.5285/f98b053b-0cbc-6c23-e053-6c86abc0af7b + hi-res to 1m, SaaS Depot + Self-Hosted licensable. Sufficiency CONDITIONAL PASS: Sentinel-2 + CWB only, uploads <10 GB, streams <15 GB, geocodes minimal, clips ≤10 — actual demo bytes absent, measure via Usage Dashboard. Over-quota soft (email first); then Commercial 50GB/150GB/5k/5k/25 or sales. Reduce: Sentinel-2, `geocoder:false`, WebP, higher SSE, lower resolutionScale.

## 8. Host best (free)

Winner: Cloudflare Pages — unlimited bandwidth + requests, 500 builds/mo, 100 projects, 100 domains/project. Bind: 25 MiB/file → big Cesium chunks in R2. Vercel Hobby: non-commercial personal only + 100 GB cap. Netlify free: ~15 GB effective (300 credits/mo, 20/GB) + 15 credits/prod deploy. GH Pages: soft 100 GB, no headers/rewrite (404.html hack), 1 GB site, commercial/SaaS ban. Equivalents: Pages `_headers` (100 rules) + `_redirects` (`/* /index.html 200`); Netlify `netlify.toml`; vercel.json keep. R2 CORS native, egress free. `dist` never built — largest-file UNVERIFIED. Test: build once, deploy Pages + Vercel preview, check cache-control + deep-link 200 + R2 CORS + GB/load.

## 9. Base best (free)

Winner: GIBS Blue Marble + ion World Bathymetry. Keeps $0, adds true depth, light-ocean shading per Cesium bathymetry guidance. Current code = option #2 (World Terrain land-only) — swap one call in `config.ts`:

```ts
const terrain = Cesium.Terrain.fromWorldBathymetry({
  requestVertexNormals: true,
});
```

Optional: `BlueMarble_ShadedRelief_Bathymetry` GIBS layer (probe 200, 41,359 bytes/tile — UNVERIFIED in-viewer). Google Photorealistic dropped (quota cliff ~30 judge loads/day, oceans weak, combine + high-risk bans). Drop: Bing base, BaseLayerPicker Bing entries, `createWorldImagery` default, Geocoder, night-lights call (lighting off = dead weight), auto-test runs on ion assets. Tests: terrain bytes/load (DevTools `assets.ion.cesium.com` cold vs reload), quality screenshots 20,000 km + 500 km coast, quota headroom 20 reloads, airplane-mode reload.

## 10. Phase 0 ordered steps

1. Pin `zarr-cesium@0.2.0` + `cesium@1.142.0` + `zarrita@^0.7.4`; verify `gitHead` starts `1e5f18d`; inspect lockfile fork tarball + tiling/colormap 0.2.0.
2. Configure R2 public + CORS `GET,HEAD` + expose headers (r2.dev dev only, custom domain prod).
3. Probe chunk Range+Origin: expect 206 + `Access-Control-Allow-Origin`; fix 401/403 first (not CORS).
4. Wire provider (`url` public / `store` Icechunk-custom; `requestOverrides` static headers; `transformRequest` sign/proxy preserving Range; `onAuthError` refresh 400/401).
5. Smoke `createLayer` + `queryData` Point; tiles 200/206; colormap update; typecheck `CesiumHost`; drop deep imports.
6. A/B custom ImageryProvider vs zarr-cesium; record FPS + GETs + bytes.
7. Fail → freeze 0.1.4 + cesium 1.119.0, log diff.

## 11. Open items

Laptop matrix (§3); particle FPS (§4); render FPS/chunk-ms (§5); dist size + deploy A/B (§8); terrain bytes + quota + offline (§9). No gate pass without measurements.
