# 100% Free Deployment Plan — Zero Cost

Complete deployment strategy using **only free tiers** — no payment method required.

> **Total cost: $0/month, forever.**

---

## The Key Insight

Render's free tier has **no persistent disk** — data is lost on every redeploy. But
we don't need the backend to store data at all. We split the data out:

| Data | Free Service | How browser accesses |
|---|---|---|
| Zarr chunks (ocean arrays) | **Cloudflare R2** (10 GB free) | **Directly** — browser fetches from R2 public URL, no backend |
| Argo/Glider metadata | **Supabase** (500 MB Postgres free) | **Directly** — frontend queries Supabase JS client |
| Isosurface compute | **Render free** web service | On-demand — only when user requests isosurface |
| OPeNDAP (if needed) | **Render free** web service | On-demand — standards compliance |

**The backend becomes nearly unnecessary for the hot path.** Zarr chunks stream from
R2 directly to the browser. Supabase handles metadata queries directly. The Render
backend is only for occasional isosurface computation.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  USER BROWSER                                                    │
│  React + CesiumJS + zarrita.js + Supabase JS client             │
└────────────────────────────┬─────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼

┌─────────────────┐ ┌──────────────┐ ┌─────────────────────┐
│  VERCEL (free)   │ │ CLOUDFLARE R2 │ │  SUPABASE (free)    │
│  Frontend SPA    │ │ (free, 10 GB) │ │  (free, 500 MB)    │
│                  │ │               │ │                     │
│  React + Vite +  │ │ Zarr chunks   │ │ Argo/Glider metadata│
│  CesiumJS       │ │ (ocean data)  │ │ (Postgres + R-tree) │
│                  │ │               │ │                     │
│  CDN-served      │ │ Zero egress   │ │ Direct JS client    │
│  vercel.app URL  │ │ S3-compatible │ │ supabase.co URL    │
└─────────────────┘ └───────────────┘ └─────────────────────┘
                             │
                             │ (browser fetches Zarr chunks directly from R2)
                             │ (browser queries Supabase directly)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  RENDER (free) — only for compute, not data storage              │
│  ─────────────────────────────────────────────                   │
│  Web Service (free, 512 MB RAM, 0.1 CPU)                        │
│  Spins down after 15 min idle (~30s cold start)                 │
│  750 instance hours/month per workspace                         │
│                                                                  │
│  Endpoints:                                                      │
│  ├── /isosurface  → marching cubes (PyVista) — on demand       │
│  ├── /opendap     → OPeNDAP (standards) — on demand             │
│  └── /health      → health check                                │
│                                                                  │
│  NO persistent disk — reads Zarr from R2, writes cache to R2    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Service Breakdown

### 1. Vercel (Frontend) — FREE

| Aspect | Value |
|---|---|
| Plan | Hobby ($0) |
| Bandwidth | 100 GB/month |
| Build minutes | 6000/month |
| Static sites | Unlimited |
| Preview deploys | Every PR |
| Custom domain | 1 (free) |

**What it serves:** React + CesiumJS SPA, static assets (Workers, Assets, Widgets)

### 2. Cloudflare R2 (Zarr Data) — FREE

| Aspect | Value |
|---|---|
| Storage | 10 GB/month free |
| Egress | **Free** (zero egress fees — this is huge) |
| Class A ops (writes) | 1 million/month |
| Class B ops (reads) | 10 million/month |
| S3-compatible | Yes — zarrita.js works directly |

**What it stores:** GLORYS Zarr stores (chunked ocean arrays). Browser fetches chunks
directly from R2 public bucket URL — no backend involved in the hot path.

**10 GB capacity:** Enough for ~5 GLORYS variables × Indian Ocean subset × 1-2 months
of daily data (compressed Zarr chunks are small).

### 3. Supabase (Database) — FREE

| Aspect | Value |
|---|---|
| Plan | Free ($0) |
| Database size | 500 MB |
| Disk | 1 GB |
| Egress | 5 GB/month |
| API requests | Unlimited |
| Pauses after | 1 week inactivity (wakes on next request) |
| Projects | 2 free projects |

**What it stores:** Argo/Glider float metadata + profile data (Postgres with R-tree
spatial index). Frontend queries directly via Supabase JS client — no backend needed.

**500 MB capacity:** Enough for ~4000 Argo floats × ~100 profiles each × metadata.
Profile data (depth + temp arrays) can be stored as JSONB or in a separate table.

### 4. Render (Backend Compute) — FREE

| Aspect | Value |
|---|---|
| Plan | Free ($0) |
| RAM | 512 MB |
| CPU | 0.1 |
| Spins down | After 15 min idle (~30s cold start) |
| Instance hours | 750/month per workspace |
| Persistent disk | **No** (reads from R2, writes cache to R2) |

**What it does:** Only the things that can't be done in the browser:
- Isosurface computation (marching cubes via PyVista) — on demand
- OPeNDAP endpoints (standards compliance) — on demand
- Data ingestion scripts (run via SSH or initial deploy hook)

