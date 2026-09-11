# 07 — Merged Build Plan + Dataset/ADR Gates + Deep-Research Queue

**Date:** 2026-09-09
**Formula:** Lakshya phases/gates/code + prem22k residual/scope/presets/cards/ADRs/mandates/outreach.
**Rule:** do not start next milestone until exit gate passes. No gate pass = no milestone pass.

---

## 1. Ordered sequence (Phase 0 → M1–M5)

### Phase 0 — de-risk, 1-2d

| Step | Verify | Fail → |
|------|--------|--------|
| R2 bucket + small GLORYS Indian Ocean Zarr upload | `curl` public URL `…/.zmetadata` | Fix bucket policy, retry |
| zarrita.js loads it from public URL | FetchStore open + chunk read | Fix CORS/URL, retry |
| ZarrLayerProvider renders SST | Overlay visible on globe | **Fallback: custom ImageryProvider + zarrita.js** (2-3d, CPU Canvas, slower but reliable) |
| Velocity particles animate | `ZarrCubeVelocityProvider` u/v advect | Fallback: cesium-wind-layer v0.11.0 + Vite alias/dedupe → custom GPU shader |
| Supabase browser queries work | `floats` select from browser | Fallback: R2 JSON for metadata |
| Cesium globe renders on Vercel | Clean-browser load | Fix `vite-plugin-cesium` + `vercel.json` rewrites |

**Exit gate:** all six ✅ or fallback confirmed. Re-pin zarr-cesium 0.2.0 (npm latest, pushed 2026-09-08) + Cesium ≥1.119. Test #13092 translucency at pin before ADR.

### M1 — globe + presets

Light-theme Cesium globe. Terrain + bathymetry + lighting + atmosphere. **Preset fly-to buttons only** (Bay Bengal eddy, Arabian Sea). No live geocoder.

| Gate item | Threshold |
|-----------|-----------|
| Frame rate | 60 FPS |
| Terminator | Visible scrub |
| Reload | Clean-browser pass |
| Empty bbox | Blocked-view message, never blank globe |
| Offline | Pre-warmed presets + assets |

### M2 — surface + time

GLORYS subset from R2. `ZarrLayerProvider` SST. Palette, min/max, log/linear, opacity as shader uniforms. Time scrub.

| Gate item | Threshold |
|-----------|-----------|
| Dataset cards | Checksum + license + bbox (glorys12 minimum) |
| Chunk ADR | Shape + device + sizes recorded |
| Slice load | ≤750 ms |
| Cold load | ≤10 s (locked laptop) |
| Colormap change | Instant (no re-fetch) |

### M3 — depth + currents

`ZarrCubeProvider` slices + curtain. Labeled exaggeration. `ZarrCubeVelocityProvider` particles depth + time bound. Isosurfaces server-side or precomputed + cached first. Browser volume deferred.

| Gate item | Threshold |
|-----------|-----------|
| Scope rule enforced | Enter 3D/4D requires bbox + 3-5 depths + 3-5 timesteps + 1 variable |
| Unlabeled block | Missing units / standard_name / missing-value rule / source version / ETag → blocked |
| Particles | Sync time + depth, re-seed on scrub |
| Isosurface | Cached in R2, cold start acceptable (keep-warm 08:00-18:00) |

### M4 — markers + residual

Supabase floats. Click → Plotly profile. Model-vs-obs residual panels.

| Gate item | Threshold |
|-----------|-----------|
| Residual | `residual = model − observation` on every compare panel |
| QC/method | Required, panel blocked if missing |
| Provenance | Dataset, variable, units, UTC, QC/mode, transform version on every sample |
| Arrow cutoff | Applied (<500 GeoJSON proposed, measure to lock) |
| Markers | ≤5000 at 30 FPS on locked laptop |
| Query | Bbox fast (<10ms target, measure) |

### M5 — polish + outreach

Deep links (layers + plots). Embed iframe. Guided tour (beginners) distinct from forecaster mode. Plugin registry. OPeNDAP facade scope note. Docker deliverable for INCOIS infra.

| Gate item | Threshold |
|-----------|-----------|
| Mandate beats | Hazard / SAR / fishery / climate each named on one beat, 90s dry run |
| Recorded backup | After live attempt, before judging |
| Compose | nginx + uvicorn + xpublish runs on INCOIS-like infra |
| ADRs | PyNIO-drop + Cesium-over-Three + OPeNDAP-facade written |
| Shareable view | Clean-browser reload with layers/plots restored |

