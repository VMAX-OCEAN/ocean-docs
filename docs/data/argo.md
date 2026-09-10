# Argo GDAC — dataset card (D1)

Contract card for the Argo Global Data Assembly Centre (GDAC). Every field below is either
verified against the live authority on the access date shown, or reads `UNKNOWN`/`NONE`
with the search trail. Card written 2026-09-10.

---

## Source + access

| Property | Value |
|---|---|
| Canonical URL (FTP) | `ftp://ftp.ifremer.fr/ifremer/argo` (PS source) |
| Canonical URL (HTTPS) | `https://data-argo.ifremer.fr` (root HTTP 200, 5462 B, accessed 2026-09-10; directory index live, files dated 2026-09-10) |
| US GDAC mirror | `https://usgodae.org/pub/outgoing/argo` (listed in argopy host shortcuts; NOT independently fetched this run) |
| DOI | `10.17882/42182` — resolves HTTP 200 → `https://www.seanoe.org/data/00311/42182/` (accessed 2026-09-10) |
| Citation (README, verbatim) | "These data were collected and made freely available by the International Argo Program and the national programs that contribute to it (http://www.argo.ucsd.edu, http://argo.jcommops.org). The Argo Program is part of the Global Ocean Observing System." |
| SEANOE citation string (verbatim) | `Argo (2026). Argo float data and metadata from Global Data Assembly Centre (Argo GDAC). SEANOE. https://doi.org/10.17882/42182` |
| User's manual | Argo data management, `3.44.0` (2025-07-09), DOI `10.13155/29825` |
| Readme | `https://data-argo.ifremer.fr/readme_before_using_the_data.txt` (HTTP 200, 1859 B, file mtime 2017-11-27) |
| Ingest version | v0 (card only; no ingest run) |

Two access dates, one per URL, recorded inline above.

---

## License

| Property | Value |
|---|---|
| License | **CC-BY 4.0** — `https://creativecommons.org/licenses/by/4.0/` |
| Evidence | SEANOE DOI landing JSON, quoted verbatim: `"license":"https://creativecommons.org/licenses/by/4.0/"` (accessed 2026-09-10). Licence icon served as `assets/images/licence-icon/by.png`. |
| Access wording (ADMT `DataAccess.html`, verbatim) | "Argo data are freely available from US-Godae and Coriolis GDAC sites with ftp, https or s3 protocols." (HTTP 200, 39390 B, accessed 2026-09-10) |
| Caveat (README/user manual) | "Argo data are published without any warranty, express or implied. The user assumes all risk arising from his/her use of Argo data." Attribution requested: acknowledge + cite the DOI. |
| `argo.ucsd.edu/data/data-policy/` | HTTP **404** at that path this run — policy wording taken from the GDAC README, SEANOE record and ADMT access page instead. |
| `argodatamgt.org/Access-to-data/Data-policy` and `.../Argo-DOI-Digital-Object-Identifier` | HTTP **404** this run (site path changed; do not cite these URLs). |

---

## Access points (verified 2026-09-10)

| Access path | Status |
|---|---|
| FTP `ftp://ftp.ifremer.fr/ifremer/argo` | LIVE — root listing matches HTTPS root exactly (same 20 entries: 4 index `.txt` + `.gz`, `argo_bio-profile_index`, `argo_synthetic-profile_index`, `aux/ dac/ etc/ geo/ latest_data/`, readme) |
| HTTPS `https://data-argo.ifremer.fr` | LIVE, HTTP 200 |
| s3 | `s3://argo-gdac-sandbox/pub/idx` (argopy option), AWS registry `argo-gdac-marinedata` (ADMT/argo.ucsd) — not fetched this run |
| rsync | `vdmzrs.ifremer.fr::argo/` (dac mirror) and `::argo-index/` (indices) — from argopy docs / dataset-portals.md |
| ERDDAP | `https://erddap.ifremer.fr` (ADMT Coriolis report) — not fetched this run |
| argopy | Default host `https://data-argo.ifremer.fr`; shortcuts `http/https`→Ifremer, `us-http/us-https`→usgodae, `ftp`→`ftp://ftp.ifremer.fr/ifremer/argo`, `s3/aws`→`s3://argo-gdac-sandbox/pub/idx`. Default index `ar_index_global_prof.txt`, default dataset `phy`, default mode `standard`. |

