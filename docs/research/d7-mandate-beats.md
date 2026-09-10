# D7 — Mandate Beats (Demo Cards + Presets + 90s Scripts)

Date: 2026-09-10. 4 agents, free-only. Each beat: dataset IDs + preset JSON + script naming mandate aloud. `$NINEROUTER_KEY` absent, gateway skipped. Access dates per URL.

## Beat 1 — Hazard assessment: cyclone/storm-surge (Fani 2019 Bay arc)

Story: pre-storm heat (Mar 2019) → wind intensify (Apr–May) → surge landfall Odisha. Mandate: INCOIS SSEWS + TCHP (`https://incois.gov.in/site/services/StormSurge.jsp`, `.../aboutus.jsp`, `.../services/tchp.jsp`, `.../services/osf.jsp`, all 2026-09-10). Tsunami dropped (viz-only, no download). Static SST dropped (ends 2011-10-04).

Datasets: `ascat_daily_datasets` (wind U/V 10m) + `incois_valueadded_products_datasets` (D26/HTCNT/MLD/GEO_U/GEO_V) + `incois_argo_10d_VAM` (TEMP/SAL 5–2000m) + `cmems_mod_glo_phy_my_0.083deg_P1D-m` (thetao/uo/vo/zos/mlotst; product page + PUM `CMEMS-GLO-PUM-001-030.pdf` 2026-09-10) + `Indian_ARGO_Floats` markers. ERDDAP 1-pt CSV no-auth OK: ASCAT `2023-05-01T12Z 10.125N 80.125E 1.7 m/s`; VAP `2019-03-20T00Z 10.5N 80.5E D26 60.24m`. GLORYS free + registration.

```json
{
  "beat": "cyclone-storm-surge-fani-2019",
  "bbox": {"lon_min": 80, "lon_max": 95, "lat_min": 5, "lat_max": 22},
  "depths_m": [5, 25, 50, 100, 150, 200, 300, 500],
  "surface_m": 5,
  "timesteps": ["2019-03-30T00:00:00Z", "2019-04-27T12:00:00Z", "2019-05-02T12:00:00Z", "2019-05-03T12:00:00Z"],
  "layers": {
    "ascat": {"id": "ascat_daily_datasets", "vars": ["eastward_wind", "northward_wind", "wind_speed"], "depth": 10},
    "vap": {"id": "incois_valueadded_products_datasets", "vars": ["D26", "HTCNT", "MLD", "GEO_U", "GEO_V"]},
    "vam": {"id": "incois_argo_10d_VAM", "vars": ["TEMP", "SAL"]},
    "glorys": {"dataset": "cmems_mod_glo_phy_my_0.083deg_P1D-m", "vars": ["thetao", "uo", "vo", "zos", "mlotst"]},
    "floats": {"id": "Indian_ARGO_Floats", "vars": ["latitude", "longitude", "time", "TEMP", "PSAL", "PRES"]}
  },
  "erddap_templates": {
    "ascat_pt": "https://erddap.incois.gov.in/erddap/griddap/ascat_daily_datasets.csv?wind_speed[(2019-05-02T12:00:00Z):1:(2019-05-02T12:00:00Z)][(10.0)][(5.0):1:(22.0)][(80.0):1:(95.0)]",
    "vap_pt": "https://erddap.incois.gov.in/erddap/griddap/incois_valueadded_products_datasets.csv?D26[(2019-03-30T00:00:00Z):1:(2019-03-30T00:00:00Z)][(5.0):1:(22.0)][(80.0):1:(95.0)]"
  }
}
```

Script 90s: 0–15 "INCOIS hazard assessment mandate: storm surge early warning. Bay preset loaded." 15–30 "Heat reservoir: D26 deep, heat content high Mar 30. Cyclone fuel." 30–45 "Wind spins up: ASCAT particles Apr 27–May 2. Same box." 45–60 "Ocean answers: curtain TEMP warm deep, currents + sea level rise." 60–75 "Floats disagree/agree: markers vs model, residual on click." 75–90 "Landfall May 3 Odisha: surge risk zone. Hazard assessment done, no backend."

Cesium: 2D slice VAP D26 / GLORYS thetao 5m; ASCAT U/V particles; VAM TEMP curtain along storm lon; Argo markers + landfall pin.

## Beat 2 — Search-and-rescue: drift (Arabian Sea, Konkan)

Story: missing fishing boat, last-known Konkan coast. GLORYS uo/vo advect particles; GDP drifter grounds truth; SARAT frames ops; HF radar refines coast (registered). Maps PS mandate search-and-rescue.