---

## 2. Demo vs deliverable (resolve F5 tension)

| Aspect | Demo (judging) | Deliverable (INCOIS) |
|--------|----------------|----------------------|
| Frontend | Vercel free CDN | Docker nginx static |
| Chunks | R2 direct, zero egress | Zarr store HTTP/S3 on INCOIS infra |
| Metadata | Supabase direct | SQLite/Postgres on INCOIS infra |
| Compute | Render free (isosurface only) | Docker uvicorn + xpublish |
| Client install | Zero both | Zero both |
| WMS/WCS | Roadmap-only both | Roadmap-only until live |
| Doc owed | One page: demo≠deliverable mapping | Compose proof |

---

## 3. Dataset / ADR gates (no pass = no milestone pass)

| Gate | Requires | Blocks |
|------|----------|--------|
| M2 | Dataset cards (glorys12 minimum, then all 5) + chunk ADR (shape + device + sizes, dual-rep vs balanced verdict) | No M2 pass without card + ADR |
| M4 | Residual ADR (sign + QC/method gate + provenance fields) + Arrow cutoff ADR (feature count + Supabase bbox + R2 JSON fallback measure) | No M4 pass without both |
| M5 | PyNIO-drop ADR (one line: xarray netCDF4 backend covers F3) + Cesium-over-Three ADR (mine approach-comparison Shift 1 + tech-stack table) + OPeNDAP-facade ADR (scope: `xpublish-zarr` real, OPeNDAP via THREDDS/Hyrax separate or MVP-skip) | No M5 pass without all three |
| All | #13092 verification at pin (≥1.119) before version-pin ADR | No pin ADR without test |

**Card template (per `docs/data/README.md`):** source URL, access date, sha256, license, bbox, variables, ingest version, assumptions. One card per PS link: `glorys12.md`, `incois-las.md`, `argo.md`, `glider.md`, `insitu-collection.md` (unknown, do not invent).

---

## 4. Bbox + residual rules (paste on wall)

| Rule | Text |
|------|------|
| Scope | Enter 3D/4D requires bbox + 3-5 depths + 3-5 timesteps + 1 variable |
| Full-cube ban | 24×40×500×500 ≈ 0.96GB float32 never ships whole |
| Fetch | Abort superseded, preload low-res slice first, downsample-while-drag |
| Residual | `residual = model − observation` |
| QC gate | No residual without QC + method labels |
| Provenance | Dataset, variable, units, UTC, QC/mode, transform version every sample |
| Unlabeled | Missing units/standard_name/missing-value/source-version/ETag → blocked |
| Anomaly | Only with stated baseline |
| Empty bbox | Blocked message, never blank globe |

---

## 5. Kill mitigations (K1–K9 owner + action)

| Kill | Action | Owner |
|------|--------|-------|
| K1 full-cube OOM | Subset API + scope rule + abort + downsample | M2/M3 |
| K2 offline net-death | Pre-warm + offline assets + recorded backup | M1/M5 |
| K3 lib churn + #13092 | Pin 0.2.0 + ≥1.119, test at pin, fallback ready | Phase 0 |
| K4 PyVista OOM | scikit-image, R2 cache, test early | Phase 0/M3 |
| K5 Supabase tight + pause | PG metadata + R2 JSON profiles, keep-warm | M4 |
| K6 fly-vs-fetch jank | Low-res first + abort | M1/M3 |
| K7 empty-bbox blank | Presets-first + blocked message | M1 |
| K8 INCOIS tension | Demo≠deliverable + compose | M5 |
| K9 R2 overflow | IO subset + monthly + compression | M2 |

---

## 6. Scene arc 01→07 + mandate beats (R5 demo spine)

| Scene | Beat | Mandate slot |
|-------|------|--------------|
| 01 Enter | Global → Indian Ocean fly-to (preset) | Climate monitoring (basin context) |
| 02 Approach | Arabian Sea / Bay Bengal eddy preset | Hazard assessment (feature watch) |
| 03 Reality | SST + depth slice + curtain | Fishery advisories (SST/front) |
| 04 Grab | Float-as-anchor, click marker → profile | Search-and-rescue (currents + drift context) |
| 05 Compare | Model field + instrument profile co-viz | Climate / hazard (agreement check) |
| 06 Divergence | Residual = model − obs, QC/method shown | Forecaster verdict (<2 min) |
| 07 Investigate | Time scrub + trajectory + shareable view | Presenter handoff (guided tour) |

