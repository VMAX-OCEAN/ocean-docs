# Verification Ledger — Every Load-Bearing Claim

Date: 2026-09-10. Method: exa MCP + npm/PyPI registry + GitHub API + raw files + vendor docs via direct curl. `$NINEROUTER_KEY` absent in tool shell all runs (length checked, never printed) — gateway skipped, direct fetch used. Access date per row = 2026-09-10 unless stated.

Status key: **CONFIRMED** = 2+ independent sources; **CORRECTED** = earlier claim was wrong, fixed; **UNVERIFIED** = not proven, never cite; **PROVISIONAL** = arithmetic/hypothesis pending measurement.

---

## 1. Corrections made this program (were wrong → now)

| # | Earlier claim | Truth | Where fixed |
|---|---|---|---|
| C1 | `xpublish-opendap` nonexistent / REFUTED; real is `xpublish-zarr` | **Both real and distinct**: `xpublish-opendap` v0.2.0 BSD-3 (pushed 2026-09-07), `xpublish-zarr` v0.1.0 Apache-2.0 | ADR-003 + comparison README/02/04/06/07 + checklist |
| C2 | `glorys-dataset.md` lists `wmo` vertical velocity | 001_030 has **only uo/vo**; no vertical velocity (PUM Table 2) | `glorys-dataset.md` fixed |
| C3 | `argo-data.md` `region([-90,30,180,90,dates])` | argopy box = `[lon_min, lon_max, lat_min, lat_max, dpt_min, dpt_max, dates?]` — depth required | `argo-data.md` fixed (verified argopy 1.4.0) |
| C4 | `argo-data.md` `ArgoIndex().search_lat_lon([...])` | old API; use `ArgoIndex().query.box([lon_min,lon_max,lat_min,lat_max])` | `argo-data.md` fixed |
| C5 | `xpublish-opendap` listed as "bad dep name" in lakshya docs | real package, not a defect | comparison 02/04/06/07 patched |
| C6 | Cesium 2019 wind blog "dead" | **LIVE** 2026-09-10, full post returned | d4-lib-pins §4 |
| C7 | ion storage 5 GB | live pricing page says **10 GB** source-only | d4-lib-pins §7 |
| C8 | Vercel Hobby "6000 build minutes" | stale bucket, removed — `build_minutes hobby: not_available` | d4-lib-pins §6 |
| C9 | Supabase 4000×100 profiles fits 500 MB | **false**: ≈3 GB heap, 6x over | d6-capacity §2 |
| C10 | `xpublish-opendap` initial ADR premise | agent rejected premise with evidence — see C1 | ADR-003 |
| C11 | NOC fork v0.11.0 latest | **v0.11.1** (same day, 2026-08-21) | d4-lib-pins §4 |
| C12 | GLORYS DOI `10.48670/moi-00019` | that DOI = BGC 001_029; physics = **`10.48670/moi-00021`** | glorys12.md + ADR context |
| C13 | 931 GB Argo GDAC size | unverified (2023-era); live count 3,386,798 records / 20,484 floats | argo.md |

---

## 2. Stack + library claims

