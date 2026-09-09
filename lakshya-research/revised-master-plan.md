# Revised Master Plan — The Best Approach

**The definitive plan.** Supersedes all previous plans. Incorporates cross-check
findings, risk mitigation, and the final architecture.

---

## The Best Approach: De-Risk First, Then Build in Phases

We have two medium-risk dependencies (zarr-cesium, cesium-wind-layer). The best
approach is **not** to commit to them blindly, nor to avoid them entirely. Instead:

1. **Phase 0 (De-risk):** Build a minimal proof-of-concept for the risky parts.
   This takes 1-2 days and tells us whether to use the library or the fallback.
2. **Phases 1-6 (Build):** Build the full platform in milestones, with fallbacks
   ready if any dependency fails.

**Why this is the best approach:**
- We don't waste weeks building on a broken dependency
- We don't over-engineer fallbacks we may not need
- We get a working globe fast (Phase 1) for stakeholder demos
- Each phase delivers something visible and testable

---

## Architecture (Final — No Changes)

```
┌─────────────────────────────────────────────────────────────────┐
│  USER BROWSER                                                    │
│  React + CesiumJS + zarrita.js + zarr-cesium + Supabase JS      │
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
│  CesiumJS       │ │ (GLORYS data) │ │ (Postgres + PostGIS)│
│                  │ │               │ │                     │
│  CDN-served      │ │ Zero egress   │ │ Direct JS client    │
└─────────────────┘ └───────────────┘ └─────────────────────┘
                             │
                             │ (browser fetches Zarr directly via zarrita.js)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  RENDER (free) — compute only                                    │
│  Isosurface computation (marching cubes) — on demand            │
│  Reads Zarr from R2, returns glTF mesh                          │
│  Keep-warm via cron-job.org (08:00-18:00)                      │
└─────────────────────────────────────────────────────────────────┘
```

**Cost: $0/month.** No changes from the free-tier plan.

---

## zarr-cesium: The Key Discovery

zarr-cesium provides **three providers** that map exactly to our needs:

| Provider | Our Use Case | What It Does |
|---|---|---|
| `ZarrLayerProvider` | SST, salinity, sea level (2D surface) | Renders Zarr arrays as Cesium imagery layers with GPU colormap |
| `ZarrCubeProvider` | Depth slices, vertical sections (3D) | Renders horizontal/vertical slices from 3D Zarr cubes |
| `ZarrCubeVelocityProvider` | Ocean currents (U/V particles) | Animated particle advection from U/V components |

**This means zarr-cesium handles ALL our ocean rendering needs.** If it works, we
don't need cesium-wind-layer at all (zarr-cesium has its own velocity provider).

**The API is clean:**
```typescript
import { ZarrLayerProvider } from 'zarr-cesium';

const layer = await ZarrLayerProvider.createLayer(viewer, {
  url: 'https://pub-xxx.r2.dev/glorys_temp.zarr',
  variable: 'thetao',
  colormap: 'viridis',
  scale: [0, 32]  // temperature range °C
});
viewer.imageryLayers.add(layer);
```

---

## Phase 0: De-Risk (1-2 Days)

**Goal:** Verify the two risky dependencies work with our actual data before
committing to the full build.

### Step 0.1: Set up R2 + upload test Zarr
- [ ] Create Cloudflare R2 bucket `sih-ocean-zarr`
- [ ] Enable public access
- [ ] Convert a small GLORYS subset (Indian Ocean, 1 day, surface temp) to Zarr:
  ```python
  import xarray as xr
  ds = xr.open_dataset('glorys_sample.nc')
  ds.to_zarr('glorys_temp.zarr', mode='w')
  ```
- [ ] Upload to R2:
  ```bash
  aws s3 sync glorys_temp.zarr/ s3://sih-ocean-zarr/glorys_temp.zarr/ \
    --endpoint-url=https://xxx.r2.cloudflarestorage.com
  ```
- [ ] Verify public access: `curl https://pub-xxx.r2.dev/sih-ocean-zarr/glorys_temp.zarr/.zmetadata`

