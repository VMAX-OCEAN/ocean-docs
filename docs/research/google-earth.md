# How Google Earth Works

Google Earth is the reference standard for a "perfect" 3D globe. This document
breaks down its architecture, rendering techniques, and what we can learn for the
SIH-OCEAN project.

---

## Lineage (why the design is what it is)

Google Earth is **not** a web-native app. It's a 25-year-old C++ desktop engine
progressively ported to the browser. This history explains every architectural decision.

| Year | Milestone | Technology |
|---|---|---|
| 2001 | Keyhole EarthViewer (Intrinsic Graphics → Keyhole Inc.) | C++ desktop, OpenGL, **clip mapping** (the core invention) |
| 2004 | Google acquires Keyhole → "Google Earth" | Same C++ engine |
| ~2014 | Google Earth API plugin deprecated | C++ via NPAPI browser plugin |
| 2017 | Earth on Web (Chrome-only) | C++ engine compiled to **Native Client (NaCl)** |
| 2019 | Cross-browser port | C++ engine compiled to **WebAssembly (WASM)** |
| 2023–24 | UI rewrite | **Flutter** for UI chrome (web + Android + iOS); C++ engine still powers the globe |

**Key insight:** the globe (the "pale blue dot in the middle of the screen") is a
**C++ engine**, not JavaScript. The browser shell around it (menus, panels, search)
is Flutter. On web, the C++ engine runs as WASM.

---

## Core Rendering Trick: Clip Mapping / "Universal Texture"

This is the single most important concept. Without it, Google Earth is impossible.

### The Problem

To texture the whole Earth at 1-meter resolution needs a ~40 million × 20 million
texel texture — a mip-map pyramid of **~11 petabytes**. No GPU can hold that.

### The Solution

Invented at SGI by Chris Tanner (doi:10.1145/280814.280855), adapted by Keyhole/Google
as "Universal Texture":

1. **Virtualize a giant mip-map pyramid** in software — far more levels and resolution
   than any hardware can store.
2. At any given camera angle/height, you only ever **use a narrow "column" of the
   pyramid** — a specific set of mip levels across a specific region. The algorithm
   computes exactly which texels are needed for the current view.
3. **Page only those needed texels** from system RAM → GPU texture memory, in real
   time. Everything else stays on disk/server.
4. This is a **software-emulated clip-stack** (after SGI's hardware "clipmap" which
   virtualized a 170 GB texture at 60 Hz).

### Why This Beats Naive Tiling

Tiling (cutting Earth into millions of 256px squares, mip-mapping each independently)
causes visual artifacts — blurring, popping, seams. Universal Texture gives
**high-quality tri-linear / anisotropic filtering across the entire virtual texture**
as if it were one seamless image, because the filtering happens on the GPU over the
paged-in region.

**Modern equivalent:** This concept evolved into **3D Tiles** (the OGC standard Google
co-developed with Cesium) and **virtual texturing** in general. CesiumJS implements
the same idea for terrain/imagery streaming.

---

## Data Streaming Pipeline

Google's own description: *"we're constantly streaming 3D data and imagery across the
network, decompressing it and then showing it on the globe."*

```
Google servers (multi-terabyte imagery/terrain/3D mesh)
   │  quadtree-tiled, multi-LOD, compressed (JPEG/KTX2)
   ▼
Network fetch  ──►  Background WASM threads (decode + decompress)
   │                    │
   ▼                    ▼
Cache (RAM/disk) ──►  GPU texture memory (only the paged-in clip region)
                        │
                        ▼
                    WebGL render (60 Hz main thread)
```

