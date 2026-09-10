# Architecture Decision Records (ADRs)

Binding, dated decisions for the SIH-OCEAN platform. One file per decision,
immutable once Accepted (supersede with a new ADR rather than editing).

Naming: `ADR-NNN-short-slug.md`. Each ADR carries Status, Date, Context,
Decision, Consequences (positive/negative), Alternatives considered,
Evidence (claim/source/access date), References. Every factual claim links to a
source + access date; unverifiable items are marked `UNVERIFIED`; no estimated
dates.

---

## Index

| ADR | Title | Status | Date |
|---|---|---|---|
| [ADR-001](ADR-001-pynio-drop.md) | Drop PyNIO; ingest NetCDF via xarray + netCDF4 engine | Accepted | 2026-09-10 |
| [ADR-002](ADR-002-cesium-over-three.md) | CesiumJS over Three.js for the 3D globe engine | Accepted | 2026-09-10 |
| [ADR-003](ADR-003-opendap-facade.md) | OPeNDAP / OGC facade — scope and non-claims | Accepted | 2026-09-10 |
| [ADR-004](ADR-004-chunking-strategy.md) | Chunking strategy for GLORYS12 Zarr on object storage | Proposed — pending benchmark | 2026-09-10 |
| [ADR-005](ADR-005-marker-format-cutoff.md) | Marker transport format and cutoff (Argo/Glider markers, ≤5,000) | Proposed — pending benchmark | 2026-09-10 |

---

## Status legend

- **Proposed** — under review, not binding.
- **Accepted** — binding; implementation should follow it.
- **Superseded** — replaced by a later ADR (link the replacement).
- **Deprecated** — no longer relevant, kept for history.
