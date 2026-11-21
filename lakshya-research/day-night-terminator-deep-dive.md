# Day/Night Terminator: Deep Dive Research

Purpose: understand exactly how the day/night terminator works in Google
Earth vs. Cesium, why our current night side looks wrong, and how to fix
it so the night side is sun-locked (fixed in space) while the globe
surface rotates underneath — matching Google Earth's behavior.

---

## 1. The physics: what "sun-locked" actually means

The sun is effectively infinitely far away. Its direction is fixed in
**inertial space** (the celestial reference frame). The Earth rotates on
its axis once per 24 hours. So:

- The **subsolar point** (where the sun is directly overhead) moves
  westward across the Earth's surface at 15° per hour.
- The **terminator** (day/night boundary) is a great circle on the
  Earth's surface, perpendicular to the sun direction.
- At any frozen instant in time, the terminator is fixed on the Earth's
  surface. The Earth doesn't "move underneath" a fixed terminator unless
  time is advancing.

**What this means for globe interaction:**

When you "move the globe" with the mouse in Google Earth or Cesium, you
are **orbiting the camera** around a fixed globe. The globe itself does
not rotate. The sun direction is fixed in the Earth-fixed frame (ECEF)
at the current clock time. The terminator is painted on the Earth's
surface at that instant. As you orbit, you see different parts of the
Earth — some in day, some in night — but the terminator doesn't move
on the globe. It stays on the same geographic locations.

This is **correct behavior**. The night side should NOT stay fixed on
your screen (e.g., always on the left) — it should stay fixed on the
*Earth* (e.g., always over the Pacific if that's where night is right
now). When you orbit the camera, the night side appears to move across
your screen because you're seeing different parts of the Earth, not
because the terminator is following you.

**When time IS advancing** (clock animating), the Earth rotates
underneath the fixed sun direction, and the terminator sweeps across
the surface. This is the day/night cycle. Google Earth shows this when
you use the "Time of Day" feature with a time slider.

---

## 2. How Cesium implements the terminator (source code analysis)

I read the actual Cesium globe fragment shader (`GlobeFS.glsl`) to
understand exactly how the day/night shading works.

### 2.1 The sun direction is in world coordinates (ECEF)

From `GlobeFS.glsl`:

```glsl
// Line 347-348: surface normal in two coordinate spaces
vec3 normalMC = czm_geodeticSurfaceNormal(v_positionMC, vec3(0.0), vec3(1.0));
//   ^ model coordinates = ECEF for the globe
vec3 normalEC = czm_normal3D * normalMC;
//   ^ eye coordinates = camera-relative

// Line 443: the actual day/night shading
float diffuseIntensity = clamp(
    czm_getLambertDiffuse(czm_lightDirectionEC, normalEC) * 5.0 + 0.3,
    0.0, 1.0
);
```

`czm_lightDirectionEC` is the light (sun) direction transformed from
world coordinates (ECEF) to eye coordinates (camera-relative).
`normalEC` is the surface normal transformed from model coordinates
(ECEF) to eye coordinates.

**Key insight:** both vectors are in the *same* coordinate space (eye
coordinates). The view matrix transforms both equally, so the dot
product between them is the *same* as if computed in world coordinates.
The terminator stays fixed on the globe surface regardless of camera
position. This is correct.

### 2.2 The atmosphere uses world coordinates directly

```glsl
// Line 471-474
#if defined(DYNAMIC_ATMOSPHERE_LIGHTING_FROM_SUN)
    vec3 atmosphereLightDirection = czm_sunDirectionWC;
#else
    vec3 atmosphereLightDirection = czm_lightDirectionWC;
#endif
```

`czm_sunDirectionWC` and `czm_lightDirectionWC` are in world coordinates
(ECEF). The atmosphere darkening on the night side uses these directly,
so it's also sun-locked.

### 2.3 The night-fade distance

```glsl
// Line 549-553
float fadeInDist = u_nightFadeDistance.x;
float fadeOutDist = u_nightFadeDistance.y;
float sunlitAtmosphereIntensity = clamp(
    (cameraDist - fadeOutDist) / (fadeInDist - fadeOutDist),
    0.05, 1.0
);
float darken = clamp(dot(normalize(positionWC), atmosphereLightDirection), 0.0, 1.0);
```

