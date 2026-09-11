# 02 — Lakshya Deployment/Execution Track (14 files)

**Namespace:** `../../individuals/lakshya/`
**Role:** Deployment + execution. How to ship $0, de-risk libs, run phases.
**Definitive plan:** `revised-master-plan.md` (supersedes paid docs). Primary architecture: `free-tier-deployment.md`.
**Date:** 2026-09-09. Verification: 9router gateway.

---

## 1. Namespace at a glance

| # | File | Role | Status | Serves |
|---|------|------|--------|--------|
| 1 | `README.md` | Index | Current | Points definitive plan, marks paid docs reference-only |
| 2 | `revised-master-plan.md` | **Definitive build plan** Phases 0-6 | **PRIMARY** | F1 partial, F5 demo cost, de-risk gates |
| 3 | `free-tier-deployment.md` | **Primary architecture** $0 hot-path split + runnable code | **PRIMARY** | F1, F5, demo cost |
| 4 | `cross-check-verification.md` | Risk audit, 10 decisions | Current | Honest versions/pins, OPeNDAP correction, test-first |
| 5 | `approach-comparison.md` | Decision log, 5 shifts, 7 decision points | Current | Kills Three/single-platform/paid/blind-commit |
| 6 | `change-log.md` | History, 10 changes | Current history | Change3 OPeNDAP line stale, rest valid |
| 7 | `vercel-deployment.md` | Frontend deploy | Half-stale | vite-plugin-cesium + vercel.json + chunk split valid; backend-proxy code superseded by direct R2 |
| 8 | `cesium-deployment.md` | Cesium assets/ion/CORS/bundle | Half-stale | Ion token + CORS + cache headers valid; self-host GEBCO on Render disk stale (no disk free) |
| 9 | `deployment-architecture.md` | Old paid split Vercel+Render | **SUPERSEDED** | Paid $9.50 path only |
| 10 | `render-deployment.md` | Backend paid deploy | **SUPERSEDED** | Paid Starter+disk reference only |
| 11 | `render-blueprint.md` | IaC render.yaml | **SUPERSEDED** | Paid + dep name `xpublish-opendap` (real package, BSD-3) |
| 12 | `pricing-analysis.md` | Paid cost breakdown | **SUPERSEDED** | $9.50 prod, contradicts free-only |
| 13 | `deployment-checklist.md` | Step checklist | **SUPERSEDED** | Paid Starter+disk flow; free-tier needs R2/Supabase/cron steps |
| 14 | `render-vs-alternatives.md` | Backend vendor compare | **SUPERSEDED** | Matrix useful, $9.50 conclusion stale |

**Keep runnable:** revised-master-plan, free-tier-deployment, cross-check-verification, approach-comparison, change-log, vercel-deployment (frontend half), cesium-deployment (frontend half).
**Keep matrix only:** render-vs-alternatives.
**Kill / banner as superseded:** render-deployment, pricing-analysis, render-blueprint, deployment-architecture (paid flow), deployment-checklist (paid flow).

---

## 2. Per-file deep dive

### 2.1 `README.md` — index

| Aspect | Detail |
|--------|--------|
| Serves | Index. Names definitive plan, labels paid docs reference-only |
| Assumptions | Free stack permanent, no card. R2+Supabase direct kills backend hot path |
| Risks | Multi-account advice ToS gray. Paid docs still listed as reference confuse build |
| Stale | Current. Paid files marked reference only |
| Gaps | No R/F trace, no residual, no cards, no ADRs |
| Verdict | Keep as entry. Add banner links to superseded files |

### 2.2 `revised-master-plan.md` — DEFINITIVE PLAN

Phases 0-6, decision tree, fallbacks, pinned versions, scope discipline table.

| Phase | Duration | Deliverable | Gate |
|-------|----------|-------------|------|
| Phase 0 de-risk | 1-2d | PoC zarr-cesium + Supabase | R2 test Zarr loads via zarrita; ZarrLayerProvider SST renders; velocity particles animate; Supabase browser query works; Cesium on Vercel renders. Fail = fallback ImageryProvider |
| Phase 1 globe | 3-4d | Light-theme CesiumJS globe on Vercel | Globe renders, terminator visible, light theme |
| Phase 2 SST | 3-4d | Temp overlay from R2 Zarr | Overlay renders, colorbar works |
| Phase 3 time+depth | 3-4d | Animated depth exploration | Time smooth, slices render |
| Phase 4 currents | 3-4d | Particle advection | Particles animate, sync time/depth |
| Phase 5 Argo | 3-4d | Float markers + profiles | Markers load, profiles render on click |
| Phase 6 isosurface | 3-4d | 3D thermocline via Render | Isosurface renders, cold start acceptable |
| **Total** | **20-26d** | Full platform | Earlier phases alone = strong SIH submission |

