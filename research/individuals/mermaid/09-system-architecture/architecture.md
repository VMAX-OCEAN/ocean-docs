# Proposed Architecture

DATA SOURCES
→ normalization
→ spatiotemporal index
→ analytics + data API
→ Web client
→ GPU renderer + interaction engine

### Evaluate
Frontend: React/Next.js
3D: Three.js / CesiumJS / Mapbox
GPU: WebGPU / Babylon.js / Three.js WebGPU
Scientific: Python, xarray, NumPy, SciPy, Dask, Zarr
Backend: FastAPI + object storage + scientific-data API

### Principle
Browser: interaction + rendering + lightweight analytics.
Server: heavy interpolation, feature extraction, dataset preparation.
GPU: rendering and selected real-time numerical operations.
