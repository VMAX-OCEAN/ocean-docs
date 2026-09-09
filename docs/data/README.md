# Data — dataset cards + contracts (placeholder)

Cards required before any fixture is used. One card per PS source:

- `glorys12.md` — GLOBAL_MULTIYEAR_PHY_001_030 (thetao/so/uo/vo/zos, 1/12°, 50 levels)
- `incois-las.md` — las.incois.gov.in holdings
- `argo.md` — ftp://ftp.ifremer.fr/ifremer/argo
- `glider.md` — ftp://ftp.ifremer.fr/ifremer/glider/v2/
- `insitu-collection.md` — PS link blank; flag unknown, do not invent URL

Each card: source URL, access date, sha256, license, bbox, variables, ingest version, assumptions.
NetCDF→Zarr conversion + chunking notes reference `../architecture/backend-strategy.md`.