This controls how the atmosphere darkening on the night side fades with
camera altitude. The defaults are:
- `nightFadeInDistance` = `5/2 * π * ellipsoid.minimumRadius` ≈ 31,785 km
- `nightFadeOutDistance` = `1/2 * π * ellipsoid.minimumRadius` ≈ 6,357 km

Google Earth uses 8,000 km / 3,000 km for the city-lights texture fade.

### 2.4 The `nightBlend` factor for texture compositing

```glsl
// Line 352
float nightBlend = 1.0 - clamp(
    czm_getLambertDiffuse(czm_lightDirectionEC, normalEC) * 5.0,
    0.0, 1.0
);
```

`nightBlend` is 0.0 on the day side, 1.0 on the night side, with a soft
transition. This is used to control per-layer alpha:

```glsl
// Line 221-222
#if defined(APPLY_DAY_NIGHT_ALPHA) && defined(ENABLE_DAYNIGHT_SHADING)
    textureAlpha *= mix(textureDayAlpha, textureNightAlpha, nightBlend);
#endif
```

This means each imagery layer can have `dayAlpha` and `nightAlpha`
values. If you set `dayAlpha = 0` and `nightAlpha = 1` for a city-lights
layer, it will **only show on the night side**. This is Cesium's
built-in, shader-level support for night textures — no custom shader
needed.

### 2.5 Conclusion: Cesium's terminator IS correct

The Cesium implementation is physically correct:
- Sun direction is fixed in ECEF (world coordinates) at the current
  clock time.
- Surface normals are in ECEF (model coordinates for the globe).
- The dot product determines day/night — it's the same in any
  coordinate space.
- When you orbit the camera, the terminator stays fixed on the globe.
- When time advances, the sun direction changes in ECEF, and the
  terminator sweeps across the surface.

**The "bug everyone hits" (from the Timetate article) does NOT apply
to Cesium.** That bug occurs when a custom shader uses view-space
normals with a world-space sun direction. Cesium's built-in
`enableLighting` uses the correct coordinate spaces internally.

---

## 3. Why our night side looks wrong (the real issue)

The Cesium terminator is correct, but our night side looks wrong for
three reasons:

### 3.1 No city lights (the biggest gap)

Without a night-lights texture, the night side is just "dark surface
texture." From space, this reads as a flat black/gray blob — not the
living, glowing Earth that Google Earth shows. This is the single
biggest visual difference.

Google Earth composites a **NASA Black Marble** (city lights) texture
on the night side. The lights make the terminator read as "real
day/night" instead of "broken rendering." Without lights, the same
correct terminator looks like a bug.

### 3.2 Harsh darkness (no ambient term)

Cesium's default `enableLighting` uses:
```glsl
float diffuseIntensity = clamp(
    czm_getLambertDiffuse(czm_lightDirectionEC, normalEC) * 5.0 + 0.3,
    0.0, 1.0
);
```

The `* 5.0` makes the terminator sharp. The `+ 0.3` adds a small
ambient term, but it's not enough. On the night side,
`diffuseIntensity` goes to 0.0 (the `+ 0.3` is multiplied by the
diffuse, not added as a floor). The night side is pitch black.

Google Earth has:
- City lights (which provide their own illumination)
- A small ambient term (moonlight, airglow) so the night side is
  never fully black
- A soft terminator (smoothstep, not a sharp Lambertian)

### 3.3 The "dark region follows the camera" illusion

The user reported: "when we move the globe only the globe should move
not the night side along with it."

This is actually **correct behavior**, but it *looks* wrong because of
issues 3.1 and 3.2. When you orbit the camera:
- The globe appears to rotate (from your perspective)
- The terminator stays fixed on the globe surface (correct)
- The night side appears to "move with the globe" (because it IS on
  the globe)

With city lights, this reads as "I'm flying around the Earth at night"
— obviously correct. Without city lights, it reads as "the dark area
is following the globe, which looks like a lighting bug."

**The fix is not to change the terminator behavior** (it's already
correct). **The fix is to add city lights and a small ambient term**
so the night side looks real instead of broken.

