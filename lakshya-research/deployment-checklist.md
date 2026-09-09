# Deployment Checklist — Step by Step

Complete checklist for deploying SIH-OCEAN on Vercel (frontend) + Render (backend).

---

## Prerequisites

- [ ] GitHub repo: `VMAX-OCEAN/ocean-docs` (already done)
- [ ] Cesium ion account: https://ion.cesium.com/signup (free)
- [ ] Cesium ion access token (copy from Access Tokens page)
- [ ] Copernicus Marine account: https://data.marine.copernicus.eu/ (free, for data download)
- [ ] Vercel account: https://vercel.com/signup (free, sign in with GitHub)
- [ ] Render account: https://render.com/signup (free, sign in with GitHub)

---

## Phase 1: Deploy Backend on Render

### 1.1 Create the Web Service
- [ ] Go to Render Dashboard → New → **Web Service**
- [ ] Connect GitHub repo: `VMAX-OCEAN/ocean-docs`
- [ ] Settings:
  - Name: `sih-ocean-backend`
  - Runtime: **Python 3** (or Docker if PyVista needs system deps)
  - Region: **Oregon** (or closest)
  - Branch: `main`
  - Root Directory: `backend/`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
  - Plan: **Starter** ($7/month)
- [ ] Click **Create Web Service**

### 1.2 Add Persistent Disk
- [ ] In the service → Disks → **Add Disk**
  - Name: `ocean-data`
  - Mount Path: `/var/data`
  - Size: **10 GB**
- [ ] Save (triggers redeploy)

### 1.3 Set Environment Variables
- [ ] In the service → Environment:
  - `ZARR_DATA_PATH` = `/var/data/zarr`
  - `SQLITE_PATH` = `/var/data/sqlite/ocean.db`
  - `CACHE_PATH` = `/var/data/cache`
  - `PYTHONPATH` = `/opt/render/project/src`
  - `CESIUM_ION_TOKEN` = (your Cesium ion token)
  - `CORS_ORIGINS` = (leave empty for now — set after Vercel deploys)

### 1.4 Wait for Deploy
- [ ] Watch the build logs
- [ ] Verify health check: `curl https://sih-ocean-backend.onrender.com/health`
- [ ] Note the backend URL: `https://sih-ocean-backend.onrender.com`

### 1.5 Upload Sample Data
- [ ] SSH into the service (Render → Shell)
- [ ] Run: `python scripts/download_samples.py`
- [ ] Verify: `ls /var/data/zarr/` (should see GLORYS Zarr stores)
- [ ] Verify: `curl https://sih-ocean-backend.onrender.com/glorys_temp/zarr/.zmetadata`

---

## Phase 2: Deploy Frontend on Vercel

### 2.1 Create the Project
- [ ] Go to Vercel Dashboard → **New Project**
- [ ] Import repo: `VMAX-OCEAN/ocean-docs`
- [ ] Configure:
  - Framework Preset: **Vite** (auto-detected)
  - Root Directory: `frontend/`
  - Build Command: `npm run build` (auto-detected)
  - Output Directory: `dist` (auto-detected)
- [ ] Click **Deploy** (initial deploy with placeholder env vars)

### 2.2 Set Environment Variables
- [ ] In Vercel → Project → Settings → Environment Variables:
  - `VITE_CESIUM_ION_TOKEN` = (your Cesium ion token) — Production + Preview
  - `VITE_API_URL` = `https://sih-ocean-backend.onrender.com` — Production
  - `VITE_API_URL` = `http://localhost:8000` — Development

### 2.3 Add vercel.json
- [ ] Ensure `frontend/vercel.json` exists (SPA rewrites + cache headers)
- [ ] Push to GitHub → triggers redeploy

### 2.4 Redeploy
- [ ] Vercel → Deployments → Redeploy (to pick up new env vars)
- [ ] Wait for build (~2-3 min)
- [ ] Note the frontend URL: `https://sih-ocean.vercel.app` (or `https://ocean-docs.vercel.app`)

