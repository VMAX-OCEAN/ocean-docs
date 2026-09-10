# GLORYS12 — Dataset Contract Card (GLOBAL_MULTIYEAR_PHY_001_030)

**Status:** CONTRACT card — fixture-use terms for GLORYS12. Overview/rationale lives in [`glorys-dataset.md`](glorys-dataset.md). Access dates 2026-09-10.

---

## Contract fields

| Field | Value |
|---|---|
| Source URL (product) | https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description (accessed 2026-09-10, HTTP 200) |
| Source URL (services/datasets) | https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/services (accessed 2026-09-10, HTTP 200) |
| PUM | https://documentation.marine.copernicus.eu/PUM/CMEMS-GLO-PUM-001-030.pdf (`CMEMS-GLO-PUM-001-030`, Issue 1.7, approval Nov 2025; accessed 2026-09-10, HTTP 200, PDF 28 pp, 792021 bytes) |
| QUID | https://documentation.marine.copernicus.eu/QUID/CMEMS-GLO-QUID-001-030.pdf (referenced from product page; not fetched) |
| DOI | **10.48670/moi-00021** (verified: `https://doi.org/10.48670/moi-00021` → `GLOBAL_MULTIYEAR_PHY_001_030/description`, title "Global Ocean Physics Reanalysis", accessed 2026-09-10) |
| sha256 | **NONE** — no netCDF fetched/downloaded, so no file hash exists. Card is metadata-only; hash a subset file at first ingest and record exact URL + sha256 + bytes here. |
| License | Copernicus Marine Service Licence. Product metadata `licence` = `http://marine.copernicus.eu/services-portfolio/service-commitments-and-licence/` → redirects to https://marine.copernicus.eu/user-corner/service-commitments-and-licence (accessed 2026-09-10, HTTP 200). Free of charge, worldwide, non-exclusive, royalty-free, perpetual; permits copy/modify/derive/redistribute; requires crediting "E.U. Copernicus Marine Service Information" and citing the DOIs. Full text quoted below. |
| bbox | Global: lon −180 to 180, lat −90 to 90. Product `geoExtent` = `[[-180,90],[180,-90]]`. PUM spec: "Global (180°E to 180°E ; 89°S to 90°N)"; model domain "GLOBAL (180°W-180°E ; 80°S – 90°N)", grid 4320 × 2041. |
| Spatial resolution | 1/12° = 0.083° (`geoResolution.row/column.magnitude = 0.083 degree`); equirectangular regular grid |
| Vertical | 50 standard levels; product `vertExtentMin = -5500 m`, `vertExtentMax = 0 m`; PUM: e3t cell thickness, deptho bathymetry |
| Temporal | 1993-01-01 to present (M-1). Product `tempExtentBegin = 1993-01-01`, `tempExtentEnd` empty (rolling). Services page daily extent observed 01/01/1993–23/06/2026; monthly 01/01/1993–01/05/2026. Update frequency: yearly. PUM "Available time series: 01/01/1993 to M-1". |
| Temporal resolutions | Daily mean (P1D-m), Monthly mean (P1M-m), Monthly climatology (climatology_P1M-m, 1993–2016 per-month average; PUM §, "for each month of the year, the 1993-2016 average") |
| Format | NetCDF-4 (files also CF-1.4 / annex shows CF-1.6 in places); product `format = NetCDF-4`, PUM "NetCDF CF1.4" |
| Ingest version | **v0** — card only, no ingest run. No Zarr/NetCDF artifact produced from this dataset yet. |
| Fixture-use status | NOT usable as fixture yet: ingest v0 not run, no sample fetched, sha256 NONE. May be cited as a documented source. |

---

## Dataset IDs (verified from product/services pages, 2026-09-10)

| Dataset ID | Type | Notes |
|---|---|---|
| `cmems_mod_glo_phy_my_0.083deg_P1D-m` | daily mean | 3D daily fields + 2D surface/bottom/ice |
| `cmems_mod_glo_phy_my_0.083deg_P1M-m` | monthly mean | monthly averages, same variables |
| `cmems_mod_glo_phy_my_0.083deg-climatology_P1M-m` | monthly climatology | 1993–2016 per-month average |
| `cmems_mod_glo_phy_my_0.083deg_static_202311` | static | coordinates, mask, bathymetry, mdt — not one of the 3 reanalysis datasets; listed because it holds grid invariants |

Superseded/alias IDs seen on pages: `..._P1D-m_202311`, `..._P1M-m_202311`, `...-climatology_P1M-m_202311`, `cmems_mod_glo_phy_my_0.083_P1M-m_202112`. Use the unversioned IDs for the Toolbox; treat `_202311` as a versioned alias.

---

## Variables (exact, from product metadata JSON + PUM Table 2, 2026-09-10)

### 3D (dims: time, elevation, latitude, longitude)

| Abbrev | standard_name | Unit (metadata) | Unit (PUM/NetCDF) | Long name |
|---|---|---|---|---|
| `thetao` | `sea_water_potential_temperature` | `degrees_C` | °C | Temperature |
| `so` | `sea_water_salinity` | `1e-3` | psu | Salinity |
| `uo` | `eastward_sea_water_velocity` | `m s-1` | m/s | Eastward ocean current velocity |
| `vo` | `northward_sea_water_velocity` | `m s-1` | m/s | Northward ocean current velocity |

