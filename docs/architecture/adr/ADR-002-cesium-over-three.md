# ADR-002: CesiumJS over Three.js for the 3D Globe Engine

## Status

Accepted

## Date

2026-09-10

## Context

PS requirement **F1** (R1) mandates a browser-based, platform-independent 3D render of
the full water column: depth slices, isosurfaces, time animation. The PS names the
render stack as **WebGL / Three.js _or_ Cesium.js** — either satisfies the mandate
(`problem-statement/PROBLEM-STATEMENT-ANALYSIS.md:32,62`).

This ADR fixes the globe engine only. The ocean-field render path (custom
`ImageryProvider` vs `zarr-cesium` providers) is decided separately in
`docs/research/d4-lib-pins.md` §5; the `cesium@1.142.0` pin is `d4-lib-pins.md` §3.

Constraint: **free-only, $0/month**. No paid engine, no paid tile/terrain plan.

The original prototype (`realistic-earth-globe.html`) was a hand-rolled Three.js
`SphereGeometry(1, 96, 96)` with a CDN Blue Marble texture — a perfect sphere, no
terrain, no LOD, no geospatial coordinate system, no real day/night
(`research/individuals/lakshya/approach-comparison.md` Shift 1). Argo/Glider markers
placed at real lat/lon would be offset from a perfect sphere; Earth is a WGS84
oblate spheroid.

## Decision

**Use CesiumJS (`cesium@1.142.0`) as the globe engine.** Three.js is rejected for the
globe role; it remains acceptable as an embedded non-geospatial renderer if ever
needed, but not as the geo substrate.

CesiumJS advantages that map directly to F1 and the mandate set:

| Need (F1 / mandate) | CesiumJS provision | Source (access 2026-09-10) |
|---|---|---|
| Geospatially accurate overlay (Argo/Glider, bbox) | High-precision **WGS84** globe | `https://cesium.com/platform/cesiumjs/` |
| Real terrain + bathymetry | Streams Cesium World Terrain; World Bathymetry (GEBCO 2023) via ion | `https://cesium.com/platform/cesiumjs/` ; `docs/research/d4-lib-pins.md` §9 |
| Imagery at any zoom | Imagery/terrain layer streaming, open + custom tiling schemes | `https://cesium.com/platform/cesiumjs/` |
| LOD / performance | Quadtree LOD + Screen-Space Error tile selection | `docs/architecture/tech-stack.md` |
| Real day/night terminator | `scene.globe.enableLighting = true` (sun from clock, no shader math) | `docs/architecture/tech-stack.md` |
| Atmosphere | Built-in Rayleigh + Mie single-scatter | `docs/architecture/tech-stack.md` |
| Zarr → globe without backend | `zarr-cesium@0.2.0` providers stream Zarr from HTTP/S3/GCS with no preprocessing/backend | `https://github.com/NOC-OI/zarr-cesium` README (access 2026-09-10) |
| Free + open | **Apache 2.0**, free commercial and non-commercial | `https://cesium.com/platform/cesiumjs/` |
| WebGL2 baseline | Locked `cesium@1.142.0`; WebGL2 effectively mandatory (billboards/labels since 1.140) | `docs/research/d4-lib-pins.md` §3 ; `docs/performance/reference-laptop.md` |

Engine pins (registry-verified, access 2026-09-10):

- `cesium@1.142.0` (2026-06-01T20:02:38Z; npm latest `1.145.0`). Exact pin per
  `d4-lib-pins.md` §3: 101-day soak, `zarr-cesium` peer-compatible, fork wind-layer
  compatible; avoids 1.145 `ClippingPolygons` freeze.
- `zarr-cesium@0.2.0` (2026-08-21T14:32:01Z, `gitHead 1e5f18daccbb…`); peer
  `cesium >=1.119.0 <2`; MIT; deps `zarrita ^0.7.4`, `zarr-maps-tiling ^0.2.0`,
  `zarr-maps-colormap ^0.2.0`, NOC `cesium-wind-layer` v0.11.1 tarball.
