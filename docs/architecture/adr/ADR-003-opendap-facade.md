# ADR-003: OPeNDAP / OGC Facade — Scope and Non-Claims

**Status:** Accepted
**Date:** 2026-09-10
**Deciders:** Architecture (SIH-OCEAN / VMAX-OCEAN)
**Supersedes:** none
**Related:** `docs/architecture/backend-strategy.md`, `docs/research/d5-externals.md` §3, `problem-statement/PROBLEM-STATEMENT-ANALYSIS.md` (F5, F7)

---

## Context

PS F5 requires a "lightweight REST/OPeNDAP backend" and F7 requires "OGC WMS/WCS, CF Conventions" with national/international portal interop. The locked stack (`backend-strategy.md`) names `xpublish` with an "OPeNDAP plugin (`xpublish-opendap`)". This ADR fixes the scope of the standards facade and pins the exact package facts, because prior docs carried two unverified assumptions:

1. That `xpublish-opendap` is a real, installable package.
2. That standards compliance (OPeNDAP, WMS/WCS) can be claimed from the xpublish path.

Both required verification. A false package name in a build plan is a broken dependency; an unverified compliance claim in a problem-statement response is a credibility failure.

### Constraint that decides the shape

The hot path is Zarr chunks streamed browser-direct (`backend-strategy.md`, strategy A). OPeNDAP/WMS/WCS are **not** the runtime hot path — they are interop surfaces. Any facade must therefore be additive, not on the critical path, and must not block the volumetric runtime.

### Upstream data reality (INCOIS)

`d5-externals.md` §3: INCOIS ERDDAP is live (16 datasets, griddap/tabledap confirmed 200) and is the working INCOIS interop surface. The INCOIS THREDDS catalog returns HTTP 200 but exposes a **single DatasetScan ("Data form LAS") with no per-dataset listing** — the OPeNDAP path on that host is **UNVERIFIED and must not be coded against**. INCOIS TLS needs `-k` (missing intermediate).

---

## Decision

1. **Package truth.** `xpublish-opendap` is a real package (PyPI 0.2.0, repo `xpublish-community/xpublish-opendap`, BSD-3-Clause). The stated premise "real package `xpublish-zarr`, `xpublish-opendap` is FALSE" is **rejected**: both packages exist, are distinct, and are actively maintained. Use the correct plugin for the surface: `xpublish-zarr` for Zarr REST, `xpublish-opendap` for OPeNDAP.

2. **Facade scope — MVP-skip for WMS/WCS.** WMS/WCS are **roadmap-only**. The MVP ships:
   - Zarr chunk streaming (hot path, `xpublish-zarr`).
   - REST metadata/profile endpoints (custom FastAPI over SQLite).
   - INCOIS interop via the **verified ERDDAP endpoints** (`erddap.incois.gov.in`, griddap/tabledap), not via an unverified THREDDS OPeNDAP path.
   
   OPeNDAP stays optional: `xpublish-opendap` may be mounted for portal interop, but it is **not** a launch gate and never the hot path. WMS/WCS are implemented only if a named consumer appears; when reached, prefer `xpublish-wms` (same ecosystem) over standing up a separate GeoServer/MapServer unless raster-tile serving is the actual requirement.

3. **Never claim live compliance.** Any OPeNDAP/WMS/WCS mention in pitch, demo, or docs must be labeled **"roadmap"** or **"interop-ready"** until a live endpoint is demonstrated end-to-end and recorded with an access date. No document may assert "OGC-compliant" or "OPeNDAP-compliant" as a shipped capability. This binds F7 to a labellable roadmap item, per `PROBLEM-STATEMENT-ANALYSIS.md` §62.

4. **Free-only fallback services.** If a separate standards service is ever required, the verified free options are:
   - **OPeNDAP:** THREDDS Data Server (TDS) — free, active (`Unidata/tds`, v5.9 2026-07-14); Hyrax (OPeNDAP Inc) — free, active (`OPENDAP/hyrax`, pushed 2026-05-21); pydap — free, MIT, active (PyPI 3.5.10).
   - **WMS/WCS:** GeoServer — free, active (`geoserver/geoserver`, pushed 2026-09-10); MapServer — free, active (`MapServer/mapserver`, pushed 2026-09-06).
   - Note: `Unidata/thredds` (the old repo) is **archived since 2022-08-08**; the live TDS source is `Unidata/tds`. Do not cite the archived repo.