| Claim | Status | Sources |
|---|---|---|
| zarr-cesium 0.2.0 is npm latest, pushed 2026-08-21T14:32:01Z | CONFIRMED | registry JSON dist-tags + times; GitHub releases API `v0.2.0`; tags sha `1e5f18d` = npm gitHead |
| Providers unchanged: ZarrLayerProvider / ZarrCubeProvider / ZarrCubeVelocityProvider | CONFIRMED | noc-oi docs + raw v0.2.0 README + src list |
| Peer `cesium >=1.119.0 <2`; dev-tested 1.142.0 | CONFIRMED | registry peerDeps + raw package.json + registry cesium 1.142.0 |
| url optional + store alt; old url callers work | CONFIRMED | raw types.ts lines 39-42/71-74/98-101 + README + release body |
| npmjs page + releases page stale (show 0.1.4) | CONFIRMED | registry wins |
| `ZarrCubeVelocityProvider` imports `cesium-wind-layer` runtime (wrapper, cannot drop) | CONFIRMED | raw src/zarr-cube-velocity-provider.ts line 2 + registry docs |
| NOC fork latest v0.11.1 | CONFIRMED | releases API (a1fcc4c) + tarball dep in zarr-cesium 0.2.0 |
| upstream cesium-wind-layer 0.10.1 peer `^1.127.0` | CONFIRMED | npm registry + npmjs |
| ≥1.127 dual-engine singleton break real | CONFIRMED | issue #17 error string + upstream readme troubleshooting |
| Vite alias+dedupe fix valid | CONFIRMED | issue #17 + PR #18 + readme |
| Cesium 1.145.0 latest, published 2026-09-01 | CONFIRMED | registry + September blog |
| #13092 closed 2026-02-02, fix PR #13098, shipped 1.138 | CONFIRMED (timeline strong, changelog-text weak) | issue API + PR API + release 1.138 + compare 1.137…1.138; grep returns 0 changelog strings |
| Floor ≥1.119 unsafe (includes 1.136–1.137) | CONFIRMED | 1.136 reporter + 1.137 CHANGES |
| `enableCollisionDetection=false` invalid fix | CONFIRMED | ref-doc + 1.139.1 crash #13078 + reporter #12999 |
| Cesium 1.142.0 chosen (101d soak, avoids 1.145 freeze) | DECISION | d4-lib-pins §3 |
| WebGL2 mandatory on 1.142 (billboards/labels + pickAsync) | CONFIRMED | Cesium docs/changelog since 1.140 |
| WebGPU irrelevant to Cesium (no impl/roadmap) | CONFIRMED | CesiumGS/cesium#4989 + staff replies |

---

## 3. Host + quota claims (free tier)

| Claim | Status | Sources |
|---|---|---|
| Cloudflare Pages: unlimited BW + requests; 25 MiB/file | CONFIRMED | Pages product page + limits page |
| Vercel Hobby 100 GB Fast Data Transfer + 10 GB Origin + 1M Edge | CONFIRMED | docs/limits (2026-09-03) + plans/hobby + pricing + fair-use |
| Vercel Hobby non-commercial personal only | CONFIRMED | plans/hobby |
| Netlify free ~15 GB effective (300 credits, 20/GB) | CONFIRMED | Netlify credit docs ×2 |
| GitHub Pages: no headers/rewrite, 1 GB site, commercial ban | CONFIRMED | GH Pages limits + plan docs |
| Apr 2026 Vercel bandwidth cut | UNVERIFIED (no source; real Apr changes = Turbo price 2026-04-15, 30d retention 2026-04-27) | Vercel changelog |
| ion Community: 10 GB storage, 15 GB/mo streaming ex-Bing, 1000 sessions/mo, 1000 Google root tiles/mo, 50000 geocodes/mo, 10 clips/mo | CONFIRMED | pricing + optimizing-quotas + bathymetry + sentinel-2 + community staff post |
| Default `Viewer` burns a Bing session per load; fix `baseLayer:false` + Sentinel-2 3954 | CONFIRMED | optimizing-quotas + Viewer ref-doc |
| Bathymetry = GEBCO 2023, ~450m + hi-res coasts, assetId 2426648 | CONFIRMED | bathymetry content page + blog |
| R2 free: 10 GB-mo, 1M Class A, 10M Class B, egress free | CONFIRMED | R2 pricing (2026-08-07) + limits |
| Supabase free: 500 MB, 5 GB egress, 7d pause, 2 projects | CONFIRMED | pausing guide + pricing |
| Mapbox pricing: Map Loads 50k free then $5/$4/$3/$2.50; 12h session | CONFIRMED | mapbox.com/pricing + GL JS pricing guide |

---

## 4. Dataset claims