**Not in the hot path:** The browser fetches Zarr from R2 and metadata from Supabase
directly. The Render backend is only called when the user requests an isosurface.

---

## Multi-Account Render Strategy (if needed)

If you need multiple backend services (e.g., separate isosurface + OPeNDAP), use
multiple Render accounts (workspaces). Each workspace gets its own 750 free hours.

> **Note:** Render's free hours are per **workspace**, not per service. One always-on
> service uses ~744 hours/month. Two always-on services would need ~1488 hours — over
> the 750 limit. **Multiple workspaces (accounts) each get their own 750 hours.**

### Keep-warm strategy (to avoid cold starts)

Use a free cron service (cron-job.org) to ping the Render service during working hours:

```
08:00-18:00 → ping every 14 minutes (keeps service warm)
18:00-08:00 → no ping (service sleeps, saves hours)

10 hours/day × 31 days = 310 hours/month (well under 750)
```

This leaves 440 hours for a second service in the same workspace if needed.

### Multi-account layout (if needed)

| Account | Service | Purpose | Hours/month |
|---|---|---|---|
| Account 1 | `sih-ocean-compute` | Isosurface + OPeNDAP | ~310 (keep-warm 8-18) |
| Account 2 | `sih-ocean-ingest` | Data ingestion (cron) | ~50 (occasional) |

---

## Data Flow (Runtime) — Zero Backend in Hot Path

### 1. Page load
```
Browser → Vercel CDN → index.html + JS + Cesium assets
         (~2-3s first paint)
```

### 2. Globe render
```
Browser → Cesium ion API → terrain + imagery tiles
         (Cesium ion free tier, no backend)
```

### 3. SST overlay load (NO BACKEND!)
```
Browser → Cloudflare R2 public URL → Zarr .zmetadata
         → zarrita.js reads metadata
Browser → Cloudflare R2 public URL → Zarr chunk (thetao/0.1.2.3)
         → ~100 KB, ms latency, zero egress cost
         → GPU texture → Cesium renders SST overlay
```

### 4. Argo markers (NO BACKEND!)
```
Browser → Supabase REST API → SELECT * FROM floats WHERE bbox...
         → Supabase JS client (direct, no backend)
         → JSON markers
```

### 5. Argo profile (NO BACKEND!)
```
Browser → Supabase REST API → SELECT * FROM profiles WHERE float_id=...
         → Supabase JS client (direct)
         → Plotly renders depth-vs-temp chart
```

### 6. Isosurface (ONLY backend call)
```
Browser → Render free service → /isosurface?var=thetao&value=20
         → Backend reads Zarr from R2 (S3 API)
         → PyVista marching cubes
         → Returns glTF mesh
         → Cesium renders 3D primitive
         (Cold start ~30s if service was sleeping; ~500ms if warm)
```

---

## Why This Works (and Why It's Better)

### Traditional approach (needs paid disk)
```
Browser → Backend → Disk (Zarr + SQLite) → Backend → Browser
         (backend is bottleneck, needs persistent disk = $)
```

### Free-tier approach (no backend in hot path)
```
Browser → R2 (Zarr chunks directly)     ← zero egress, ms latency
Browser → Supabase (metadata directly)  ← direct JS client
Browser → Render (only for isosurface)  ← occasional, can cold-start
```

**Benefits:**
- **$0/month** — no paid services
- **Faster** — R2 CDN + Supabase direct are faster than a Render backend
- **Scalable** — R2 and Supabase handle concurrent reads natively
- **No cold-start penalty** for the hot path (R2 + Supabase are always on)
- **Backend only for compute** — isosurface is occasional, cold start acceptable

---

## Setup Guide

### Step 1: Cloudflare R2 (Zarr storage)

1. Sign up at https://dash.cloudflare.com (free, no credit card for R2)
2. R2 → Create bucket → `sih-ocean-zarr`
3. Settings → Public access → Enable (or use custom domain)
4. Note the public URL: `https://pub-xxx.r2.dev/sih-ocean-zarr/`
5. Upload Zarr stores:
   ```bash
   # Using rclone or aws-cli with R2 S3-compatible API
   aws s3 sync data/zarr/ s3://sih-ocean-zarr/ \
     --endpoint-url=https://xxx.r2.cloudflarestorage.com
   ```

### Step 2: Supabase (Argo/Glider database)

1. Sign up at https://supabase.com (free, GitHub login)
2. New Project → `sih-ocean`
3. Note the URL: `https://xxx.supabase.co`
4. Note the anon key: `eyJxxx...`
5. Create tables:
   ```sql
   -- In Supabase SQL Editor
   CREATE TABLE floats (
     wmo INTEGER,
     cycle INTEGER,
     latitude REAL,
     longitude REAL,
     date TEXT,
     variables TEXT
   );

   CREATE TABLE profiles (
     wmo INTEGER,
     cycle INTEGER,
     depth REAL[],
     temperature REAL[],
     salinity REAL[]
   );

   -- Enable PostGIS for spatial queries
   CREATE EXTENSION postgis;
   ALTER TABLE floats ADD COLUMN geom geometry(Point, 4326);
   CREATE INDEX floats_geom ON floats USING GIST(geom);
   ```