5. **Gateway.** Any gateway-mediated fetch is authorized only by a non-zero-length check of `$NINEROUTER_KEY`; the key is **never printed**. In this environment the key was absent (length 0), so all verification was direct `curl` / GitHub API / PyPI JSON.

---

## Package-truth table

| Name | PyPI | Latest | Repo | License | Pushed | Status |
|---|---|---|---|---|---|---|
| `xpublish` | 200 | 0.5.2 | `xpublish-community/xpublish` | Apache-2.0 | 2026-09-10 | real, active |
| `xpublish-zarr` | 200 | 0.1.0 | `xpublish-community/xpublish-zarr` | Apache-2.0 | 2026-09-07 | real, active |
| `xpublish-opendap` | 200 | 0.2.0 | `xpublish-community/xpublish-opendap` | BSD-3-Clause | 2026-09-07 | real, active |
| `xpublish-wms` | 200 | 0.13.2 | `xpublish-community/xpublish-wms` | BSD-3-Clause | 2026-08-31 | real, active |
| `xpublish-edr` | 200 | 0.11.1 | `xpublish-community/xpublish-edr` | BSD-3-Clause | 2026-09-08 | real, active |
| `xpublish-ogc-core` | 200 | 0.1.2 | `xpublish-community/xpublish-ogc-core` | Apache-2.0 | 2026-09-07 | real, young |
| `opendap-protocol` | 200 | 1.1.1 | `xpublish-community/opendap-protocol` | — | 2022-02-28 | real; dep of xpublish-opendap; low churn |
| `pydap` | 200 | 3.5.10 | `pydap/pydap` | MIT | 2026-09-08 | real, active |
| `Unidata/tds` | — | v5.9 (2026-07-14) | `Unidata/tds` | — | 2026-09-04 | free, active |
| `Unidata/thredds` | — | — | `Unidata/thredds` | — | 2022-08-08 | **archived** — do not cite |
| `OPENDAP/hyrax` | — | — | `OPENDAP/hyrax` | — | 2026-05-21 | free, active |
| `geoserver/geoserver` | — | — | `geoserver/geoserver` | GPL (NOASSERTION) | 2026-09-10 | free, active |
| `MapServer/mapserver` | — | — | `MapServer/mapserver` | MIT-style (NOASSERTION) | 2026-09-06 | free, active |

Premise correction: `xpublish-opendap` HTTP 200, not 404. Only the *assumption that it does not exist* is false.

---

## Consequences

**Positive**
- Build plan uses real, pinned, permissively-licensed packages; no phantom dependency.
- WMS/WCS kept off the critical path — the Zarr hot path is unaffected by standards work.
- F7 answered with an honest roadmap label rather than an unbacked compliance claim.
- INCOIS interop routed through the one verified surface (ERDDAP); the unverified THREDDS path is explicitly fenced.

**Negative / costs**
- F7 is not "satisfied" at MVP — it is roadmap. This must be stated in the PS response.
- Two OPeNDAP-capable paths (`xpublish-opendap` vs a separate TDS/Hyrax service) create a latent either/or; resolved only when a real external consumer appears. Recorded as an open question, not built.
- `opendap-protocol` (dep of `xpublish-opendap`) last pushed 2022-02-28; low churn is a maintenance risk to watch, not a blocker at MVP.
- INCOIS TLS requires `-k`; any INCOIS integration code carries that caveat.

---

## Alternatives

| Alternative | Why not chosen |
|---|---|
| **Ship WMS/WCS at MVP** | No named consumer; raster-tile service (GeoServer/MapServer) is heavyweight and off the hot path. YAGNI until a portal requires it. |
| **Separate THREDDS/Hyrax service now** | Adds a second data-serving stack and a second auth/TLS surface for a non-hot-path feature. Deferred until a consumer exists. |
| **Claim OGC/OPeNDAP compliance from the xpublish path** | Not demonstrable end-to-end at MVP; would be an unbacked claim. Rejected outright. |
| **Code against INCOIS THREDDS OPeNDAP** | Catalog exposes a single DatasetScan, no per-dataset listing — path UNVERIFIED (`d5-externals.md` §3). Fenced. |
| **Use INCOIS LAS for interop** | GWT app, `getDatasets.do?catid=` ignores catid (md5-identical dump); brittle. ERDDAP preferred (clean griddap/tabledap). |
| **Stand up pydap standalone** | Duplicates `xpublish-opendap` capability; pydap is better used as a library/protocol reference than a parallel server. |
| **Drop standards surface entirely** | F5/F7 are binding PS requirements; a roadmap item preserves intent without overbuilding. |