### Step 0.2: Test zarr-cesium ZarrLayerProvider
- [ ] Create minimal Vite + Cesium + zarr-cesium app
- [ ] Load the test Zarr from R2:
  ```typescript
  import { ZarrLayerProvider } from 'zarr-cesium';
  const layer = await ZarrLayerProvider.createLayer(viewer, {
    url: 'https://pub-xxx.r2.dev/sih-ocean-zarr/glorys_temp.zarr',
    variable: 'thetao',
    colormap: 'viridis',
    scale: [0, 32]
  });
  viewer.imageryLayers.add(layer);
  ```
- [ ] **Decision point:** Does the SST overlay render correctly on the globe?
  - **If YES:** Proceed with zarr-cesium for all ocean rendering. ✅
  - **If NO:** Fall back to custom `ImageryProvider` + zarrita.js (see below)

### Step 0.3: Test zarr-cesium ZarrCubeVelocityProvider (currents)
- [ ] Upload a small U/V Zarr to R2
- [ ] Test:
  ```typescript
  import { ZarrCubeVelocityProvider } from 'zarr-cesium';
  const velocityLayer = await ZarrCubeVelocityProvider.createLayer(viewer, {
    url: 'https://pub-xxx.r2.dev/sih-ocean-zarr/glorys_currents.zarr',
    uVariable: 'uo',
    vVariable: 'vo',
  });
  ```
- [ ] **Decision point:** Do particles animate correctly?
  - **If YES:** Use zarr-cesium for currents. Skip cesium-wind-layer entirely. ✅
  - **If NO:** Fall back to cesium-wind-layer (with Vite alias fix) or custom shader

### Step 0.4: Test Supabase
- [ ] Create Supabase project `sih-ocean`
- [ ] Create `floats` table with PostGIS
- [ ] Insert 10 test Argo floats
- [ ] Query from browser:
  ```typescript
  import { createClient } from '@supabase/supabase-js';
  const supabase = createClient(URL, ANON_KEY);
  const { data } = await supabase.from('floats').select('*');
  ```
- [ ] **Decision point:** Does direct browser query work?
  - **If YES:** Proceed with Supabase. ✅
  - **If NO:** Use R2 JSON files for metadata instead

### Phase 0 Exit Criteria
- [ ] Zarr loads from R2 via zarrita.js ✅
- [ ] zarr-cesium renders SST overlay (or fallback confirmed) ✅
- [ ] zarr-cesium renders current particles (or fallback confirmed) ✅
- [ ] Supabase queries work from browser ✅
- [ ] CesiumJS globe renders on Vercel ✅

---

## Fallback: Custom ImageryProvider + zarrita.js

If zarr-cesium fails, build a custom Cesium `ImageryProvider` that:
1. Uses `zarrita.js` `FetchStore` to read Zarr chunks from R2
2. Renders chunks to a Canvas with a colormap (d3-scale-chromatic)
3. Returns the Canvas as the imagery tile

```typescript
// fallback/ZarrImageryProvider.ts
import * as zarr from 'zarrita';
import { scale as d3scale } from 'd3-scale-chromatic';

class ZarrImageryProvider {
  // Open Zarr store from R2
  async load(url: string, variable: string) {
    const store = new zarr.FetchStore(url);
    this.array = await zarr.open(store, { kind: 'array' });
  }

  // Cesium calls this for each tile
  async requestImage(x: number, y: number, level: number) {
    // Fetch Zarr chunk for this region
    const chunk = await zarr.get(this.array, [this.time, level, y, x]);
    // Map values to colors via colormap
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const imageData = ctx.createImageData(width, height);
    for (let i = 0; i < chunk.data.length; i++) {
      const color = d3scale(this.colormap)(chunk.data[i]);
      imageData.data[i * 4] = color.r;
      imageData.data[i * 4 + 1] = color.g;
      imageData.data[i * 4 + 2] = color.b;
      imageData.data[i * 4 + 3] = 255;
    }
    ctx.putImageData(imageData, 0, 0);
    return canvas;
  }
}
```

This is more work (~2-3 days) but removes the zarr-cesium dependency entirely.
The rendering is CPU-side (Canvas 2D) instead of GPU-side (WebGL shader), so it's
slower for animation but works reliably.

