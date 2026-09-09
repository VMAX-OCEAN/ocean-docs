# Benchmark teardowns (2026-09-09)

Live fetch failed this session (model access error + empty search). From cutoff knowledge + docs.

## earth.nullschool.net

- Data: GFS wind, OSCAR currents, WW3 waves, SST overlays. 2D canvas particle advection. Not volumetric.
- Code: `github.com/cambecc/earth`. D3 + canvas. Projection + particle integrator reusable.
- Interaction: drag rotate, scroll zoom, click values, time scrub. Minimal chrome.
- Borrow: current trails for `u,v`. Instant scrub feel. Location readout.
- Limit: no depth axis. No Argo profiles. No QC. No match-up. No NetCDF ingest.
- Lesson: particles for surface currents in M4. Science stays separate.

## Esri 3D Ocean Explorer (assumed Living Atlas/EMU stack)

- Stack: ArcGIS JS API `WebScene` + hosted bathymetry tiles + popups. Globe fly-to built-in.
- Borrow: preset fly-to. Bathymetry base. Storytelling for outreach mode.
- Limit: vendor lock. No NetCDF/Zarr pipeline. No residual/QC logic. INCOIS hosting unclear.
- Correct assumption if target differs (archwatch ambiguous).

## Peers

- Copernicus Marine viewer: 4D nav, depth/time controls, subset pattern. Interaction benchmark.
- Argovis: trajectory + profile + QC query (space/time/depth/parameter/quality/platform/year). Query pattern.
- webODV: no-install flow profile → context → trajectory → comparison. Flow reference.
- MyOcean Pro: layers, profiles, histograms, comparison. Panel reference.
- HUB Ocean: region select → retrieval → viz workspace. Workflow reference.
- NASA Eyes: real data + immersive 3D + time nav proof. Not stack commitment.
- Mapbox Globe: camera/globe/terrain precedent. Fly-to proof.
- INCOIS holdings + training (xarray, Cartopy, Plotly, 3D, anomaly, profiles, vectors): judge baseline. Missing from `sources.md`, add next.

## Sources (accessed 2026-09-09)

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