### 2D (dims: time, latitude, longitude)

| Abbrev | standard_name | Unit (metadata) | Unit (PUM) | Long name |
|---|---|---|---|---|
| `zos` | `sea_surface_height_above_geoid` | `m` | m | Sea surface height |
| `bottomT` | `sea_water_potential_temperature_at_sea_floor` | `degrees_C` | °C | Sea floor potential temperature |
| `mlotst` | `ocean_mixed_layer_thickness_defined_by_sigma_theta` | `m` | m | Density ocean mixed layer thickness |
| `siconc` | `sea_ice_area_fraction` | `1` | 1 | Ice concentration |
| `sithick` | `sea_ice_thickness` | `m` | m | Sea ice thickness |
| `usi` | `eastward_sea_ice_velocity` | `m s-1` | m/s | Sea ice eastward velocity |
| `vsi` | `northward_sea_ice_velocity` | `m s-1` | m/s | Sea ice northward velocity |

### Static dataset variables (table 2)

`e1t [m]`, `e2t [m]`, `e3t [m/s]` (cell dimensions X/Y/Z), `cell_thickness`, `mask [1]` (`sea_binary_mask`), `deptho [m]` (`sea_floor_depth_below_geoid`, bathymetry), `deptho_lev [1]` (`model_level_number_at_sea_floor`), `mdt [m]` (`sea_surface_height_above_geoid`, mean dynamic topography).

**Exactness note:** NO vertical-velocity (`wo`/`wmo`) variable exists in this product's metadata or PUM Table 2. `glorys-dataset.md` lists `wmo` — that is wrong for 001_030; do not request it. Horizontal velocities only (`uo`, `vo`).

---

## License text (verbatim, from the Licence page, accessed 2026-09-10)

Key clauses quoted:

> "2.1 This Licence is granted free of charge."
>
> "2.2 The Licensee is hereby granted a worldwide, non exclusive, royalty free, perpetual licence, (subject to the terms and conditions of this agreement) to: (a) make and use such reasonable copies of Copernicus Marine Service Products for internal use and back up purposes; (b) modify, adapt, develop, create and distribute Value Added Products or Derivative Work from Copernicus Marine Service Products for any purpose; (c) redistribute, disseminate any Copernicus Marine Service Product in their original form via any media."
>
> "2.3 … the Licensee will communicate to the public the source of the products and services by crediting the Copernicus Marine Environment Monitoring Service;"
>
> "2.4 (b) … in case of redistribution of Copernicus Marine Service products or documents, including pictures – shall credit the Copernicus Marine Service … 'E.U. Copernicus Marine Service Information; insert DOIs links here'"
>
> "2.4 (c) In case of any publication … 'This study has been conducted using E.U. Copernicus Marine Service Information; insert all relevant DOIs links here'"

Source value in each NetCDF file header (PUM annex, verbatim): `:licence = "http://marine.copernicus.eu/services-portfolio/service-commitments-and-licence/" ;`

---

## Assumptions

1. **Registration required, free** — Copernicus Marine data download requires a free Copernicus Marine account/credentials. Not exercised in this card (no download performed); verify at first ingest.
2. **Subset via `copernicusmarine` CLI** — intended access path is the Copernicus Marine Toolbox (CLI or Python API), not raw FTP. Registration/toolbox credentials needed.
3. **PyNIO dropped → xarray/netCDF4** — this environment does not use PyNIO; read NetCDF-4 with `xarray` + `netcdf4` engine. PUM files are NetCDF-4 (CF-1.4/1.6).
4. Product is "multiyear" reanalysis; product page also exposes ARCO/Zarr mirrors (`timeChunked.zarr`, `geoChunked.zarr`, downsampled) on `s3.waw3-1.cloudferro.com` — reachable but NOT adopted as source here; canonical source remains the Copernicus Marine product/Toolbox.
5. `tempExtentEnd` is empty on the product page (rolling M-1); do not hardcode an end date in any fixture.

---

## Search trail / corrections

- **DOI correction:** the brief suggested `10.48670/moi-00019` or "correct". `10.48670/moi-00019` resolves to `GLOBAL_MULTIYEAR_BGC_001_029` (biogeochemistry), NOT physics. The physics product's DOI is `10.48670/moi-00021` (verified). Related 10.48670 neighbors: `-00019` BGC 001_029, `-00020` BGC 001_033, `-00022` WAV 001_032.
- Product page HTML does NOT expose per-dataset temporal extents via `/api/metadata/dataset/...` (404). Daily/monthly extents taken from the services page rendering (01/01/1993–23/06/2026 daily, 01/01/1993–01/05/2026 monthly, observed 2026-09-10) — treat as live values, re-check at ingest.
- No sample netCDF fetched → sha256 NONE by design, not a failed lookup.

---

## References

- [`glorys-dataset.md`](glorys-dataset.md) — narrative overview (has known errors: `wmo`, `vsi` units, PUM date).
- [`netcdf-to-zarr.md`](netcdf-to-zarr.md) — conversion/chunking.
- `../architecture/backend-strategy.md` — NetCDF→Zarr + chunking strategy.