GDAC layout, three views (from skill `dataset-portals.md` + root listing): `dac/`, `geo/`, `latest_data/`.

---

## Structure + file naming

DACs (11, from live `dac/` listing 2026-09-10): `aoml bodc coriolis csio csiro incois jma kiost kma meds nmdis`.

Per-float files (verified by live directory listing; `coriolis/6901254/` and `aoml/13857/`):

| File | Contents |
|---|---|
| `<WMO>_prof.nc` | All profiles for the float (multi-profile, N_PROF × N_LEVELS) — **verified present** |
| `<WMO>_Rtraj.nc` | Trajectory |
| `<WMO>_meta.nc` | Metadata |
| `<WMO>_tech.nc` | Technical |
| `profiles/<D\|R><WMO>_<NNN>[D].nc` | Mono-profile, descending `D…` or ascending `R…`; trailing `D` = delayed-mode file |

`<WMO>` is the float identifier, e.g. `6901254`, `13857`. Multi-profile directory `profiles/` confirmed under each float dir.

### Index files (top level, live listing 2026-09-10)

| File | Size (listing) | Updated |
|---|---|---|
| `ar_index_global_prof.txt` / `.txt.gz` | 302M / 56M | 2026-09-10 15:24 |
| `ar_index_global_meta.txt` / `.gz` | 1.0M / 172K | 2026-09-10 14:27 |
| `ar_index_global_traj.txt` / `.gz` | 2.0M / 542K | 2026-09-10 10:40 |
| `ar_index_global_tech.txt` / `.gz` | 947K / 185K | 2026-09-09 18:27 |
| `argo_bio-profile_index.txt` / `.gz` | 118M / 7.5M | 2026-09-10 15:24 |
| `argo_synthetic-profile_index.txt` / `.gz` | 61M / 7.7M | 2026-09-10 15:24 |
| `argo_bio-traj_index.txt` / `.gz` | 15K / 3.6K | 2026-09-10 10:43 |

**Profile index header (verbatim, fetched 2026-09-10):**
`file,date,latitude,longitude,ocean,profiler_type,institution,date_update`
(meta-line `# GDAC node : CORIOLIS`, `# Date of update : 20260910142414`).

Per skill `ocean-dataset-provenance`: latitude = column 3, longitude = column 4 (0-based 2, 3);
float id = path segment **1** (`<dac>/<float>/profiles/<file>`), not segment 2.

---

## GDAC size / file count — claim check

Card in `argo-data.md` claimed **931 GB / 3.5M NetCDF files**. Verdict: **size label UNVERIFIED for 2026; file count ~matches (profile files ~3.39M, all NetCDF incl. meta/traj/tech larger).**

| Claim | Evidence | Status |
|---|---|---|
| 3.5M NetCDF files | ADMT National Data Management Report: "total number of NetCDF files on the GDAC/dac directory was **3 535 214**" (2023 report) and "**3 773 576** (+7%)" in a Coriolis 2024 report | PARTIAL — 2023 figure was 3.5M; 2024 report 3.77M |
| 931 GB GDAC total | Same ADMT report table: `gdac total 931` Gb (branch table: dac 423, geo 24, latest_data 159, aux 12) | SIZE UNVERIFIED for 2026 — last authoritative figure is 931 GB (2023-era report, repeated in a 2024 deck). Not re-measured this run. |
| Profile file count now | Live `ar_index_global_prof.txt.gz` parsed 2026-09-10: **3,386,798 profile file records**, **20,484 unique floats**, latest profile date 2026-09-10 | VERIFIED (this run) |
| `dac/` size | ADMT report: 423 GB (2023) / 484 GB (2024 Coriolis deck) | UNVERIFIED for 2026 |
| SEANOE monthly snapshot size | DOI page lists "Global GDAC Argo data files (2026-08-08 snapshot)" = **87 Go** (Go = GB), compressed `.tar.gz`; BGC Sprof snapshot = 6 Go | VERIFIED (SEANOE page 2026-09-10). Compressed snapshot ≠ live uncompressed `dac/` tree; do not conflate. |

