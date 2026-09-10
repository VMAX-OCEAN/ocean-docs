# Glider Data — CONTRACT CARD

Underwater glider data from the OceanGliders / EGO Global Data Assembly Centre
(GDAC), hosted by Ifremer. Real-time transects of temperature, salinity, pressure
and biogeochemistry, extending the Argo observation pattern to piloted, high-
resolution, upper-1000 m sections.

**Status:** SOURCE VERIFIED, 2026-09-10. FTP root live. Indian Ocean coverage is
REAL but sparse and clustered — see bbox section and Assumptions.

---

## Source

| Property | Value |
|---|---|
| Primary source URL | `ftp://ftp.ifremer.fr/ifremer/glider/v2/` (accessed 2026-09-10, FTP handshake HTTP-226, 185 entries: 183 platforms + 2 index files) |
| HTTPS mirror (same tree) | `https://ftp.ifremer.fr/ifremer/glider/v2/` — **DEAD on this network**, curl timeout after 40 s (HTTP 000, accessed 2026-09-10). Do not rely on it. |
| HTTPS snapshot (alternative) | `https://www.seanoe.org/data/00453/56509/` (DOI landing, accessed 2026-09-10, HTTP 200) — quarterly `.tar.gz` snapshots, not the live tree |
| HTTPS query API (alternative) | `https://erddap.ifremer.fr/erddap/tabledap/OceanGlidersGDACTrajectories.html` (accessed 2026-09-10, HTTP 200) — **merged UFO-project subset only**, not the full GDAC; tabledap queries returned HTTP 400 through this network's proxy (encoded and raw) |
| Portal root (no glider path) | `https://data.ifremer.fr/` (HTTP 200) but `https://data.ifremer.fr/ifremer/glider/v2/` → HTTP 404 (accessed 2026-09-10) |
| DOI (snapshot) | `10.17882/56509` — SEANOE, "Ocean gliders : Data and metadata from Global Data Assembly Centre (OceanGliders GDAC)". Quarterly snapshots, successive versions preserved. |
| DOI (format manual) | `10.13155/34980` — "EGO gliders NetCDF format reference manual" |
| Format manual URL | `https://archimer.ifremer.fr/doc/00239/34980/113818.pdf` (accessed 2026-09-10, HTTP 200, 1,681,298 bytes) |
| Citation (per file `citation` attr, verbatim) | `"These data were collected and made freely available by the international EGO project and the national programs that contribute to it."` |
| sha256 | `71976eece1724fe3e25738d89bf61b640867cbe6c4286875afe01a3f99e6ec1d` — sample trajectory file fetched + hashed (see Sample below). Live GDAC has no single hash. |
| Ingest version | **v0** (card only, no ingest run) |
| Fixture use | NOT a fixture yet |

### Sample fetched + hashed (2026-09-10)

| Field | Value |
|---|---|
| URL | `ftp://ftp.ifremer.fr/ifremer/glider/v2/sea006/sea006_20250918/sea006_20250918_R.nc` |
| Bytes | `2,464,969` (Content-Length, FTP HTTP-226 transfer) |
| sha256 | `71976eece1724fe3e25738d89bf61b640867cbe6c4286875afe01a3f99e6ec1d` |
| Last-Modified | Wed, 19 Nov 2025 16:03:33 GMT |
| Role | Subset/hash anchor only; NOT the ingest fixture |

Other probed sizes: `/bonpland/bonpland_20190109/bonpland_20190109_R.nc` = 22,416,023 bytes (Last-Modified 2024-10-07).

---

## Licence

Verbatim from the sample file's global `license` attribute (confirmed identically in
`deployment_sea006_20250918.json`, extracted 2026-09-10):

```
license = "https://creativecommons.org/licenses/by-nc/4.0/"
```

The format manual (v1.2, §global-attributes table) documents the same convention:
`License="https://creativecommons.org/licenses/by-nc/4.0/"`.

Distribution statement, verbatim from the file's `distribution_statement` attribute:

> "EGO data are published without any warranty, express or implied. The user assumes
> all risk arising from his/her use of EGO data. EGO data are intended to be research-
> quality and include estimates of data quality and accuracy, but it is possible that
> these estimates or the data themselves contain errors. It is the sole responsibility
> of the user to assess if the data are appropriate for his/her use, and to interpret
> the data, data quality, and data accuracy accordingly. EGO welcomes users to ask
> questions and report problems to the contact addresses listed in the data files or
> on the EGO internet page."

