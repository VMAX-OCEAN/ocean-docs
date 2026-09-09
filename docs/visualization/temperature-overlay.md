# Temperature Overlay — Scalar Field Rendering

How temperature (and salinity, sea surface height) is rendered as colored overlays on
the globe using zarr-cesium providers and GPU colormap shaders.

---

## The "Temperature Effect" — How It Works

The temperature visualization you see on nullschool/Windy/OceanStream is a **scalar
field → colormap → color** mapping, done per-pixel in a shader:

1. The scalar value at each grid point becomes a **texture** on the GPU
2. The fragment shader samples a **1D color lookup table (LUT)** by that value
3. The LUT maps `temperature_value → RGB color`
4. Changing the LUT (palette/min/max/log) → **instant recolor** (shader uniform, no re-fetch)

This is exactly how nullschool does it (but on CPU Canvas 2D), and how Cesium does it
(on GPU — instant).

---

## Surface SST (2D Overlay)

Uses zarr-cesium `ZarrLayerProvider`:

```js
import { ZarrLayerProvider } from 'zarr-cesium';

const sstLayer = new ZarrLayerProvider(viewer, {
  url: 'https://backend/glorys/sst.zarr',
  variable: 'thetao',           // sea water potential temperature
  time: '2026-09-09',
  colormap: 'turbo',            // scientific colormap
  opacity: 0.7,
  min: -2,                      // colorbar min (°C)
  max: 32,                      // colorbar max (°C)
  logScale: false
});
await sstLayer.load();
```

### Data Flow

```
1. User selects "Temperature" variable, "Surface" depth
2. ZarrLayerProvider requests Zarr chunk for (t=current, depth=0, bbox=view)
3. zarrita.js fetches chunk (~100 KB) from xpublish Zarr REST ──► ms latency
4. Provider builds Cesium imagery layer, applies colormap LUT in shader
5. Globe renders with SST overlay, colorbar shown in panel
6. User scrubs time slider ──► next chunk fetched ──► re-texture ──► animation
7. User changes colormap ──► shader uniform update ──► instant recolor (no fetch)
```

---

## 3D Depth Slice (Volumetric)

Uses zarr-cesium `ZarrCubeProvider` for depth-resolved 3D rendering:

```js
import { ZarrCubeProvider } from 'zarr-cesium';

const tempCube = new ZarrCubeProvider(viewer, {
  url: 'https://backend/glorys/temp3d.zarr',
  variable: 'thetao',
  bounds: { west: 60, south: 5, east: 100, north: 30 },  // Indian Ocean
  colormap: 'plasma',
  verticalExaggeration: 50,   // make thin ocean layer visible
  depth: 500,                 // selected depth level (meters)
  opacity: 0.8
});
await tempCube.load();
```

### Depth Slider

```js
// User changes depth slider
tempCube.setDepth(1000);  // fetch new chunk at 1000m, re-render
```

### Vertical Exaggeration

The ocean is thin relative to Earth's radius (~4 km vs 6371 km). The
`verticalExaggeration` parameter multiplies Z so the ocean layer is visible:

```js
tempCube.setVerticalExaggeration(100);  // 100× exaggeration
```

---

## Time Animation

The time slider cycles through Zarr time chunks:

```js
// Timeline slider in UI
const timeSlider = {
  min: '1993-01-01',
  max: '2026-06-23',
  step: '1 day',
  value: '2026-09-09',
  onChange: (newTime) => {
    sstLayer.setTime(newTime);  // fetch new chunk, re-texture
  }
};

// Play/pause animation
const playButton = {
  onClick: () => {
    isPlaying = !isPlaying;
    if (isPlaying) animateTime();
  }
};

function animateTime() {
  if (!isPlaying) return;
  currentTime = addDays(currentTime, 1);
  sstLayer.setTime(currentTime);
  setTimeout(animateTime, 200);  // 5 FPS animation
}
```

### Why Animation Is Smooth

- Only the **visible bbox + current depth + current time** chunk is fetched (few hundred KB)
- Zarr chunks are **ms latency** (parallel HTTP range reads)
- Colormap is a **GPU shader LUT** — no re-fetch on palette change
- Time animation = fetch next chunk + re-upload texture (one frame)

---

## Sea Surface Height (Water Levels)

GLORYS includes `zos` (sea surface height above geoid) and `SLA` (sea level anomaly):

### As a 2D overlay (anomaly)
```js
const slaLayer = new ZarrLayerProvider(viewer, {
  url: 'https://backend/glorys/sla.zarr',
  variable: 'zos',
  colormap: 'RdBu',     // diverging: blue-white-red
  min: -0.5,             // meters
  max: 0.5,
  opacity: 0.6
});
```

### As a displaced mesh (3D)
Exaggerate the sea surface height as actual 3D geometry on the globe — the sea
surface bulges where water is higher. Cesium supports this via custom primitives.

---

## Colormaps (Scientific)

Available colormaps (from d3-scale-chromatic / cesium-color-maps):

| Colormap | Use case |
|---|---|
| `turbo` | General temperature (rainbow, perceptually improved) |
| `plasma` | Temperature, salinity (perceptually uniform) |
| `viridis` | Temperature, salinity (perceptually uniform, print-safe) |
| `RdBu` | Temperature/sea level anomaly (diverging: blue-white-red) |
| `coolwarm` | Temperature anomaly |
| `Spectral` | Multi-category ocean variables |
| `cubehelix` | nullschool-style (perceptually uniform, optional) |

All changes are **instant** because the colormap is a shader LUT — the data texture
doesn't change, only the color mapping does.

---

## Rendering Modes Summary

| Mode | Technique | When to use | Library |
|---|---|---|---|
| Surface SST | 2D overlay | Default landing view | `ZarrLayerProvider` |
| Depth Slice | Horizontal sheet | Explore a specific depth | `ZarrCubeProvider` + depth slider |
| Vertical Section | Vertical curtain | Temp vs depth along transect | `ZarrCubeProvider` vertical slice |
| Isosurface | Marching cubes | Find thermocline (20°C isotherm) | Server compute or client Three.js |
| Volume Render | Ray casting | Showcase "wow" 3D cloud | Three.js volume renderer |
| Current Particles | GPU advection | Animate ocean currents | `cesium-wind-layer` |
| Argo Profiles | Plotly chart | Click float → depth-vs-temp | Plotly.js |

See [`ocean-currents.md`](ocean-currents.md) for particles, [`isosurfaces.md`](isosurfaces.md)
for isosurfaces, [`colorbar-editor.md`](colorbar-editor.md) for the colorbar UI.