Rule: quote **931 GB** only with the ADMT-report attribution and year; do not present it as a 2026 live measurement.

---

## Variables (from live NetCDF files, attrs verbatim)

Core sample: `https://data-argo.ifremer.fr/dac/coriolis/6901254/6901254_prof.nc` (HTTP 200, **1,199,768 B**).
BGC sample: `https://data-argo.ifremer.fr/dac/aoml/1900722/profiles/BD1900722_001.nc` (HTTP 200, **22,880 B**).

### Core (PRES / TEMP / PSAL)

| Variable | units | standard_name | QC variable |
|---|---|---|---|
| `PRES` | `decibar` | `sea_water_pressure` | `PRES_QC` (Argo reference table 2) |
| `TEMP` | `degree_Celsius` | `sea_water_temperature` | `TEMP_QC` |
| `PSAL` | `psu` | `sea_water_salinity` | `PSAL_QC` |

Each core parameter also has `_ADJUSTED`, `_ADJUSTED_QC`, `_ADJUSTED_ERROR` (units as above).
File global attr `Conventions = Argo-3.1 CF-1.6` (sample `user_manual_version` 3.1, `featureType = trajectoryProfile`).

Position/time variables: `LATITUDE` (`degree_north`, `latitude`), `LONGITUDE` (`degree_east`, `longitude`),
`JULD` (`days since 1950-01-01 00:00:00 UTC`, `time`), with `POSITION_QC`, `JULD_QC`.

### BGC (`DOXY`)

| Variable | units | standard_name | QC variable |
|---|---|---|---|
| `DOXY` | `micromole/kg` | `moles_of_oxygen_per_unit_mass_in_sea_water` | `DOXY_QC` |
| `DOXY_ADJUSTED` | `micromole/kg` | `moles_of_oxygen_per_unit_mass_in_sea_water` | `DOXY_ADJUSTED_QC` |

BGC sample also carries `TEMP_DOXY`, `BPHASE_DOXY` (+ `_QC`/`_ADJUSTED`/`_ADJUSTED_ERROR`), and
`PARAMETER_DATA_MODE`. `DOXY_QC` conventions = Argo reference table 2.

`valid_min` / `valid_max` for these variables: **UNKNOWN** — attr values not extracted (no `netCDF4`/`xarray`/`scipy`
in the environment; pip blocked by PEP 668). Attr *names* confirmed present in the CDF header, numeric values not read.

**QC flag scale (Argo reference table 2, verbatim meanings):** `0` No QC performed; `1` Good data;
`2` Probably good; `3` Probably bad, potentially adjustable; `4` Bad data; `5` Value changed;
`6`/`7` Not used; `8` Estimated; `9` Missing value.

---

## BBox

| Scope | Bounds | Evidence |
|---|---|---|
| Global (GDAC nominal) | lat −90 to 90, lon −180 to 180 | SEANOE JSON `"spatialCoverage":{"box":"-90 180 90 -180"}` (accessed 2026-09-10) |
| Global (measured, profiles) | **20,484 floats / 3,386,798 profile records** across full index; latest profile date 2026-09-10 | Live `ar_index_global_prof.txt.gz`, `scripts/argo_bbox_count.py` + local parse, this run |
| **Indian Ocean subset (project scope)** | lon **30°E – 120°E**, lat **30°S – 30°N** | Live index parse this run: **354,696 profile files**, **2,421 floats**, latest 2026-09-10. Ocean code `I` count (whole-index) = 650,340. |

Indian Ocean window above is the project's chosen subset bbox, not an official Argo extent.
The `I` ocean code (index column 5) marks the Indian basin; the bbox is a rectangular approximation of it.

---

## sha256

