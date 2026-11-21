# Google Earth — Dark Side & Clouds: Research Notes

Purpose: capture exactly how google.earth.com renders the night side and
the cloud layer, including the precise fade thresholds, so we can pick
the best implementation strategy for our Cesium-based ocean globe.

Sources are cited inline. Everything below is research only — no code
changes are made in this document.

---

## 1. The night side (Time of Day)

### 1.1 What Google Earth actually does

From the official Google Earth Studio docs
(https://earth.google.com/studio/docs/advanced-features/special-attributes/):

> "Time of Day is a powerful cinematic effect. When enabled, Earth
> Studio renders realistic lighting, stars, and atmospherics based on
> the position of the sun. These elements are controlled by a date and
> time (GMT) value.
>
> Depending on your location and the time of day at that location,
> Earth Studio will simulate daylight, nighttime, dawn and dusk.
>
> **At high altitudes, Earth Studio renders a nighttime texture of the
> Earth with city lights. This texture fades out between 8000 km and
> 3000 km.**
>
> The appropriate shading is applied to 3D features on top of their
> existing textures, based on the angle of light. **Shadows are cast
> by clouds on the landscape beneath them.**
>
> When Time of Day is enabled, Earth Studio will generate accurate
> atmospheric effects. These look especially beautiful at dawn and dusk."

Key takeaways:

1. **Two distinct mechanisms**, not one:
   - **Per-fragment sun-direction shading** of the existing surface
     texture (the "angle of light" — this is what makes the day side
     bright and the night side dark, with a soft terminator). This is
     always on when Time of Day is on, at every altitude.
   - **A separate "night texture" with city lights** that is composited
     on top, *only at high altitude*. This is what gives Google Earth
     its characteristic glowing-cities-at-night look from space. It
     fades out as you descend: fully visible above 8000 km, fully gone
     below 3000 km.
2. **Clouds cast shadows on the ground** beneath them — this is a
   real shadow pass, not just darkening the cloud itself.
3. **Atmospherics are sun-aware** — dawn/dusk produce colored sky, and
   overcast skies (where clouds are present) tint the atmosphere blue.

### 1.2 Why our current night side looks wrong

Our current setup uses only mechanism #1 (per-fragment sun shading via
`globe.enableLighting = true`). That is *correct* in principle, but it
looks different from Google Earth for two reasons:

a. **No night texture.** Without city lights, the night side is just
   "dark surface texture" — which reads as a flat black/gray blob from
   space, not the living Earth Google Earth shows. This is the single
   biggest visual gap.

b. **No ambient term.** Cesium's default `enableLighting` uses a pure
   Lambertian term: pixels where the sun is below the horizon go to
   *zero* contribution from the surface texture. Real Earth is never
   fully black on the night side — there's moonlight, airglow, and
   (critically) the city-light texture. Google Earth's night texture
   is what fills that gap; without it, the night side is too harsh.

c. **The "dark region follows the camera" illusion.** This is actually
   *correct* behavior — the terminator is fixed in space (sun-locked),
   and the Earth rotates underneath it. But because our night side is
   just flat black with no city lights, it *looks* like a rendering bug
   rather than a real terminator. Adding the night texture makes the
   same behavior read as "correct day/night" instead of "broken
   lighting."

### 1.3 Cesium's built-in support for the night texture

Cesium has first-class support for exactly this. From the Cesium source
and API:

- `Globe.enableLighting = true` — per-fragment sun shading (mechanism
  #1). We already have this.
- `viewer.imageryLayers` — you can add a second imagery layer using a
  **night imagery provider** (e.g. NASA Black Marble) and configure it
  to only show on the dark side. Cesium's `GlobeFS` shader already
  blends a "night" version of imagery when lighting is enabled — but
  only if you supply a night texture/source. The relevant Cesium
  properties are:
    - `Globe.nightFadeInDistance` / `Globe.nightFadeOutDistance` —
      these control the altitude fade of the night texture, exactly
      mirroring Google Earth's 8000 km → 3000 km band.
    - The Cesium PR that added this
      (https://github.com/AnalyticalGraphicsInc/cesium/pull/6877)
      explicitly cites Google Earth as the visual reference and uses
      the same altitude-based fade approach.

So the *correct* Cesium-native way to match Google Earth's night side
is:

1. Keep `enableLighting = true` (already done).
2. Add a NASA Black Marble (or similar) night-lights imagery layer.
3. Set `nightFadeInDistance` / `nightFadeOutDistance` to match Google
   Earth's 8000 km / 3000 km thresholds (or tune to taste).

This is far better than trying to write a custom shader to fake city
lights, because Cesium's shader already knows how to composite the
night texture *only on the dark side* and fade it with altitude.

### 1.4 Data source for the night texture

- **NASA Black Marble** — the standard, free, public-domain
  night-lights dataset. Available as tiled imagery via NASA GIBS
  (https://earthdata.nasa.gov/gibs) with no API key, CORS-enabled,
  tile-based (so it streams progressively like terrain, no pole
  pinching, no 7 MB single-texture download).
- GIBS provides it as a WMTS layer; Cesium has a built-in
  `WebMapTileServiceImageryProvider` that consumes this directly.

---

## 2. Clouds

### 2.1 What Google Earth actually does

From the official Google Earth Studio docs (same page as above):

> "Earth Studio renders clouds over the Earth by default. Cloud data
> is pulled from NOAA multiple times a day, so you'll always have a
> fairly accurate depiction of current weather patterns around the
> world.
>
> **When Time of Day is turned off, clouds begin to fade out at
> 20,000 km. Below 8000 km, they don't render at all.**"

And from the consumer Google Earth support docs
(https://support.google.com/earth/answer/9261465):

> "Google Earth shows stationary clouds by default, and animated
> clouds fade and then disappear when you zoom in."
> "Both animated and stationary clouds fade, and then disappear, when
> zooming in."

And from the Google Earth team's own Medium post
(https://medium.com/google-earth/see-the-clouds-animate-in-google-earth-175c0fb140e4):

> "The cloud data you see in Google Earth is a mosaic of seven
> individual satellite images, put together by the U.S. Naval Research
> Laboratory. We get a new one of these images roughly once an hour...
>
> The complete cloud image provided to Google by NRL is 9000x4500
> pixels — that's about 40 million pixels. At Google, we perform some
> additional processing to prepare it for use in Earth. Using Google
> Earth Engine, we smooth out some of the hour-to-hour changes, add
> visual shadowing effects to enhance the appearance, and export a
> 24-hour period to our own scalable video format.
>
> **Our scalable video format supports downloading, decoding and
> rendering just the pixels needed for your current view of the Earth,
> at a resolution appropriate for your screen and zoom level.**
>
> We display the clouds at a comfortable animation rate of one frame
> per second, corresponding to one hour of cloud motion time per
> second in Google Earth, with smooth blending (or cross-fading)
> between successive frames."

Key takeaways:

1. **Cloud fade thresholds (Time of Day OFF):** begin fade at
   **20,000 km**, fully gone below **8,000 km**. This is *much* higher
   than our current 500 km / 350 km band — Google Earth hides clouds
   far earlier in the zoom-in.
2. **Cloud fade thresholds (Time of Day ON):** the docs don't give
   explicit numbers for this case, but the implication is that clouds
   persist longer (so you can see cloud shadows on the landscape and
   lit clouds at dawn/dusk), but still fade out as you approach the
   surface.
3. **Data source:** NOAA / NRL mosaic, ~9000×4500, refreshed hourly.
4. **Delivery:** Google uses a *custom scalable video format* — a
   tileable, resolution-adaptive video. They download only the pixels
   needed for the current view at the current zoom. This is the cloud
   equivalent of quadtree imagery — *not* a single equirectangular
   texture stretched over a sphere.
5. **Animation:** 1 fps playback = 1 hour of real cloud motion per
   second, with cross-fade between frames.
6. **Visual processing:** Google Earth Engine pre-processes the cloud
   data to add "visual shadowing effects" — i.e. the clouds are not
   just alpha-textured; they have built-in shading that makes them
   look volumetric/3D.

### 2.2 Why our current clouds look wrong / different

Our current approach (and its problems):

- **Single equirectangular PNG on an ellipsoid shell.** This is the
  root cause of the pole pinwheel artifact (UV pinching at ±90°) and
  the reason clouds don't sharpen as you zoom — there's no higher-LOD
  data to load.
- **One 2048×1024 (now) or 4096×2048 (before) image.** Google Earth's
  source is 9000×4500 and delivered as a *scalable video format* that
  streams tiles. We download the whole thing up front.
- **No animation.** Google Earth animates 24 hours of cloud movement
  at 1 fps. Ours is a static image with a slow rotation hack.
- **No cloud shadows on the ground.** Google Earth casts shadows from
  clouds onto the landscape. Ours doesn't.
- **Fade band is way too low.** We fade clouds between 350 km and
  500 km. Google Earth fades between 8,000 km and 20,000 km. This is
  why our clouds are still visible when zoomed in much further than
  Google Earth allows.
- **Lighting mismatch.** We fixed the "clouds bright on night side"
  issue by enabling normal-based lighting on the shell, but Google
  Earth's clouds have *built-in* visual shadowing from Earth Engine
  preprocessing, so they look 3D even without real-time lighting.

### 2.3 Implementation possibilities for clouds (ranked)

#### Option A: Keep the ellipsoid shell, tune the fade band (smallest change)

- Change fade band from 350–500 km to 8000–20000 km to match Google
  Earth.
- Keep the pole fade shader fix.
- Keep the 2048×1024 texture.
- **Pros:** minimal change, fast, no new dependencies.
- **Cons:** still has the fundamental single-texture limitations (no
  zoom-adaptive detail, pole artifact only masked not eliminated, no
  animation, no cloud shadows).

#### Option B: Replace the shell with a tiled cloud imagery layer

- Use a real tile-based cloud imagery provider (e.g. NOAA GIBS cloud
  layers, or a tile pyramid built from the matteason image).
- Add as a second `ImageryLayer` on the globe.
- Set `minimumTerrainLevel` / `maximumTerrainLevel` to control when
  it fades out, matching Google Earth's 8000–20000 km band.
- **Pros:** no pole pinching (tiling schemes handle poles correctly),
  progressive loading, zoom-adaptive detail, no 7 MB upfront
  download, native Cesium LOD.
- **Cons:** imagery layers are UV-locked to the globe surface — they
  rotate *with* the Earth, so we lose the independent cloud drift
  effect. No animation unless we swap tile URLs over time (possible
  but more work). Cloud shadows still not supported.

#### Option C: Use a Cesium `CustomShader` on the globe for clouds + lighting

- Write a `CustomShader` that samples a cloud texture in the globe's
  own fragment shader, applies sun-direction lighting to the cloud
  term, and composites it over the surface.
- This gives cloud shadows "for free" (the shader knows both the
  surface point and the cloud density above it).
- **Pros:** best visual fidelity (cloud shadows, sun-lit clouds,
  unified lighting), no pole artifact if the cloud texture is tiled.
- **Cons:** most complex to implement; `CustomShader` is a newer
  Cesium API and has a learning curve; cloud animation requires
  uniform updates per frame.

#### Option D: Hybrid — tiled cloud imagery for the static base + shell for animation

- Use Option B (tiled imagery) for the high-fidelity static cloud
  view from space.
- Optionally layer a thin, low-res animated shell on top for the
  "drift" effect, with very low opacity.
- **Pros:** gets both fidelity and animation.
- **Cons:** two cloud systems to maintain; potential visual
  conflicts.

#### Option E: Use a real cloud tile service (NOAA GIBS / OpenWeatherMap)

- NOAA GIBS provides cloud layers as WMTS tiles, free, no API key,
  CORS-enabled, tile-based (so progressive loading and no pole
  pinching).
- Can be added as a `WebMapTileServiceImageryProvider` imagery layer.
- Time-enabled — GIBS supports a `time` parameter per tile, so we
  can animate clouds by changing the layer's time over the clock.
- **Pros:** real data, tile-based, animatable, free, no API key,
  handles poles correctly, zoom-adaptive detail.
- **Cons:** GIBS cloud layers are typically IR/visible satellite
  composites that may look different from the "white cloud map"
  aesthetic; need to pick the right GIBS layer (e.g. `MODIS_Terra_
  CorrectedReflectance_Bands367_Day` or a cloud-top product).

### 2.4 Recommendation

For the *immediate* goal of matching Google Earth's look and fixing
the visible artifacts, the ranking is:

1. **Option A (tune fade band) — do first, today.** It's a 2-line
   change and immediately fixes the "clouds visible too long when
   zoomed in" mismatch. No risk.

2. **Option B or E (tiled cloud imagery) — do next, as the real
   fix.** This eliminates the pole artifact at its source, gives
   zoom-adaptive detail, and removes the 7 MB upfront download.
   Option E (NOAA GIBS) is preferable because it's real data, free,
   and animatable, but requires picking the right layer. Option B
   (build a tile pyramid from the matteason image) is a fallback if
   GIBS layer selection proves finicky.

3. **Option C (CustomShader) — long-term, if needed.** Only worth
   the complexity if cloud shadows on the landscape become a hard
   requirement. For an ocean-data visualization platform, cloud
   shadows on the *ocean* are arguably less important than on land.

4. **Option D (hybrid) — skip unless animation is critical.** Adds
   complexity for marginal benefit.

---

## 3. Summary of thresholds (Google Earth reference values)

| Feature | Fade start (begin to disappear) | Fade end (fully gone) |
|---|---|---|
| Clouds (Time of Day OFF) | 20,000 km | 8,000 km |
| Clouds (Time of Day ON) | (higher than 8,000 km, exact value not documented) | (still fades before surface) |
| Night city-lights texture | 8,000 km | 3,000 km |
| Ocean overlay (smooth ocean) | 630 km | 400 km |

Our current values vs. Google Earth:

| Feature | Our current | Google Earth |
|---|---|---|
| Cloud fade | 350–500 km | 8,000–20,000 km |
| Night texture | (none) | 3,000–8,000 km fade |

---

## 4. Next steps (proposed, not yet implemented)

1. **Clouds — Option A (immediate):** change fade band from
   350–500 km to 8000–20000 km in `clouds.ts`. Two-line change.
2. **Night side — add NASA Black Marble imagery layer:** add a
   second imagery layer using GIBS WMTS Black Marble, configure
   `nightFadeInDistance` / `nightFadeOutDistance` to 8000 km / 3000 km.
   This is the single biggest visual win for the night side.
3. **Clouds — Option E (next session):** evaluate NOAA GIBS cloud
   layers as a tiled, animatable replacement for the ellipsoid shell.
   If a good layer is found, replace the shell entirely (eliminates
   pole artifact, adds animation, removes upfront download).
4. **Cloud shadows (future):** only if needed, via Option C
   (CustomShader).

---

## 5. Sources

- Google Earth Studio — Special Attributes:
  https://earth.google.com/studio/docs/advanced-features/special-attributes/
- Google Earth Help — See clouds in Google Earth:
  https://support.google.com/earth/answer/9261465
- Google for Developers — See clouds in Google Earth:
  https://developers.google.com/maps/documentation/earth/see-clouds
- Google Earth team Medium — See the clouds animate in Google Earth:
  https://medium.com/google-earth/see-the-clouds-animate-in-google-earth-175c0fb140e4
- Google Earth Blog — The 'Clouds' layer in Google Earth:
  https://gearthblog.com/blog/archives/2015/11/clouds-layer-google-earth.html
- Cesium PR #6877 — Add ground atmosphere (cites Google Earth, adds
  night fade distances): https://github.com/AnalyticalGraphicsInc/cesium/pull/6877
- Cesium Community — Adding clouds to central body:
  https://community.cesium.com/t/adding-clouds-to-central-body/821
- Ricky Reusser — Night and Day (Mapbox terminator + Black Marble):
  https://rreusser.github.io/notebooks/night-and-day/
- NASA GIBS — Black Marble / night lights:
  https://earthdata.nasa.gov/gibs
- matteason/live-cloud-maps (our current cloud texture source):
  https://github.com/matteason/live-cloud-maps
