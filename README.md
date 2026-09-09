# SIH-OCEAN — Web-based 3D Ocean Data Visualization Platform

> **SIH Problem Statement ID:** 26067
> **Organization:** Ministry of Earth Sciences (MoES) / INCOIS
> **Theme:** Disaster Management
> **Category:** Software

A browser-native 3D Ocean Data Visualization System that integrates numerical ocean
model outputs (temperature, salinity, currents) with in-situ observations (Argo floats,
Gliders, CTD, BGC) on a single interactive platform.

---

## Problem Statement Summary

India's vast EEZ and coastline demand continuous, high-resolution monitoring of ocean
state variables. INCOIS generates large volumes of ocean model outputs (3D fields of
temperature, salinity, current vectors, chlorophyll) plus real-time observations from
Argo floats and underwater Gliders — stored in NetCDF and ASCII formats across multiple
depth levels, spatial grids, and time steps.

**No integrated, web-based 3D visualization platform currently exists** that can
simultaneously render model fields and in-situ instrument observations in a single
interactive environment. This project builds that platform.

### Core Requirements (from PS 26067)

- 3D volumetric rendering of ocean model fields (temp, salinity, currents) with
  depth-slice views, isosurface extraction, and time-step animation (WebGL/Three.js or Cesium.js)
- Instrument data overlay — Argo floats, Gliders, CTD, BGC — with click-to-inspect
  depth-vs-variable profile charts
- Multi-format data ingestion — NetCDF (xarray backend) and ASCII/text — modular and extensible
- Customizable colorbar, variable selector, layer opacity, vertical exaggeration slider
- Web-based, scalable, deployable on INCOIS infrastructure with no client-side install
- Open standards — OGC WMS/WCS, CF Conventions for NetCDF, OPeNDAP

---

## Documentation Index

This repository contains the complete research, architecture, and implementation plan.
Documentation is organized into folders:

Start with [`docs/DOC-MAP.md`](docs/DOC-MAP.md) (canonical layout), then [`docs/00-problem/`](docs/00-problem/) (PS authority).

| Folder | Contents |
|---|---|
| [`docs/00-problem/`](docs/00-problem/) | PS analysis — binding requirements, mandates, datasets, open items |
| [`docs/research/`](docs/research/) | Research on Google Earth, earth.nullschool, open-source ocean viz projects, temperature rendering techniques |
| [`docs/architecture/`](docs/architecture/) | System architecture, tech stack decisions, data flow, backend strategy |
| [`docs/visualization/`](docs/visualization/) | Globe rendering, day/night lighting, temperature overlay, ocean currents, isosurfaces, colorbars |
| [`docs/data/`](docs/data/) | Dataset cards (placeholder) — GLORYS12, Argo, Glider, INCOIS LAS |
| [`docs/roadmap/`](docs/roadmap/) | Milestone plan (`MILESTONES.md`) |
| [`docs/performance/`](docs/performance/) | Runtime performance benchmarks, latency analysis, optimization |
| [`docs/references/`](docs/references/) | Open-source project references, papers, libraries, links |

---

## Repository Rules

1. `docs/` is shared, team-owned. Never rewrite another contributor's file. Link fixes only where paths moved.
2. Personal research lives under `research/individuals/<username>/`. Never edit another namespace.
3. `problem-statement/` is the requirement authority. New claims cite its R/F IDs or stay in personal namespace.
4. `docs/data/` cards required before any fixture use: source URL, sha256, license, bbox, variables, assumptions.
5. Reorganize by moving paths only — one commit per move, no content changes in moved files.
6. No bulk science data in Git. Fixtures + checksums + acquisition scripts only.

---

## Tech Stack (Summary)

| Layer | Technology |
|---|---|
| Globe engine | **CesiumJS** (with resium React bindings) |
| Ocean volumetric rendering | **zarr-cesium** providers |
| Current particle animation | **cesium-wind-layer** (GPU advection) |
| Backend | **xpublish** (FastAPI + Zarr REST + OPeNDAP) |
| Argo data | **argopy** + SQLite |
| Frontend | **React 18 + Vite + TypeScript** |
| UI | **Material UI** / shadcn (light theme) |
| Data format | **Zarr** (chunked, cloud-streamed) |

See [`docs/architecture/tech-stack.md`](docs/architecture/tech-stack.md) for full details.

---

## Quick Start (planned)

```bash
# Clone
git clone https://github.com/VMAX-OCEAN/ocean-docs.git
cd ocean-docs

# Backend
cd backend && pip install -r requirements.txt && uvicorn main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```

---

## Datasets

| Dataset | Source | Format | Size |
|---|---|---|---|
| GLORYS12 (ocean reanalysis) | Copernicus GLOBAL_MULTIYEAR_PHY_001_030 | NetCDF | ~PB scale |
| Argo floats | ftp.ifremer.fr/argo | NetCDF | 931 GB (3.5M files) |
| Glider data | ftp.ifremer.fr/glider | NetCDF | — |
| INCOIS LAS | las.incois.gov.in | NetCDF/OPeNDAP | — |

See [`docs/data/`](docs/data/) for card template (cards pending).

---

## License

MIT (planned)

## Acknowledgments

- INCOIS — Indian National Centre for Ocean Information Services
- Copernicus Marine Service
- Argo Program
- CesiumGS, zarr-cesium (NOC-OI), cesium-wind-layer, xpublish communities