---

## Evidence

| Claim | Source | Result | Access date |
|---|---|---|---|
| `xpublish-opendap` exists (premise false) | `https://pypi.org/pypi/xpublish-opendap/json` | HTTP 200, v0.2.0, 5 releases | 2026-09-10 |
| `xpublish-zarr` real | `https://pypi.org/pypi/xpublish-zarr/json` | HTTP 200, v0.1.0 | 2026-09-10 |
| `xpublish` core real/active | `https://pypi.org/pypi/xpublish/json`; `https://api.github.com/repos/xpublish-community/xpublish` | 0.5.2, 209★, pushed 2026-09-10, Apache-2.0 | 2026-09-10 |
| `xpublish-opendap` repo/license/activity | `https://api.github.com/repos/xpublish-community/xpublish-opendap` | BSD-3-Clause, pushed 2026-09-07, not archived | 2026-09-10 |
| `xpublish-wms` exists | PyPI JSON + `https://api.github.com/repos/xpublish-community/xpublish-wms` | v0.13.2, 31 releases, pushed 2026-08-31 | 2026-09-10 |
| `xpublish-edr` exists | PyPI JSON + GitHub API | v0.11.1, 28 releases | 2026-09-10 |
| xpublish plugin ecosystem list | `https://xpublish.readthedocs.io/en/latest/ecosystem/index.html` | Plugins: Zarr, OGC EDR, OpenDAP, WMS, Intake — docs confirm | 2026-09-10 |
| TDS free/active | `https://api.github.com/repos/Unidata/tds`; `https://docs.unidata.ucar.edu/tds/current/userguide/index.html` | v5.9 2026-07-14, pushed 2026-09-04, docs HTTP 200 | 2026-09-10 |
| Old THREDDS repo archived | `https://api.github.com/repos/Unidata/thredds` | archived=true, pushed 2022-08-08 | 2026-09-10 |
| Hyrax free/active | `https://api.github.com/repos/OPENDAP/hyrax`; `https://www.opendap.org/software/hyrax-data-server` | pushed 2026-05-21, not archived; page HTTP 200 | 2026-09-10 |
| pydap free/active | `https://pypi.org/pypi/pydap/json`; `https://api.github.com/repos/pydap/pydap` | v3.5.10, MIT, pushed 2026-09-08 | 2026-09-10 |
| GeoServer free/active | `https://api.github.com/repos/geoserver/geoserver`; `https://geoserver.org/` | pushed 2026-09-10, not archived; page HTTP 200 | 2026-09-10 |
| MapServer free/active | `https://api.github.com/repos/MapServer/mapserver`; `https://mapserver.org/` | pushed 2026-09-06, not archived; page HTTP 200 | 2026-09-10 |
| INCOIS ERDDAP interop surface | `d5-externals.md` §3 | live, 16 datasets, griddap/tabledap 200 | 2026-09-10 |
| INCOIS THREDDS OPeNDAP path UNVERIFIED | `d5-externals.md` §3 | catalog 200, single DatasetScan, no per-dataset listing | 2026-09-10 |

**UNVERIFIED / not claimed:** live xpublish+OPeNDAP endpoint demonstration; INCOIS THREDDS per-dataset OPeNDAP; WMS/WCS serving (roadmap only). Gateway not used — `$NINEROUTER_KEY` absent (length 0, never printed); all checks direct.

---

## References

- `docs/architecture/backend-strategy.md` — hybrid Zarr + xpublish recommendation, hot-path constraint.
- `docs/research/d5-externals.md` §3 — INCOIS ERDDAP/THREDDS/LAS findings.
- `problem-statement/PROBLEM-STATEMENT-ANALYSIS.md` — F5 (REST/OPeNDAP), F7 (WMS/WCS, CF), §62 roadmap-only, §67 facade scope note.
- PyPI JSON API — `https://pypi.org/pypi/<name>/json`.
- GitHub REST API — `https://api.github.com/repos/<owner>/<repo>`.
- Xpublish ecosystem docs — `https://xpublish.readthedocs.io/en/latest/ecosystem/index.html`.
- Unidata TDS — `https://docs.unidata.ucar.edu/tds/current/userguide/index.html`; repo `https://github.com/Unidata/tds`.
- OPeNDAP Hyrax — `https://www.opendap.org/software/hyrax-data-server`.
- GeoServer — `https://geoserver.org/`; MapServer — `https://mapserver.org/`.