---

## 4. How Google Earth does it (from the official docs)

From the Google Earth Studio docs:

> "At high altitudes, Earth Studio renders a nighttime texture of the
> Earth with city lights. This texture fades out between 8000 km and
> 3000 km."
>
> "The appropriate shading is applied to 3D features on top of their
> existing textures, based on the angle of light."

So Google Earth uses:
1. **Per-fragment sun-direction shading** of the surface texture (same
   as Cesium's `enableLighting`).
2. **A separate night-lights texture** composited on the dark side,
   fading out between 8000 km and 3000 km altitude.
3. **Cloud shadows** cast on the landscape beneath them.

The night texture is a **separate imagery layer** with altitude-based
fade, not a custom shader. Cesium has the exact same capability via
`ImageryLayer.dayAlpha` / `ImageryLayer.nightAlpha` and
`Globe.nightFadeInDistance` / `Globe.nightFadeOutDistance`.

---

## 5. The Cesium API for night textures (exact code)

Cesium has first-class support for night textures. From the official
Cesium docs and PR #8868 (which added this feature):

```js
// Enable sun-based lighting (we already have this)
globe.enableLighting = true;
globe.dynamicAtmosphereLightingFromSun = true;

// Add a night-lights imagery layer
// Option A: Cesium ion "Earth at Night" (asset ID 3812)
const nightLayer = Cesium.ImageryLayer.fromProviderAsync(
  Cesium.IonImageryProvider.fromAssetId(3812)
);
nightLayer.dayAlpha = 0.0;   // invisible on the day side
nightLayer.nightAlpha = 1.0;  // fully visible on the night side
nightLayer.brightness = 2.0;  // boost the city lights
viewer.imageryLayers.add(nightLayer);

// Option B: NASA GIBS Black Marble (free, no API key, no ion token needed)
const nightLayer = viewer.imageryLayers.addImageryProvider(
  new Cesium.WebMapTileServiceImageryProvider({
    url: 'https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/wmts.cgi?',
    layer: 'VIIRS_Black_Marble',
    style: 'default',
    tileMatrixSetID: '500m',
    format: 'image/png',
    maximumLevel: 8,
  })
);
nightLayer.dayAlpha = 0.0;
nightLayer.nightAlpha = 1.0;
nightLayer.brightness = 2.0;
```

The `dayAlpha` / `nightAlpha` properties are compiled into the globe
shader's `APPLY_DAY_NIGHT_ALPHA` path (see section 2.4 above). The
shader automatically blends the layer's alpha based on the `nightBlend`
factor, which is derived from the sun direction. **No custom shader
needed.**

### 5.1 Altitude fade for the night texture

```js
// Match Google Earth's 8000 km / 3000 km fade band
globe.nightFadeInDistance = 8_000_000;   // 8000 km
globe.nightFadeOutDistance = 3_000_000;  // 3000 km
```

These control when the night-side atmosphere darkening fades in/out
with camera altitude. The city-lights layer itself stays visible (it's
controlled by `dayAlpha`/`nightAlpha`, not altitude), but the
atmosphere darkening that makes the night side look "night-like"
fades with these distances.

### 5.2 Ambient light (to prevent pitch-black night)

```js
// Increase the minimum brightness on the night side
globe.minimumBrightness = 0.05; // small ambient term (default varies)

// Or increase the sun light intensity (affects day side too)
viewer.scene.light = new Cesium.SunLight({ intensity: 2.5 });
```

---

## 6. Data sources for the night-lights texture

### Option A: Cesium ion "Earth at Night" (asset ID 3812)

- **Pros:** one-line setup, high quality, already processed.
- **Cons:** requires a Cesium ion account/token. The default
  grandfathered demo token may or may not include this asset. Free
  tier has a monthly request limit.

### Option B: NASA GIBS Black Marble (VIIRS)

- **URL:** `https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/wmts.cgi?`
- **Layer:** `VIIRS_Black_Marble`
- **TileMatrixSetID:** `500m` (or `1km` for lower resolution)
- **Format:** `image/png`
- **Pros:** free, no API key, no token, no request limit, CORS-enabled,
  tile-based (progressive loading, no pole pinching, no upfront
  download), time-enabled (can show different dates).
- **Cons:** need to verify the exact layer name and tile matrix set ID
  from the GIBS capabilities XML.

### Option C: Both (ion as primary, GIBS as fallback)

Use ion if a token is available; fall back to GIBS if not.

---

## 7. Implementation plan

### Phase 1: Add the night-lights layer (biggest visual win)

1. In `config.ts`, after viewer creation, add a night-lights imagery
   layer using NASA GIBS Black Marble (no token needed).
2. Set `dayAlpha = 0.0`, `nightAlpha = 1.0`, `brightness = 2.0`.
3. Set `globe.nightFadeInDistance = 8_000_000` and
   `globe.nightFadeOutDistance = 3_000_000` to match Google Earth.
4. Set `globe.minimumBrightness` to a small value (e.g. 0.05) to
   prevent pitch-black night.

### Phase 2: Tune the terminator softness

The `* 5.0` multiplier in the shader makes the terminator sharp. We
can't change the shader constant directly, but we can:
- Increase `globe.minimumBrightness` to add more ambient light.
- Increase `SunLight.intensity` to make the day side brighter (which
  makes the terminator appear softer by contrast).

### Phase 3: Verify the terminator is sun-locked

After adding city lights:
1. Orbit the camera — the terminator should stay fixed on the globe
   surface (same geographic locations stay dark/lit).
2. Animate the clock (`shouldAnimate = true`, `multiplier = 1000`) —
   the terminator should sweep across the surface as time advances.
3. The night side should show city lights; the day side should show
   normal imagery.

### Phase 4 (optional): Cloud shadows

Google Earth casts cloud shadows on the landscape. This requires a
`CustomShader` on the globe that samples the cloud texture and
darkens the surface where clouds are. This is more complex and can
be deferred.

---

## 8. Key takeaway

**The terminator is already correct in Cesium.** The night side IS
sun-locked — it stays fixed on the globe surface at a given time. When
you orbit the camera, you see different parts of the Earth, and the
night side appears to move across your screen because you're moving,
not because the terminator is following you.

**The reason it looks wrong is the missing city lights.** Without
city lights, the night side is a flat black blob that reads as a
rendering bug. With city lights (NASA Black Marble), the same
terminator reads as "real day/night" — exactly like Google Earth.

**The fix is to add a night-lights imagery layer**, not to change the
lighting logic. Cesium has built-in support for this via
`ImageryLayer.dayAlpha` / `nightAlpha` — no custom shader needed.

---

## 9. Sources

- Cesium GlobeFS.glsl source (day/night shading):
  https://github.com/CesiumGS/cesium/blob/0c585fe5/packages/engine/Source/Shaders/GlobeFS.glsl
- Cesium Globe API (nightFadeInDistance, nightFadeOutDistance):
  https://cesium.com/learn/cesiumjs/ref-doc/Globe.html
- Cesium ImageryLayer API (dayAlpha, nightAlpha):
  https://cesium.com/learn/cesiumjs/ref-doc/ImageryLayer.html
- Cesium PR #8868 (dayAlpha/nightAlpha feature):
  https://github.com/CesiumGS/cesium/pull/8868
- Cesium "Visualizing Imagery" tutorial (Earth at Night example):
  https://cesium.com/learn/cesiumjs-learn/cesiumjs-imagery/
- Cesium PR #6877 (ground atmosphere, night fade):
  https://github.com/AnalyticalGraphicsInc/cesium/pull/6877
- Google Earth Studio — Special Attributes (Time of Day, Clouds):
  https://earth.google.com/studio/docs/advanced-features/special-attributes/
- "Drawing day and night on a 3D globe" (the view-space vs world-space
  normal bug): https://dev.to/timetate/drawing-day-and-night-on-a-3d-globe-the-shader-behind-my-world-clock-391k
- NASA GIBS access basics:
  https://nasa-gibs.github.io/gibs-api-docs/access-basics/
- NASA GIBS map library usage (Cesium examples):
  https://nasa-gibs.github.io/gibs-api-docs/map-library-usage/
- NASA GIBS web examples (Cesium):
  https://github.com/nasa-gibs/gibs-web-examples
