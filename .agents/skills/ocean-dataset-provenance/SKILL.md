---
name: ocean-dataset-provenance
description: Use when writing or auditing a dataset/source card for an oceanographic product (Copernicus/GLORYS, Argo GDAC, OceanGliders, INCOIS) or when a source's URL, licence, DOI, bbox, size, or access date must be verified. Triggers on "dataset card", "source URL", "verify license", "licence", "DOI", "access date", "sha256", "in-situ blank", "is this the source".
---

Rule: every card carries source URL, access date, sha256, licence, bbox, variables, ingest version, and fixture-use status — and none of those is invented. Missing evidence reads `UNKNOWN`/`NONE` with the search trail; a plausible candidate is not a source.

## Blank or unverifiable source slot
If the canonical source list (the pasted problem statement, the spec) has a blank slot, the card stays BLOCKED/UNKNOWN. Quote what the authority page actually contains, park candidates under "reference — not adopted" with why, and never let a fixture, demo beat, or citation call a candidate "the source". Only an authoritative link resolves the blank.

## Verify against the authority, not a mirror
Fetch the product description, PUM, or DOI landing page directly (curl / MCP fetch) and quote licence text, DOI, bbox, spatial and temporal extent verbatim. One access date per URL, two sources minimum. A portal listing many possible datasets proves choices exist, not which one was meant. Verified portal facts: `references/dataset-portals.md`.

## Argo GDAC index
`ar_index_global_prof.txt.gz` header is `file,date,latitude,longitude,ocean,profiler_type,institution,date_update`; latitude is column 3 and longitude column 4 (0-based 2,3). The float id is path segment 1 (`<dac>/<float>/profiles/<file>`), not segment 2 — using 2 collapses every float into one, which is the tell that the layout is wrong. Use `scripts/argo_bbox_count.py` rather than re-deriving this; sanity-check `unique_floats > 1` before trusting any count.
