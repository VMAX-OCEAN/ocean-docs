# Temperature Rendering Techniques — Complete Taxonomy

There are **4 distinct techniques** for rendering temperature/ocean scalar fields.
We need to understand all of them because the SIH problem statement requires several.

---

## Technique A: 2D Scalar Overlay

**Used by:** earth.nullschool, Windy, Ventusky, OceanStream, IMOS Live

### What it shows
Color each surface pixel by its scalar value via a colormap. Shows SST, surface
temperature, 2D fields.

### How it works
1. Bilinear-interpolate the gridded data to screen pixels
2. Apply a 1D color lookup table (LUT): `value → RGB`
3. Draw to canvas (nullschool) or as a GPU texture (Cesium imagery layer)

### Performance
- Cheap once data is loaded
- Colormap changes are instant (shader uniform, no re-fetch)
- nullschool does it in JS on CPU (expensive); Cesium does it on GPU (free)

### Limitations
- **Cannot show depth** — 2D only
- Cannot show 3D structure (thermoclines, eddies)

### For our project
Use for the **surface SST layer** — the easy 2D part. Cesium's `ImageryProvider` or
zarr-cesium `ZarrLayerProvider` does this on the GPU natively.

---

## Technique B: Particle Advection

**Used by:** earth.nullschool (wind), cesium-wind-layer, maplibre-wind-gl, IMOS Live

### What it shows
Animate particles following a velocity (u,v) field to *reveal flow direction*. Shows
current direction, eddies, flow patterns. Does NOT show the scalar value itself —
that's a separate overlay.

### How it works
1. Particle positions stored in a GPU texture (ping-pong FBOs)
2. Each frame, a shader reads the velocity field at each particle's position
3. Moves the particle using **semi-Lagrangian advection** (backward trace):
   `pos_new = pos_old - velocity * dt`
4. Draw particles as fading line trails
5. Particles "die" after a lifetime and respawn at random

### The semi-Lagrangian method
Instead of pushing each pixel forward (which causes gaps/overlaps), trace backward
from each output pixel to find where the value came from, then sample there. This
avoids the write-conflict problem of forward mapping.

### Performance
- GPU ping-pong textures — 10k+ particles at 60 FPS
- Zero CPU overhead per frame (all on GPU)
- `cesium-wind-layer` supports terrain occlusion (particles blocked by terrain)

### For our project
Use for **ocean current visualization** (u/v from GLORYS). Particles colored by speed.
This is the "wow" animated layer. Uses `cesium-wind-layer` (hongfaqiu) — the same
library zarr-cesium's `ZarrCubeVelocityProvider` uses.

### Key library: cesium-wind-layer
```js
const windLayer = new WindLayer(viewer, windData, {
  particlesTextureSize: 100,        // max particles = size² = 10,000
  particleHeight: 1000,
  lineWidth: { min: 1, max: 2 },
  lineLength: { min: 20, max: 100 },
  speedFactor: 1.0,
  dropRate: 0.003,
  colors: ['white'],
  dynamic: true
});
```

---

## Technique C: Depth Slices / Isosurfaces

**Used by:** nordicseas3d, DOVis, zarr-cesium

### What it shows
Show the 3D ocean by slicing it — either horizontal slices at a chosen depth, or
isosurfaces (the depth where temperature = X°C). Shows the 3D structure of
temperature/salinity — thermoclines, haloclines, eddies.

### How it works

**Horizontal slice:**
- Pick a depth level → render that 2D layer as a colored sheet floating at that depth
- Essentially Technique A applied per-depth-level
- zarr-cesium `ZarrCubeProvider` does this

**Isosurface:**
- March through the volume, find all cells where `value == target`
- Build a mesh (marching cubes) or render as a depth sheet
- Color by depth (shows the thermocline depth)
- DOVis does this server-side; nordicseas3d does it client-side in Three.js

**Vertical exaggeration:**
- The ocean is thin relative to Earth's radius (~4 km vs 6371 km)
- Multiply Z by an exaggeration factor (e.g., 50×) so the ocean layer is visible
- zarr-cesium `verticalExaggeration` parameter

### Performance
- Slices: cheap (one 2D layer per depth)
- Isosurfaces: moderate (marching cubes or ray casting)
- Both interactive at 60 FPS with chunked data

