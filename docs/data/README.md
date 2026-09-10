# Data — dataset cards + contracts (placeholder)

Cards written 2026-09-10 (all 5 PS sources + INCOIS):

- `glorys12.md` — GLOBAL_MULTIYEAR_PHY_001_030, DOI `10.48670/moi-00021`, Copernicus licence, sha NONE metadata-only
- `incois-las.md` — las.incois.gov.in holdings, 16 ERDDAP IDs, 13 LAS cats, 44 holdings rows, sha NONE (live APIs)
- `argo.md` — ftp://ftp.ifremer.fr/ifremer/argo, DOI `10.17882/42182` CC-BY 4.0, sample sha+, Indian subset 354,696 files
- `glider.md` — ftp://ftp.ifremer.fr/ifremer/glider/v2/, CC-BY-NC 4.0, sample sha+, Indian coverage sparse = risk
- `insitu-collection.md` — PS link blank AUTHORITY-SIDE (sih.gov.in/sih2026PS item d), 8 candidates, fail closed

Each card: source URL, access date, sha256, license, bbox, variables, ingest version, assumptions. All cards at ingest v0 (metadata-complete, no ingest run).
NetCDF→Zarr conversion + chunking notes reference `../architecture/backend-strategy.md`.
