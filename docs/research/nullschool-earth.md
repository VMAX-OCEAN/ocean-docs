# How earth.nullschool.net Works

earth.nullschool.net is the reference for animated weather/ocean scalar visualization.
This document breaks down its architecture and the techniques we can learn from.

---

## Architecture (open-source 2013 version: github.com/cambecc/earth)

| Layer | Technology | Purpose |
|---|---|---|
| Globe projection | **D3** (geo projections: orthographic, etc.) | Maps lat/lon → screen pixels; handles sphere distortion |
| Map outlines | **SVG** (coastlines/lakes/rivers from Natural Earth) | The base map drawn under the data |
| Animation canvas | **HTML5 Canvas 2D** (one layer) | Draws moving wind/current particles |
| Overlay canvas | **HTML5 Canvas 2D** (second layer on top) | Draws the colored temperature/scalar field |
| Data pipeline | **grib2json** (Java, uses Unidata netcdf-java) | Server-side: GFS GRIB2 → JSON; runs offline, results pushed to S3 |
| Hosting | Static S3/Cloudflare | No server logic at runtime — pure static files |
| Color scales | ColorBrewer2, Kindlmann, cubehelix, Dave Green | Scientific colormaps for temperature etc. |

**Critical:** nullschool is **NOT WebGL/3D**. It's a **2D D3 + Canvas** app with an
orthographic projection that *looks* like a globe. The "3D" is an illusion — a
projected sphere. This is why it's so fast and runs everywhere.

---

## How Temperature is Rendered (the key technique)

Temperature (and SST, salinity, etc.) on nullschool is a **scalar field overlay**
rendered in steps:

### Step 1 — Bilinear interpolation of the scalar field to a pixel grid

- GFS data is on a 1° grid (~360×180 points). The screen has millions of pixels.
- For every overlay-canvas pixel inside the globe's bounding sphere, the code:
  1. Inverts the screen pixel (x,y) → (lat,lon) using D3's projection inverse
  2. Finds the 4 surrounding grid cells in the data
  3. **Bilinearly interpolates** the temperature value at that point
  4. Maps the value → color via the chosen **colormap** (e.g., temperature → blue-to-red)
  5. Writes the color to the overlay canvas pixel
- This is **expensive** (nullschool's own comment: "this operation is quite costly") —
  done per-pixel in JS.

### Step 2 — Masking to the globe

- The overlay canvas must only show colors *inside* the globe's silhouette.
- nullschool re-renders the globe's bounding sphere to a hidden canvas as a mask, then
  uses pixel-alpha to clip the overlay to the globe shape.

### Step 3 — The colormap (the "temperature effect")

- A 1D **lookup table** (LUT): temperature value → RGB color.
- nullschool uses perceptually-uniform scales (Kindlmann, cubehelix) plus ColorBrewer
  diverging scales for anomalies (blue-white-red for SST anomaly).
- The overlay canvas is drawn with `globalAlpha` for opacity blending over the map.

---

## How Wind/Current Particles are Animated (separate from temperature)

Temperature is a **static colored overlay** per timestep. Wind/current is **animated
particles** — a completely different technique:

1. Spawn N particles at random grid cells.
2. Each frame: look up the (u,v) velocity vector at the particle's position (bilinear
   interp), move the particle by `velocity × dt`.
3. **Projection distortion correction**: on a globe, a particle moving "north" from
   the screen center goes straight up, but from the edge it curves toward the pole.
   nullschool uses **finite-difference approximations** of the projection's Jacobian
   to correct particle paths so they follow true great-circle-ish flow.
4. Draw each particle as a short fading line (trail). Particles "die" after a lifetime
   and respawn.
5. The animation is a **2D Canvas redraw loop** — no GPU, no shaders. Pure JS. This is
   why it's CPU-heavy but works everywhere.

---

## The Modern nullschool (closed-source, 2015+)

The live earth.nullschool.net has evolved beyond the open repo:

- Added **ocean surface currents, SST, SST anomaly, waves, aurora, fires, particulates,
  water temp at depth, ocean currents at depth**
- Added a **"detailed" tiled base map** (Natural Earth 6 at 1:7.5m, 6 zoom levels,
  quadtree tiling) — because the original single-file map couldn't zoom
- Uses a **non-Web-Mercator tiling scheme** to show poles cleanly (most map sites can't)
- Still **2D Canvas-based** for the data overlay (the author confirmed the open repo
  is "frozen for posterity"; the live version is closed-source)

---

## Data Sources (nullschool)

| Variable | Source | Update |
|---|---|---|
| Wind, temp, RH, pressure | NOAA GFS (GRIB2) | Every 3 hours |
| Ocean surface currents | — | Daily |
| Sea surface temperature (SST) | RTG-SST, OSTIA, OI SST | Daily |
| SST anomaly | RTG-SST (1981-2011 avg), OSTIA (Pathfinder climatology) | Daily |
| Ocean waves | — | Every 3 hours |
| Auroras | — | Every 30 minutes |

---

## Key Takeaways for SIH-OCEAN

1. **nullschool's temperature rendering is 2D scalar-field → colormap → canvas.** It
   does NOT do true 3D volumetric depth. For our PS (which requires depth-resolved 3D
   volumetric views), nullschool's technique is the **2D surface layer** only — we need
   more for the 3D part.

2. **The colormap LUT approach is correct** — we use the same idea but on the GPU
   (Cesium/zarr-cesium shader) instead of Canvas 2D, which is instant for palette/range
   changes.

3. **Particle advection for currents** — nullschool does it in JS on CPU. We use
   `cesium-wind-layer` which does the same algorithm on the GPU (10k+ particles, 60 FPS).

4. **Non-Web-Mercator tiling** — nullschool's insight that Web Mercator can't show
   poles cleanly matters for ocean data near Antarctica/Arctic. CesiumJS uses a
   geographic projection that handles this correctly.

5. **Static hosting** — nullschool pre-computes everything server-side and serves
   static files. Our Zarr approach is similar (pre-converted chunks, streamed on demand)
   but more dynamic (any subset, any time).