**Critical performance detail (from Google's own benchmarks):** doing fetch + decode
on **background threads** (WASM threads / SharedArrayBuffer) is what keeps the main
render loop at high FPS. Without threading, frame-dropping is severe.

**Tiling structure:** quadtree on a Mercator projection. LOD 0 = single tile; each
level subdivides into 4. Higher LOD = smaller area, more detail. Tiles are requested
based on **Screen-Space Error (SSE)** — only fetch a tile if its error exceeds a
pixel threshold at the current view.

---

## Photorealistic 3D Tiles (modern building/city data)

For 3D buildings, cities, and terrain relief, Google now serves **Photorealistic 3D
Tiles** via the **Map Tiles API**:

- **Format:** OGC 3D Tiles (open standard, co-developed with Cesium) — each tile is glTF
- **Content:** 3D mesh textured with high-res satellite/aerial imagery (actual geometry)
- **Hierarchy:** Hierarchical LOD (HLOD) — quadtree/octree/k-d tree; parents are
  simplified versions of children
- **Implicit Tiling** (3D Tiles 1.1): compact sparse quadtrees/octrees, tiles located
  directly by `(level, x, y, [z])` → random access, efficient partial updates
- **KTX2 + ETC1S compression:** 10–30% smaller textures, ~30% faster loading, 80% less
  GPU memory
- **Renderable by:** CesiumJS, deck.gl, Cesium for Unreal/Unity, Three.js, Babylon.js,
  QGIS, Godot — any OGC 3D Tiles renderer
- **Session-based:** a root tileset request returns a `session` token; subsequent tile
  requests must include it + API key. A single root session allows ~3 hours of requests.

**Key for our project:** Google's Photorealistic 3D Tiles are designed to be consumed
by **CesiumJS** — the exact library we chose. The official Google docs show CesiumJS
as the primary renderer. We can drop Google's 3D Tiles straight into a Cesium viewer.

---

## Geometry & Precision Layer

- **WGS84 ellipsoid** (not a sphere) — accurate Earth shape
- **Hybrid multi-frustum logarithmic depth buffer + emulated double precision** —
  eliminates z-fighting and jittering at planet scale (coordinates in the 6-million+
  meter range). Cesium also solves this.
- **Ellipsoidal clipmaps** (academic follow-on): divides the ellipsoid into 3
  partitions, stitches seamlessly, streams geometry via clipmap application with
  geographic projection to minimize distortion.

---

## Current Web Stack (earth.google.com today)

| Layer | Technology |
|---|---|
| UI chrome (menus, search, panels, projects) | **Flutter** (compiled to web) — single codebase for web + Android + iOS |
| Globe rendering engine | **C++** (the original Keyhole engine), compiled to **WebAssembly** on web |
| Bridge | Flutter platform/method channels → C++ engine |
| Graphics | **WebGL** (via WASM, low-overhead GL calls) |
| Threading | WASM threads (SharedArrayBuffer) for fetch/decode |
| Data | Quadtree-tiled imagery + terrain + Photorealistic 3D Tiles (OGC 3D Tiles / glTF) |
| Texture technique | Universal Texture (software clip-mapping) |
| Compression | KTX2 / ETC1S for textures |

**Why not pure JS/WebGL?** JavaScript has function-call overhead into WebGL that limits
how much you can render at Earth's quality. The C++→WASM path gives near-native GL
access, letting Earth render more geometry and higher-res textures than a JS-only
engine could. The trade-off is a large WASM payload ("loads as if booting an OS") —
but smooth after.

---

## What This Means for SIH-OCEAN

We **cannot and should not** replicate Google Earth's architecture (C++/WASM engine,
petabyte tile servers, 25 years of engineering). But the **principles** map directly
onto our chosen stack:

| Google Earth concept | Our equivalent (CesiumJS + zarr-cesium) |
|---|---|
| Universal Texture / clip-mapping | Cesium's built-in terrain/imagery streaming (same quadtree + LOD + SSE logic) — free |
| Photorealistic 3D Tiles (OGC) | Cesium 3D Tiles — same standard; can load Google's 3D Tiles via Map Tiles API |
| Background-thread decode | Browser fetch + zarrita.js decodes Zarr chunks; Cesium handles tile decode internally |
| Quadtree LOD / Screen-Space Error | Cesium's tile selection — automatic, we don't write it |
| WGS84 + log-depth buffer (no jitter) | Cesium's precision system — built-in |
| Multi-terabyte virtual texture | Zarr chunk streaming — chunked arrays, streamed on demand, same "page only what you see" principle |
| KTX2 texture compression | Cesium supports KTX2; Zarr chunks use blosc/zstd compression |

**The single most important takeaway:** Google Earth's entire rendering philosophy is
**"stream only what the camera needs, at the resolution the screen needs, decode off
the main thread."** Our Zarr + zarr-cesium architecture implements exactly this for
ocean volumetric data — chunked, on-demand, parallel.

**One concrete opportunity:** if we want our globe to look as polished as Google Earth,
we can **load Google's Photorealistic 3D Tiles** (free tier via Map Tiles API key) into
our Cesium viewer for coastal/city regions, and overlay our ocean volumetric data on
top. This gives Google-Earth-quality basemap + our scientific data layer.
