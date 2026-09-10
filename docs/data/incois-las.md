# INCOIS LAS / ERDDAP Holdings

INCOIS gridded analysis products + in-situ holdings index. Live query APIs (ERDDAP griddap/tabledap, LAS GWT), not file downloads.

---

## Product Details

| Property | Value |
|---|---|
| Provider | INCOIS (ESSO/INCOIS, Hyderabad) |
| Holdings index | https://incois.gov.in/site/dataholdings.jsp (accessed 2026-09-10, HTTP 200, 44 data rows) |
| ERDDAP root | https://erddap.incois.gov.in/erddap/ (accessed 2026-09-10, live, 16 datasets) |
| ERDDAP index | https://erddap.incois.gov.in/erddap/info/index.csv?page=1&itemsPerPage=1000 (note: bare `/info/index.csv` 302-redirects; `-L` required) (accessed 2026-09-10) |
| LAS root | https://las.incois.gov.in/las (accessed 2026-09-10; `getCategories.do` HTTP 200, 13 categories) |
| ESSDP portal | https://incois.gov.in/essdp/ (accessed 2026-09-10, HTTP 200; "1047 datasets" string NOT found in page — claim UNVERIFIED) |
| THREDDS | https://las.incois.gov.in/thredds/catalog.html (accessed 2026-09-10, HTTP 200; catalog holds single DatasetScan ref "Data form LAS", no per-dataset listing) |
| TLS note | cert chain needs `-k` / verify-off on this network |
| sha256 | NONE — live APIs only, no file downloaded (see Assumptions) |
| License (ERDDAP `.das`, verbatim) | "The data may be used and redistributed for free but is not intended for legal use, since it may contain inaccuracies. Neither the data Contributor, ERD, NOAA, nor the United States Government, nor any of their employees or contractors, makes any warranty, express or implied, including warranties of merchantability and fitness for a particular purpose, or assumes any legal liability for the accuracy, completeness, or usefulness, of this information." |
| Ingest version | v0 (card only, no ingest run) |

---

## ERDDAP datasets (16, from index.csv 2026-09-10)

| Dataset ID | Type | Title |
|---|---|---|
| AMSRE_MONTHLY_GLOBAL | griddap | AMSRE Monthly Global Data |
| ascat_daily_datasets | griddap | Daily ASCAT global wind field |
| ascat_mnt_datasets | griddap | Monthly ASCAT global wind field |
| NOAA_AVHRR_AMSR_datasets | griddap | Daily-OI-V2, final, Data (Ship, Buoy, AMSR-E, AVHRR, GSFC-ice) |
| incois_argo_10day_McCreary | griddap | INCOIS ARGO 10 Day data Kessler-McCreary Methodology |
| incois_argo_10d_VAM | griddap | INCOIS ARGO 10 day data Variational Analysis Methodology |
| incois_argo_mnt_McCreary | griddap | INCOIS ARGO Monthly data Kessler-McCreary Methodology |
| incois_argo_mnt_VAM | griddap | INCOIS ARGO Monthly data Variational Analysis Methodology |
| incois_argo_sst_weekly | griddap | INCOIS argo SST data Weekly |
| incois_oceansat2_datasets | griddap | INCOIS Oceansat 2 OCM Data |
| incois_quickscat_daily_datasets | griddap | INCOIS Quickscat Daily Data |
| incois_quickscat_mnt_datasets | griddap | INCOIS Quickscat Monthly Data |
| incois_tmi_3day_datasets | griddap | INCOIS TMI 3Day Data |
| incois_valueadded_products_datasets | griddap | INCOIS Value Added Products |
| IRS_chlorophyll_datasets | griddap | IRS P4 OCM-Chlorophyll |
| Indian_ARGO_Floats | tabledap | INDIAN ARGO Floats Data |

---

## Variables + bbox (from per-dataset `.das`, fetched 2026-09-10)

### NOAA_AVHRR_AMSR_datasets — regional daily SST (key dataset)

| Variable | Unit | Description |
|---|---|---|
| `sst` | degrees C | Daily sea surface temperature |
| `anom` | degrees C | Daily SST anomaly |

| Bound | Value |
|---|---|
| Lat | -29.875 – 29.875 (0.25° res) |
| Lon | 20.125 – 139.875 (0.25° res) |
| Time | 2002-06-01 – 2011-10-04 (static archive, ends 2011) |

### incois_valueadded_products_datasets — Argo-derived layers (key dataset)

| Variable | Unit | Description |
|---|---|---|
| `MLD` | m | Mixed Layer Depth |
| `ILD` | m | Isothermal Layer Depth |
| `D26` | m | Depth of 26°C isotherm |
| `D20` | m | Depth of 20°C isotherm |
| `HTCNT` | J/m² ×1E-08 | Heat content to 300 m |
| `DYN_HT` | dyn-cm | Dynamic height |
| `GEO_U` / `GEO_V` | cm/s | Geostrophic currents |

