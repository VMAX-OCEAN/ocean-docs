#!/usr/bin/env bash
# Scaffold an ADR: adr-new.sh <slug>  (ADR_DIR overrides docs/architecture/adr)
set -euo pipefail
slug=${1:?usage: adr-new.sh <slug>}
dir=${ADR_DIR:-docs/architecture/adr}
mkdir -p "$dir"
n=$(ls "$dir" 2>/dev/null | grep -cE '^ADR-[0-9]+-' || true)
id=$(printf 'ADR-%03d' $((n + 1)))
f="$dir/$id-$slug.md"
[ -e "$f" ] && { echo "exists: $f" >&2; exit 1; }
cat > "$f" <<EOF
# $id — <title>

- Status: Proposed
- Date: $(date +%F)

## Context

## Decision

## Consequences

- Positive:
- Negative:

## Alternatives considered

- <alternative> — rejected because ...

## Evidence

| Claim | Source | Access date | Status |
|---|---|---|---|
|  |  | $(date +%F) | VERIFIED |

## References
EOF
echo "$f"