The manual also records EGO adopting the CLIVAR data policy (free and unrestricted
exchange; contact PI before commercial use) — but the per-file machine-readable
licence is CC BY-NC 4.0. **SDN/Licence caveat:** ERDDAP's merged
`OceanGlidersGDACTrajectories` dataset carries a *different* global `license`
(CLIVAR wording, not CC BY-NC); that is the UFO-project merge, not the GDAC file
licence. Use the per-file `license` attr for the GDAC.

---

## File layout + naming (EGO NetCDF)

Layout under `v2/`:

```
v2/
  glider_traj_index.txt        # trajectory/ deployment index (1,115 deployment rows)
  glider_prof_index.txt        # per-profile index (824,632 profile rows)
  <platform>/<platform>_<YYYYMMDD>/<file>
  <platform>/<platform>_<YYYYMMDD>/deployment_<platform>_<YYYYMMDD>.json
  <platform>/<platform>_<YYYYMMDD>/profiles/<profile files>
```

Naming (EGO manual §6.1, verbatim):

- Trajectory/technical: `YYY/YYY_XXX/YYY_ZZZ_T.nc`
  - `YYY` platform code (EGO catalogue), `XXX` deployment start day `YYYYMMDD`,
    `ZZZ` deployment code, `T` = data mode (`R` real-time, `P` provisional,
    `D` delayed mode, `M` mixed), `.nc` suffix.
  - Example from the manual: `milou/milou_20150112/milou_mooseperseust02_08_R.nc`
- Profiles: `TVVV_XXX_NNN[D].nc` (§6.2, verbatim)
  - `T` data mode, `VVV` glider Id (WMO/`platform_code`), `XXX` deployment start day,
    `NNN` profile number, **`D` = descending profile** (without it, the profile was
    collected during ascent).

> **Correction to `glider-data.md`:** the trailing `D` in a profile filename means
> *descending*, **not** delayed-mode. `R<id>_<date>_003D.nc` is a real-time descending
> profile. The real-time examples observed (e.g. `R8901048_20250918_003D.nc`) confirm
> this: the mode letter is the leading `R`.

Observed live example directory
`/sea006/sea006_20250918/` (2026-09-10): `deployment_sea006_20250918.json`,
`sea006_20250918_R.nc`, `profiles/` containing `R8901048_20250918_001D.nc`,
`R8901048_20250918_002.nc`, `R8901048_20250918_003D.nc`, …

Format versions actually observed: deployment JSON reports
`Conventions = "CF-1.4 EGO-1.5"` and `format_version = "1.5"` (REVOSIMA 2025). The
manual describes EGO v1.x; ERDDAP's merged dataset reports `CF-1.6 EGO-1.2 ACDD-1.3`.
Treat conventions as **per-file**, read from global attrs at ingest.

---

## Variables (units / standard_name / QC)

Core CTD variables present on essentially every deployment (counts from the 131
Indian-Ocean deployments in the trajectory index, 2026-09-10):

| Variable | standard_name | units | Indian count /131 |
|---|---|---|---|
| `PRES` | `sea_water_pressure` | `decibar` | 131 |
| `TEMP` | `sea_water_temperature` (ITS-90) | `degree_Celsius` | 131 |
| `CNDC` | `sea_water_electrical_conductivity` | `mhos/m` | 131 |
| `PSAL` | `sea_water_practical_salinity` | `PSU` | 131 |
| `DOXY` | oxygen concentration | `micromole/kg` (sample-file unit; see note) | 130 |
| `MOLAR_DOXY` | `mole_concentration_of_dissolved_molecular_oxygen_in_sea_water` | `micromole/l` | 54 |
| `CHLA` | chlorophyll-a fluorescence | raw counts (no CF standard_name exposed) | 7 |
| `CDOM` | coloured dissolved organic matter fluorescence | raw counts | 3 |
| `BBP700` | particle backscattering at 700 nm | raw counts | 4 |

Notes:
- The sample trajectory file's raw strings contain `micromole/kg`, and ERDDAP's
  merged dataset exposes `MOLAR_DOXY` as `micromole/l`. Oxygen unit is **not
  uniform across all gliders** — read `units` from the file, never assume.
- `DOXY` count from traj index is 130/131; the ERDDAP merged subset lists
  `MOLAR_DOXY` rather than `DOXY` because its aggregation is UFO-project-specific.