| Bound | Value |
|---|---|
| Lat | -29.5 – 29.5 (1.0° res) |
| Lon | 30.5 – 119.5 (1.0° res) |
| Time | 2004-01-10 – 2019-03-30 |

### incois_argo_10d_VAM — 10-day T/S grids (key dataset)

| Variable | Unit | Description |
|---|---|---|
| `TEMP` | degs | Temperature |
| `TERR` | degs | Temp relative error |
| `SAL` | PSU | Salinity |
| `SERR` | PSU | Salinity relative error |

| Bound | Value |
|---|---|
| Lat | -29.5 – 29.5 (1.0° res) |
| Lon | 30.5 – 119.5 (1.0° res) |
| Depth (`ZAX`) | 5 – 2000 m, uneven |
| Time | 2004-01-10 – 2026-07-30 (most current Argo grid) |

### AMSRE_MONTHLY_GLOBAL — global microwave (key dataset)

| Variable | Unit | Description |
|---|---|---|
| `SST` | Degree C | Sea Surface Temperature |
| `WSPD_LF` / `WSPD_MF` | m/s | Wind speed (10.7 / 18.7 GHz) |
| `VAPOR` | mm | Columnar water vapor |
| `CLOUD` | mm | Columnar cloud liquid water |
| `RAIN` | mm/hr | Rain rate |

| Bound | Value |
|---|---|
| Lat | -90.0 – 89.75 (0.25° res, global) |
| Lon | 0.0 – 359.75 (0.25° res) |
| Time | 2002-06-14 – 2011-09-14 (static, AMSR-E era) |

### Indian_ARGO_Floats — point profiles (key dataset, tabledap `.das`)

| Variable group | Contents |
|---|---|
| Position/time | `latitude`, `longitude`, `time`, `JULD_QC`, `JULD_LOCATION` |
| Profile | `PRES` / `PRES_ADJUSTED` (dbar), `TEMP` / `TEMP_ADJUSTED` (°C), `PSAL` / `PSAL_ADJUSTED` (PSU), per-var QC flags |
| Meta | `PLATFORM_NUMBER`, `CYCLE_NUMBER`, `DIRECTION`, `PLATFORM_TYPE` |

| Bound | Value |
|---|---|
| Lat | -69.735 – 47.783 (actual_range) |
| Lon | -179.988 – 179.903 (actual_range) |
| Time | 2002-10-24 – 2025-04-23 (epoch 1035487803 – 1745414880) |

Remaining 11 datasets: `.das` NOT fetched (same pattern; fetch on demand). Variables per index.csv summary: ASCAT daily/monthly (wind_speed, eastward/northward wind, wind_stress ×3); Argo McCreary 10-day/monthly (T/S_ANALYZED, _MEAN, _STDEV, _RMSE, _ROIOBS, _BOXOBS); argo_sst_weekly (ASST, ERR); oceansat2 (CHL, KD490, TSM); quickscat daily/monthly (WIND_SPEED, ZONAL/MERI components, WIND_STRESS + CURL); tmi_3day (SST, WSPD_LF/MF, VAPOR, CLOUD, RAIN); IRS_chlorophyll (CHLOROPHYLL).

---

## LAS categories (13, `getCategories.do` 2026-09-10)

ARGO DATA PRODUCTS, ASCAT DATA Products, Global Ocean Analaysis (GODAS), INCOIS Global Ocean Reanalysis (IGORA), MaMetAtTIO Datasets, MICROWAVE DATA PRODUCTS, NEW GLOBAL CLIMATOLOGY (NIO), NOAA High Resolution SST (data provided by the NOAA OAR ESRL), Ocean Carbonate Products, OCEAN COLOUR PRODUCTS, Oscat Wind Dataset, QUICKSCAT DATA PRODUCTS, Tropflux Variables (1940-2025).

`getDatasets.do?catid=<ID>` returns one 17 MB dump of 52 datasets regardless of catid (endpoint ignores catid; parse as latin-1 — contains 0xb2 unit bytes). Dataset names include: ARGO DATA PRODUCTS (10 DAYS), VAM 10DAY ARGO, Argo SST Weekly, ARGO Value Added Products, ARGO DATA PRODUCTS (Monthly), VAM MNT ARGO, AMSRE/TMI/AMSR2 3-day+monthly, NOAA AVHRR-only + AVHRR+AMSR SST, ASCAT daily/monthly, QUICKSCAT daily/monthly, OCM-1/OCM-2, OSCAT WINDS, GODAS 2022–2025, IGORA (sal/temp/u/v, INCOIS BIO ROMS/TA/REML), Tropflux fluxes (latent/sensible/net heat, wind stress, SST, air temp, humidity, radiation).

