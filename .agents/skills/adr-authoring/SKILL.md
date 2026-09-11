---
name: adr-authoring
description: Use when writing or updating an architecture decision record in this repo — `docs/architecture/adr/ADR-00N-*.md` or the ADR index — or when a decision rests on a benchmark that has not run yet. Triggers on "write the ADR", "architecture decision record", "add an ADR", "ADR for", "decision record", "provisional decision", "mark it Proposed", "why did we reject Three.js".
---

Rule: an ADR records one decision, the alternatives rejected and why, and the evidence for both. Status is `Proposed` (or `Proposed — pending benchmark`) until measured numbers exist — never flip to `Accepted` on arithmetic, citations, or a protocol that merely passed review.

## Provisional until measured
Any decision that depends on an unrun benchmark carries `Proposed — pending benchmark` and cites the gate section of the protocol that will settle it (e.g. the chunk protocol's measured-run gate). No gate passes on a blank or UNVERIFIED cell. Scaffold a new one with `scripts/adr-new.sh <slug>`.

## Alternatives carry the reason
List every serious alternative with an explicit reject reason (capability gap, licence, quota cliff, unmaintained), not just the winner. A reject reason is a fact with a source, the same as a supporting claim.

## Evidence table
Every claim gets a row: claim | source URL | access date | VERIFIED/UNVERIFIED. A blocked landing page (403/bot-block) is UNVERIFIED for that URL only — confirm the fact through a registry and cite the registry. Never invent a date, version, or licence.

## Format
`docs/architecture/adr/ADR-00N-<slug>.md`, numbered in creation order, linked from `docs/architecture/adr/README.md`. Sections: Status, Date, Context, Decision, Consequences (positive/negative), Alternatives considered, Evidence, References.