**zarr-cesium 3-provider mapping (key discovery):**

| Provider | Use | Does |
|----------|-----|------|
| `ZarrLayerProvider` | SST, salinity, sea level 2D | Renders Zarr arrays as Cesium imagery layers, GPU colormap |
| `ZarrCubeProvider` | Depth slices, vertical sections 3D | Horizontal/vertical slices from 3D cubes |
| `ZarrCubeVelocityProvider` | Currents U/V particles | Animated advection from U/V |

If velocity provider works, skip cesium-wind-layer entirely.

**Fallback sketch:** Custom `ImageryProvider` + zarrita.js `FetchStore` → Canvas + d3-scale-chromatic → return Canvas as tile. ~2-3d work, CPU-side slower but reliable.

**Pinned versions (re-pin needed):**

| Package | Pin in doc | Current 2026-09-09 | Action |
|---------|------------|--------------------|----|
| cesium | ^1.127.0 | >=1.119 <2, incl 1.142+ | Keep floor ≥1.119, test #13092 at pin |
| zarr-cesium | 0.1.4 | npm latest **0.2.0**, pushed 2026-09-08 | **Re-pin 0.2.0, retest Phase 0** |
| zarrita | ^0.7.0 | OK | Keep |
| supabase-js | ^2.45.0 | OK | Keep |
| plotly | ^2.35.0 | OK | Keep |
| xarray/zarr/pyvista/scikit-image | pinned | OK | Prefer scikit-image marching cubes on 512MB (PyVista doubtful) |

**Scope discipline (`Not doing` table):** OPeNDAP skipped MVP; full volume deferred (isosurface instead); Glider/CTD/BGC skipped (Argo only); custom terrain skipped (ion suffices); backend not in hot path; paid services no; true 3D particle trajectories no (no w data in GLORYS).

| Aspect | Detail |
|--------|--------|
| Assumptions | Phase0 1-2d proves zarr-cesium. Velocity provider replaces wind-layer. R2 10GB + Supabase 500MB fit Indian Ocean subset. Render free 512MB runs marching cubes |
| Risks | zarr-cesium 0.1.4 immature. PyVista on 512MB/0.1CPU doubtful. Capacity math unverified |
| Gaps | F1 partial (isosurface only, full volume deferred). F2 zero beyond Argo. F3 zero ASCII adapter. F6 no registry. F7 no live WMS/WCS. F4 missing log/linear. F5 no INCOIS on-prem path. Outreach zero. Mandate beats zero. Cards zero. Residual zero. QC zero. Arrow cutoff zero. Chunk benchmark zero. Laptop zero |
| Verdict | Keep as build spine. Graft prem22k residual/bbox/cards/ADRs/mandates on top |

### 2.3 `free-tier-deployment.md` — PRIMARY ARCHITECTURE

$0 hot-path split + runnable R2/Supabase code. Core insight: Render free has no disk — move data out, backend becomes compute-only.

| Data | Free service | Browser access |
|------|--------------|----------------|
| Zarr chunks | Cloudflare R2 10GB free | Direct, public URL, zarrita FetchStore, zero egress |
| Argo/Glider metadata | Supabase 500MB Postgres free | Direct, JS client, PostGIS |
| Isosurface compute | Render free 512MB/0.1CPU | On-demand only |
| OPeNDAP (if needed) | Render free | On-demand |

**Runtime flows:**

| Flow | Path | Backend? |
|------|------|----------|
| Page load | Browser → Vercel CDN → index.html + JS + Cesium | No |
| Globe | Browser → Cesium ion → terrain + imagery | No |
| SST overlay | Browser → R2 public URL → `.zmetadata` → chunk (~100KB, ms) → GPU texture | **No** |
| Argo markers | Browser → Supabase REST → `SELECT * FROM floats WHERE bbox` | **No** |
| Argo profile | Browser → Supabase REST → `SELECT * FROM profiles WHERE float_id` | **No** |
| Isosurface | Browser → Render `/isosurface?var=thetao&value=20` → reads R2 → PyVista marching cubes → glTF | **Yes, only call** |

**Runnable code included:** R2 upload (`aws s3 sync` via R2 S3 API), Supabase schema (`floats` + `profiles` + PostGIS `GIST`), frontend `zarrClient.ts` (zarrita openArray from R2 URL), `supabaseClient.ts` (`getFloatsInBbox`, `getProfile`), `isosurface.ts` (fetch Render), keep-warm cron-job.org 08:00-18:00 every 14min (~310 hrs/mo).