| Claim | Status | Sources |
|---|---|---|
| GLORYS 001_030: DOI `10.48670/moi-00021`, 1/12°, 50 levels, 3 dataset IDs, 4 3D + 7 2D + 8 static vars | CONFIRMED | product page + PUM 1.7 (28pp) + metadata JSON |
| No vertical velocity in 001_030 | CONFIRMED | PUM Table 2 + product metadata |
| Argo DOI `10.17882/42182`, CC-BY 4.0 | CONFIRMED | SEANOE JSON license field |
| Argo Indian subset 354,696 files / 2,421 floats | CONFIRMED (live count) | GDAC index parse |
| Glider DOI `10.17882/56509`, CC-BY-NC 4.0 | CONFIRMED | file attr + deployment JSON |
| Glider Indian coverage 11.7% deployments, 124/131 one array | CONFIRMED (measured) | index parse |
| Glider all profiles real-time only (0 delayed) | CONFIRMED | 824,632 profile scan |
| INCOIS holdings 44 rows; ERDDAP 16 datasets; LAS 13 cats | CONFIRMED | holdings page + info/index.csv + getCategories.do |
| INCOIS ESSDP "1047 datasets" string | UNVERIFIED | not found on page |
| INCOIS THREDDS per-dataset OPeNDAP | UNVERIFIED | single DatasetScan only |
| PS item-d `Collection of In-situ Data` URL | UNKNOWN — authority-side blank | sih.gov.in/sih2026PS modal, 3x |
| EMU: 37 units, 6 vars, 4 depth bands, 52M+, WOA13 v2 | CONFIRMED | ScienceBase + TOS paper |
| Esri EMU Explorer code Apache-2.0; item CC BY 4.0 (item-scope) | CONFIRMED | GitHub API + ArcGIS item JSON |

---

## 5. Capacity arithmetic (deterministic, not measured)

| Quantity | Value | Basis |
|---|---|---|
| IO bbox 60–100E/5S–30N cells/slice | 480×420 = 201,600 | 1/12° grid |
| float32 slice bytes | 806,400 B (0.806 MB) | ×4 |
| daily full-50 per month @10:1 | 493.39 MB | 4×50+1 slices ×30.44 ÷10 |
| 10 GB fit daily full-50 | ~20.3 mo (zero headroom) | arithmetic |
| R2 default scope | ~1.2 GB | daily surface+5-depths 12mo + monthly full-50 24mo |
| 10:1 ratio | CEILING, optimistic for lossless float32 | CESM 1.35x, earth cube 3.06x |
| Supabase float row | ~84 B | PG MAXALIGN 8 + 24 B header |
| Supabase profile row | ~76 B | same |
| Supabase latest-10+metadata | ~60 MB (fits 500 MB) | row math |
| Supabase full Indian history | 527–678 MB heap (NO fit) | row math |
| balanced chunk effective | (1,10,480,420) = 8.064 MB raw | min(chunk, shape) |
| time chunk effective | (30,50,108,216) = 139.968 MB raw | min(chunk, shape) |
| Subset raw (30t×50z×480×420) | 1.2096 GB | deterministic |

All arithmetic is PROVISIONAL until `chunk-benchmark-protocol.md` §9 runs.

---

## 6. Open items (no pass claimed)

| Item | Status |
|---|---|
| Locked-laptop slice ≤750 ms / cold ≤10 s | UNVERIFIED — protocol written |
| 30 FPS + 5000 markers | UNVERIFIED — protocol written; app has no marker code yet |
| Dual-rep vs balanced verdict | UNVERIFIED — benchmark gate |
| GeoJSON/Arrow/FGB N_LOCK | UNVERIFIED — benchmark gate |
| zarr-cesium R2 real-data render | UNVERIFIED — Phase 0 test owed |
| terrain bytes + ion 20-reload headroom | UNVERIFIED — protocol written |
| offline/airplane-mode behavior | UNVERIFIED — protocol written |
| Mermaid residual sign rewrite | OPEN — D8 |
| Q7/Q9/Q10 feature/GPU/random-access gates | OPEN — D8 |
| `ocean-web` cesium pin still `^1.127.0` | OPEN — apply ADR-002 |

---

## 7. Citation rules carried through

- Pasted PS portal text is canonical; listing URL differs — pasted wins.
- Never invent the blank in-situ URL.
- Never cite Esri archwatch externally (resolved to EMU/Ocean Base — cite those).
- Never cite Unity for NASA Eyes (engine undisclosed).
- Never cite star counts as maturity proof.
- Never claim WMS/WCS live compliance (roadmap-only).
- Residual is canonical `model − observation`; reject `O − M`.
- Key via env only; never print, log, or commit.
