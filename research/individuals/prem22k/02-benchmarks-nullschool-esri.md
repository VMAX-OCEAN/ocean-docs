# Benchmark teardowns (2026-09-09, verified via 9router tavily fetch)

## earth.nullschool.net — CONFIRMED 2026-09-09

- Data: GFS weather, OSCAR v2.0 currents, CMEMS global physics analysis/forecast (DOI 10.48670/moi-00016), OI SST v2.1, OSTIA, RTGSST, WAVEWATCH III. Source: [about page](https://earth.nullschool.net/about).
- Pipeline: grib2json (netcdf-java) offline → static JSON → S3/Cloudflare. No runtime server. Source: [EQUINOCT fork](https://github.com/EQUINOCT/earth-nullschool).
- Code: `github.com/cambecc/earth`. D3 + canvas. Projection + particle integrator reusable. 2D only, no depth axis.
- Interaction: drag rotate, scroll zoom, click values, time scrub. Minimal chrome.
- Borrow: current trails for `u,v`. Instant scrub feel. Location readout.
- Limit: no depth axis. No Argo profiles. No QC. No match-up. No NetCDF ingest.
- Lesson: particles for surface currents in M4. Science stays separate.

## Esri 3D Ocean Explorer — UNVERIFIED, assumption only

- "archwatch" target ambiguous; no search run 2026-09-09. Assumed Living Atlas/EMU stack — do not cite externally until resolved.
- Assumed stack: ArcGIS JS API `WebScene` + hosted bathymetry tiles + popups. Globe fly-to built-in.
- Borrow: preset fly-to. Bathymetry base. Storytelling for outreach mode.
- Limit: vendor lock. No NetCDF/Zarr pipeline. No residual/QC logic. INCOIS hosting unclear.

## Peers

- Copernicus Marine viewer / MyOcean Pro: 4D nav (lon/lat/depth/time), depth/time controls, time-series, depth-profile, line/polygon section + trajectory, histogram, `.nc`/`.CSV` export, palettes LINEAR/LOG, deep link, guided tour. Interaction benchmark. Verified 2026-09-09: [main features](https://help.marine.copernicus.eu/en/articles/4794675-main-features-of-myocean-pro-viewer). Differentiator: it has NO geocoder (❌ UX table) — our fly-to is differentiation, not parity.
- Argovis: trajectory + profile + QC query (space/time/depth/parameter/quality/platform/year). Query pattern.
- webODV: no-install flow profile → context → trajectory → comparison. Flow reference.
- MyOcean Pro: layers, profiles, histograms, comparison. Panel reference.
- HUB Ocean: region select → retrieval → viz workspace. Workflow reference.
- NASA Eyes: suite of browser-run 3D apps over real NASA data/imagery, click-and-zoom-to, temporal nav. Engine undisclosed — closed showcase, not stack. Verified 2026-09-09: [NASA Eyes](https://science.nasa.gov/eyes).
- Mapbox Globe: camera/globe/terrain precedent. Fly-to proof.
- INCOIS holdings + training (xarray, Cartopy, Plotly, 3D, anomaly, profiles, vectors): judge baseline. Missing from `sources.md`, add next.

## Sources (accessed 2026-09-09)

- https://earth.nullschool.net/about (fetched: OSCAR v2.0, CMEMS, OI SST, OSTIA, D3 + Canvas)
- https://github.com/EQUINOCT/earth-nullschool (pipeline: grib2json offline → static)
- https://help.marine.copernicus.eu/en/articles/4794675-main-features-of-myocean-pro-viewer (fetched: 4D toolset, no geocoder)
- https://science.nasa.gov/eyes (Eyes suite verified)
- https://data.marine.copernicus.eu/viewer
- https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description
- https://argo.ucsd.edu/data/data-from-gdacs/
- https://argo.ucsd.edu/data/how-to-use-argo-files/
- https://odv.awi.de/en/services/odv-online/
- https://www.incois.gov.in/site/services/rsmc.jsp
- https://iioe-2.incois.gov.in/site/datainfo/modelling/godas.jsp
- https://cfconventions.org/
- https://docs.xarray.dev/en/stable/user-guide/io.html
- https://zarr.readthedocs.io/en/main/quickstart.html
- https://docs.ogc.org/is/09-110r3/09-110r3.pdf
- https://maplibre.org/maplibre-gl-js/docs/