Datasets: GLORYS product `GLOBAL_MULTIYEAR_PHY_001_030` DOI `10.48670/moi-00021` — `cmems_mod_glo_phy_my_0.083deg_P1D-m` / `P1M-m` / `climatology_P1M-m`; vars `uo`/`vo` eastward/northward m s-1, 1/12°, 50 levels, 1993 onward; free + registration + Licence tab. GDP `drifter_6h` (AOML tabledap, Trajectory, ve/vn) + `drifter_hourly_qc`, CC0-1.0 public domain. HF radar: holdings row real-time 2008–till date registered (no public ID, no fee stated); ESSDP 10 remote sites Chennai + Hyderabad since 2010. NIOT page timeout UNVERIFIED (Exa snapshot only: CODAR SeaSonde, hourly, doi:10.18520/cs/v116/i3/372-378).

```json
{
  "beat": "sar-drift-arabian-sea",
  "bbox": {"west": 68, "south": 12, "east": 74, "north": 20},
  "outerScope": {"west": 60, "south": -5, "east": 100, "north": 30, "note": "repo canonical Indian Ocean subset, glorys-dataset.md"},
  "depths": [0.49],
  "depthNote": "surface level only, SAR drift",
  "timesteps": 5,
  "timeStep": "daily",
  "variables": ["uo", "vo"],
  "overlays": ["gdp-drifter-trajectory", "last-known-marker", "search-cone", "hfradar-slot-registered"]
}
```

Script ~90s: 1. "A fishing boat missed its harbor call off the Konkan coast last night." 2. "Last known position marked here, time-stamped." 3. "INCOIS runs SARAT for exactly this: currents plus winds drive where objects drift." 4. "Our globe loads the same kind of current field: GLORYS reanalysis, surface uo and vo." 5. "Watch particles advect. Flow bends shoreward through the day." 6. "We seed a drift cone from last-known, stepped over five daily timesteps." 7. "Independent check: NOAA drifter tracks crossed this same water. Trajectory overlaid." 8. "Drifter and model agree on direction. Cone narrows, search area shrinks." 9. "Near shore, registered HF radar would tighten this further. Login-gated, shown as overlay slot." 10. "Result: one probable sector, shared as map plus text, SARAT-style." 11. "All data free: Copernicus with free account, NOAA drifters public domain." 12. "That is the beat: currents in, drift out, search area down."

Sources 2026-09-10: Copernicus product + files pages (200s); holdings page (200); ESSDP metadata `3277b2d5-…` (200); AOML ERDDAP index + `drifter_6h.html` (200); `sarat.incois.gov.in/sarat/home.jsp` (200). `ponytail:` preset bbox/depths ceiling now, full column + live 4D later.

## Beat 3 — Fishery advisories: SST front + chlorophyll (PFZ logic)

Story: fishers hunt fronts — warm meets cold, chlorophyll spikes, fish gather. PFZ = SST front + chlorophyll front overlap. Datasets: `NOAA_AVHRR_AMSR_datasets` (sst/anom °C, daily, 2002-06-01–2011-10-04, 3413 steps, lat -29.875–29.875 / lon 20.125–139.875, 0.25°, dims [3413][1][240][480], zlev 0m surface-only) + `IRS_chlorophyll_datasets` (CHLOROPHYLL mg/m³, log 0.03–30, 2003-01-05–2006-03-21, 97 steps, lat 0.023–26.046 / lon 60.010–103.948 uneven, dims [97][2556][4315], surface-only) + PFZ Advisories holdings row (near real-time, 2003–till date, ASCII/JPEG; access blank → restricted-by-default). Joint window lon 60–104 lat 0–25, overlap 2003-01-05–2006-03-21, demo 2005-01-15 (nearest-neighbor snap; IRS cadence UNVERIFIED). Thresholds (PFZ automation paper `http://moeseprints.incois.gov.in/4506`): 0.3 °C (3×3 SST) + 0.5 mg/m³ (5×5 CHL). Curtain = legibility wall 0 to -300m, not data.

```json
{
  "beat": "fishery-advisory",
  "bbox": {"lonMin": 60.0, "lonMax": 104.0, "latMin": 0.0, "latMax": 25.0},
  "depths": [0],
  "timeRange": ["2003-01-05T00:00:00Z", "2006-03-21T12:00:00Z"],
  "demoSample": "2005-01-15T00:00:00Z",
  "datasets": [
    {"id": "NOAA_AVHRR_AMSR_datasets", "vars": ["sst", "anom"], "dims": "[3413][1][240][480]"},
    {"id": "IRS_chlorophyll_datasets", "vars": ["CHLOROPHYLL"], "dims": "[97][2556][4315]"},
    {"id": "PFZ-Advisories-holdings-row", "format": "ASCII/JPEG", "period": "2003-till date"}
  ],
  "erddap": {
    "sst": "https://erddap.incois.gov.in/erddap/griddap/NOAA_AVHRR_AMSR_datasets.nc?sst[(2005-01-15):1:(2005-01-15)][(0.0):1:(0.0)][(0.0):1:(25.0)][(60.0):1:(104.0)]",
    "anom": "https://erddap.incois.gov.in/erddap/griddap/NOAA_AVHRR_AMSR_datasets.nc?anom[(2005-01-15):1:(2005-01-15)][(0.0):1:(0.0)][(0.0):1:(25.0)][(60.0):1:(104.0)]",
    "chl": "https://erddap.incois.gov.in/erddap/griddap/IRS_chlorophyll_datasets.nc?CHLOROPHYLL[(2005-01-15):1:(2005-01-15)][(0.0):1:(25.0)][(60.0):1:(104.0)]"
  }
}
```

