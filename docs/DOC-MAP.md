# DOC-MAP — canonical shared-docs layout

Single entry point. Folder READMEs mirror this table; this file wins on conflict.

| # | Folder | Owns | Key files |
|---|---|---|---|
| 00 | `00-problem/` | PS truth + analysis | `PROBLEM-STATEMENT-ANALYSIS.md` (binding R/F IDs, mandates, datasets, open items) |
| — | `RESEARCH-PROGRAM.md` | research program overview + status | D1-D8 map, open items, reading order |
| 01 | `research/` | benchmarks, teardowns, techniques | google-earth, nullschool, platform-comparison, open-source-projects, temperature-rendering, d4-lib-pins, d5-externals, d6-capacity, d7-mandate-beats, remaining-research-checklist |
| 02 | `architecture/` | stack + system + backend + code layout | system-architecture, tech-stack, `TECH-STACK-SUMMARY.md`, backend-strategy, project-structure, `adr/` (5 ADRs) |
| 03 | `visualization/` | render techniques + controls | globe-rendering, day-night-lighting, temperature-overlay, ocean-currents, isosurfaces, colorbar-editor |
| 04 | `data/` | dataset cards, contracts, ingest | `README.md` (placeholder — cards per PS link go here) |
| 05 | `roadmap/` | build order + acceptance | `MILESTONES.md` (M1–M5 + PS checklist) |
| 06 | `performance/` | budgets, latency, tuning | benchmarks, runtime-latency, optimization |
| 07 | `references/` | links library | references.md |
| — | `research/individuals/` | personal workspaces | `prem22k/`, others — never edit another namespace |

## Rules

- `00-problem` = requirement authority. New claims cite R/F IDs or land in personal namespace.
- `docs/data/` cards required before any fixture use: source URL, sha256, license, bbox, variables, assumptions.
- Personal namespaces reference shared contracts, never duplicate them.
- Lakshya deployment docs (`lakshya-research/`) stay top-level until M5 merge.