### 2.5 Verify Frontend
- [ ] Open the Vercel URL in browser
- [ ] Globe should render with terrain + imagery
- [ ] Day/night terminator should be visible
- [ ] Open browser console — check for errors

---

## Phase 3: Wire Frontend ↔ Backend

### 3.1 Update CORS on Render
- [ ] Render → sih-ocean-backend → Environment:
  - `CORS_ORIGINS` = `https://sih-ocean.vercel.app,https://ocean-docs.vercel.app`
- [ ] Save (triggers backend redeploy)

### 3.2 Update Cesium ion Allowed URLs
- [ ] Cesium ion Dashboard → Access Tokens → Edit your token:
  - Allowed URLs: `https://sih-ocean.vercel.app/*`
  - Add: `https://*-sih-ocean.vercel.app/*` (for preview deployments)
- [ ] Save

### 3.3 Test End-to-End
- [ ] Open `https://sih-ocean.vercel.app`
- [ ] Globe renders ✓
- [ ] Select "Temperature" variable → SST overlay loads ✓
- [ ] Time slider works → animation plays ✓
- [ ] Colorbar editor works → palette changes instantly ✓
- [ ] Depth slider works → 3D slice renders ✓
- [ ] Current particles animate ✓
- [ ] Argo markers visible ✓
- [ ] Click Argo marker → profile chart appears ✓
- [ ] Open browser console — no CORS errors ✓
- [ ] Open Network tab — Zarr chunks loading from Render ✓

---

## Phase 4: Custom Domain (Optional)

### 4.1 Vercel Custom Domain
- [ ] Vercel → Project → Settings → Domains
- [ ] Add: `ocean.yourdomain.com` (or similar)
- [ ] Update DNS: CNAME `ocean` → `cname.vercel-dns.com`
- [ ] Wait for SSL (auto-provisioned by Vercel)

### 4.2 Render Custom Domain
- [ ] Render → sih-ocean-backend → Settings → Custom Domains
- [ ] Add: `api.ocean.yourdomain.com`
- [ ] Update DNS: CNAME `api.ocean` → `sih-ocean-backend.onrender.com`
- [ ] Wait for SSL (auto-provisioned by Render)

### 4.3 Update Env Vars
- [ ] Vercel: `VITE_API_URL` = `https://api.ocean.yourdomain.com`
- [ ] Render: `CORS_ORIGINS` = `https://ocean.yourdomain.com`
- [ ] Cesium ion: Add `https://ocean.yourdomain.com/*` to Allowed URLs
- [ ] Redeploy both

---

## Phase 5: Monitoring

### 5.1 Render Monitoring
- [ ] Render Dashboard → sih-ocean-backend → Metrics
  - CPU usage (should be <50% on Starter)
  - Memory usage (should be <400 MB of 512 MB)
  - Response times (should be <200ms for Zarr chunks)
- [ ] Set up alerts: Render → Settings → Alerts (email on deploy failure)

### 5.2 Vercel Monitoring
- [ ] Vercel Dashboard → Project → Analytics
  - Bandwidth usage (should be <100 GB/month on free tier)
  - Build minutes (should be <6000/month)
- [ ] Vercel → Project → Speed Insights (Core Web Vitals)

### 5.3 Cesium ion Monitoring
- [ ] Cesium ion Dashboard → Usage
  - Tile requests per month
  - Asset storage used

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Frontend loads but no data | CORS blocking or backend down | Check CORS_ORIGINS, verify backend health |
| Cesium "default token" warning | VITE_CESIUM_ION_TOKEN not set | Set env var in Vercel, redeploy |
| 404 on SPA routes | Missing vercel.json rewrites | Add vercel.json with rewrites to index.html |
| Cesium assets 404 | vite-plugin-cesium not installed | `npm install vite-plugin-cesium` |
| Backend spins down (Free tier) | 15 min inactivity | Upgrade to Starter ($7/mo) |
| Zarr chunks slow | Disk I/O or network | Check Render region, consider CDN |
| Isosurface timeout | CPU too low | Upgrade to Standard ($25/mo) |
| EMFILE too many open files | Cesium import issue | Dynamic import: `await import('cesium')` |