---

## Build Phases (After Phase 0)

### Phase 1: Light-Theme Globe (3-4 days)

**Goal:** A polished, light-theme CesiumJS globe with day/night lighting.

- [ ] Scaffold Vite + React + TypeScript project (`frontend/`)
- [ ] Install: `cesium`, `vite-plugin-cesium`, `zarr-cesium`, `zarrita`
- [ ] Configure `vite.config.ts` (Cesium plugin, env vars, chunk splitting)
- [ ] Create `CesiumViewer` component:
  - Light theme (white background, light UI)
  - `viewer.scene.globe.enableLighting = true` (day/night terminator)
  - Dynamic atmosphere lighting from sun
  - Cesium World Terrain + Bing imagery (ion free tier)
  - Set `Ion.defaultAccessToken` from `VITE_CESIUM_ION_TOKEN`
- [ ] Deploy to Vercel
- [ ] **Verify:** Globe renders, day/night terminator visible, light theme

**Deliverable:** Working globe on Vercel at `https://sih-ocean.vercel.app`

### Phase 2: SST Overlay (3-4 days)

**Goal:** Temperature overlay from GLORYS Zarr on R2.

- [ ] Convert full GLORYS Indian Ocean subset to Zarr (multi-variable)
- [ ] Upload to R2
- [ ] Add `ZarrLayerProvider` (or fallback) for `thetao` (temperature)
- [ ] Add colorbar UI (palette selector, min/max, opacity)
- [ ] Add variable selector (SST, salinity, sea level)
- [ ] **Verify:** Temperature overlay renders on globe, colorbar works

**Deliverable:** Globe with switchable temperature/salinity/sea-level overlays

### Phase 3: Time Animation + Depth (3-4 days)

**Goal:** Time slider + depth slider.

- [ ] Add time slider UI (date range from Zarr time coordinate)
- [ ] Time animation (play/pause/step) — swaps Zarr time index
- [ ] Add depth slider UI (0-5000m from Zarr depth coordinate)
- [ ] `ZarrCubeProvider` for horizontal depth slices
- [ ] `ZarrCubeProvider` for vertical sections (cross-section view)
- [ ] **Verify:** Time animation smooth, depth slices render

**Deliverable:** Animated ocean temperature with depth exploration

### Phase 4: Ocean Currents (3-4 days)

**Goal:** Particle advection for currents.

- [ ] Upload U/V Zarr to R2
- [ ] Add `ZarrCubeVelocityProvider` (or cesium-wind-layer fallback)
- [ ] Particle controls (density, speed, color by speed)
- [ ] Sync particles with time + depth sliders
- [ ] **Verify:** Particles animate, sync with time/depth

**Deliverable:** Animated current particles overlaid on temperature

### Phase 5: Argo Observations (3-4 days)

**Goal:** Argo float markers + profile charts.

- [ ] Set up Supabase tables (floats, profiles) with PostGIS
- [ ] Ingest Argo data via `argopy` → Supabase
- [ ] Add Argo markers on globe (from Supabase query)
- [ ] Click marker → Plotly profile chart (depth vs temp/salinity)
- [ ] Filter by date range, variable, bbox
- [ ] **Verify:** Markers load, profiles render on click

**Deliverable:** Argo floats on globe with interactive profiles

### Phase 6: Isosurfaces + Backend (3-4 days)

**Goal:** 3D isosurface rendering via Render backend.

- [ ] Deploy FastAPI on Render (free tier)
- [ ] `/isosurface` endpoint (marching cubes via PyVista/scikit-image)
- [ ] Backend reads Zarr from R2 (S3 API), returns glTF
- [ ] Frontend fetches glTF, renders as Cesium 3D primitive
- [ ] Cache isosurfaces in R2 (write back)
- [ ] Set up cron-job.org keep-warm
- [ ] **Verify:** Isosurface renders, cold start acceptable

**Deliverable:** 3D thermocline visualization

---

## Dependency Decision Tree