| Aspect | Detail |
|--------|--------|
| Assumptions | R2 10GB holds 5 vars × 1-2mo. Supabase 500MB holds 4000×100 profiles. Render 310h keep-warm under 750h. zarrita FetchStore works on R2 public URL |
| Risks | R2 10GB ~2mo only. Supabase pause 1wk. Render cold 30s. No disk = cache in R2. Multi-account ToS flag |
| Gaps | Same as master plan + no R/F trace + stale Vercel BW number (says 100GB; Apr 2026 Hobby change — verify) |
| Verdict | Keep as hot-path bible. Fix backend-proxy remnants in sibling docs to match direct-R2 |

### 2.4 `cross-check-verification.md` — risk audit

10 decisions rated, honest risk matrix, OPeNDAP correction, test-first mandate.

| Decision | Verdict | Confidence | Fallback |
|----------|---------|------------|----------|
| CesiumJS globe | ✅ Solid | High | None |
| zarr-cesium | ⚠️ Risk | Medium | Direct zarrita.js + custom primitive; nordicseas3d Three.js |
| cesium-wind-layer | ⚠️ Risk, known compat | Medium | Custom GPU shader (Cesium blog wind viz) |
| Zarr format | ✅ Solid | High | None |
| R2 storage | ✅ Solid | High | GitHub Releases / Supabase Storage |
| Supabase DB | ✅ Solid | High | Metadata in PG, profiles as R2 JSON |
| Render free | ✅ Solid | Medium-high | Fly.io / Vercel serverless |
| Vercel frontend | ✅ Solid | High | None |
| xpublish backend | ✅ Solid | Medium | Plain FastAPI |
| Multi-account Render | ✅ Solid | High | Single account hour management |

**Self-corrections inside:** flags zarr-cesium 0.1.4 / 48 stars / 14 issues / EPSG3857 bug; wind-layer Cesium>=1.127 break; CORRECTED 2026-09-10: `xpublish-opendap` exists (BSD-3 v0.2.0); earlier nonexistent claim wrong; Supabase 480MB tight; PyVista 512MB tight → scikit-image; multi-account ToS.

| Aspect | Detail |
|--------|--------|
| Assumptions | Stars/downloads prove maturity. Pin + Vite alias fixes wind-layer. R2 zero egress permanent. 750h/workspace allows 2 accounts |
| Risks | Own kills listed (see §4). Demands Phase0 test |
| Verdict | Keep as risk register. Update star counts or drop them (rot fast — prefer version/API facts) |

### 2.5 `approach-comparison.md` — decision log

5 shifts + 7 decision points with rejected alternatives.

| Shift | From | To | Reason |
|-------|------|----|--------|
| 1 | Hand-rolled Three.js globe | CesiumJS | Three.js can't do geospatial accurately (sphere vs WGS84, no terrain/LOD/imagery stream, fake day-night/atmosphere, no camera/geospatial system) |
| 2 | Single platform Render only | Split Vercel + Render | No single platform handles frontend + backend well (Vercel CDN/preview vs Render Python/disk) |
| 3 | Paid $9.50/mo | Free $0/mo | User requested free only; disk was only cost driver, eliminated via R2+Supabase |
| 4 | Backend in hot path | No backend in hot path | Backend = bottleneck (512MB, GIL), needs paid disk, cold start hits every request, SPOF. R2+Supabase designed for direct browser |
| 5 | Commit zarr-cesium blindly | De-risk first (Phase 0) | v0.1.4, 10mo old, 3 contrib, 14 issues. 1-2d PoC = cheap insurance |

**7 decision points:** data format (Zarr over NetCDF/GRIB2/OPeNDAP/HDF5/COG), ocean rendering (zarr-cesium + fallback), database (Supabase over SQLite/Render PG/Mongo/R2-JSON/PlanetScale), Zarr storage (R2 over disk/S3/GCS/Supabase-storage/Releases/B2), frontend hosting (Vercel over Render-static/Netlify/Pages/GH-Pages), backend hosting (Render free over Fly/Vercel-serverless/Railway/Heroku/Lambda), currents (zarr-cesium velocity over wind-layer/custom/Canvas/streamlines).

| Aspect | Detail |
|--------|--------|
| Assumptions | No single platform fits both. Direct faster than proxy. 1-2d PoC cheaper than blind commit |
| Risks | Inherits v0.1.4 trust gap, 500MB/10GB tight, Render weak for xarray |
| Verdict | Keep as ADR source. Mine for Cesium-over-Three + chunking + R2 ADRs |