- Providers: `ZarrLayerProvider` (2D scalar), `ZarrCubeProvider` (3D cube / slices),
  `ZarrCubeVelocityProvider` (U/V particles). README states support for CesiumJS
  1.119+ "including CesiumJS 1.142+".

## Consequences

Positive:

- Geospatial correctness (WGS84) for free — marker placement, bbox/spatial queries,
  terrain draping do not need to be built.
- Terrain, imagery streaming, LOD, day/night, atmosphere are engine features, not
  custom shader projects. Removes the "months of work" Three.js path
  (`approach-comparison.md` Shift 1).
- `zarr-cesium` is purpose-built for the Zarr→Cesium case, covering all three
  render modalities (scalar, cube, velocity) with no backend in the hot path.
- Precedent: DOVis (Indian Ocean, Cesium) and OceanStream globe-3d-viewer (Cesium,
  Copernicus) are the closest-matching shipped systems
  (`docs/research/platform-comparison.md`).
- Bundle/precision cost is real but bounded; the engine is Apache-2.0 and free.

Negative / accepted risks:

- **Bundle size:** Cesium is heavy vs Three.js (static assets ~8 MB class). Mitigation:
  Cloudflare Pages host choice + splitting; explicitly an accepted tradeoff for
  geospatial correctness (`d4-lib-pins.md` §8).
- **WebGL2 effective requirement** on 1.142 for billboards/labels and 5000
  Argo/Glider markers. Weak-iGPU machines may fail the FPS gate; device matrix and
  floor config documented in `docs/performance/reference-laptop.md`.
- **ion quota dependency** for terrain/imagery (Community tier). Mitigation:
  Sentinel-2 assetId 3954 + World Bathymetry 2426648 only, `baseLayer:false`
  (`d4-lib-pins.md` §7, §9). Quota sufficiency still conditional pending measured
  demo bytes.
- **Dependency freshness:** `zarr-cesium` is pre-1.0 (0.2.0). Mitigated by Phase 0
  de-risk + custom `ImageryProvider` fallback (`d4-lib-pins.md` §5, §10).
- **Performance claims unverified:** slice ms / FPS are UNVERIFIED until the locked
  reference machine run (`docs/performance/reference-laptop.md` §8). No numbers are
  claimed here.

## Alternatives

### Three.js (`three@0.186.0`, MIT) — REJECTED

| Factor | Assessment |
|---|---|
| Raw flexibility | Highest — render anything, any shader |
| Bundle | Smaller than Cesium |
| nordicseas3d precedent | Real: the most complete open-source 3D ocean viewer uses React + Three.js + zarrita, browser-direct Zarr, with slices, isosurfaces, particles, class clouds (`docs/research/open-source-projects.md` §3; README access 2026-09-10) |
| **Geospatial** | **None.** Sphere geometry, no WGS84 ellipsoid, no geospatial coordinate system. Argo/Glider at real lat/lon misplace |
| **Terrain / bathymetry** | No streaming terrain; a flat/bump sphere only |
| **Imagery streaming / LOD** | No quadtree LOD, no SSE tile selection; a static texture |
| **Day/night, atmosphere** | Hand-written shaders (sun-vector math, Rayleigh/Mie) — error-prone |
| **Cost to parity** | Months of custom work to replicate what Cesium gives free |

Reject reason: wrong tool class. Three.js is a general 3D library, not a geospatial
engine (`approach-comparison.md` Shift 1). Its virtues (flexibility, bundle) do not
compensate for the missing geo substrate that F1 + the mandate set require.

Sub-alternatives rejected too:

- **`three-globe@2.45.2`** (MIT, peer `three >=0.154`, access 2026-09-10): a data-viz
  globe object — `globeImageUrl`, `bumpImageUrl` (fake terrain), `showAtmosphere`
  halo, hex/arcs/points, slippy tile engine. Still an equirectangular sphere; no
  WGS84 ellipsoid, no real terrain, no geospatial coordinate system. Suitable only as
  a decorative landing-page globe, not the scientific substrate.
- **`netcdf-three`**: no npm package, v1.0.1, stale 2024-03-22, Three-only, NetCDF v3
  only (`d4-lib-pins.md` §5).