---

## Holdings access tiers (exact page wording, dataholdings.jsp 2026-09-10)

| Wording (verbatim) | Count | Applies to |
|---|---|---|
| `Public Access with visualisation, download options` | 11 | Drifting Buoy, Current Meter Array (spelled `visualization`), AMSR-E, LAS Argo-SST-weekly, ASCAT, NIO climatology, NOAA HR SST, GODAS, QuikSCAT, TMI, OCM-1, INCOIS AVHRR |
| `Public Access with visualisation, download facilities for open Ocean data.` | 1 | Argo Floats |
| `Public Access with visualisation option. No download option.` | 3 | XBT/XCTD, Ship AWS, Wave Rider Buoy |
| `Public Access with only visualisation option. No download option.` | 1 | Moored Buoy (row truncated in fetch) |
| `Tsunami Early Warning Centre Website Visualization. No download facility` (+ `No download facility` variants) | 3 | Tsunami Buoy, Seismic, BPR |
| `Registered access through Website` | 1 | HF Radar |
| `Restricted; as per DoS guidelines` (+ `... (Data being in EEZ)` for MEDAS) | 3 | OCM-1, OCM-2, MEDAS |
| `Non-Sensitive` | 3 | AVHRR-NOAA raw, AVHRR-SST archives, VIIRS |
| `Recent data is available on web; Remaining archived` | 1 | Wave Watch III |
| `Available for PI's of CTCZ programme` | 1 | CTCZ |
| (blank cell) | ~15 | Tide gauges, BPR-adjacent, SATCORE, COMAPS, ICMAM, OMM, Sagar Sampada, MODIS, bloom/CDOM indices, MIKE, ROMS, PFZ, Coastal ADCP, Ship wave meter |

---

## Access

### ERDDAP subset (recommended)

```
# NOAA regional SST, Indian Ocean window
https://erddap.incois.gov.in/erddap/griddap/NOAA_AVHRR_AMSR_datasets.nc?sst[(2002-06-01):1:(2011-10-04)][(-29.875):1:(29.875)][(20.125):1:(139.875)]
# Value-added MLD
https://erddap.incois.gov.in/erddap/griddap/incois_valueadded_products_datasets.nc?MLD[(2004-01-10):1:(2019-03-30)][(-29.5):1:(29.5)][(30.5):1:(119.5)]
# Argo float points
https://erddap.incois.gov.in/erddap/tabledap/Indian_ARGO_Floats.nc?latitude,longitude,time,TEMP,PSAL,PRES&time>=2002-10-24
```

### LAS

GWT app: https://las.incois.gov.in/las — `getCategories.do` (no args) → `getDatasets.do?catid=<ID>` (17 MB dump, latin-1). No OPeNDAP-per-dataset URLs in dump; `url` fields are server-local paths (`/home/las/datasets/...`).

---

## Indian Ocean Subset

| Bound | Value |
|---|---|
| Longitude | 30.5°E – 119.5°E (Argo grids; NOAA SST window 20.125–139.875) |
| Latitude | 29.5°S – 29.5°N (Argo grids; NOAA SST ±29.875) |
| Depth | 5 – 2000 m (VAM ZAX); MLD/D20/D26 2D |
| Time | 2004 – present (VAM 10-day ends 2026-07-30; NOAA SST frozen at 2011-10-04) |

---

## Assumptions

1. No sha256 recorded — live query APIs, no file downloaded; hashes apply at ingest time per subset request, not to card.
2. ERDDAP `.das` license is generic ERDDAP boilerplate (names NOAA/ERD), NOT an INCOIS-specific license; holdings-page tiers govern actual reuse.
3. Holdings page has ~15 blank accessibility cells — treated as unknown/restricted-by-default, never assumed public.
4. LAS `getDatasets.do` ignores catid (identical 17 MB/52-dataset dump for all 13 cats, verified by md5) — category→dataset mapping unavailable.
5. NOAA_AVHRR_AMSR + AMSRE series are static archives ending 2011 — unsuitable as live SST; use VAM/weekly or external SST for current dates.
6. ESSDP "1047 datasets" claim NOT reproduced (page HTTP 200 but string absent) — left UNVERIFIED.
7. THREDDS endpoint live but exposes only one DatasetScan catalogRef — not a usable ingest path; ERDDAP/LAS preferred.
8. Gateway unavailable this run ($NINEROUTER_KEY length 0) — direct curl with `-k` used; re-verify via gateway before D5 sign-off if policy requires.