- Each deployment also carries engineering/technical variables (`TECH_heading`,
  `TECH_pitch`, `TECH_roll`, `TECH_ballast_pumped`, `TECH_battery_position`, and
  `_C` corrected twins). Not oceanographic — not ingested for SIH-OCEAN.

### QC flags

Every measured variable `X` has an ancillary byte variable `X_QC`, plus global
`TIME_QC` and `POSITION_QC`. Convention = **EGO reference table 2.1** (verbatim
from ERDDAP attrs, 2026-09-10):

```
flag_values    = 0, 1, 2, 3, 4, 5, 8, 9
flag_meanings  = no_qc_performed good_data probably_good_data
                 bad_data_that_are_potentially_correctable bad_data
                 value_changed interpolated_value missing_value
```

`_FillValue` for measured floats is `99999.0`. Ingest must apply/qc-filter on
`X_QC` and drop `_FillValue`.

---

## Structure (NetCDF, CF + EGO)

- `featureType = Trajectory`; `cdm_data_type = Trajectory` (per deployment JSON).
- Per-profile files are the fine-grained unit (`trajectoryProfile`-style: one
  descent or ascent). Each profile file has `N_LEVELS` observations; index column
  `n_levels` gives levels per profile, `pressure_max` the profile's max pressure.
- The trajectory file (`<...>_R.nc`) carries the full time series + deployment
  metadata; the `deployment_*.json` carries platform/institution/PI/authors/licence.
- Index files (ASCII CSV, `#`-prefixed header block) allow discovery without
  downloading NetCDF:

  `glider_traj_index.txt` columns:
  `file, wmo, deployment_start_date, deployment_start_latitude,
  deployment_start_longitude, time_coverage_start, time_coverage_end,
  glider_model, owning_institution, program, sensors_model, parameter, ocean,
  date_update, gdac_date_creation, gdac_date_update`

  `glider_prof_index.txt` columns:
  `file, wmo, date, latitude, longitude, pressure_max, n_levels, parameter,
  ocean, date_update, gdac_date_creation, gdac_date_update`

  `ocean` codes observed: `A` Atlantic (576,529 profiles), `P` Pacific (178,134),
  `I` Indian (63,153), blank (6,816). Header also carries
  `# Date of update : 20260910063630`.

---

## bbox + Indian Ocean coverage (VERDICT)

**Global bbox:** worldwide, all major basins. Deployment-start positions in the
trajectory index span lat `-55.014 … 78.841`, lon `-140.109 … 178.45`; ocean code
counts cover Atlantic, Pacific, Indian. Gliders sample the upper ~1,000 m
(observed `pressure_max` median 213.9 dbar, max 10,475.8 dbar — deep outliers exist
but routine profiles are shallow).

**Indian Ocean (ocean code `I`): 131 deployments / 1,115 global (11.7%) and 63,153
profiles / 824,632 global (7.7%).** Profile time span 2018-07-18 → 2026-06-17.

Verdict: **present, but sparse and highly clustered — a data-availability risk,
NOT a gap.**

| Cluster | Platforms | Position | Program | Comment |
|---|---|---|---|---|
| Mayotte / REVOSIMA | `sea006`, `sea017`, `sea023`, `sea027`, `sea037`, `sea042`, `sea083` (7) | lat -12.94…-12.77, lon 45.26…45.39 | REVOSIMA | 124 / 131 Indian deployments; 126 of 130 IF-owned gliders are SEAEXPLORER. Dense in one ~0.13° box. |
| W Indian / SW Indian | `bonpland`, `tintin` | lat -21.1, lon 55.2 | (blank) | Réunion/Mauritius; 2 deployments. |
| N Indian | `sea057` | lat 24, lon 57–58 | (blank) | Gulf of Oman; 2 deployments. |
| Arabian Sea / Bay | `pheidippides` | lat 10, lon 78 | INTAROS | 1 deployment. |
| Gulf of Aden / NW | `hannon` | lat 5.99, lon 42.99 | (blank) | 1 deployment. |

Consequence: Indian-Ocean glider data is **not spatially representative**. 95% of
Indian deployments are the Mayotte REVOSIMA volcano-monitoring array; the open
Arabian Sea, Bay of Bengal and southern Indian Ocean are barely sampled. For the
SIH-OCEAN Indian-Ocean domain, gliders are an opportunistic overlay, not a coverage
layer. Pair with Argo (dense) + GLORYS (complete) rather than relying on gliders.

---

## Access latency — real-time only

