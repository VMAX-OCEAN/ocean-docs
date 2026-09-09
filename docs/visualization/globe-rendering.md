# Globe Rendering — The "Perfect Globe"

How to achieve a Google-Earth-quality globe using CesiumJS, with real terrain,
bathymetry, imagery, and atmosphere.

---

## The Three-Layer Globe

All built into CesiumJS — no custom shaders needed:

### 1. Terrain + Bathymetry

```js
// Cesium World Terrain (land elevation)
viewer.terrainProvider = await Cesium.createWorldTerrainAsync();

// OR with GEBCO bathymetry for seafloor relief
viewer.terrainProvider = await Cesium.GeoTerrainProvider.fromUrl(
  'https://tiles.gebco.net/...'
);
```

This gives real elevation — mountains rise, ocean floor has ridges/trenches. This is
what makes it look like Google Earth, not a smooth ball.

### 2. Imagery (satellite base layer)

Options:
- **Bing Maps Aerial** (Cesium ion default, free tier) — photorealistic
- **MapTiler satellite** — high quality, free API key
- **NASA Blue Marble** — equirectangular imagery layer (the look from our current file)
- **ArcGIS World Imagery** — alternative satellite

```js
viewer.imageryLayers.addImageryProvider(
  new Cesium.IonImageryProvider({ assetId: 2 })  // Bing Aerial
);
```

For **light theme**: use a brighter imagery (MapTiler satellite or topographic) or
adjust `scene.backgroundColor` to white.

### 3. Atmosphere + Lighting (day/night)

```js
// Sky atmosphere (blue rim/halo, sun-aware scattering)
viewer.scene.skyAtmosphere.show = true;

// Day/night terminator from real sun position
viewer.scene.globe.enableLighting = true;
viewer.scene.globe.dynamicAtmosphereLighting = true;
viewer.scene.globe.dynamicAtmosphereLightingFromSun = true;

// Visible sun + moon discs at correct positions
viewer.scene.sun.show = true;
viewer.scene.moon.show = true;

// Set clock to real time for live terminator
viewer.clock.currentTime = Cesium.JulianDate.now();
```

See [`day-night-lighting.md`](day-night-lighting.md) for full details.

---

## Why This Beats Hand-Rolled Three.js

Our current `realistic-earth-globe.html` is a hand-rolled Three.js sphere:

```js
// Current approach (fragile, limited)
const globe = new THREE.Mesh(
  new THREE.SphereGeometry(1, 96, 96),
  new THREE.MeshBasicMaterial({ color: 0x1b3a5c })
);
texLoader.load('https://cdn.jsdelivr.net/npm/three-globe/example/img/earth-blue-marble.jpg', ...);
```

Problems:
- **No terrain** — flat sphere, no elevation
- **No bathymetry** — no seafloor relief (critical for ocean viz)
- **No geospatial accuracy** — sphere geometry, wrong for Argo/Glider overlay
- **No LOD streaming** — one static texture, no zoom detail
- **Fragile** — depends on jsDelivr CDN
- **No day/night** — would need custom shader (sun position math + dot product + smoothstep)
- **Dark only** — hardcoded `background:#000`

CesiumJS solves all of these with built-in features.

---

## Light Theme Configuration

Since the project requires a light theme:

| Element | Setting |
|---|---|
| Background | `viewer.scene.backgroundColor = Cesium.Color.WHITE` (or light gray) |
| Sky box | Disable (`viewer.scene.skyBox.show = false`) or use light gradient |
| Sun | Keep visible (`scene.sun.show = true`) — looks good on light bg |
| Atmosphere | Keep — the blue rim works on light backgrounds |
| Imagery | Use brighter base (MapTiler satellite or topographic) or Blue Marble |
| UI panels | Light Material UI / shadcn theme |
| Starfield | Remove (our current file has 1500 stars — delete for light theme) |
| Day/night | Keep `enableLighting = true` — night side darker against light bg is correct |

---

## Performance

| Operation | Cost |
|---|---|
| Globe render (terrain/imagery) | 60 FPS — Cesium LOD streaming, only visible tiles fetched |
| Day/night terminator | 0 cost — shader calculation, no data fetch |
| Atmosphere | 0 cost — shader calculation |
| Zoom/pan | Smooth — tiles stream on demand with SSE-based selection |

Cesium uses the same principle as Google Earth: **stream only what the camera needs,
at the resolution the screen needs**. Quadtree LOD + Screen-Space Error tile selection.

---

## Optional: Google Photorealistic 3D Tiles

For Google-Earth-quality city/coastal regions, load Google's Photorealistic 3D Tiles:

```js
const tileset = viewer.scene.primitives.add(
  new Cesium.Cesium3DTileset({
    url: "https://tile.googleapis.com/v1/3dtiles/root.json?key=YOUR_API_KEY",
    showCreditsOnScreen: true,
  })
);
```

This gives photorealistic 3D buildings and terrain for populated areas, overlaid with
our ocean data. Requires a Google Maps Platform API key (free tier available).

**Note:** Check Map Tiles API Terms of Service for usage restrictions.