### 2.6 `change-log.md` — 10-change ledger

| # | Change | From → To |
|---|--------|-----------|
| 1 | Rendering engine | Three.js → CesiumJS |
| 2 | Data format | NetCDF direct → Zarr |
| 3 | Backend | Custom FastAPI → xpublish (Zarr REST + OPeNDAP + custom) — OPeNDAP line stale, corrected in cross-check |
| 4 | Deploy platform | Single Render → Vercel + Render split |
| 5 | Deploy cost | Paid $9.50 → Free $0 |
| 6 | Database | SQLite disk → Supabase Postgres |
| 7 | Zarr storage | Render disk → R2 |
| 8 | Backend role | Hot path → compute-only |
| 9 | Multi-account | Single → multiple Render workspaces |
| 10 | Frontend access | Backend proxy → direct R2+Supabase |

Cost evolution: $9.50 → $9.50 → **$0**. Unchanged throughout: CesiumJS, zarr-cesium, wind-layer, Plotly, d3-chromatic, React+Vite+TS, light theme, GLORYS12, argopy.

| Aspect | Detail |
|--------|--------|
| Assumptions | Change1-10 trace Three→Cesium, NetCDF→Zarr, paid→free, proxy→direct. zarr-cesium drop-in |
| Risks | Change3 cites `xpublish-opendap` as decision; corrected only later. Wind-layer kept though velocity provider replaces it |
| Verdict | Keep history. Fix Change3 OPeNDAP line |

### 2.7 `vercel-deployment.md` — frontend deploy

Valid: Vite preset, root `frontend/`, `vercel.json` rewrites + 1yr cache headers for `/cesium/*` + `/assets/*`, `vite-plugin-cesium` config, chunk splitting (cesium/plotly/react), ion token `VITE_CESIUM_ION_TOKEN`, env per-environment, deploy steps, free-tier limits, SPA 404 / Cesium 404 / ion token / EMFILE / CORS fixes.

Stale: code shows `fetchSST` via Render `/zarr/.zmetadata` backend-proxy — superseded by direct R2. `VITE_API_URL` preview per-PR Render URLs — superseded by compute-only backend.

| Aspect | Detail |
|--------|--------|
| Verdict | Keep frontend half. Patch backend-proxy snippet to direct-R2 `zarrClient.ts` |

### 2.8 `cesium-deployment.md` — Cesium notes

Valid: Workers/Assets/ThirdParty/Widgets sizes, `vite-plugin-cesium` + `CESIUM_BASE_URL`, 1yr cache headers, ion token + Allowed URLs, CORS middleware snippet, chunk splitting + ~15MB first load (~5MB wire) + Vercel gzip/brotli, 404/workers/EMFILE/terrain fixes.

Stale: self-host GEBCO on Render disk + `GeoTerrainProvider.fromUrl(backend/terrain/gebco/)` — no disk on free. Zarr chunks from Render backend CORS section — stale vs R2 direct.

| Aspect | Detail |
|--------|--------|
| Verdict | Keep frontend half. Drop disk-terrain path or move to R2-hosted terrain |

### 2.9–2.14 Superseded / reference-only

| File | Why superseded | Keep what |
|------|----------------|-----------|
| `deployment-architecture.md` | Paid Vercel+Render disk flow. Backend hot-path bottleneck. Contradicts free-tier direct | Nothing (diagram superseded). Drop or banner |
| `render-deployment.md` | Paid Starter 512MB/0.5CPU + disk. 512MB tight for xarray+marching cubes. No disk on free = data loss. Paid contradicts $0 | Nothing. Drop or banner |
| `render-blueprint.md` | Paid render.yaml disk Starter. Requires `xpublish-opendap` (nonexistent, use `xpublish-zarr`). PyVista/VTK heavy on 512MB | Nothing. Drop or banner |
| `pricing-analysis.md` | $9.50 prod (Starter $7 + 10GB disk $2.50). Recommends paid, ignores free R2+Supabase split. No egress math | Nothing. Drop or banner |
| `deployment-checklist.md` | Step checklist builds paid Starter+disk path. Troubleshooting says upgrade Starter/Standard | Checklist shape only. Rewrite for R2/Supabase/cron |
| `render-vs-alternatives.md` | Conclusion $9.50/mo contradicts free mandate. Ignores R2/Supabase split | **Matrix only** (Render vs Railway/Fly/Heroku/AWS). Drop conclusion |

---

