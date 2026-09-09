# CesiumJS Deployment Notes

CesiumJS-specific deployment considerations for Vercel (frontend) + Render (backend).

---

## Cesium Static Assets

CesiumJS requires static files that must be served alongside the app:

| Asset folder | Contents | Size |
|---|---|---|
| `Workers/` | WebAssembly workers (terrain processing, geometry) | ~2 MB |
| `Assets/` | Built-in textures, fonts, icons | ~5 MB |
| `ThirdParty/` | Third-party libs (e.g., KML parser) | ~1 MB |
| `Widgets/` | Widget CSS (navigation, timeline) | ~100 KB |

### Handling with vite-plugin-cesium

`vite-plugin-cesium` copies these to `dist/cesium/` at build time and sets
`CESIUM_BASE_URL` automatically:

```typescript
// vite.config.ts
import cesium from 'vite-plugin-cesium';

export default defineConfig({
  plugins: [react(), cesium()],
});
```

### Vercel cache headers

Cesium assets are immutable (content-hashed). Cache them for 1 year:

```json
// vercel.json
{
  "headers": [
    {
      "source": "/cesium/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
```

This means returning users load the Cesium app instantly (assets from browser cache).

---

## Cesium Ion Token

### What it's used for
- **Cesium World Terrain** — global terrain elevation tiles (streamed from Cesium ion)
- **Bing Maps Aerial** — satellite imagery (streamed from Cesium ion)
- **Cesium ion assets** — 3D Tiles, glTF models hosted on ion

### Setting the token
```typescript
// src/globe/CesiumViewer.tsx
import { Ion } from 'cesium';

// Read from Vite env var (baked at build time)
Ion.defaultAccessToken = import.meta.env.VITE_CESIUM_ION_TOKEN;
```

### Security: Allowed URLs
In Cesium ion Dashboard → Access Tokens → Edit:
- Set **Allowed URLs** to `https://sih-ocean.vercel.app/*`
- This prevents others from using your token on their domains
- For preview deployments, add `https://*-sih-ocean.vercel.app/*` too

### Free tier limits
- Cesium ion free tier includes terrain + imagery
- Rate limits are generous (not publicly specified, but sufficient for a demo)
- If you exceed limits, self-host terrain (GEBCO) to reduce ion calls

---

## Self-Hosting Terrain (to avoid ion dependency)

If you want to avoid Cesium ion entirely (for offline or high-traffic scenarios):

### GEBCO bathymetry (self-hosted)
```typescript
import { createWorldTerrainAsync } from 'cesium';

// Self-hosted GEBCO terrain
viewer.terrainProvider = await Cesium.GeoTerrainProvider.fromUrl(
  'https://sih-ocean-backend.onrender.com/terrain/gebco/'
);
```

Host GEBCO terrain tiles on Render's persistent disk and serve via FastAPI static files.

### MapTiler imagery (alternative to Bing)
```typescript
viewer.imageryLayers.addImageryProvider(
  new Cesium.UrlTemplateImageryProvider({
    url: 'https://api.maptiler.com/maps/satellite/{z}/{x}/{y}.jpg?key=' + MAPTILER_KEY,
    credit: 'MapTiler'
  })
);
```

---

## CORS for Cesium Tile Requests

Cesium makes cross-origin requests for:
1. **Terrain tiles** — from Cesium ion (CORS enabled by default)
2. **Imagery tiles** — from Cesium ion or MapTiler (CORS enabled)
3. **Zarr chunks** — from our Render backend (must configure CORS)
4. **3D Tiles** — from Google Maps API or our backend (must configure CORS)

### Render backend CORS (for Zarr chunks)
```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sih-ocean.vercel.app",
        "https://ocean-docs.vercel.app",
        "https://*-sih-ocean.vercel.app",  # Preview deployments
        "http://localhost:5173",            # Local dev
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
```

---

## Build Size Optimization

CesiumJS is large. Optimize the Vite build:

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
  chunkSizeWarningLimit: 2000,  // Cesium chunk ~5 MB gzipped
  assetsInlineLimit: 0,          // Don't inline Cesium assets
}
```

### Expected bundle sizes (gzipped)
| Chunk | Size | Notes |
|---|---|---|
| `cesium-[hash].js` | ~5 MB | The main Cesium library |
| `plotly-[hash].js` | ~1 MB | Profile charts |
| `react-[hash].js` | ~150 KB | React + ReactDOM |
| `index-[hash].js` | ~200 KB | App code |
| Cesium assets | ~8 MB | Workers, Assets, Widgets (cached 1 year) |
| **Total first load** | ~15 MB | Subsequent loads use cache (instant) |

### Vercel gzip + brotli
Vercel automatically compresses responses with gzip and brotli. The ~15 MB total
becomes ~5 MB over the wire on first load.

---

## Known Issues

### "Default ion token" warning
**Cause:** Token not set or `VITE_` prefix missing.
**Fix:** Use `VITE_CESIUM_ION_TOKEN` env var in Vercel, redeploy.

### Cesium assets 404 on Vercel
**Cause:** `vite-plugin-cesium` not installed or not in plugins array.
**Fix:** `npm install vite-plugin-cesium` and add to `vite.config.ts` plugins.

### Workers fail to load
**Cause:** `CESIUM_BASE_URL` not set correctly.
**Fix:** `vite-plugin-cesium` sets this automatically. If manual:
```typescript
window.CESIUM_BASE_URL = '/cesium/';
```

### EMFILE: too many open files
**Cause:** Cesium imports many modules (seen with Next.js, rare with Vite).
**Fix:** Dynamic import:
```typescript
const Cesium = await import('cesium');
const viewer = new Cesium.Viewer(...);
```

### Terrain not loading
**Cause:** Cesium ion token invalid or rate-limited.
**Fix:** Check token in ion Dashboard, verify Allowed URLs match your Vercel domain.