### For our project
This is the **headline 3D requirement**. zarr-cesium `ZarrCubeProvider` does
horizontal/vertical slices; DOVis does isosurfaces server-side; nordicseas3d does both
in Three.js.

---

## Technique D: Volumetric Ray Casting

**Used by:** i4Ocean (paper), WebGPU ocean volume (MDPI 2025), three.js-volume-renderer

### What it shows
True volume rendering — shoot a ray through the 3D grid per pixel, accumulate
color/opacity via a transfer function. Shows the full continuous 3D field — clouds of
temperature, no hard slice boundaries. Most scientifically accurate.

### How it works
1. Upload the 3D scalar field as a **3D texture** on the GPU
2. Fragment shader marches a ray through the volume per pixel
3. At each sample point, read the scalar value
4. Apply a **transfer function** (value → RGBA) — this is the colormap + opacity
5. Accumulate color/opacity along the ray (front-to-back compositing)
6. **Early ray termination** — stop when opacity is near 1 (optimization)
7. **Adaptive sampling** — fewer samples in uniform regions (optimization)

### The transfer function
The 2D equivalent of a colormap, but with an opacity channel. Lets you make certain
value ranges transparent (e.g., show only the 15-25°C water mass) and others opaque.

### Performance
- Heaviest technique — needs WebGPU or careful WebGL
- The MDPI 2025 paper uses Babylon.js + WebGPU with early termination + adaptive sampling
- Three.js volume renderer (Donitzo) does it in WebGL with raymarching

### For our project
The "premium" visualization mode. Use Three.js volume renderer (Donitzo) or a custom
ray-casting shader for the showcase isosurface/volume view. Not needed for every layer
— use slices for interactivity (Technique C), volume for the "wow" demo (Technique D).

---

## Summary: Which Technique for Which PS Requirement

| PS Requirement | Technique | Library |
|---|---|---|
| 3D volumetric rendering (temp/salinity/currents) | C (slices) + D (volume) | zarr-cesium `ZarrCubeProvider` + Three.js volume renderer |
| Depth-slice views | C | zarr-cesium horizontal/vertical slices + depth slider |
| Isosurface extraction | C | DOVis-style server marching cubes OR nordicseas3d client-side |
| Time-step animation | A + B | Timeline slider cycling through Zarr time chunks; particles re-seed |
| Current vectors | B | `cesium-wind-layer` (GPU particles from u/v) |
| Customizable colorbar | A | d3-scale-chromatic / colormap LUT editor |
| Layer opacity | A | Cesium primitive `alpha` / shader uniform |
| Vertical exaggeration | C | zarr-cesium `verticalExaggeration` param |
| Argo/Glider profile charts | (separate) | Plotly depth-vs-variable on marker click |
| Co-visualization model + instruments | All | Cesium globe hosts both volumetric + instrument markers |

---

## The Temperature Animation Pipeline (end to end)

```
GLORYS NetCDF (temp[time, depth, lat, lon])
   │ one-time convert (xarray)
   ▼
Zarr store, chunked [time, depth, lat, lon]
   │ browser streams only needed chunks
   ▼
zarrita.js fetches chunk for (t_current, depth_selected, view_bbox)
   │
   ▼
zarr-cesium ZarrCubeProvider
   ├── builds a Cesium primitive (colored sheet at depth_selected)
   ├── applies colormap LUT (temp → RGB) in shader  ← the "temperature effect"
   ├── applies vertical exaggeration
   └── renders into Cesium globe
   │
   ▼  (user drags time slider OR plays animation)
   ▼
next time chunk fetched → primitive re-textured → smooth animation
   │
   ▼  (optional: current particles overlaid)
cesium-wind-layer reads u/v at same (t, depth) → animated particle trails
```

**Why this is smooth (no user delay):**
- Only the **visible bbox + current depth + current time** chunk is fetched (few hundred KB)
- Zarr chunks are **ms latency** (parallel HTTP range reads)
- Colormap is a **GPU shader LUT** — changing palette/range is instant, no re-fetch
- Time animation = fetch next chunk + re-upload texture (one frame)

**The "temperature effect" you see** = the **colormap shader**. The scalar value at each
grid point becomes a texture; the fragment shader samples a 1D color LUT by that value.
Change the LUT (palette/min/max/log) → instant recolor.
