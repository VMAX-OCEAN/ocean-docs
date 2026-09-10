# ADR-001: Drop PyNIO; ingest NetCDF via xarray + netCDF4 engine

**Status:** Accepted
**Date:** 2026-09-10
**Deciders:** VMAX-OCEAN / SIH-OCEAN architecture
**Supersedes:** PS F3 mention of "PyNIO/xarray backend" for NetCDF ingest

---

## Context

The problem statement (F3: automated NetCDF ingest + new variables/sources with
minimal code change) names **PyNIO/xarray** as the NetCDF ingest backend. The
repo already assumes the drop in practice — `docs/data/glorys12.md` note 3 reads
"PyNIO dropped → xarray/netCDF4", and `docs/research/remaining-research-checklist.md`
lists "PyNIO-drop: one line, xarray netCDF4 backend covers F3" as an open item
requiring a one-line ADR. This ADR closes that item.

PyNIO is a multi-format data I/O package by NCAR/CISL with a NetCDF-style data
model, historically installed via conda-forge. It must be evaluated against the
project's free-only constraint and against the formats F3 actually needs
(NetCDF-4/HDF5, CF conventions, and GRIB2 if the source mix includes it).

## Decision

**Drop PyNIO entirely.** Ingest NetCDF-4/HDF5 with **xarray**, using the
**`netcdf4` engine** as primary and **`h5netcdf`** as fallback. Optionally read
GRIB2 with the **`cfgrib`** engine when a source is GRIB2.

```
xr.open_dataset(path, engine="netcdf4")   # primary; netCDF-4 on HDF5
xr.open_dataset(path, engine="h5netcdf")  # fallback, pure-HDF5 route
xr.open_dataset(path, engine="cfgrib")    # only if source is GRIB2
```

xarray auto-selects backend order `netcdf4 → h5netcdf → scipy → pydap → zarr`
when no engine is passed; the order is overridable via
`xr.set_options(netcdf_engine_order=[...])`. All four packages are free
(Apache-2.0 / MIT / BSD-3-Clause) and actively maintained as of 2026-09-10.

## Consequences

### Positive

- **Free and maintained.** xarray (Apache-2.0), netcdf4-python (MIT), h5netcdf
  (BSD-3-Clause), cfgrib (Apache-2.0) — all OSI permissive, all with commits in
  2026. PyNIO is unmaintained: no code commit since 2024-02-26, conda-forge
  feedstock archived, last binary release 2023-02-12.
- **Capability parity for F3.** netCDF-4 is HDF5-backed; netcdf4-python reads and
  writes netCDF-4 on HDF5 and can create files readable by HDF5 clients; h5netcdf
  is a pure-HDF5 route for the same files. CF decoding (scale/offset, `_FillValue`,
  calendars) is built into xarray `open_dataset` with `decode_cf=True` (default).
- **GRIB2 covered if needed.** xarray reads GRIB via the cfgrib engine, which
  maps GRIB to the NetCDF Common Data Model following CF.
- **One fewer exotic dependency.** xarray is already the project's declared
  backend (`docs/architecture/*`, `docs/data/netcdf-to-zarr.md`), so this adds no
  new abstraction — it removes one.
- **Kills a stale PS claim.** F3 no longer names a dead package in the pipeline
  diagram.

### Negative

- **GRIB2 needs an extra optional dependency** (`cfgrib`, which itself needs
  ecCodes) — not a stdlib/default install. Only relevant if a source is GRIB2;
  the current GLORYS12 PUM/card is NetCDF-4 (CF-1.4/1.6), so this is not on the
  critical path.
- **HDF4 / HDF-EOS / Shapefile formats that PyNIO handled** are not covered by
  the xarray netCDF path. No current F3 source uses these; if one appears, use a
  purpose-built reader rather than resurrecting PyNIO.
- **Minor API divergence** for any code written against PyNIO's NetCDF-style
  interface (`Nio.open_file`). Fresh code should call xarray directly; no
  PyNIO shim is introduced.

## Alternatives considered