## 3. Lakshya kills (ranked)

| # | Kill | Mechanism | Mitigation |
|---|------|-----------|------------|
| 1 | Render 512MB PyVista/VTK OOM | Marching cubes on 512MB/0.1CPU free kills Phase6 isosurface | scikit-image marching cubes (lighter); cache isosurfaces in R2; test early |
| 2 | Offline judging net-dependence | Vercel+R2+Supabase+ion all net, no pre-warm/recorded backup kills live demo | Pre-warm presets + offline assets + recorded backup after live attempt |
| 3 | Supabase 480/500MB tight + 1wk pause | Capacity overflow + wake latency kills Argo Phase5 | Metadata in PG, profiles overflow to R2 JSON; keep-warm ping |
| 4 | zarr-cesium v0.1.4 API churn / 14 issues / EPSG3857 | Core Phase2-4 render path breaks, fallback costs 2-3d | Phase 0 PoC mandatory; pin 0.2.0; zarrita fallback ready |
| 5 | R2 10GB overflow | GLORYS subset + isosurface cache growth kills time/depth range | Indian Ocean subset only; monthly only; aggressive compression |
| 6 | INCOIS-deployable vs public-cloud tension | F5 on-prem required, plan locked Vercel/R2/Supabase, no compose. Judging score hit | Document deliverable = Docker nginx+uvicorn+xpublish on INCOIS infra. Demo ≠ deliverable |
| 7 | Full-cube fetch OOM | No subset API/abort/downsample enforcement in phases → browser OOM | Adopt prem22k scope rule: bbox + 3-5 depths + 3-5 timesteps + 1 var; abort superseded; downsample-while-drag |
| 8 | 30s cold-start isosurface + time-slider-vs-fetch race | 15min spin-down + no low-res-first/abort → jank during demo | Keep-warm 08:00-18:00; preload low-res slice first; abort superseded |

---

## 4. Lakshya inventions (flag, don't cite externally)

| # | Claim | File | Fix |
|---|-------|------|-----|
| 1 | 48 stars / 5 forks / 3 contrib zarr-cesium, no access date; stale vs 39 mirror | cross-check Decision2 | Drop stars or re-date 2026-09-09: stars ~49, forks 5, open issues ~4, pushed 2026-09-08. Prefer version/API facts |
| 2 | 112 stars / 31 forks / 205 downloads cesium-wind-layer, no date | cross-check Decision3 | Same — date or drop |
| 3 | 40x faster than OPeNDAP/GRIB2, no source | approach-comparison, change-log Change#2, cross-check Decision4 | Cite Gowan 2022 / benchmark study doi:10.1002/essoar.10511054.2 or mark estimate |
| 4 | ~100KB chunk / ms latency / ~200ms / 60FPS / 10k particles, no device | free-tier-deployment, cesium-deployment | Mark estimate until locked-laptop run |
| 5 | CesiumGS officially recommends Vercel (2025 tutorials), no URL | approach-comparison Decision5, cross-check Decision8 | Add URLs or soften to "Vercel well-documented for Cesium" |
| 6 | R2 10GB fits 5 vars × Indian Ocean × 1-2mo, no byte math | free-tier-deployment | Add byte math in chunk ADR |
| 7 | Supabase 500MB fits 4000×100 profiles ~480MB JSONB compact, unproven tight | cross-check Decision6 | Measure; fallback R2 JSON ready |
| 8 | `xpublish-opendap` exists | render-blueprint requirements, change-log Change#2-3 | **False.** Real `xpublish-zarr`. Self-corrected in cross-check Decision9 only — fix callers |
| 9 | GLORYS12 1/12° / 50 levels primary + `cmems_mod_glo_phy_my_0.083deg_P1D-m` id, no card/sha256/provenance | change-log, render-deployment | Needs dataset card before M2 gate |
| 10 | Ion free tier sufficient, generous unspecified limits | cesium-deployment | Specify or mark assumption |
| 11 | Render 750hrs / 512MB / 0.1CPU / 15min idle / 30s cold start, no source date | free-tier-deployment, pricing-analysis | CONFIRMED 2026-09-09 via 9router — add access date |

## 5. Shared perf bible link (`docs/performance/optimization.md`)

Chunk/cache/prefetch/GPU methods feed lakshya gates. Dual chunking shapes + `lru_cache` isosurface + `tileCacheSize=1000` + prefetch-3 + KTX2 + progressive render. Cite in chunk ADR. Detail: `01-ps-authority-and-shared-canonical.md` §11a.

Next: `03-prem22k-product-science-track.md`.