All 824,632 indexed profiles carry the `R` (real-time) mode prefix; **0 delayed-mode
(`D`) profiles and 0 provisional (`P`) profiles** are listed (2026-09-10). Trajectory
files: 970 `_R.nc` + 145 `_P.nc`. The sample deployment JSON reports
`data_mode = "R"`. The GDAC distributes **near-real-time glider data with real-time QC
only** — there is no delayed-mode glider product to fetch. Any delayed-mode QC wording
in the manual describes a processing step, not files present on this GDAC.

---

## Volume / scale

| Quantity | Value | Source |
|---|---|---|
| Full GDAC snapshot size | ~25 Go (2026-07 snapshot) | SEANOE DOI 10.17882/56509, accessed 2026-09-10 |
| Snapshot history | 2026-04 24 Go, 2026-01 24 Go, 2025-10 24 Go, 2025-07 23 Go | same |
| Distinct platforms (dirs) | 183 | FTP listing 2026-09-10 |
| Deployments | 1,115 | traj index 2026-09-10 |
| Profile files | 824,632 | full prof index download 2026-09-10 |
| Trajectory files | 1,115 (970 R + 145 P) | traj index |
| Index update cadence | daily (`update_interval = "daily"`) | ERDDAP global attrs / traj index header date 20260910063630 |

> Do NOT use the ERDDAP merged dataset's `geospatial_lat/lon_*` attributes as a bbox:
> they report `696970.15` sentinels. Derive bbox from the index files instead.

---

## Ingestion plan (v0 — not run)

```
ftp://ftp.ifremer.fr/ifremer/glider/v2/glider_prof_index.txt   (discovery, 248 MB CSV)
        │  parse CSV (#-header) → one row per profile: file, lat, lon, date,
        │  pressure_max, n_levels, parameter, ocean
        ▼
   bbox / date / ocean filter  ──►  fetch only matching profiles/*.nc over FTP
        │
        ▼  xarray (NOT argopy — argopy is Argo-only)
   per-profile NetCDF → TEMP/PSAL/PRES/DOXY + X_QC flags
        │  apply QC (flag 1/2 keep; 0/3/4/5/8/9 drop or flag) + _FillValue drop
        │
        ├──► SQLite: gliders      (platform, deployment, lat, lon, date, vars)
        │           + R-tree spatial index
        └──► SQLite: glider_profiles (platform, profile_id, depth, temp, sal, doxy)
                    indexed by (platform, profile_id)
```

Mirrors/latency plan: fetch from FTP directly (HTTPS tree unavailable here). Use the
SEANOE tarball only if a reproducible pinned snapshot is required (quarterly cadence).

---

## Assumptions

1. **HTTPS mirror unavailable on this network.** `https://ftp.ifremer.fr/ifremer/glider/v2/`
   times out; `data.ifremer.fr` has no glider path. Ingest must use FTP, or the
   SEANOE quarterly download, or the ERDDAP merged subset. Flagged risk for
   environments where outbound FTP is blocked.
2. **Real-time only, no delayed-mode.** No QC-upgraded product exists on this GDAC;
   all data is real-time. Scientific users must accept real-time QC or treat gliders
   as indicative.
3. **Indian Ocean coverage is sparse and clustered** (see verdict). Data-availability
   risk: ~95% of Indian deployments are one Mayotte array. Do not present glider
   coverage as representative of the Indian Ocean domain.
4. **Licence is CC BY-NC 4.0 per file**, while the ERDDAP merge states CLIVAR terms.
   Resolve from the file's own `license` attr; non-commercial constraint must be
   respected.
5. **Variable set and units are per-glider, not uniform** (oxygen `micromole/kg` vs
   `micromole/l`; CHLA/CDOM/BBP700 in raw counts). Read attrs at ingest; never
   hard-code units.
6. Profile-file granularity: the descending `D` suffix is a direction flag, not a
   data mode. Both ascent and descent files for one Yo may exist; de-duplicate by
   `(platform, deployment, profile number)` at ingest if a single profile per cycle
   is wanted.
7. `n_levels` ranges 1 … 154,490, so profiles must be stored variable-length (do not
   pad to a fixed level count).

---

## Cross-refs

- FTP/source shape and prior ingestion sketch: `glider-data.md` (contains the
  descending-vs-delayed-mode error corrected above).
- Argo card: `argo-data.md`.
- Model overlay: `glorys-dataset.md`.
- INCOIS in-situ holdings: `incois-las.md`.
- NetCDF→Zarr conversion + chunking: `../architecture/backend-strategy.md`.