### Step 3: Render (backend compute)

1. Sign up at https://render.com (free, GitHub login)
2. New → Web Service → Connect repo `VMAX-OCEAN/ocean-docs`
3. Settings:
   - Name: `sih-ocean-compute`
   - Runtime: Python 3
   - Root: `backend/`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Plan: **Free**
4. Environment variables:
   - `R2_BUCKET` = `sih-ocean-zarr`
   - `R2_ENDPOINT` = `https://xxx.r2.cloudflarestorage.com`
   - `R2_ACCESS_KEY` = (from R2 API tokens)
   - `R2_SECRET_KEY` = (from R2 API tokens)
   - `SUPABASE_URL` = `https://xxx.supabase.co`
   - `SUPABASE_KEY` = (anon key)
   - `CORS_ORIGINS` = `https://sih-ocean.vercel.app`

### Step 4: Vercel (frontend)

1. Sign up at https://vercel.com (free, GitHub login)
2. New Project → Import `VMAX-OCEAN/ocean-docs`
3. Root Directory: `frontend/`
4. Environment variables:
   - `VITE_CESIUM_ION_TOKEN` = (Cesium ion token)
   - `VITE_R2_URL` = `https://pub-xxx.r2.dev/sih-ocean-zarr`
   - `VITE_SUPABASE_URL` = `https://xxx.supabase.co`
   - `VITE_SUPABASE_ANON_KEY` = `eyJxxx...`
   - `VITE_API_URL` = `https://sih-ocean-compute.onrender.com`
5. Deploy

### Step 5: Keep-warm (optional)

1. Sign up at https://cron-job.org (free)
2. Create cronjob:
   - URL: `https://sih-ocean-compute.onrender.com/health`
   - Schedule: every 14 minutes, hours 8-18
   - This keeps the Render service warm during working hours

---

## Frontend Code Changes (for R2 + Supabase direct)

### Zarr from R2 (no backend)
```typescript
// src/api/zarrClient.ts
import { openArray } from 'zarrita';

const R2_URL = import.meta.env.VITE_R2_URL;

// Open Zarr store directly from R2 public URL
const store = await openArray({
  store: 'http',
  url: `${R2_URL}/glorys_temp.zarr`,
  mode: 'r'
});

// Fetch a chunk — goes directly to R2, no backend
const chunk = await store.get([0, 10, 540, 1080]);
```

### Supabase direct (no backend)
```typescript
// src/api/supabaseClient.ts
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
);

// Query Argo floats in view — direct to Supabase, no backend
export async function getFloatsInBbox(west, south, east, north) {
  const { data, error } = await supabase
    .from('floats')
    .select('wmo, cycle, latitude, longitude, date, variables')
    .filter('latitude', 'gte', south)
    .filter('latitude', 'lte', north)
    .filter('longitude', 'gte', west)
    .filter('longitude', 'lte', east);
  return data;
}

// Get profile — direct to Supabase
export async function getProfile(wmo, cycle) {
  const { data } = await supabase
    .from('profiles')
    .select('depth, temperature, salinity')
    .eq('wmo', wmo)
    .eq('cycle', cycle)
    .single();
  return data;
}
```

### Isosurface (only backend call)
```typescript
// src/api/isosurface.ts
const API_URL = import.meta.env.VITE_API_URL;

export async function getIsosurface(variable, value, time) {
  const response = await fetch(
    `${API_URL}/isosurface?var=${variable}&value=${value}&t=${time}`
  );
  return response.json();  // glTF mesh
}
```

---

## Limitations & Mitigations

| Limitation | Impact | Mitigation |
|---|---|---|
| Render spins down after 15 min | Isosurface cold start ~30s | Keep-warm cron during working hours |
| Render 750 hours/month | ~31 days always-on | Keep-warm only 8-18h = 310 hours |
| R2 10 GB limit | ~2 months GLORYS data | Use monthly data only; compress aggressively |
| Supabase 500 MB | ~4000 floats with metadata | Store profiles as JSONB arrays (compact) |
| Supabase pauses after 1 week | First query slow after pause | Keep-warm ping (same cron) |
| No Render persistent disk | No server-side cache | Cache isosurfaces in R2 (write back) |
| Cesium ion free tier | Rate limits on terrain tiles | Self-host GEBCO terrain on R2 if needed |

---

## Cost Summary

| Service | Plan | Cost |
|---|---|---|
| Vercel (frontend) | Hobby | $0 |
| Cloudflare R2 (Zarr) | Free (10 GB) | $0 |
| Supabase (database) | Free (500 MB) | $0 |
| Render (compute) | Free (750 hrs) | $0 |
| Cesium ion (terrain) | Free | $0 |
| cron-job.org (keep-warm) | Free | $0 |
| **Total** | | **$0/month** |

All services have generous free tiers that are **permanently free** (not trials).
No credit card required for any of them (R2 may ask but free tier is honored).
