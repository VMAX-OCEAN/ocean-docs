# Vercel Deployment — Frontend Strategy

Complete deployment plan for the SIH-OCEAN **frontend** on Vercel.

> **Architecture:** Frontend on Vercel (this document), Backend on Render
> (see [`render-deployment.md`](render-deployment.md)).

---

## Why Vercel for the Frontend

| Requirement | Vercel support |
|---|---|
| React + Vite + TypeScript SPA | First-class framework detection |
| CesiumJS static assets (Workers, Assets, Widgets) | Static file serving via CDN |
| Fast global delivery | Edge network (CDN) — Cesium tiles load fast |
| Preview deployments | Every PR gets a unique URL |
| Auto-deploy from GitHub | Push → build → deploy automatically |
| Custom domains + HTTPS | Built-in (Let's Encrypt) |
| Environment variables | Per-environment (dev/preview/production) |
| Free tier | Generous (100 GB bandwidth, unlimited static sites) |

---

## Project Configuration

### Vercel Project Settings

| Setting | Value |
|---|---|
| Framework Preset | **Vite** (auto-detected) |
| Root Directory | `frontend/` |
| Build Command | `npm run build` (auto-detected) |
| Output Directory | `dist` (auto-detected) |
| Install Command | `npm install` (auto-detected) |
| Node.js Version | 18.x or 20.x |

### vercel.json (SPA routing + Cesium assets)

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "rewrites": [
    {
      "source": "/((?!api/).*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/cesium/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    },
    {
      "source": "/assets/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
```

**Key points:**
- The `rewrites` rule sends all non-API routes to `index.html` (SPA routing)
- Cesium static assets (Workers, Assets, Widgets) get 1-year cache headers
- Do NOT use `cleanUrls: true` with the `index.html` destination (causes 404s)

---

## CesiumJS Static Assets

CesiumJS requires static files (WASM workers, SVG icons, widget CSS) to be hosted
alongside the app. Use `vite-plugin-cesium` to handle this automatically:

### vite.config.ts

```typescript
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import cesium from 'vite-plugin-cesium';
import { viteStaticCopy } from 'vite-plugin-static-copy';
import path from 'path';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [
      react(),
      cesium(),  // Handles Cesium static assets + CESIUM_BASE_URL
    ],
    base: '/',  // Critical for Vercel — must be root
    build: {
      outDir: 'dist',
      assetsInlineLimit: 0,  // Don't inline Cesium assets
      chunkSizeWarningLimit: 1600,  // Cesium is a large chunk
    },
    define: {
      // Inject Cesium Ion token at build time
      'import.meta.env.VITE_CESIUM_ION_TOKEN': JSON.stringify(env.VITE_CESIUM_ION_TOKEN),
      // Backend URL (Render)
      'import.meta.env.VITE_API_URL': JSON.stringify(env.VITE_API_URL),
    },
    server: {
      proxy: {
        '/api': env.VITE_API_URL || 'http://localhost:8000',
      }
    }
  };
});
```

### Alternative: vite-plugin-cesium-engine (newer, zero-config)

```typescript
import { cesiumEngine } from 'vite-plugin-cesium-engine';

export default defineConfig({
  plugins: [
    react(),
    cesiumEngine({
      // Auto-reads CESIUM_ION_TOKEN from .env
      // Per-environment tokens supported
      ionToken: {
        development: process.env.CESIUM_ION_TOKEN_DEV,
        production: process.env.CESIUM_ION_TOKEN_PROD,
      },
      assetsPath: 'cesium',  // Output subfolder for Cesium assets
    }),
  ],
});
```

---

## Environment Variables (Vercel Dashboard)

Set these in Vercel → Project → Settings → Environment Variables:

| Variable | Environment | Value |
|---|---|---|
| `VITE_CESIUM_ION_TOKEN` | Production + Preview | `eyJhbGci...` (your Cesium ion token) |
| `VITE_API_URL` | Production | `https://sih-ocean-backend.onrender.com` |
| `VITE_API_URL` | Preview | `https://sih-ocean-backend-pr-N.onrender.com` (if using preview deploys) |
| `VITE_API_URL` | Development | `http://localhost:8000` |

**Important:** Vite only exposes env vars prefixed with `VITE_` to the client. These
are baked into the build at compile time (not runtime).

---

## Cesium Ion Token

### Getting the token
1. Sign up at https://ion.cesium.com/signup (free)
2. Go to Access Tokens → Create token
3. Set **Allowed URLs** to your Vercel domain (e.g., `https://sih-ocean.vercel.app/*`)
4. Copy the token

### Setting it in Vercel
1. Vercel Dashboard → Project → Settings → Environment Variables
2. Key: `VITE_CESIUM_ION_TOKEN`, Value: your token
3. Select environments: Production, Preview
4. Redeploy

### Using it in code
```typescript
// src/globe/CesiumViewer.tsx
import { Ion, Viewer, Terrain } from 'cesium';

// Set token from Vite env var
Ion.defaultAccessToken = import.meta.env.VITE_CESIUM_ION_TOKEN;

// Create viewer
const viewer = new Viewer('cesiumContainer', {
  terrain: Terrain.fromWorldTerrain(),
  // ... other options
});
```

---

## API URL Configuration (Vercel → Render)

The frontend on Vercel calls the backend on Render. Configure the API URL:

```typescript
// src/api/client.ts
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function fetchSST(time: string, bbox: BBox) {
  const response = await fetch(
    `${API_URL}/glorys_temp/zarr/.zmetadata`
  );
  return response.json();
}

export async function fetchArgoProfile(floatId: number, variable: string) {
  const response = await fetch(
    `${API_URL}/argo/profile?float_id=${floatId}&variable=${variable}`
  );
  return response.json();
}
```

### CORS on the backend
The Render backend must allow the Vercel origin. See
[`render-deployment.md`](render-deployment.md) → CORS Configuration.

---

## Build Optimization

CesiumJS is a large library (~30 MB uncompressed). Optimize the build:

### Chunk splitting
```typescript
// vite.config.ts
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        cesium: ['cesium'],
        plotly: ['plotly.js-dist-min'],
        react: ['react', 'react-dom'],
      }
    }
  },
  chunkSizeWarningLimit: 2000,  // Cesium chunk will be large
}
```

### Asset handling
```typescript
build: {
  assetsInlineLimit: 0,  // Don't inline large assets
}
```

### Expected build output
```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js         (app code, ~200 KB)
│   ├── cesium-[hash].js        (Cesium, ~5 MB gzipped)
│   ├── plotly-[hash].js        (Plotly, ~1 MB gzipped)
│   └── vendor-[hash].js         (React etc, ~150 KB)
└── cesium/
    ├── Workers/                 (Cesium web workers)
    ├── Assets/                  (Cesium built-in assets)
    ├── ThirdParty/              (Cesium third-party)
    └── Widgets/                 (Cesium widget CSS)
```

---

## Deployment Steps

1. Push code to GitHub (already done)
2. Go to https://vercel.com → New Project
3. Import the `VMAX-OCEAN/ocean-docs` repo
4. Set Root Directory to `frontend/`
5. Framework preset auto-detected as **Vite**
6. Add environment variables:
   - `VITE_CESIUM_ION_TOKEN` = your token
   - `VITE_API_URL` = `https://sih-ocean-backend.onrender.com`
7. Click **Deploy**
8. Wait for build (~2-3 min)
9. Your app is live at `https://sih-ocean.vercel.app` (or `https://ocean-docs.vercel.app`)

---

## Free Tier Limits (Vercel Hobby)

| Limit | Value | Impact |
|---|---|---|
| Bandwidth | 100 GB/month | Plenty for a viz app |
| Build minutes | 6000 min/month | Plenty |
| Static sites | Unlimited | No limit |
| Deploy frequency | 100/day | Plenty |
| Custom domains | 1 per project | Enough for 1 domain |

**The Vercel free tier is sufficient for the SIH demo.**

---

## Known Issues & Fixes

### 404 on SPA routes
**Cause:** Vercel doesn't know it's an SPA by default.
**Fix:** Add `vercel.json` with rewrites (see above).

### Cesium assets 404
**Cause:** Cesium's Workers/Assets/Widgets not copied to `dist/`.
**Fix:** Use `vite-plugin-cesium` (handles copying automatically).

### "Cesium is using default ion token" warning
**Cause:** Token not set or not prefixed with `VITE_`.
**Fix:** Use `VITE_CESIUM_ION_TOKEN` env var, redeploy.

### EMFILE: too many open files
**Cause:** Cesium imports too many modules at once (seen with Next.js, rare with Vite).
**Fix:** Import Cesium dynamically:
```typescript
const Cesium = await import('cesium');
```

### CORS errors (frontend can't reach backend)
**Cause:** Backend on Render not allowing Vercel origin.
**Fix:** Add Vercel URL to CORS_ORIGINS on Render backend.
