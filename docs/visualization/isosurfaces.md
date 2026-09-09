# Isosurfaces — Thermoclines and Isohalines

How isosurfaces (constant-value surfaces) are extracted and rendered to show
thermoclines, isohalines, and isopycnals.

---

## What Isosurfaces Show

An isosurface is the 3D surface where a scalar field equals a target value:

| Isosurface | Target | What it reveals |
|---|---|---|
| **Isothermal** (isotherm) | temperature = 20°C | The thermocline — depth of the 20°C water mass |
| **Isohaline** | salinity = 35 PSU | Halocline — depth of a specific salinity |
| **Isopycnal** | density = 1025 kg/m³ | Density surface — water mass boundaries |

The isosurface depth shows where that water mass sits in the water column — critical
for understanding ocean stratification, eddies, and mixing.

---

## Two Implementation Approaches

### Approach A: Server-Side Marching Cubes (DOVis pattern)

The backend computes the isosurface mesh and sends it to the frontend.

```
1. User selects "Isosurface" mode, target = 20°C
2. Frontend calls /isosurface?variable=thetao&value=20&t=2026-09-09&bbox=...
3. Backend loads Zarr chunk, runs marching cubes
4. Returns mesh (vertices + faces + depth colors) as glTF or JSON
5. Frontend renders as Cesium 3D primitive
6. Result cached for subsequent requests at same (t, target, bbox)
```

**Backend (Python, using PyVista/VTK as DOVis does):**
```python
import pyvista as pv
import numpy as np

@app.get("/isosurface")
def get_isosurface(variable: str, value: float, t: str, bbox: str):
    # Load Zarr chunk
    ds = xr.open_zarr(f'data/{variable}.zarr')
    subset = ds.sel(time=t).sel(bbox=bbox)

    # Build PyVista grid
    grid = pv.UniformGrid()
    grid.dimensions = np.array(subset.shape) + 1
    grid.spacing = (dx, dy, dz)
    grid.cell_data['values'] = subset.values.flatten()

    # Marching cubes
    isosurface = grid.contour([value])

    # Export as glTF
    return isosurface.export_gltf()
```

**Pros:** Full marching cubes quality, handles complex topologies
**Cons:** Server compute, latency on first request (cached after)

### Approach B: Client-Side (nordicseas3d pattern)

The frontend computes the isosurface in the browser using Three.js.

nordicseas3d's isosurface mode: "show the shallowest depth where the active variable
reaches a target value. The surface is colored by depth."

**Pros:** No server compute, instant interaction
**Cons:** Limited to depth-sheet isosurfaces (not full 3D marching cubes)

---

## Rendering the Isosurface

### As a 3D Mesh (Cesium primitive)

```js
// Fetch isosurface mesh from backend
const response = await fetch('/isosurface?variable=thetao&value=20&t=2026-09-09');
const meshData = await response.json();

// Render as Cesium 3D primitive
const isosurfacePrimitive = new Cesium.Primitive({
  geometryInstances: new Cesium.GeometryInstance({
    geometry: new Cesium.PolygonGeometry.fromPositions({
      positions: meshData.vertices,
      vertexFormat: Cesium.VertexFormat.POSITION_AND_COLOR
    })
  }),
  appearance: new Cesium.PerInstanceColorAppearance()
});
viewer.scene.primitives.add(isosurfacePrimitive);
```

### Colored by Depth

The isosurface mesh is colored by depth — shallow areas (where the isotherm is near
the surface) are one color, deep areas (where the isotherm dives deep) are another.
This reveals the 3D structure of the thermocline.

---

## Interactive Controls

| Control | Action |
|---|---|
| Variable selector | Choose temp/salinity/density for isosurface |
| Target value slider | Set the isosurface value (e.g., 20°C) |
| Time slider | Animate isosurface over time (thermocline rises/falls) |
| Vertical exaggeration | Make depth variations visible |
| Opacity | Control isosurface transparency |

---

## Use Cases

### Thermocline Visualization
Set isosurface to temperature = 20°C. The resulting surface shows the depth of the
20°C water mass across the ocean. In the tropics, it's shallow (~100m); at high
latitudes, it deepens or disappears. This reveals the ocean's vertical structure.

### Eddy Detection
Isosurfaces bulge upward or downward in eddies. A cyclonic eddy lifts the isotherm
(dome shape); an anticyclonic eddy pushes it down (bowl shape). nordicseas3d has a
dedicated "eddy detection / eddy volume view" mode.

### Water Mass Boundaries
Isopycnal surfaces (constant density) show water mass boundaries — where different
water masses meet. Critical for understanding ocean circulation.

---

## Performance

| Operation | Latency |
|---|---|
| First isosurface request | ~500ms (server marching cubes + transfer) |
| Cached isosurface request | ~50ms (cache hit) |
| Client-side depth-sheet | ~100ms (browser compute) |
| Time animation (per frame) | ~500ms (new isosurface per time step) |

For smooth animation, **precompute isosurfaces** for a time range, or use the
client-side depth-sheet approach for real-time interaction.

---

## Summary

| Aspect | Recommendation |
|---|---|
| Algorithm | Marching cubes (server) for full 3D; depth-sheet (client) for speed |
| Library | PyVista/VTK (backend); Three.js (client) |
| Coloring | By depth (reveals thermocline structure) |
| Caching | Cache isosurface meshes by (variable, value, time, bbox) |
| Animation | Precompute or use client-side for real-time |
