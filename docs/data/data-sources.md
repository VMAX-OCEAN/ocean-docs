# Data Sources

All data source links for the SIH-OCEAN platform, as specified in the problem statement.

---

## Problem Statement Datasets

The PS (26067) specifies these dataset links:

### Numerical Ocean Model Outputs

| Source | URL | Format | Access |
|---|---|---|---|
| INCOIS Live Access Server | https://las.incois.gov.in/ | NetCDF, OPeNDAP | Web portal, subset download |
| Copernicus GLORYS12 | https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description | NetCDF | Copernicus Marine, subset API, OPeNDAP |

### In-situ Observations

| Source | URL | Format | Access |
|---|---|---|---|
| Argo Global Data | ftp://ftp.ifremer.fr/ifremer/argo | NetCDF | FTP, argopy |
| Glider Data | ftp://ftp.ifremer.fr/ifremer/glider/v2/ | NetCDF | FTP, xarray |
| Collection of In-situ Data | (specified in PS) | Various | Various |

---

## INCOIS Data Holdings

INCOIS provides extensive ocean data holdings:

| Observation Type | Platform | Parameters | Period | Format |
|---|---|---|---|---|
| In-situ | Drifting Buoy | Atm pressure, SST, currents | 1991–present | ASCII/NetCDF/HDF/Binary |
| In-situ | Argo Floats | Temperature, salinity profiles | 2000–present | NetCDF |
| In-situ | CTD | Temperature, salinity | Various | NetCDF |
| Satellite | AMSR-E | Water vapor, cloud, rain, SST, wind | 2002–2011 | NetCDF |
| Model | Ocean Reanalysis (GODAS-MOM) | SST, daily anomalies | 2012–present | NetCDF |
| Satellite | AVHRR (INCOIS ground station) | SST | 2004–present | NetCDF |

**INCOIS Data Holdings page:** https://incois.gov.in/site/dataholdings.jsp

---

## Copernicus Marine Service

### GLORYS12 (primary model output)

- **Product:** GLOBAL_MULTIYEAR_PHY_001_030
- **Variables:** temperature, salinity, currents, sea level, mixed layer, sea ice
- **Resolution:** 1/12° (~8 km), 50 depth levels, daily
- **Period:** 1993 to present
- **Access:**
  - Web: https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description
  - Subset API: `copernicusmarine.subset(...)` (Python)
  - OPeNDAP: via THREDDS server
  - Files: https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/files

### Other Copernicus products (potential)

| Product | Description |
|---|---|
| GLOBAL_MULTIYEAR_BGC_001_029 | Biogeochemical (chlorophyll, oxygen, nutrients) |
| GLOBAL_ANALYSISFORECAST_PHY_001_024 | Near-real-time forecast |
| INDOI_ANALYSISFORECAST_PHY_001_014 | Indian Ocean analysis (regional) |

---

## Argo Data

### Global Data Assembly Centers (GDACs)

| GDAC | URL |
|---|---|
| Ifremer (Brest) | ftp://ftp.ifremer.fr/ifremer/argo |
| NOAA (Monterey) | ftp://ftp.aoml.noaa.gov/pub/argo |

### Argo snapshots (DOI-archived)

- Full GDAC tarball: ~50 GB
- BGC Sprof tarball: ~2 GB
- DOI: 10.17882/42182

### Access via argopy

```python
from argopy import DataFetcher
ds = DataFetcher().region([lon_min, lat_min, lon_max, lat_max, date_min, date_max]).to_xarray()
```

### Euro-Argo fleet monitoring

- API: https://fleetmonitoring.euro-argo.eu/
- Dashboard with active float positions

---

## Glider Data

### Ifremer FTP

```
ftp://ftp.ifremer.fr/ifremer/glider/v2/
```

Organized by deployment, each with NetCDF profile files following CF conventions
(`featureType = trajectoryProfile`).

### OceanGliders

- Organization: https://www.oceangliders.org/
- Data: via Ifremer FTP and ERDDAP servers

---

## Bathymetry (for the globe)

| Source | Resolution | URL |
|---|---|---|
| GEBCO | 15 arc-second (~450 m) | https://www.gebco.net/data_and_products/gridded_bathymetry_data/ |
| Cesium World Terrain | varies | Cesium ion (built-in) |
| SRTM15+ | 15 arc-second | https://topex.ucsd.edu/WWW_html/srtm15_plus.html |

GEBCO bathymetry gives real seafloor relief — critical for ocean visualization.

---

## Coastlines and Boundaries

| Source | Scale | URL |
|---|---|---|
| Natural Earth | 1:10m, 1:50m, 1:110m | https://www.naturalearthdata.com/ |
| Natural Earth 6 (nullschool uses) | 1:7.5m | (preliminary) |
| GSHHG (Global Self-consistent Hierarchical High-res) | various | https://www.soest.hawaii.edu/pwessel/gshhg/ |

---

## Satellite Imagery (for the globe)

| Source | Type | URL |
|---|---|---|
| NASA Blue Marble | Equirectangular Earth texture | https://visibleearth.nasa.gov/collection/148/blue-marble |
| Bing Maps Aerial | Cesium ion default | (Cesium ion asset) |
| MapTiler Satellite | High quality satellite | https://www.maptiler.com/ |
| ArcGIS World Imagery | Satellite | https://www.arcgis.com/ |
| Google Photorealistic 3D Tiles | 3D mesh + imagery | https://tile.googleapis.com/v1/3dtiles/root.json |

---

## Access Notes

- **Copernicus:** Requires free registration for an account
- **Argo FTP:** Anonymous access
- **INCOIS LAS:** Web portal, may require registration
- **Cesium ion:** Free tier with access token
- **Google Map Tiles API:** Requires API key, free tier available
- **MapTiler:** Requires API key, free tier available