```
Phase 0: Test zarr-cesium
├── ZarrLayerProvider works?
│   ├── YES → Use zarr-cesium for SST/salinity/sea level ✅
│   └── NO  → Custom ImageryProvider + zarrita.js (fallback) ⚠️
│
├── ZarrCubeProvider works?
│   ├── YES → Use zarr-cesium for depth slices/sections ✅
│   └── NO  → Custom Cesium.Primitive + zarrita.js (fallback) ⚠️
│
└── ZarrCubeVelocityProvider works?
    ├── YES → Use zarr-cesium for currents ✅
    └── NO  → cesium-wind-layer (with Vite alias fix) ⚠️
        └── cesium-wind-layer works?
            ├── YES → Use it ✅
            └── NO  → Custom GPU particle shader (fallback) ⚠️
```

**Most likely outcome:** zarr-cesium works for all three (it's designed for exactly
this use case). The fallbacks exist only as insurance.

---

## What We're NOT Doing (Scope Discipline)

| Not doing | Why |
|---|---|
| OPeNDAP endpoints | Standards compliance for INCOIS portals — not needed for demo. Add later if required. |
| Full volume rendering | Too heavy for browser. Isosurfaces (marching cubes) are the practical alternative. |
| Glider/CTT/BGC overlays | Argo is sufficient for the demo. Add other instruments post-SIH. |
| Custom terrain hosting | Cesium ion free tier is sufficient. Self-host GEBCO only if ion limits hit. |
| Backend in hot path | R2 + Supabase handle hot path directly. Backend only for isosurface compute. |
| Paid services | User requested free tier only. All services have permanent free tiers. |
| True 3D particle trajectories | Requires vertical velocity (w) data. GLORYS doesn't provide it. Use 2D (U/V) particles. |

---

## Tech Stack (Final — Pinned Versions)

```json
{
  "frontend": {
    "react": "^18.3.0",
    "cesium": "^1.127.0",
    "zarr-cesium": "0.1.4",
    "zarrita": "^0.7.0",
    "@supabase/supabase-js": "^2.45.0",
    "plotly.js-dist-min": "^2.35.0",
    "zustand": "^4.5.0",
    "vite": "^5.4.0",
    "vite-plugin-cesium": "^1.2.30",
    "typescript": "^5.5.0"
  },
  "backend": {
    "fastapi": "^0.115.0",
    "uvicorn": "^0.30.0",
    "xarray": "^2024.7.0",
    "zarr": "^2.18.0",
    "pyvista": "^0.44.0",
    "scikit-image": "^0.24.0",
    "httpx": "^0.27.0",
    "boto3": "^1.35.0"
  }
}
```

**Why pinned:**
- `cesium ^1.127.0` — compatible with cesium-wind-layer (if we need it)
- `zarr-cesium 0.1.4` — latest stable, pin exactly (pre-1.0, API may change)
- `zarrita ^0.7.0` — latest, FetchStore with custom fetch for R2

---

## Timeline

| Phase | Duration | Deliverable |
|---|---|---|
| Phase 0: De-risk | 1-2 days | Proof-of-concept for zarr-cesium + Supabase |
| Phase 1: Globe | 3-4 days | Light-theme CesiumJS globe on Vercel |
| Phase 2: SST | 3-4 days | Temperature overlay from R2 Zarr |
| Phase 3: Time+Depth | 3-4 days | Animated depth exploration |
| Phase 4: Currents | 3-4 days | Particle advection |
| Phase 5: Argo | 3-4 days | Float markers + profile charts |
| Phase 6: Isosurfaces | 3-4 days | 3D thermocline via Render backend |
| **Total** | **20-26 days** | **Full platform** |

Each phase delivers something demoable. If we run out of time, earlier phases
(globe + SST + time/depth) are already a strong SIH submission.

---

## Immediate Next Step

**Start Phase 0: De-risk.** Create the R2 bucket, upload a test Zarr, and verify
zarr-cesium renders it. This single test determines our entire rendering approach.

If zarr-cesium works → we use it for everything (fastest path).
If it fails → we build the custom ImageryProvider fallback (2-3 extra days).

Either way, we proceed to Phase 1 (globe) immediately after.
