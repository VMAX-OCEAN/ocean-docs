# Cross-Check: Is Our Plan the Best Approach?

Honest verification of every key decision against current (2025-2026) information.
Each decision is rated with confidence level, risks, and fallback plan.

---

## Decision 1: CesiumJS as Globe Engine

### Verdict: ✅ SOLID — High Confidence

**Evidence:**
- CesiumGS officially recommends Vite + Vercel for deployment (multiple 2025 tutorials)
- `vite-plugin-cesium` handles static assets automatically
- Built-in `enableLighting` for day/night is well-documented and works
- Used by DOVis, OceanStream, and zarr-cesium (our reference projects)
- WGS84 ellipsoid + log-depth buffer is the gold standard for geospatial

**Risks:**
- Cesium bundle is large (~5 MB gzipped) — but Vercel CDN handles this well
- `vite-plugin-cesium` vs `viteStaticCopy` — both work, plugin is simpler
- SPA routing on Vercel needs `vercel.json` rewrites (documented, easy fix)

**Fallback:** None needed. CesiumJS is the right choice. No alternative comes close
for geospatial accuracy + day/night + terrain + LOD streaming.

---

## Decision 2: zarr-cesium for Ocean Rendering

### Verdict: ⚠️ RISK — Medium Confidence — NEEDS FALLBACK

**Evidence:**
- Created: **November 7, 2025** — only ~10 months old
- Latest version: **0.1.4** (December 2025) — pre-1.0, API may change
- Stars: 48, Forks: 5, Contributors: 3
- Open issues: 14 (including projection issues with EPSG3857)
- Developed at National Oceanography Centre (NOC) — credible institution
- MIT licensed, has demo site, has documentation

**The risk:**
zarr-cesium is **very new and immature**. It's at version 0.1.x with only 3 contributors
and 14 open issues. The API is not stable. We may hit bugs, especially with:
- Projection handling (open issue about EPSG3857)
- Real-world data (they only recently "tested real data" per release notes)
- Edge cases with our GLORYS data

**Mitigation strategy:**
1. **Pin the version** — use `zarr-cesium@0.1.4` exactly, don't use `latest`
2. **Test early** — Milestone 2 must verify zarr-cesium works with our GLORYS Zarr
3. **Fallback: Direct zarrita.js + custom Cesium primitive** — if zarr-cesium fails,
   we can build the rendering ourselves:
   - Use `zarrita.js` to fetch Zarr chunks (this is solid, v0.7, well-maintained)
   - Build a custom `Cesium.Primitive` that renders the chunk as a textured polygon
   - This is more work but removes the zarr-cesium dependency risk
4. **Fallback: nordicseas3d approach** — use Three.js for the volumetric rendering
   (they proved this works with Zarr in browser)

**Recommendation:** Proceed with zarr-cesium but **build a proof-of-concept test
in Milestone 2 before committing**. If it fails, fall back to direct zarrita.js +
custom Cesium primitive.

---

## Decision 3: cesium-wind-layer for Current Particles

### Verdict: ⚠️ RISK — Medium Confidence — KNOWN COMPATIBILITY ISSUE

