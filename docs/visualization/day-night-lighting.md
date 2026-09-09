# Day/Night Lighting — Accurate Light and Dark Side

How the globe shows the accurate light/dark side (day/night terminator) using CesiumJS
built-in sun-position lighting.

---

## The Built-In Solution (CesiumJS)

CesiumJS has built-in sun-position lighting. The key property is
`scene.globe.enableLighting = true`. Once enabled, the globe and terrain shade based
on the current sun position, which CesiumJS derives automatically from the viewer's
clock time.

```js
// Enable sun-based shading on the globe and models
viewer.scene.globe.enableLighting = true;

// Set the clock to a specific time to see the effect
viewer.clock.currentTime = Cesium.JulianDate.fromIso8601("2026-09-09T12:00:00Z");

// Or animate through day/night automatically
viewer.clock.multiplier = 500;  // 500x real time
viewer.clock.shouldAnimate = true;
```

### Atmosphere Lighting

```js
// Dynamic atmosphere lighting using sun direction
viewer.scene.globe.dynamicAtmosphereLighting = true;
viewer.scene.globe.dynamicAtmosphereLightingFromSun = true;
```

This makes the atmosphere color shift with the sun — sunset oranges near the terminator,
deep blue on the day side, dark on the night side.

### Sun and Moon Discs

```js
viewer.scene.sun.show = true;   // Visible sun disc at correct position
viewer.scene.moon.show = true;  // Visible moon disc
```

### Light Intensity (if night side too dark)

```js
// Default SunLight intensity is 2.0; increase to prevent pitch-black night
viewer.scene.light = new Cesium.SunLight({ intensity: 3.0 });
```

---

## How It Works Internally

### Sun Position Calculation

CesiumJS computes the sun's position from the clock time using real astronomy:
- **Declination** — how far north/south of the equator the sun sits (swings ±23.44°
  over the year)
- **Subsolar longitude** — where local solar noon is right now (moves 15° west per hour)

This is the same calculation that, if done in hand-rolled Three.js, requires:
```js
// The naive approach (error-prone, from Timetate dev post)
const declination = 23.44 * Math.sin((2 * Math.PI * (dayOfYear - 80)) / 365.25);
const subsolarLon = (12 - utcHours) * 15;
```
CesiumJS does this correctly with full astronomical precision (including equation of
time, which the naive version ignores — can be off by ~16 minutes at year extremes).

### The Terminator Shader

The day/night terminator is a **Lambert diffuse shading** calculation in the globe
fragment shader (`GlobeFS.glsl`):

```glsl
// Simplified from Cesium's GlobeFS.glsl
float diffuse = czm_LambertDiffuse(m_lightDirectionEC, normal);
float lightingFade = clamp((cameraDist - fadeOutDist) / (fadeInDist - fadeOutDist), 0.0, 1.0);
float dayNightBlend = mix(1.0, diffuse, lightingFade);
```

- `m_lightDirectionEC` — the sun direction in eye coordinates
- `czm_LambertDiffuse` — standard Lambertian diffuse: `max(dot(normal, lightDir), 0.0)`
- The terminator is where `dot(normal, sunDirection) ≈ 0` — the smooth day/night boundary
- `lightingFade` controls how lighting fades with camera distance (so far views aren't
  harshly dark)

### Atmosphere Scattering

CesiumJS uses **single-scatter volumetric ray casting** for the atmosphere (improved
in 2022, contributed by Xavier Tassin of GeoFS):

1. Shoot a ray from camera to edge of atmosphere
2. Sample points along the ray inside the atmosphere
3. At each sample, shoot another ray toward the sun
4. Model light scattered toward the sample (Rayleigh + Mie scattering)
5. Numerically integrate to get final sky color

This is why the atmosphere glows correctly at the terminator (sunset oranges) and
looks realistic from space.

---

## The Bug Everyone Hits (in hand-rolled Three.js)

If we were doing this in Three.js, the classic bug (documented in the Timetate dev
post) is using the **wrong normal space**:

```glsl
// WRONG — view space normal (sun follows camera when you orbit)
vNormal = normalize(normalMatrix * normal);

// CORRECT — world space normal (sun stays fixed)
vWorldNormal = normalize(vec3(modelMatrix * vec4(normal, 0.0)));
```

`sunDirection` is a world vector, so every sun-dependent term must use `vWorldNormal`.
Using `normalMatrix` (view space) renders fine until you orbit — then the sun follows
the camera.

**CesiumJS handles this correctly internally** — we don't need to worry about it.

---

## Light Theme + Day/Night

For the light theme, the day/night terminator still works correctly:

- **Day side:** Full brightness imagery (satellite textures visible)
- **Night side:** Darker (Lambert diffuse → 0) — but not pitch black if we set
  `minimumBrightness` or increase `SunLight intensity`
- **Terminator:** Smooth gradient (the `smoothstep` in the shader) — sunset colors
  from atmosphere scattering

The night side being darker against a light background is the **correct visual** —
it's how Earth looks from space. We don't want the night side to be as bright as the
day side.

### Optional: City Lights at Night

For extra realism, add a night lights imagery layer that only shows on the dark side:
```js
// NASA Black Marble (night lights) as a second imagery layer
// with night-day blending enabled
viewer.imageryLayers.addImageryProvider(
  new Cesium.IonImageryProvider({ assetId: NIGHT_LIGHTS_ASSET_ID })
);
```

CesiumJS supports `nightTextureAlpha` for blending night lights with day imagery
based on the sun position.

---

## Time Controls

The day/night terminator is tied to the clock. UI controls:

| Control | Action |
|---|---|
| "Now" button | Set clock to real time (live terminator) |
| Time slider | Scrub to any date/time (terminator moves) |
| Play/pause | Animate time (terminator sweeps across globe) |
| Speed multiplier | Control animation speed (1x, 100x, 1000x) |

This doubles as the **time animation control for ocean data** — the same clock drives
both the day/night lighting AND the ocean data time step. Moving the time slider
updates both simultaneously.

---

## Summary

| What | How | Cost |
|---|---|---|
| Accurate day/night terminator | `scene.globe.enableLighting = true` | 0 (shader) |
| Sun position | Auto from `viewer.clock.currentTime` | 0 (astronomy calc) |
| Atmosphere glow | `scene.skyAtmosphere` + `dynamicAtmosphereLighting` | 0 (shader) |
| Sunset colors at terminator | Atmospheric scattering (built-in) | 0 (shader) |
| Sun/moon discs | `scene.sun` / `scene.moon` | 0 |
| Time animation | `clock.shouldAnimate = true` + `clock.multiplier` | 0 |

**All of this is free in CesiumJS** — no custom shaders, no sun position math, no
normal-space bugs. We get the accurate light/dark side that Google Earth shows.
