# D8 — Residual Sign + Open-Question Gates

Date: 2026-09-10. Blocks M4 (sign) and M5 (feature/GPU/volume claims).

---

## 1. Residual sign — RESOLVED

Canonical authority: `problem-statement/PROBLEM-STATEMENT-ANALYSIS.md:70` — `residual = model − observation`. Never `O − M`.

| File | Was | Now | Verified |
|---|---|---|---|
| `research/individuals/mermaid/06-scientific-analytics/analytics.md:4` | `E(x,y,z,t) = O − M` | `E(x,y,z,t) = M − O` | matches canonical |
| `research/individuals/mermaid/04-interaction-patterns/pattern-library.md:7` | `E = Observation − Model` | `E = Model − Observation` | matches canonical |
| `research/individuals/mermaid/deep-dive-analysis.md:19,23` | `E = Observation - Model` | `E = Model - Observation` | matches canonical |

Status: **all three rewritten to canonical**, observed in working tree 2026-09-10 (mtimes 18:55). Attribution of the edit unknown — not this session. Content verified against the authority line; not reverted.

Cross-check no flipped form remains: `grep -rn "O − M\|O - M\|Observation − Model\|O(x,y,z,t) − M"` over `research/`, `problem-statement/`, `docs/` returns only **descriptions of the rejected form** (comparison docs, ledger citation rules), never an implemented formula.

Panel-code check: app has no residual/compare panel yet (`ocean-web/src/` is globe-only: CesiumViewer, ZoomControls, cesium/*). Zero `O − M` in code. Re-run the grep before M4 ships any panel.

Rule carried: `residual = model − observation`, gated on QC + method labels, provenance (dataset, variable, units, UTC, QC/mode, transform version) on every sample. Anomaly only with stated baseline.

---

## 2. Q7 gate — feature detection (one-feature proof)

Source: mermaid `11-research-questions/questions.md` Q7; pattern-library item 7; experiments P5.

Risk: eddy/front/upwelling detection is claimed but unproven. Detection methods (gradients, vorticity, Okubo-Weiss) exist but no robust validation in this repo.

Gate: before M5 claims feature detection, produce a **one-feature proof**:
1. Pick one feature type (eddy) in one region (Arabian Sea or Bay of Bengal) in one window.
2. Implement a single method (Okubo-Weiss or max-|∇SST| front line) over model output.
3. Cross-check against an independent source (altimetry SLA from CMEMS, or literature-documented eddy).
4. Record: method, threshold, false-positive rate on a second region, and what breaks.
5. Ship only that one feature; no multi-feature claims.

Status: **OPEN** — no proof built. Blocks any F6/feature claim until done.

---

## 3. Q9 gate — GPU vs server split

Source: mermaid `06/analytics.md` AI/GPU policy; `11/questions.md` Q9; `10/experiments.md` P6; `08-rendering-and-performance/metrics`.

Risk: "GPU real-time analytics" is proposed but unbenchmarked. Locked stack prefers server/precomputed isosurface first, browser volume deferred.

Gate: before committing any GPU numerical op (other than already-locked rendering: particle advection, colormap LUT), run the chunk-benchmark + render protocols and compare:
1. Same operation (e.g. isosurface, or a derived field) computed server-side/precomputed vs GPU-side.
2. Record from the D2 protocols: latency, GPU mem, first-render, device (locked Acer A715-79G).
3. Adopt GPU only if measurably better on the locked device and it does not break the free-tier split.

Status: **OPEN** — no benchmark run. GPU analytics stay evaluate-only (mermaid P6 note).

---

## 4. Q10 gate — random-access / volume

Source: mermaid `11/questions.md` Q10; `deep-dive-analysis.md`; volume-subset rule.

Risk: volume claims (full 3D/4D) exceed the random-access path. D6 caps scope: full-cube 0.96 GB never ships.

Gate: before any volume claim:
1. Prove the random-access path on locked laptop: bounded bbox + 3–5 depths + 3–5 timesteps + 1 variable via `ZarrCubeProvider`/`queryData`.
2. Record slice ≤750 ms + cold ≤10 s results (D2 protocols).
3. Volume claims only within proven bounds; full-column render stays deferred.

Status: **OPEN** — protocol written, run owed. Volume stays bounded until measured.

---

## 5. Key + gateway note — RESOLVED 2026-09-10

`$NINEROUTER_KEY` now loads from gitignored `.env` (verify `.gitignore` covers `.env`). It does **not** persist across Bash tool calls — load per call with `set -a; . .env; set +a`, check length only, never print.

Working routes (verified 2026-09-10):
- **Search**: `POST /v1/search`, Bearer, `{"provider":"exa|tavily","query":"...","numResults":N}`. `exa` + `tavily` work. `gemini` 404 (model retired), `searxng` 502 (internal-host block).
- **Fetch**: `POST /v1/web/fetch`, Bearer, `{"provider":"exa|tavily|ollama-cloud","url":"..."}` → `{title, content:{format:"markdown",text}}`.
- `/v1/models` open. `kr/*`, `kc/*`, `nara/*` etc.

Dead routes: `/api/search`, `/api/exa/search`, `/api/tavily/search`, `/api/fetch`, `/api/websearch`, `/api/models` → 401. `/v1/fetch`, `/v1/tools/fetch` → SPA HTML fallback.

Earlier research in this program used direct curl + exa MCP fallback (key was not in the tool shell then). Key never printed/logged/committed. Routing reference: `~/.claude/skills/gateway-search-fetch-routing/references/gateway-routing.md`.

---

## 6. D8 status

| Item | Status |
|---|---|
| Residual sign in 3 mermaid files | **DONE** (observed 2026-09-10) |
| Panel code uses `O − M` | **NONE** (no panel exists); re-grep before M4 |
| Q7 one-feature proof | OPEN |
| Q9 GPU-vs-server benchmark | OPEN |
| Q10 random-access proof | OPEN |

M4 is unblocked on the sign. Q7/Q9/Q10 block M5 feature/GPU/volume claims only.