Mandate→beat final map owed in pitch doc (open item 3). Table above = starting proposal, not final. Each beat names one mandate aloud in 90s script.

---

## 7. Deep-research fan-out queue (`/deep-research` via 9router)

Tavily/search + tavily/fetch, exa fallback. Key via `$NINEROUTER_KEY`, never commit.

| # | Angle | Question | Unlocks |
|---|-------|----------|---------|
| 1 | zarr-cesium real-data proof | GLORYS Indian Ocean bbox from R2 via FetchStore? GPU colormap + cancel stale? Failure mode? | Phase 0 go/no-go |
| 2 | #13092 | Translucency camera jump status at 1.119 vs 1.142? Pin version? Repro with enableCollisionDetection=false? | Version-pin ADR |
| 3 | Esri target | Living Atlas vs EMU vs 3D Ocean Explorer? Stack? Drop assumption if unresolved? | Cite/drop decision |
| 4 | Chunk benchmark | GLORYS Zarr chunk shape for slice≤750ms + time scrub on locked laptop? Dual-rep vs balanced? Record device + sizes? | M2 chunk ADR |
| 5 | Arrow cutoff | GeoJSON vs Arrow cutoff feature count? <500 hold? Measure Supabase bbox + R2 JSON fallback? | M4 Arrow ADR |
| 6 | PyNIO ADR | PyNIO upstream dead? Confirm xarray netCDF4 backend covers F3? One-line ADR text? | M5 PyNIO ADR |
| 7 | WMS/WCS scope | F7 live vs roadmap? `xpublish-opendap``xpublish-opendap` exists (confirmed). Facade scope for M5? Label roadmap to avoid false compliance? | M5 facade ADR |
| 8 | Mandate beats | Hazard/SAR/fishery/climate → beats + datasets + presets? 90s script lines? | M5 pitch |

---

## 8. Lazier alternative + ceiling

Preset bbox + bounded 3-5 depths/timesteps replace live geocoder + full cube. Same demo effect, fewer deps.

`ponytail:` presets + bounded subsets ceiling now, upgrade when M1-M4 proven.
→ skipped: live geocoder, full volume, OPeNDAP live, glider/CTD/BGC beyond Argo. Add when M1-M4 proven + INCOIS requires.

---

## 9. Timelines reconciled

| Plan | Total | Note |
|------|-------|------|
| MILESTONES.md (shared) | 10-14d | M1 1-2d, M2 2-3d, M3 3-4d, M4 2-3d, M5 2d. No gates/fallbacks — add gates from this doc |
| revised-master-plan (lakshya) | 20-26d | Phase0 1-2d + Phases1-6 × 3-4d. Includes de-risk + currents + isosurface split. Use for resourcing |
| 01 win moves (prem22k) | M0→M5 ordered, no dates | Use for judging order, not scheduling |

Use MILESTONES for milestone names (M1-M5 match PS checklist). Use revised-master-plan for day counts (includes Phase 0 + split phases). Use 01 win moves for demo-day order.

---

## 10. Immediate next actions (ordered)

1. Phase 0 R2 bucket + test Zarr + zarr-cesium 0.2.0 retest (determines render path)
2. Verify #13092 at pin ≥1.119 (determines version ADR)
3. Write glorys12 dataset card (unlocks M2)
4. Lock reference laptop (unlocks all benchmarks)
5. Run chunk benchmark + record (unlocks chunk ADR)
6. Write Cesium-over-Three ADR from approach-comparison Shift 1 (cheap, unblocks F1 story)
7. Banner 6 superseded/stale docs (cheap, stops confusion)
8. Draft mandate→beat map + 90s script skeleton (unblocks pitch)
9. Facade note only (xpublish-opendap real; never claim WMS/WCS live)
10. Fan out deep-research queue 1-8
11. ~~Rewrite mermaid sign in 3 files to canonical~~ DONE 2026-09-10 (observed; attribution unknown). Verify no panel code uses `O − M` before M4 (K10)
12. Adopt P0–P7 ladder + citation classes + motion test (K15–K17, zero cost)

13. Cite `docs/performance/optimization.md` methods in chunk ADR (dual shapes + lru_cache + tileCacheSize + prefetch-3 + KTX2 + progressive).

Coverage closed: 74/74 stems mapped via 01 §11 + 02 §5 + 03 §5. No new gates.

End of comparison. Start at Phase 0.