| Alternative | Verdict | Reason |
|---|---|---|
| **Keep PyNIO** | Rejected | Maintenance mode since Nov 2020, announced by GeoCAT; NCAR explicitly plans to replace it with xarray et al. No code commit since 2024-02-26. Non-free-only risk avoided; unmaintained dependency. |
| **xarray + netcdf4 engine** | **Chosen (primary)** | Free, maintained, netCDF-4/HDF5, CF decoding built in. Meets F3 for GLORYS12-class NetCDF-4 CF files. |
| **xarray + h5netcdf** | Chosen (fallback) | Free, maintained; pure-HDF5 path when the netCDF-C library stack is unavailable or a file is plain HDF5. |
| **xarray + scipy engine** | Rejected for F3 | netCDF-3 only; cannot read netCDF-4/HDF5. |
| **xarray + cfgrib** | Optional | Only for GRIB2; adds ecCodes. Kept as an option, not the default. |
| **xarray + pydap** | Rejected for local ingest | OPeNDAP remote protocol, not a local file reader; retained conceptually for the OPeNDAP facade item, out of scope here. |
| **Iris** | Rejected | Heavier CF data model; xarray already chosen across the repo. |

## Evidence

Access date 2026-09-10 for every URL. `UNVERIFIED` = fetch failed or mismatch.

| # | Claim | Source | Access date | Result |
|---|---|---|---|---|
| 1 | PyNIO GitHub repo is **not** marked archived | `https://api.github.com/repos/NCAR/pynio` | 2026-09-10 | HTTP 200; `archived=false` |
| 2 | PyNIO repo last code push | `https://api.github.com/repos/NCAR/pynio` | 2026-09-10 | HTTP 200; `pushed_at=2024-02-26T18:09:26Z`; tip commit `f6c19574ac` "Merge pull request #57 from kafitzgerald/maintenance_mode" dated 2024-02-26 |
| 3 | Default branch `develop` last commits add only a maintenance warning | `https://api.github.com/repos/NCAR/pynio/commits?sha=develop&per_page=3` | 2026-09-10 | HTTP 200; `240ed46fe9` 2024-02-22 "Add maintenance mode warning to README.md"; prior substantive commit `2b772b661d` 2019-02-04 "Update version file" |
| 4 | PyNIO placed in maintenance mode as of **November 2020** | repo README rendered on `https://github.com/NCAR/pynio` and raw `https://raw.githubusercontent.com/NCAR/pynio/develop/README.md` | 2026-09-10 | HTTP 200; WARNING block: "PyNIO was placed in maintenance mode as of November of 2020" |
| 5 | NCAR announced maintenance mode and plan to replace PyNIO with xarray et al. | `https://web.archive.org/web/2021/https://geocat.ucar.edu/blog/2020/11/11/November-2020-update` (orig `https://geocat.ucar.edu/blog/2020/11/11/November-2020-update`) | 2026-09-10 | HTTP 200 (Wayback). Full announcement text: "PyNIO and PyNGL: These packages are also in maintenance mode. The GeoCAT team plans to replace their functionality with existing, well-established Python ecosystem packages (e.g. Xarray, MPL, Cartopy, etc.)". Original URL now returns HTTP 404 → cited via Wayback. |
| 6 | PyPI distribution `pynio` has **no downloadable release files** (only version 1.0) | `https://pypi.org/pypi/pynio/json` | 2026-09-10 | HTTP 200; `info.version=1.0`, `num_releases=1`, release `1.0` has no files |
| 7 | Distributable PyNIO binaries live on conda-forge; last release 1.5.5 | `https://api.anaconda.org/package/conda-forge/pynio` | 2026-09-10 | HTTP 200; `latest_version=1.5.5`; latest upload `2023-02-12T12:42:29Z` |
| 8 | conda-forge PyNIO feedstock **is archived** | `https://api.github.com/repos/conda-forge/pynio-feedstock` | 2026-09-10 | HTTP 200; `archived=true`, `pushed_at=2024-03-25T22:45:04Z` |
| 9 | xarray backend order and netCDF engines | `https://docs.xarray.dev/en/stable/user-guide/io.html` | 2026-09-10 | HTTP 200; "backends are tried in order: netcdf4 → h5netcdf → scipy → pydap → zarr"; `netcdf_engine_order` configurable; recommends `engine="netcdf4"` |
| 10 | xarray decodes CF conventions built in | `https://docs.xarray.dev/en/stable/user-guide/io.html` | 2026-09-10 | HTTP 200; `decode_cf=True` (default) applies CF conventions (scale/offset, `_FillValue`, units/calendar) |
| 11 | xarray reads GRIB via cfgrib | `https://docs.xarray.dev/en/stable/user-guide/io.html` | 2026-09-10 | HTTP 200; `xr.open_dataset(..., engine="cfgrib")` |
| 12 | netCDF-4 is implemented on HDF5 | `https://docs.unidata.ucar.edu/netcdf-c/current/file_format_specifications.html` | 2026-09-10 | HTTP 200; "The netCDF-4 format implements and expands the netCDF-3 data model by using an enhanced version of HDF5 as the storage layer" |
| 13 | netcdf4-python reads/writes netCDF-4 (HDF5) and netCDF-3 | `https://unidata.github.io/netcdf4-python/` | 2026-09-10 | HTTP 200; "netCDF version 4 ... implemented on top of HDF5. This module can read and write files in both the new netCDF 4 and the old netCDF 3 format, and can create files that are readable by HDF5 clients" |
| 14 | netcdf4-python is free + maintained; current version 1.7.4 | `https://pypi.org/pypi/netcdf4/json`; `https://api.github.com/repos/Unidata/netcdf4-python` | 2026-09-10 | PyPI HTTP 200, `version=1.7.4`, upload `2026-01-05`; GitHub `license=MIT`, `archived=false`, `pushed_at=2026-08-24` |
| 15 | h5netcdf is free + maintained; current version 1.8.1 | `https://pypi.org/pypi/h5netcdf/json`; `https://api.github.com/repos/h5netcdf/h5netcdf` | 2026-09-10 | PyPI HTTP 200, `version=1.8.1`, upload `2026-01-23`; GitHub `license=BSD-3-Clause`, `archived=false`, `pushed_at=2026-09-07` |
| 16 | cfgrib is free + maintained; current version 0.9.15.1 | `https://pypi.org/pypi/cfgrib/json`; `https://api.github.com/repos/ecmwf/cfgrib` | 2026-09-10 | PyPI HTTP 200, `version=0.9.15.1`, upload `2025-09-30`; GitHub `license=Apache-2.0`, `archived=false`, `pushed_at=2026-07-08` |
| 17 | xarray is free (Apache-2.0) + maintained | `https://api.github.com/repos/pydata/xarray` | 2026-09-10 | HTTP 200; `license=Apache-2.0`, `archived=false`, `pushed_at=2026-09-09T16:26:08Z` |

