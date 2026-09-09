# Lakshya Research — Deployment Plan

Complete research and deployment plan for hosting the SIH-OCEAN 3D ocean
visualization platform — **100% free**, no payment required.

## Architecture: 100% Free Tier

| Component | Platform | Cost |
|---|---|---|
| Frontend (React + CesiumJS) | **Vercel** (Hobby) | $0 |
| Zarr data (ocean arrays) | **Cloudflare R2** (10 GB free, zero egress) | $0 |
| Argo/Glider database | **Supabase** (500 MB Postgres free) | $0 |
| Isosurface compute | **Render** (free web service) | $0 |
| Terrain + imagery | **Cesium ion** (free) | $0 |
| Keep-warm cron | **cron-job.org** (free) | $0 |
| **Total** | | **$0/month** |

### Key Insight: No Backend in the Hot Path

The browser fetches data **directly** from R2 and Supabase — no Render backend
needed for the hot path. The backend is only for occasional isosurface compute.

```
Browser → R2 (Zarr chunks directly)      ← zero egress, ms latency
Browser → Supabase (metadata directly)   ← direct JS client
Browser → Render (only for isosurface)    ← occasional, cold start OK
```

## Files

| File | Topic |
|---|---|
| [`free-tier-deployment.md`](free-tier-deployment.md) | **100% free plan** — R2 + Supabase + Render free (PRIMARY) |
| [`deployment-architecture.md`](deployment-architecture.md) | Architecture diagram + data flow |
| [`vercel-deployment.md`](vercel-deployment.md) | Frontend on Vercel (Vite, Cesium assets, SPA routing) |
| [`render-deployment.md`](render-deployment.md) | Backend on Render (paid — for reference) |
| [`render-blueprint.md`](render-blueprint.md) | render.yaml Blueprint (paid — for reference) |
| [`cesium-deployment.md`](cesium-deployment.md) | CesiumJS notes (Ion token, assets, CORS, build size) |
| [`pricing-analysis.md`](pricing-analysis.md) | Cost breakdown (free vs paid) |
| [`deployment-checklist.md`](deployment-checklist.md) | Step-by-step checklist |
| [`render-vs-alternatives.md`](render-vs-alternatives.md) | Render vs alternatives comparison |

## Quick Start (Free Tier)

1. **Cloudflare R2** — store Zarr data (10 GB free, zero egress)
2. **Supabase** — store Argo/Glider metadata (500 MB Postgres free)
3. **Render** — deploy backend for isosurface compute (free, spins down)
4. **Vercel** — deploy frontend (free, CDN)
5. **cron-job.org** — keep Render warm during working hours (free)

See [`free-tier-deployment.md`](free-tier-deployment.md) for complete setup guide.

## Multi-Account Render (if needed)

Render gives 750 free hours per **workspace** (account). One always-on service uses
~744 hours. If you need multiple backend services, use multiple Render accounts:

| Account | Service | Purpose |
|---|---|---|
| Account 1 | `sih-ocean-compute` | Isosurface + OPeNDAP |
| Account 2 | `sih-ocean-ingest` | Data ingestion (cron) |

Keep-warm only during working hours (08:00-18:00) to stay under 750 hours/month.

## Paid Alternative (for reference)

If you later want always-on backend with persistent disk:
- Vercel free + Render Starter ($7/mo) + 10 GB disk ($2.50/mo) = **$9.50/month**

See [`pricing-analysis.md`](pricing-analysis.md) for details.
