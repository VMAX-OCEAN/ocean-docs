# Lakshya Research — Deployment Plan (Vercel + Render)

This folder contains the complete research and deployment plan for hosting the
SIH-OCEAN 3D ocean visualization platform.

## Architecture: Frontend on Vercel, Backend on Render

| Component | Platform | Plan | Cost |
|---|---|---|---|
| Frontend (React + CesiumJS) | **Vercel** | Hobby (free) | $0 |
| Backend (FastAPI + xpublish) | **Render** | Starter | $7/mo |
| Zarr data + SQLite | **Render** persistent disk | 10 GB SSD | $2.50/mo |
| Terrain + imagery | **Cesium ion** | Free tier | $0 |
| **Total** | | | **$9.50/month** |

## Files

| File | Topic |
|---|---|
| [`deployment-architecture.md`](deployment-architecture.md) | How the 3-tier architecture maps onto Vercel + Render |
| [`vercel-deployment.md`](vercel-deployment.md) | Frontend deployment on Vercel (Vite, Cesium assets, SPA routing) |
| [`render-deployment.md`](render-deployment.md) | Backend deployment on Render (FastAPI, persistent disk, CORS) |
| [`render-blueprint.md`](render-blueprint.md) | Complete `render.yaml` Blueprint (Infrastructure as Code) |
| [`cesium-deployment.md`](cesium-deployment.md) | CesiumJS-specific notes (Ion token, assets, CORS, build size) |
| [`pricing-analysis.md`](pricing-analysis.md) | Cost breakdown — free tier, production, scale |
| [`deployment-checklist.md`](deployment-checklist.md) | Step-by-step deployment checklist |
| [`render-vs-alternatives.md`](render-vs-alternatives.md) | Render vs Railway vs Fly.io vs Heroku vs Vercel serverless |

## Quick Start

1. **Deploy backend on Render** (see [`render-blueprint.md`](render-blueprint.md))
   - Use `render.yaml` Blueprint for one-click deploy
   - Add persistent disk (10 GB) for Zarr + SQLite
   - Note the backend URL: `https://sih-ocean-backend.onrender.com`

2. **Deploy frontend on Vercel** (see [`vercel-deployment.md`](vercel-deployment.md))
   - Import repo, set Root Directory to `frontend/`
   - Set `VITE_API_URL` = Render backend URL
   - Set `VITE_CESIUM_ION_TOKEN` = your Cesium ion token
   - Note the frontend URL: `https://sih-ocean.vercel.app`

3. **Wire them together** (see [`deployment-checklist.md`](deployment-checklist.md))
   - Set `CORS_ORIGINS` on Render = Vercel frontend URL
   - Add Vercel URL to Cesium ion Allowed URLs
   - Test end-to-end

## Why Split Vercel + Render?

**Vercel for frontend:**
- Edge CDN for Cesium static assets (Workers, Assets, Widgets — fast globally)
- Preview deployments (every PR gets a unique URL)
- Free tier sufficient (100 GB bandwidth, unlimited static sites)
- First-class Vite framework detection

**Render for backend:**
- Persistent disk for Zarr data + SQLite (survives deploys)
- Native Python runtime (or Docker for complex deps)
- Always-on web service (no spin-down on Starter plan)
- `render.yaml` Blueprint for Infrastructure as Code

**Why not Vercel for backend?** Vercel serverless has 10-60s timeout (too short for
marching cubes), no persistent disk (SQLite/Zarr lost between invocations), and cold
starts on every request (bad for xarray).

**Why not Render for frontend?** Render static sites work but Vercel's edge CDN is
faster for global static delivery and has better preview deployment UX.