| Item | Value |
|---|---|
| Bulk per-file hash | **NONE** — live continuously-updated FTP/HTTPS tree, no fixed artifact to hash. Hashes apply per fetch, not to the source. |
| Sample `6901254_prof.nc` | `b6ff7615f1a0aa68c8af6aaf7a791b28b387fd64e30f3843ffad9a6d571f1e10`, bytes `1199768`, URL `https://data-argo.ifremer.fr/dac/coriolis/6901254/6901254_prof.nc` (HTTP 200, fetched 2026-09-10) |
| Sample `BD1900722_001.nc` | `ee5d3c8392f2c8943b34709f5a7a2fe1cb1fe182fa6f6cdc18372dae1a447e4d`, bytes `22880`, URL `https://data-argo.ifremer.fr/dac/aoml/1900722/profiles/BD1900722_001.nc` (HTTP 200, fetched 2026-09-10) |
| Reproducibility note | These files are mutable (real-time → delayed-mode reprocessing). Sample hashes are point-in-time markers only, not a stable fixture checksum. Use the monthly SEANOE DOI snapshots for a stable artifact. |

---

## argopy access (verified against argopy docs 2026-09-10)

Default source is ERDDAP (`erddap`), dataset `phy`, mode `standard`; `src='gdac'` selects the GDAC tree.
Host shortcuts: `http`/`https` → `https://data-argo.ifremer.fr`; `ftp` → `ftp://ftp.ifremer.fr/ifremer/argo`;
`s3`/`aws` → `s3://argo-gdac-sandbox/pub/idx`. `ArgoIndex` supports index files `core`
(`ar_index_global_prof.txt`), `bgc-b` (`argo_bio-profile_index.txt`), `bgc-s`
(`argo_synthetic-profile_index.txt`), `aux`, `meta`; trajectory/technical/meta index stores are **not**
queryable (search unsupported per argopy table).

```python
import argopy
from argopy import DataFetcher, ArgoIndex

# Indian Ocean window, core T/S, from GDAC tree.
# box = [lon_min, lon_max, lat_min, lat_max, dpt_min, dpt_max, date_min, date_max]
ds = DataFetcher(src='gdac', gdac='https://data-argo.ifremer.fr').region(
    [30, 120, -30, 30, 0, 2000, '2026-01-01', '2026-12-31']
).to_xarray()

# Float index (WMO, lat, lon, date) for the subset
idx = ArgoIndex(host='https://data-argo.ifremer.fr',
                index_file='ar_index_global_prof.txt').load()
subset = idx.search_lat_lon([30, -30, 120, 30]).to_dataframe()
```

**`region` box order is `[lon_min, lon_max, lat_min, lat_max, dpt_min, dpt_max, date_min?, date_max?]`**
(verbatim from argopy docs: "lon_min: float, lon_max: float, lat_min: float, lat_max: float, dpt_min: float,
dpt_max: float, date_min: str (optional), date_max: str (optional)"). Longitude, latitude and **pressure/depth
bounds are required**. The `argo-data.md` snippet `region([-90, 30, 180, 90, '2026-01-01', ...])` is wrong on
two counts — it omits the required depth pair and its numbers parse as lon −90..30, lat 180..90 (inverted) —
fix `argo-data.md` on next edit. `search_lat_lon` takes `[lon_min, lat_min, lon_max, lat_max]` (a different
order from `region`).

---

## Assumptions

1. **Ingest path: argopy → SQLite/Supabase.** Bulk GDAC is not mirrored; argopy fetches the Indian Ocean
   subset on demand, staged into SQLite (spatial R-tree) / Supabase. Ingest version **v0** (card only).
2. **QC flag 1 only** (Good data) retained for the residual/served fixture. `2` (probably good) and
   `3` (adjustable) excluded from the residual; `0` never assumed good. Adjusted (`_ADJUSTED`) values are
   used where present, else raw.
3. **Indian Ocean subset scope:** lon 30–120 E, lat 30 S–30 N (project bbox above). Global GDAC fields
   above are for reference/citation only, not the ingest scope.
4. 931 GB / 3.5M-file figure is an ADMT-report attribution (2023–2024), **not** a 2026 live measurement;
   the live profile-file count measured this run is 3,386,798 records.
5. Sample sha256 values are point-in-time; the source is mutable — no stable per-file hash contract.
6. `valid_min`/`valid_max` values and full NC variable dump: UNKNOWN this run (no NetCDF libs available,
   pip PEP-668-blocked). Re-read with `netCDF4`+`xarray` before ingest to lock the variable contract.
7. Gateway unavailable this run (`$NINEROUTER_KEY` length 0) — all fetches were direct curl/urllib.
   Re-verify via gateway before sign-off if policy requires.
