# Google-earth fly-to (2026-09-09, strengthened 07)

Idea: search location → fly-to → zoom 3D → relevant filters.

Verified 2026-09-09: MyOcean Pro has NO geocoder (❌ UX table, [features](https://help.marine.copernicus.eu/en/articles/4794675-main-features-of-myocean-pro-viewer)). Fly-to is differentiation, not parity — keep in pitch.

## Fit

- Strong hook for outreach + opening 12s. PS wants rapid intuitive understanding.
- Cheap with `MapLibre flyTo`, easier globe with Cesium.

## Risks

- Current stack lacks globe + geocoder. True globe needs Cesium or MapLibre globe mode + ADR (PS names Cesium).
- Geocoder returns place, not feature. Needs bbox → catalogue query (`/v1/catalog/datasets?bbox=`), else empty view.
- Fly animation races chunk fetch → jank. Need abort + preload low-res slice first.
- Offline judging kills tiles + geocoder. Need pre-warmed demo locations.

## Lazier path

Preset `flyTo` buttons (`Bay Bengal eddy 2026-08-10`, `Arabian Sea`, …) replace geocoder + globe. Same demo effect, one config line, no dependency.

## Order

Presets now. Cesium globe + search only after M1-M3 proven, behind ADR.

## Open thresholds

- Observations GeoJSON vs Arrow cutoff.
- Chunk hypothesis benchmark + reference device.
- Cold ≤10s / slice ≤750ms / 30 FPS + ≤5000 markers on locked laptop.