### Babylon.js (`@babylonjs/core@9.26.0`, Apache-2.0, access 2026-09-10) — REJECTED

| Factor | Assessment |
|---|---|
| Rendering power | Strong, first-class WebGPU support; the MDPI 2025 ocean-volume paper uses Babylon.js + WebGPU ray casting with early termination (`docs/research/platform-comparison.md`; DOI 10.3390/app15052782) |
| **Geospatial engine** | Same gap as Three.js — a general 3D engine, no WGS84 globe, no terrain/imagery streaming, no quadtree LOD, no geospatial camera |
| **Ecosystem fit** | No `zarr-cesium`-equivalent Zarr provider; no Cesium ion terrain/imagery |
| **WebGPU relevance** | None for us: CesiumJS has no WebGPU impl/roadmap (issue CesiumGS/cesium#4989); WebGPU is a P6 research note only (`docs/performance/reference-laptop.md` §1) |
| **PS alignment** | PS names WebGL/Three.js or Cesium.js; Babylon is unnamed and adds integration risk |

Reject reason: cutting-edge volume-rendering performance is not our bottleneck. Our
bottleneck is geospatial correctness + terrain + streaming + Zarr integration, where
Babylon offers no engine-level support and no NOC provider. Choosing Babylon would
mean rebuilding the geo substrate for a GPU feature (WebGPU) that our workload does
not require and that the locked stack does not use.

### Also considered (non-engine)

- **MapboxGL JS / MapLibre** — 2D map with 3D terrain, not a true 3D globe; no ocean
  volume. REJECTED for globe role.
- **deck.gl** — overlay/layer library, not a globe engine; 2D-focused, needs Mapbox.
  REJECTED as globe; possible overlay later.
- **Google Maps JS API / Photorealistic 3D Tiles** — proprietary, rate-limited, quota
  cliff (~30 judge loads/day), weak oceans, ban risk (`d4-lib-pins.md` §9). REJECTED.

## Evidence table

| Claim | Value | Source | Access date | Status |
|---|---|---|---|---|
| PS F1 names WebGL/Three.js OR Cesium.js | F1/R1, either satisfies | `problem-statement/PROBLEM-STATEMENT-ANALYSIS.md:32,62` | 2026-09-10 | VERIFIED |
| CesiumJS license | Apache 2.0, free commercial + non-commercial | `https://cesium.com/platform/cesiumjs/` | 2026-09-10 | VERIFIED |
| Cesium WGS84 + terrain/imagery streaming | High-precision WGS84 globe; terrain/imagery layers, open standards | `https://cesium.com/platform/cesiumjs/` | 2026-09-10 | VERIFIED |
| cesium 1.142.0 publish time | 2026-06-01T20:02:38Z (npm latest 1.145.0) | `https://registry.npmjs.org/cesium` | 2026-09-10 | VERIFIED |
| cesium 1.142.0 pin rationale | 101d soak, peer ok, avoids 1.145 freeze | `docs/research/d4-lib-pins.md` §3 | 2026-09-10 | VERIFIED |
| zarr-cesium latest | 0.2.0, 2026-08-21T14:32:01Z, `gitHead 1e5f18daccbb…` | `https://registry.npmjs.org/zarr-cesium` | 2026-09-10 | VERIFIED |
| zarr-cesium peer / license / deps | `cesium >=1.119.0 <2`; MIT; `zarrita ^0.7.4`, `zarr-maps-tiling ^0.2.0`, `zarr-maps-colormap ^0.2.0`, NOC `cesium-wind-layer` v0.11.1 tarball | `https://registry.npmjs.org/zarr-cesium` | 2026-09-10 | VERIFIED |
| zarr-cesium providers + no-backend streaming | `ZarrLayerProvider` / `ZarrCubeProvider` / `ZarrCubeVelocityProvider`; streamed from HTTP/S3/GCS without preprocessing/backend; supports CesiumJS 1.119+ incl 1.142+ | `https://github.com/NOC-OI/zarr-cesium` (README, tag v0.2.0) | 2026-09-10 | VERIFIED |
| three latest / license | 0.186.0, 2026-09-08; MIT | `https://registry.npmjs.org/three` | 2026-09-10 | VERIFIED |
| three-globe latest / license / peer | 2.45.2, 2026-04-04; MIT; peer `three >=0.154` | `https://registry.npmjs.org/three-globe` | 2026-09-10 | VERIFIED |
| three-globe capability ceiling | equirectangular image + bump map + halo + slippy tiles; no WGS84/terrain | `https://github.com/vasturiano/three-globe` README | 2026-09-10 | VERIFIED |
| @babylonjs/core latest / license | 9.26.0, 2026-09-10; Apache-2.0 | `https://registry.npmjs.org/@babylonjs/core` | 2026-09-10 | VERIFIED |
| nordicseas3d stack | React 18 + TS + Three.js 0.180 + zarrita 0.6.1 + Plotly; browser-direct Zarr; no Cesium | `https://github.com/nordicseas3d/nordicseas3d.github.io` (README, package.json) | 2026-09-10 | VERIFIED |
| nordicseas3d last commit | `543f090`, 2026-06-26 | `docs/research/d4-lib-pins.md` §5 | 2026-09-10 | VERIFIED |
| MDPI WebGPU ocean volume = Babylon.js | DOI 10.3390/app15052782 | `docs/research/platform-comparison.md` | 2026-09-10 | VERIFIED |
| Cesium WebGPU roadmap | none; issue CesiumGS/cesium#4989 | `docs/performance/reference-laptop.md` §1 | 2026-09-10 | VERIFIED |
| Three.js prototype deficiency list | sphere, no terrain/LOD/geo/day-night | `research/individuals/lakshya/approach-comparison.md` Shift 1 | 2026-09-10 | VERIFIED (internal record) |
| Exa MCP verification | rate-limited — gateway/`$NINEROUTER_KEY` absent (length check only) | n/a | 2026-09-10 | UNVERIFIED (fetch failed; curl used instead) |

## References

1. Problem statement analysis — `problem-statement/PROBLEM-STATEMENT-ANALYSIS.md` (access 2026-09-10)
2. CesiumJS product page — `https://cesium.com/platform/cesiumjs/` (access 2026-09-10)
3. zarr-cesium repository (v0.2.0) — `https://github.com/NOC-OI/zarr-cesium` (access 2026-09-10)
4. zarr-cesium docs — `https://noc-oi.github.io/zarr-cesium/docs/` (access 2026-09-10)
5. npm registry: cesium — `https://registry.npmjs.org/cesium` (access 2026-09-10)
6. npm registry: zarr-cesium — `https://registry.npmjs.org/zarr-cesium` (access 2026-09-10)
7. npm registry: three — `https://registry.npmjs.org/three` (access 2026-09-10)
8. npm registry: three-globe — `https://registry.npmjs.org/three-globe` (access 2026-09-10)
9. npm registry: @babylonjs/core — `https://registry.npmjs.org/@babylonjs/core` (access 2026-09-10)
10. three-globe — `https://github.com/vasturiano/three-globe` (access 2026-09-10)
11. nordicseas3d — `https://github.com/nordicseas3d/nordicseas3d.github.io` (access 2026-09-10)
12. D4 library pins — `docs/research/d4-lib-pins.md` §3, §5, §7, §9 (access 2026-09-10)
13. Tech stack — `docs/architecture/tech-stack.md` (access 2026-09-10)
14. Platform comparison — `docs/research/platform-comparison.md` (access 2026-09-10)
15. Open-source projects — `docs/research/open-source-projects.md` (access 2026-09-10)
16. Reference laptop / browser matrix — `docs/performance/reference-laptop.md` (access 2026-09-10)
17. Approach comparison (Shift 1) — `research/individuals/lakshya/approach-comparison.md` (access 2026-09-10)
18. MDPI WebGPU ocean volume — DOI 10.3390/app15052782 (access 2026-09-10)
19. Cesium WebGPU issue — `https://github.com/CesiumGS/cesium/issues/4989` (access 2026-09-10)