### Evidence notes

- Claims 4 and 5 are the decisive ones: maintenance mode is **announced**, not
  merely inferred from commit inactivity. Claim 5's original URL now 404s; the
  Wayback capture is cited and the fallback is stated explicitly.
- GitHub's `archived` flag on `NCAR/pynio` is `false` — the repo is *not*
  archived; it is in maintenance mode. Both facts are recorded rather than
  overstating "archived".
- Nothing in the evidence table was inferred: all dates are read from registry
  or API fields, never estimated.
- Access dates reflect the host clock; treat as "accessed 2026-09-10".
- Rate-limit note: Exa MCP returned a free-tier rate-limit error during this
  run; all evidence above was gathered via direct registry/raw-GitHub/docs curl,
  which is the preferred "registry wins over cached HTML" path anyway.

## References

- PyNIO repository — https://github.com/NCAR/pynio
- GeoCAT maintenance announcement — https://geocat.ucar.edu/blog/2020/11/11/November-2020-update
- xarray I/O user guide — https://docs.xarray.dev/en/stable/user-guide/io.html
- netcdf4-python — https://unidata.github.io/netcdf4-python/
- Unidata netCDF file format specs — https://docs.unidata.ucar.edu/netcdf-c/current/file_format_specifications.html
- h5netcdf — https://github.com/h5netcdf/h5netcdf
- cfgrib (ECMWF) — https://github.com/ecmwf/cfgrib
- Repo context — `docs/data/glorys12.md` (note 3), `docs/research/remaining-research-checklist.md`,
  `problem-statement/PROBLEM-STATEMENT-ANALYSIS.md` (F3, line 34)