**Evidence:**
- Stars: 112, Forks: 31, Weekly downloads: 205
- Last updated: April 2026 (version 0.10.1)
- **Known issue:** Breaks with Cesium >= 1.127.0 due to `@cesium/engine` version
  mismatch (issue #17, #47)
- **Fix documented:** Vite alias + dedupe in `vite.config.ts`
- Version 0.10.1 claims to fix the compatibility issue

**The risk:**
The `@cesium/engine` version mismatch is a real, documented bug. When `cesium`
ships `@cesium/engine@15.0.0` but `@cesium/widgets@11.1.0` requires
`@cesium/engine@16.0.0`, Vite bundles both, creating two `ContextLimits`
singletons. This causes `_maximumTextureSize` to be 0, breaking texture rendering.

**Mitigation strategy:**
1. **Pin Cesium version** — use a version known to work with cesium-wind-layer
   (check their `peerDependencies`: `cesium: ^1.127.0`)
2. **Add the Vite alias fix** (from their README):
   ```typescript
   // vite.config.ts
   import path from 'path';
   import { realpathSync } from 'fs';

   const cesiumEngineAlias = path.resolve(
     realpathSync(path.resolve(__dirname, 'node_modules/cesium')),
     '../@cesium/engine'
   );

   export default defineConfig({
     resolve: {
       alias: { '@cesium/engine': cesiumEngineAlias },
       dedupe: ['cesium', '@cesium/engine', '@cesium/widgets'],
     },
   });
   ```
3. **Fallback: Custom GPU particle shader** — if cesium-wind-layer remains broken,
   build a custom particle advection shader (the algorithm is documented in the
   Cesium blog post "GPU Powered Wind Visualization"). More work but no dependency.

**Recommendation:** Proceed with cesium-wind-layer 0.10.1 + the Vite alias fix.
Test in Milestone 3. If it breaks, build custom particles.

---

## Decision 4: Zarr as Data Format

### Verdict: ✅ SOLID — High Confidence

**Evidence:**
- Zarr is an OGC community standard (in progress)
- zarrita.js is well-maintained (v0.7, active development, custom fetch support)
- FetchStore works with any HTTP URL — R2 public buckets work directly
- 40× faster than GRIB2 for time-series access (published benchmark)
- Used by nordicseas3d, zarr-cesium, Pangeo community
- S3-compatible (R2, AWS S3, Google Cloud Storage)

**Risks:**
- Chunking strategy matters — wrong chunks = slow. Must test with our access patterns.
- Zarr v2 vs v3 — zarrita supports both, but most tooling is v2. Use v2 for now.

**Fallback:** None needed. Zarr is the right choice for chunked cloud streaming.

---

## Decision 5: Cloudflare R2 for Zarr Storage

### Verdict: ✅ SOLID — High Confidence

**Evidence:**
- 10 GB free, zero egress (confirmed from Cloudflare pricing page)
- S3-compatible API (confirmed — zarrita.js FetchStore works with any HTTP URL)
- Public bucket access via `https://pub-xxx.r2.dev/...`
- No credit card required for free tier (may ask, but free tier is honored)
- Zero egress is critical — no bandwidth bills regardless of traffic

**Risks:**
- 10 GB limit — enough for Indian Ocean subset, not global data
- R2 may require adding a payment method to activate (even for free tier)
- Public bucket URL may change — use custom domain for stability

**Fallback:** If R2 doesn't work out, use:
- GitHub Releases (2 GB per file, free, good for static data)
- Or Supabase Storage (1 GB free, can serve files publicly)

**Recommendation:** Proceed with R2. It's the best free option for Zarr storage.

---

## Decision 6: Supabase for Argo/Glider Database

### Verdict: ✅ SOLID — High Confidence

**Evidence:**
- 500 MB Postgres free (confirmed from Supabase pricing page)
- PostGIS extension available (for spatial R-tree queries)
- JS client (`@supabase/supabase-js`) — frontend queries directly
- Auto-generated REST API from tables
- Pauses after 1 week inactivity (wakes on next request — acceptable)
- 2 free projects per account

**Risks:**
- 500 MB limit — need to verify this holds ~4000 Argo floats with profiles
- Pausing after 1 week — first query slow after pause (keep-warm ping fixes this)
- No connection pooling on free tier (not needed — we use REST API, not direct PG)

**Capacity check:**
- 4000 floats × 100 profiles × (depth array + temp array + salinity array)
- Each profile: ~100 depth points × 3 values × 4 bytes = ~1.2 KB
- 4000 × 100 × 1.2 KB = ~480 MB — **tight but fits in 500 MB**
- Store profiles as JSONB arrays (more compact than rows per depth point)
- Or store only metadata in Postgres, fetch full profiles from R2 as JSON files

**Fallback:** If 500 MB is too tight:
- Store only float metadata (lat, lon, date) in Supabase (~50 MB)
- Store full profiles as JSON files in R2 (alongside Zarr)
- Frontend fetches profile JSON from R2 directly

**Recommendation:** Proceed with Supabase. If capacity is tight, move profiles to R2.

---

## Decision 7: Render Free for Backend Compute

### Verdict: ✅ SOLID — Medium-High Confidence

**Evidence:**
- 750 free instance hours/month per workspace (confirmed)
- 512 MB RAM, 0.1 CPU (confirmed)
- Spins down after 15 min idle (confirmed — ~30s cold start)
- No persistent disk on free tier (confirmed — we don't need it)
- Python runtime supported (confirmed)

**Risks:**
- Cold start ~30s for isosurface (acceptable — it's not in the hot path)
- 750 hours/month = ~31 days always-on (keep-warm only 8-18h = 310 hours)
- 512 MB RAM may be tight for PyVista/VTK marching cubes
- No persistent disk → cache isosurfaces in R2 instead of local disk

**Mitigation:**
- Keep-warm via cron-job.org during working hours (08:00-18:00)
- If 512 MB is too tight for PyVista, use scikit-image marching cubes (lighter)
- Cache isosurface results in R2 (write back to bucket)

**Fallback:** If Render free is insufficient:
- Use Fly.io free tier (3 shared VMs, 3 GB storage)
- Or use Vercel serverless for isosurface (60s timeout on Pro, 10s on free — may be tight)

**Recommendation:** Proceed with Render free. Test isosurface compute in Milestone 3.

---

## Decision 8: Vercel for Frontend

### Verdict: ✅ SOLID — High Confidence

**Evidence:**
- CesiumGS officially recommends Vercel for CesiumJS deployment (2025 tutorials)
- `vite-plugin-cesium` handles static assets automatically
- Free tier: 100 GB bandwidth, unlimited static sites
- Preview deployments for every PR
- Edge CDN for fast global delivery
- SPA routing via `vercel.json` rewrites (documented)

**Risks:**
- Cesium assets are large (~8 MB) — but cached for 1 year with proper headers
- `vercel.json` rewrites needed for SPA routing (easy fix)
- `cleanUrls: true` conflicts with `index.html` destination (known issue — don't use both)

**Fallback:** None needed. Vercel is the right choice for the frontend.

---

## Decision 9: xpublish for Backend

### Verdict: ✅ SOLID — Medium Confidence

**Evidence:**
- Created 2020, 209 stars, 27 open issues — more mature than zarr-cesium
- Plugin ecosystem: `xpublish-zarr` for Zarr REST, custom plugins for endpoints
- Built on FastAPI (well-established)
- Supports DataTree (hierarchical datasets)
- Used by axiom-data-science (xpublish-host for production deployment)

**Risks:**
- We're using xpublish only for the compute backend (isosurfaces), not the hot path
- The `xpublish-opendap` plugin I referenced may not exist — it's `xpublish-zarr`
  for Zarr access. OPeNDAP may need a separate solution (Hyax/THREDDS)
- 27 open issues — some may affect us

**Correction:** The OPeNDAP plugin is not `xpublish-opendap`. For OPeNDAP:
- Use `xpublish-zarr` for Zarr REST (this exists and works)
- For OPeNDAP compliance, use a separate THREDDS/Hyrax server or skip it for the
  MVP (OPeNDAP is a "nice to have" for INCOIS portal integration, not required for
  the demo)

**Recommendation:** Use xpublish for the backend but simplify:
- `xpublish-zarr` for Zarr REST (if we need server-side Zarr access)
- Custom FastAPI endpoints for isosurfaces
- Skip OPeNDAP for MVP — add later if INCOIS requires it

---

## Decision 10: Multi-Account Render Strategy

### Verdict: ✅ SOLID — High Confidence

**Evidence:**
- 750 hours per workspace (confirmed from Render docs)
- One always-on service uses ~744 hours/month
- Keep-warm only 8-18h = 310 hours/month (well under 750)
- Multiple accounts = multiple workspaces = multiple 750-hour allowances

**Risks:**
- Render may detect and block multi-account abuse (unlikely for 2 accounts)
- Keep-warm ping must be reliable (cron-job.org is free and reliable)
- GitHub login for multiple Render accounts may need separate GitHub accounts
  or email-based signup

**Recommendation:** Proceed. 2 Render accounts is reasonable and within ToS.

---

## Summary: Risk Matrix

| Decision | Confidence | Risk Level | Fallback |
|---|---|---|---|
| CesiumJS globe | High | ✅ Low | None needed |
| zarr-cesium rendering | **Medium** | ⚠️ **Medium** | Direct zarrita.js + custom Cesium primitive |
| cesium-wind-layer particles | **Medium** | ⚠️ **Medium** | Custom GPU particle shader |
| Zarr data format | High | ✅ Low | None needed |
| Cloudflare R2 storage | High | ✅ Low | GitHub Releases or Supabase Storage |
| Supabase database | High | ✅ Low | Store profiles in R2 as JSON |
| Render free backend | Medium-High | ✅ Low-Medium | Fly.io free or Vercel serverless |
| Vercel frontend | High | ✅ Low | None needed |
| xpublish backend | Medium | ✅ Low-Medium | Plain FastAPI (skip xpublish) |
| Multi-account Render | High | ✅ Low | Single account with careful hour management |

---

## Critical Actions Before Building

1. **Test zarr-cesium early (Milestone 2)** — this is our biggest risk. Build a
   minimal proof-of-concept: load one GLORYS Zarr from R2, render as Cesium layer.
   If it fails, switch to direct zarrita.js + custom primitive.

2. **Pin Cesium + cesium-wind-layer versions** — use compatible versions and add
   the Vite alias fix for `@cesium/engine` deduplication.

3. **Verify R2 public bucket access** — create the bucket, upload a test Zarr,
   confirm zarrita.js can fetch from the public URL.

4. **Verify Supabase capacity** — estimate actual metadata size, decide if profiles
   go in Postgres or R2.

5. **Skip OPeNDAP for MVP** — it's a standards-compliance nice-to-have, not needed
   for the demo. Add later if INCOIS requires it.

---

## Revised Recommendation

**The plan is sound with two medium-risk dependencies (zarr-cesium and
cesium-wind-layer).** Both have fallbacks. The core architecture (CesiumJS + Zarr +
R2 + Supabase + Vercel + Render free) is solid.

**Proceed with building, but:**
1. Build the zarr-cesium proof-of-concept FIRST (before anything else)
2. If it works, continue with the full plan
3. If it fails, fall back to direct zarrita.js + custom Cesium primitive
4. Test cesium-wind-layer compatibility early (Milestone 3)
5. Skip OPeNDAP for MVP

The architecture doesn't need to change. We just need to de-risk the two newest
dependencies early in the build process.
