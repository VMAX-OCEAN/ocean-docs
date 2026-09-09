# References

Open-source projects, papers, libraries, and links referenced in this documentation.

---

## Open-Source Projects

| Project | GitHub | Relevance |
|---|---|---|
| DOVis | https://github.com/HungerBar/DOVis | Closest match — Indian Ocean 3D DO viz, FastAPI + Cesium |
| OceanStream globe-3d-viewer | https://github.com/OceanStreamIO/globe-3d-viewer | Closest UX — Copernicus 3D ocean globe |
| nordicseas3d | https://github.com/nordicseas3d/nordicseas3d.github.io | Best Three.js 3D reference — Zarr in browser |
| zarr-cesium | https://github.com/NOC-OI/zarr-cesium | Our rendering core — Cesium Zarr providers |
| DeepSwitch | https://github.com/19Chris98H/DeepSwitch | Space-time cube ocean viz for non-experts |
| netcdf-three | https://github.com/umrlastig/netcdf-three | Pure-frontend NetCDF to volume rendering |
| Atlas (SIH INCOIS) | https://github.com/s9swata/Atlas | Prior SIH Argo viz project |
| OceanEye (SIH INCOIS) | https://github.com/iamdipayandutta/OceanEye | Prior SIH INCOIS project |
| IMOS Live | https://github.com/aodn/imos-live-frontend | Australian marine viz — SST + particles + moorings |
| earth (nullschool) | https://github.com/cambecc/earth | Original open-source nullschool (2013) |
| three-globe | https://github.com/vasturiano/three-globe | Three.js globe library (alternative) |
| cesium-wind-layer | https://github.com/hongfaqiu/cesium-wind-layer | GPU particle advection for Cesium |
| 3D-Wind-Field | https://github.com/RaymanNg/3D-Wind-Field | Cesium GPU wind viz reference |
| maplibre-wind-gl | https://github.com/TheBeachLab/maplibre-wind-gl | GPU wind particles for MapLibre |
| Earth-Viz | https://github.com/edcatley/earth-viz | Modern nullschool-inspired globe |

---

## Libraries

| Library | URL | Purpose |
|---|---|---|
| CesiumJS | https://cesium.com/learn/cesiumjs/ | 3D globe engine |
| resium | https://github.com/gravitystorm/resium | React bindings for Cesium |
| zarrita.js | https://github.com/manzt/zarrita.js | Browser Zarr client |
| xpublish | https://github.com/xarray-contrib/xpublish | FastAPI xarray server |
| xpublish-opendap | https://github.com/xpublish-community/xpublish-opendap | OPeNDAP plugin for xpublish |
| argopy | https://argopy.readthedocs.io | Argo data access library |
| xarray | https://docs.xarray.dev | N-d array handling |
| d3-scale-chromatic | https://github.com/d3/d3-scale-chromatic | Scientific colormaps |
| Plotly.js | https://plotly.com/javascript/ | Profile charts |
| Zustand | https://github.com/pmndrs/zustand | State management |
| PyVista | https://pyvista.org/ | 3D mesh / marching cubes |
| ndpyramid | https://github.com/nci-xarray/ndpyramid | Multiscale Zarr pyramids |

---

## Papers

| Paper | DOI | Topic |
|---|---|---|
| i4Ocean | 10.1080/17538947.2021.1886355 | Transfer function ocean volume rendering |
| WebGPU ocean volume | 10.3390/app15052782 | WebGPU ray casting for ocean data |
| Clipmap | 10.1145/280814.280855 | SGI clip mapping (Google Earth basis) |
| Zarr chunk size study | 10.1002/essoar.10511054.2 | Chunk size impact on read performance |
| Zarr vs OPeNDAP throughput | 10.1002/essoar.10508824.2 | Cloud storage read throughput profiling |
| Argo data 1999-2019 | (NERC) | 2M temp-sal profiles overview |
| DeepSwitch | 10.2312/envirvis.20251146 | Space-time cube ocean viz |

---

## Standards

| Standard | URL | Purpose |
|---|---|---|
| OGC 3D Tiles | https://github.com/CesiumGS/3d-tiles | Streaming 3D geospatial data |
| CF Conventions | https://cfconventions.org/ | NetCDF metadata conventions |
| OGC WMS/WCS | https://www.ogc.org/standards/wms | Web Map/Coverage Service |
| OPeNDAP | https://www.opendap.org/ | Data access protocol |
| Zarr spec | https://zarr.dev/ | Chunked array storage format |
| glTF | https://www.khronos.org/gltf/ | 3D model format (3D Tiles content) |

---

## Data Sources

| Source | URL | Data |
|---|---|---|
| Copernicus GLORYS12 | https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description | Ocean reanalysis |
| INCOIS LAS | https://las.incois.gov.in/ | INCOIS ocean data |
| INCOIS Data Holdings | https://incois.gov.in/site/dataholdings.jsp | INCOIS data catalog |
| Argo ifremer FTP | ftp://ftp.ifremer.fr/ifremer/argo | Argo floats |
| Glider ifremer FTP | ftp://ftp.ifremer.fr/ifremer/glider/v2/ | Gliders |
| GEBCO bathymetry | https://www.gebco.net/ | Seafloor relief |
| Natural Earth | https://www.naturalearthdata.com/ | Coastlines/boundaries |
| NASA Blue Marble | https://visibleearth.nasa.gov/ | Earth textures |
| Google Map Tiles API | https://developers.google.com/maps/documentation/tile/3d-tiles | Photorealistic 3D Tiles |

---

## Blogs & Articles

| Article | URL | Topic |
|---|---|---|
| How Google Earth really works | https://onezero.medium.com/how-google-earth-really-works-d4ed11fc629d | Universal Texture, clip mapping |
| Earth on Web (Google) | https://medium.com/google-earth/earth-on-web-the-road-to-cross-browser-7338e0f46278 | NaCl to WASM port |
| Earth WASM threading | https://medium.com/google-earth/performance-of-web-assembly-a-thread-on-threading-54f62fd50cf7 | Threading performance |
| Improved Atmosphere in CesiumJS | https://cesium.com/blog/2022/05/26/improved-atmosphere-in-cesiumjs/ | Atmospheric scattering |
| Cesium Lighting IBL | https://cesium.com/blog/2025/02/20/leveling-up-lighting-in-cesiumjs-ibl-dynamic-environment-maps-ambient-occlusion/ | IBL, dynamic env maps |
| GPU Wind Visualization (Cesium) | https://cesium.com/blog/2019/04/29/gpu-powered-wind/ | GPU particle advection |
| 10x Faster 3D Tiles | https://cesium.com/blog/2019/05/07/faster-3d-tiles/ | 3D Tiles streaming optimization |
| Day/Night in web (Cesium) | https://community.cesium.com/t/day-night-in-web/45950 | enableLighting usage |
| AWS Zarr latency | https://aws.amazon.com/blogs/publicsector/decrease-geospatial-query-latency-minutes-seconds-using-zarr-amazon-s3/ | Zarr on S3 performance |
| nullschool Map Improvements | https://news.nullschool.net/p/map-improvements | Tiling scheme, non-Mercator |
| about earth.nullschool | https://earth.nullschool.net/about | Data sources, libraries |
