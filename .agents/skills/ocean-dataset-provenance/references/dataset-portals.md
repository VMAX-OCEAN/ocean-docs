# Verified ocean data portal facts (access date 2026-09-10 unless noted)

Quoted from the authority pages during the run. Re-fetch before citing; portals move.

## Copernicus Marine / GLORYS

- Product: `GLOBAL_MULTIYEAR_PHY_001_030`, "Global Ocean Physics Reanalysis", GLORYS12V1, NEMO + reduced-order Kalman, 1/12 deg, 50 levels, Level 4, 0.083 x 0.083 deg.
- Sub-datasets (three): `cmems_mod_glo_phy_my_0.083deg_P1D-m` (daily), `cmems_mod_glo_phy_my_0.083deg_P1M-m` (monthly), `cmems_mod_glo_phy_my_0.083deg-climatology_P1M-m`.
- Format: NetCDF CF1.4. Licence + SLA: `https://marine.copernicus.eu/user-corner/service-commitments-and-licence`. Product page returns 200 via Vercel; the `/api/metadata/...` JSON route is not a reliable source.
- Product description: `https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description`; PUM: `https://documentation.marine.copernicus.eu/PUM/CMEMS-GLO-PUM-001-030.pdf`.

## Argo GDAC

- DOI `10.17882/42182` (SEANOE). Access: `ftp://ftp.ifremer.fr/ifremer/argo`, `https://data-argo.ifremer.fr`, s3 `https://registry.opendata.aws/argo-gdac-marinedata` (updated daily), rsync `vdmzrs.ifremer.fr::argo/` and `::argo-index/`.
- NetCDF, three views: `dac/`, `geo/`, `latest_data/`; top-level ASCII csv index files (meta, prof, tech, traj) plus a greylist.
- Citation sentence: "These data were collected and made freely available by the international Argo project and the national programs that contribute to it." User's manual DOI `10.13155/29825`.
- Scale: ~3,000 floats, ~100,000 T/S profiles + velocity per year, ~3-degree spacing.

## OceanGliders (ex-EGO) GDAC

- DOI `10.17882/56509`; quarterly snapshots, sizes from SEANOE: 2026-07 = 25 Go, 2026-04 = 24 Go, 2026-01 = 24 Go, 2025-10 = 24 Go, 2025-07 = 23 Go. NetCDF, quality controlled, ``Acces libre``.
- EGO/CF NetCDF manual: `https://archimer.ifremer.fr/doc/00239/34980/`. Header licence convention: `licence="https://creativecommons.org/licenses/by-nc/4.0/"`.
- ERDDAP access form: `https://erddap.ifremer.fr/erddap/tabledap/OceanGlidersGDACTrajectories.html`.
- Gliders sample the upper ~1 km; parameters temperature, salinity, pressure, biogeochemical and acoustic data.

## INCOIS

- Holdings catalog: `https://incois.gov.in/site/dataholdings.jsp` — lists drifting and moored buoys, XBT/XCTD, current meters, Argo, HF radar, coastal ADCP, tide gauges, tsunami buoys, ship/cruise data. Proves options exist; identifies none.
- ESSDP: `https://incois.gov.in/essdp/`.
- National Data Buoy Programme / moored buoys: `https://incois.gov.in/site/datainfo/OON.jsp` — T/S profiles to 500 m, currents to 100 m, but access wording is "Public Access with only visualisation option. No download option." Unusable as an automated fixture source.
