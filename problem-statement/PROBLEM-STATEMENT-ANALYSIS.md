# SIH26067 — Problem Statement Analysis

Source: pasted SIH portal text, PS ID 26067, MoES/INCOIS Ocean Valley, Software, Disaster Management. Deadline 30 Sep 2026.

## One-line brief

Browser-native 3D workspace joining numerical ocean model fields with in-situ observations for forecasters, plus public outreach mode.

## Background (PS claims)

- India EEZ/coastline needs continuous high-res monitoring.
- INCOIS archives model outputs (temperature, salinity, current vectors, chlorophyll) + real-time/delayed-mode Argo floats + gliders.
- Formats: NetCDF + ASCII/text, multi-depth, multi-grid, multi-timestep.
- Current state: desktop-bound tools, 2D-only portals, or no model+instrument co-viz. Forecasters toggle packages, correlation slow.

## Five gaps (PS verbatim, mapped)

| # | Gap | Requirement ID | Milestone |
|---|---|---|---|
| 1 | No web platform-independent 3D render with depth-resolved volumetric views | R1 | M1, M3 |
| 2 | No unified Argo/Glider display (lat, lon, depth, time, T, S, chlorophyll) beside model fields | R2 | M4 |
| 3 | No variable / depth-slice / time-animation / colorbar controls | R3 | M2 |
| 4 | New streams/variables need re-engineering | R4 | M5 |
| 5 | No intuitive rapid 3D understanding for operational decisions | R5 | M1–M5 demo arc |

## Operational mandates (judging hooks)

Hazard assessment, search-and-rescue, fishery advisories, climate monitoring. Each demo beat should name one mandate. Currently unmapped — see § Open items.

## Functional requirements (binding)

- **F1 3D volumetric:** T/S/currents full water column, depth slices, isosurfaces, time animation. Stack named: WebGL / Three.js **or** Cesium.js. Either satisfies PS.
- **F2 instrument overlay:** Argo, Glider, CTD, BGC markers, geospatially accurate; click → depth-vs-variable profile + timestamps.
- **F3 ingest:** automated NetCDF (PS names PyNIO/xarray backend) + delimited text; new variables/sources with minimal code change.
- **F4 controls:** palette, min/max, log/linear, variable selector, opacity, vertical exaggeration.
- **F5 architecture:** modern JS frontend, lightweight REST/OPeNDAP backend, INCOIS-deployable, zero client install.
- **F6 extensibility:** plugin-style sensors (CTD, moorings, HF-radar, ADCP), new variables, ML products.
- **F7 standards:** OGC WMS/WCS, CF Conventions. Interop with national/international portals.

## Outreach (binding, second user class)

Students, public campaigns, policymakers; exhibitions, e-learning. Needs guided mode distinct from forecaster mode. Currently M5 scope.

## Users

| User | Job | Proof |
|---|---|---|
| Forecaster | verify model feature vs instruments | agreement/disagreement < 2 min |
| Scientist | explore front/thermocline/current | value at x,y,z,t + provenance |
| Operator | onboard feed | config-only, no frontend edit |
| Presenter | explain ocean structure | guided legible story, no setup |

## Datasets (PS links)

- Model: las.incois.gov.in + GLOBAL_MULTIYEAR_PHY_001_030 (1/12°, 50 levels, daily+monthly, thetao/so/uo/vo/zos)
- Argo: ftp://ftp.ifremer.fr/ifremer/argo
- Glider: ftp://ftp.ifremer.fr/ifremer/glider/v2/
- In-situ collection: blank in PS paste — flag as unknown, do not invent URL.

## Stack decisions already locked (shared docs)

CesiumJS + zarr-cesium + xpublish + argopy + SQLite. Satisfies F1 (Cesium named), F3 (xarray; PyNIO dropped — needs one-line ADR), F5 (REST + OPeNDAP plugin). F7 WMS/WCS roadmap-only — label as roadmap, never claim live compliance.

## Open items (no code, doc-only)

1. Dataset cards with sha256 + license + bbox for all 5 links (`docs/data/`).
2. PyNIO-drop ADR; Cesium-over-Three ADR; OPeNDAP-facade scope note.
3. Mandate→demo-beat mapping in pitch doc.
4. Observations GeoJSON-vs-Arrow cutoff; chunk hypothesis benchmark; reference laptop lock.
5. Match-up semantics: `residual = model − observation` + QC/method on every comparison panel. Shared docs currently show co-viz without residual rule — adopt before M4.
