# Ocean Currents — GPU Particle Advection

How ocean currents are visualized as animated particles using GPU advection
(cesium-wind-layer).

---

## The Technique

Ocean currents (u/v velocity fields from GLORYS) are visualized as **animated
particles** following the flow — the same technique earth.nullschool uses for wind,
but on the GPU via `cesium-wind-layer`.

### How It Works

1. Particle positions stored in a **GPU texture** (ping-pong FBOs)
2. Each frame, a shader reads the velocity field at each particle's position
3. Moves the particle using **semi-Lagrangian advection** (backward trace):
   `pos_new = pos_old - velocity * dt`
4. Draw particles as fading line trails
5. Particles "die" after a lifetime and respawn at random

### The Semi-Lagrangian Method

Instead of pushing each pixel forward (which causes gaps/overlaps), trace backward
from each output pixel to find where the value came from, then sample there:

```glsl
// advection fragment shader (simplified)
vec2 velocity = texture2D(uVelocity, vUv).xy;
vec2 sourcePos = vUv - velocity * uDt * uTexelSize;
vec4 advected = texture2D(uSource, sourcePos);
gl_FragColor = advected;
```

This avoids the write-conflict problem of forward mapping.

---

## Implementation (cesium-wind-layer)

```js
import { WindLayer } from 'cesium-wind-layer';

const currentLayer = new WindLayer(viewer, currentData, {
  particlesTextureSize: 100,        // max particles = size² = 10,000
  particleHeight: 0,                // at sea surface
  lineWidth: { min: 1, max: 2 },    // trail width range
  lineLength: { min: 20, max: 100 },// trail length range
  speedFactor: 1.0,                  // speed multiplier
  dropRate: 0.003,                   // particle death rate
  dropRateBump: 0.001,               // extra death for slow particles
  colors: ['white'],                 // or speed-based ramp
  dynamic: true                      // enable animation
});
```

### Ocean-Specific Settings

For ocean currents (slower than wind), use different settings than wind:

```js
const oceanCurrentLayer = new WindLayer(viewer, oceanUVData, {
  particlesTextureSize: 150,           // 22,500 particles
  particleHeight: 0,
  lineWidth: { min: 1.5, max: 3 },      // thicker trails
  lineLength: { min: 40, max: 150 },   // longer trails
  speedFactor: 0.3,                    // slower (ocean currents are slow)
  dropRate: 0.002,
  colors: ['#4488ff', '#88ccff', '#ffffff'],  // blue speed ramp
  dynamic: true
});
```

---

## Integration with zarr-cesium

zarr-cesium's `ZarrCubeVelocityProvider` uses cesium-wind-layer internally:

```js
import { ZarrCubeVelocityProvider } from 'zarr-cesium';

const currentProvider = new ZarrCubeVelocityProvider(viewer, {
  url: 'https://backend/glorys/currents.zarr',
  uVariable: 'uo',       // eastward sea water velocity
  vVariable: 'vo',       // northward sea water velocity
  depth: 0,              // surface currents
  time: '2026-09-09',
  bounds: { west: 60, south: 5, east: 100, north: 30 }
});
await currentProvider.load();
```

---

## Performance

| Aspect | Performance |
|---|---|
| Particle count | 10,000+ at 60 FPS |
| GPU vs CPU | All computation on GPU (zero CPU overhead per frame) |
| Terrain occlusion | Supported — particles blocked by terrain |
| Frame rate | Stable with frameRateAdjustment uniform (normalizes across refresh rates) |

### Why GPU Is Essential

nullschool does particle advection in JS on CPU — it's CPU-heavy. The Cesium blog
(GPU Powered Wind Visualization, 2019) explains: the Entity API performs computation
on CPU, and 10,000+ particles is too much for CPU. Moving to GPU via custom
`DrawCommand` + ping-pong textures gives real-time performance.

---

## Depth-Resolved Currents

GLORYS has u/v at all 50 depth levels. We can show currents at any depth:

```js
// Surface currents
currentProvider.setDepth(0);

// Deep currents at 1000m
currentProvider.setDepth(1000);
```

The particle field re-seeds when depth changes, showing how currents vary with depth
(deep currents often flow differently than surface currents).

---

## Time Animation

Particles re-seed per time step for animation:

```js
// As time advances, fetch new u/v chunks
currentProvider.setTime('2026-09-10');
// Particles gradually transition to new flow field
```

The same time slider that animates temperature also animates currents — synchronized
visualization of the ocean state over time.

---

## Color by Speed

Particles can be colored by current speed:

```js
// Speed-based color ramp (slow → fast)
colors: ['#08306b', '#2171b5', '#6baed6', '#c6dbef', '#fee391', '#fec44f', '#fe9929']
```

Or a flat color with speed affecting trail length/width (already in the config above).

---

## Summary

| Aspect | Implementation |
|---|---|
| Technique | GPU semi-Lagrangian particle advection |
| Library | `cesium-wind-layer` (via `ZarrCubeVelocityProvider`) |
| Particles | 10,000+ at 60 FPS, all on GPU |
| Data | u/v velocity from GLORYS Zarr store |
| Depth | Any of 50 levels (depth slider) |
| Time | Synchronized with temperature time animation |
| Color | Speed-based ramp or flat color |
| Terrain | Occlusion supported |