Script 90s: 0–15 "Fishers hunt fronts, not water. Warm meets cold, chlorophyll spikes, fish gather." 15–35 "SST layer here, anomaly here. Sharp gradient = thermal front. Same viewport, chlorophyll bloom from IRS-P4 OCM." 35–60 "Overlap thermal + color front. Draw front line. Drop vertical curtain for 3D read. Mark nearest landing center, distance/direction." 60–80 "Same logic as live PFZ text + map advisories, frozen on free archive dates. Live PFZ text format identical." 80–90 "Result: go / no-go zone in under a minute. Next beat: Argo profile check."

Cesium (`ocean-web/src/components/CesiumViewer.tsx`, `src/cesium/config.ts`): SST rectangle 60–104E/0–25N with ERDDAP `.png` texture + diverging palette + °C legend; chlorophyll second rectangle toggleable log stretch; front polyline along max |∇SST| + high-CHL edge; WallGeometry curtain; landing-center points + labels; click → PFZ text snippet. Sources 2026-09-10: both `.das` + `.html` forms; NCEI `gov.noaa.ncdc:C01634` (AVHRR+AMSR, ended Oct 2011 antenna failure); IOCCG OCM sensor (IRS-P4, 1420 km, ~350m, 8 bands); holdings PFZ row; `https://incois.gov.in/MarineFisheries/PfzAdvisory` (SST+chlorophyll method, 586 centers, 14 sectors); PFZ text page (200).

## Beat 4 — Climate monitoring: basin warming vs baseline

Story: monthly vs 1993–2016 baseline + model-observation residual. Datasets: GLORYS `GLOBAL_MULTIYEAR_PHY_001_030` — `P1D-m` daily, `P1M-m` monthly, `climatology_P1M-m` baseline; NOAA OISST V2.1 `ncdcOisst21Agg` DOI `10.25921/RE9P-PT57`; Argo GDAC DOI `10.17882/42182` (`ftp://ftp.ifremer.fr/ifremer/argo`, `https://data-argo.ifremer.fr`). Copernicus free + registration. NOAA pages JS-gated (Exa-verified only, curl empty).

```json
{
  "bbox": {"minLon": 60, "maxLon": 100, "minLat": -5, "maxLat": 30},
  "depth": {"min": 0, "max": 2000, "levels": 50, "var": "thetao"},
  "timesteps": ["2026-01-01", "2026-02-01", "2026-03-01", "2026-04-01", "2026-05-01", "2026-06-01", "2026-07-01", "2026-08-01", "2026-09-01", "2026-10-01", "2026-11-01", "2026-12-01"],
  "datasets": {
    "monthly": "cmems_mod_glo_phy_my_0.083deg_P1M-m",
    "climatology": "cmems_mod_glo_phy_my_0.083deg-climatology_P1M-m",
    "sst": "ncdcOisst21Agg",
    "argo": "doi:10.17882/42182"
  },
  "vars": ["thetao", "so", "uo", "vo", "sst", "anom"],
  "residual": "model-observation",
  "qc": "Argo QC flag 1 only, collocate nearest GLORYS cell + month"
}
```

Script 90s: 0s "Indian Ocean 2026, GLORYS monthly vs 1993-2016 baseline." 15s "Scrub January to December, surface warming peaks pre-monsoon." 30s "Pick Argo float, depth profile 0-2000m." 45s "Dashed model, dots observation, thermocline near 150m." 60s "Anomaly panel: monthly minus climatology." 75s "Residual canonical model minus observation. Sign never flipped." 85s "Warm bias Arabian Sea, use for advisory caveat."

Cesium: ImageryProvider monthly SST/anomaly tiles + time scrub; Argo marker entities; click profile chart; split compare panel, diverging residual palette. Paths: `docs/data/glorys-dataset.md`, `docs/data/data-sources.md`, `docs/data/argo-data.md`. Low-res monthly first; daily full-column later.

## Pitch assembly order

Beats run hazard → SAR → fishery → climate (escalate space→time). Each beat names its mandate aloud in first 15s. Still open: pitch doc assembly, live subset fetch wiring, PFZ text scrape, HF registered pull.
