# In-situ Data Collection — UNRESOLVED (PS link blank)

**Status: UNRESOLVED / BLOCKED.** The SIH26067 problem statement lists a fourth in-situ
dataset but its URL is literally absent at the authority source. No URL is recorded here
because none exists to record. This card documents the blank, the verified candidate
interpretations, and what is already covered elsewhere.

Date: 2026-09-10. Authority: SIH26067 (MoES / INCOIS Ocean Valley).

---

## Card fields (template per `README.md`)

| Field | Value |
|---|---|
| Source URL | **UNKNOWN — blank in PS, not invented** |
| Access date | n/a (no URL to access); authority pages accessed 2026-09-10 |
| sha256 | NONE — no file/source identified |
| License | UNKNOWN |
| bbox | UNKNOWN |
| Variables | UNKNOWN (PS names only "Collection of In-situ Data") |
| Ingest version | v0 — card only, no ingest; source not identified |
| Fixture-use status | **BLOCKED** — must not be cited as a source, demo beat, or fixture |

---

## PS paste text (verbatim)

Authority: `https://sih.gov.in/sih2026PS`, modal `#ViewProblemStatement26067`, field
`Dataset Link` (also mirrored at `https://sih2026.vuce.in/ps/SIH26067`, field
`dataset_link`). Accessed 2026-09-10; both HTTP 200. Text reproduced exactly:

```
The following dataset links are missing and should be included:

a. Numerical Ocean Model Outputs: https://las.incois.gov.in/ & https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description

b. Argo Global Data: ftp://ftp.ifremer.fr/ifremer/argo

c. Glider Data: ftp://ftp.ifremer.fr/ifremer/glider/v2/

d. Collection of In-situ Data: 
```

Notice: item `d. Collection of In-situ Data:` ends at the colon with nothing after it.
This is not a truncation of the local paste — it is the literal, complete authority
value. The same blank appears three times in the raw authority HTML (two commented-out
copies plus one live), and in the independent mirror's embedded `dataset_link` JSON
(`"scraped_at":"2026-09-03"`). The PS opens by declaring the links "missing and should
be included", so item d is an **author-side unfilled placeholder**, not a link that was
dropped in transit.

### Attached-dataset check (negative)

The mirror exposes a "View attached dataset" link to
`https://drive.google.com/file/d/1TrME3MMW-aYaf7KNmDXpwl2CcvLYjp-T/view` (probed
2026-09-10; 1,187,512-byte PDF, 3 pages). The file title is **`SIH26066.pdf`** — it
belongs to SIH26066 (OceanEmbed), not SIH26067. SIH26067 has **no attached dataset**.
The authority modal's `Contact info` field is also blank (`<a href=" ">`).

---

## Candidate interpretations

Ranked by likelihood. "Covered" means another card already documents the source and it
can be used without resolving this blank; it does **not** mean that card is what PS
item d meant. A candidate is not the source until SIH/INCOIS confirms.

| # | Candidate | What it is | Link / evidence | Access 2026-09-10 | Verdict |
|---|---|---|---|---|---|
| C1 | INCOIS Ocean Information Bank — in-situ holdings index | Drifting Buoy (1991–), Moored Buoy/OMNI + RAMA (1997–, T/S to 500 m, currents to 100 m), XBT/XCTD (1990–, viz-only), Current Meter Array (2000–09), Ship AWS (2009–), Wave Rider (2008–), HF Radar (registered), Coastal ADCP (2008–), Tide Gauges (2007–), Tsunami Buoy, Seismic | `https://incois.gov.in/site/dataholdings.jsp` HTTP 200, 44 rows, 46,035 B | 2026-09-10 | **Most likely intended referent.** Already indexed (not fully carded) by `incois-las.md`. Access tiers mixed: only Drifting Buoy + Current Meter Array say "download options"; moored/XBT/tide/ADCP are viz-only or blank. |
| C2 | INCOIS OON map portal | Web map of in-situ layers: Argo, Moored Buoy, AWS, Drifting Buoy, HF Radar, Rama Buoy, BPR, Tide Gauges | `https://incois.gov.in/OON/index.jsp` HTTP 200, 37,396 B | 2026-09-10 | Plausible surface, but it is a visualization shell with no dataset-level URL or download contract. Covered as an index reference only by `incois-las.md`. |
| C3 | MoES-NOAA OMNI-RAMA Joint Data Portal | Moored-buoy network data: OMNI (~12 buoys, NIO/Bay of Bengal + E Arabian Sea, managed by INCOIS), RAMA (NOAA/PMEL) | Info page `https://incois.gov.in/site/datainfo/jointportal.jsp` HTTP 200, 41,604 B; page posts no direct dataset URL, only descriptive text | 2026-09-10 | Plausible, genuinely in-situ, but no downloadable dataset link on the page. Not covered by any existing card. |
| C4 | INCOIS ERDDAP in-situ point data | `Indian_ARGO_Floats` tabledap (T/S profiles) is the only in-situ tabledap among 16 ERDDAP datasets | `https://erddap.incois.gov.in/erddap/tabledap/Indian_ARGO_Floats.html` HTTP 200, 198,732 B | 2026-09-10 | Overlaps Argo, not a distinct "collection". Covered by `incois-las.md`; Argo program detail in `argo-data.md`. |
| C5 | MoES Earth System Science Data Portal (ESSDP) | Cross-institute MoES metadata aggregator (INCOIS, NIOT, NCCR, CMLRE); includes tide gauge, wave rider, etc. | `https://incois.gov.in/essdp/` HTTP 200, 19,053 B | 2026-09-10 | Plausible as a "collection" umbrella. Covered (index-level) by `incois-las.md`. ESSDP "1047 datasets" claim remains UNVERIFIED there. |
| C6 | NOAA Global Drifter Program (GDP) | Global surface drifter dataset (`drifter_6h`, CC0) — an in-situ collection, but **not INCOIS** | `https://www.aoml.noaa.gov/phod/gdp/` HTTP 200, 86,837 B | 2026-09-10 | External, not named in PS, no INCOIS link. Already adopted for the D7 SAR demo beat; do not conflate with item d. Not covered by a data card. |
| C7 | Copernicus Marine in-situ TAC | Global in-situ T/S collections (e.g. `INSITU_GLO_*`) | Copernicus Marine portal (not re-probed this run) | — | External, not named in PS. Possible but unsupported; UNKNOWN. |
| C8 | Argo / Glider themselves | Already listed as items b and c | — | 2026-09-10 | Excluded — d is a *fourth, distinct* item, so re-listing Argo/Glider is wrong. |

### Already covered by other cards (do not duplicate)

- Argo program + GDAC + argopy + SQLite: `argo-data.md`.
- Glider program + Ifremer v2 structure: `glider-data.md`.
- INCOIS ERDDAP/LAS/holdings index, access tiers, and `Indian_ARGO_Floats`: `incois-las.md`.
- Model outputs (items a): `glorys-dataset.md` (GLORYS); LAS side indexed in `incois-las.md`.
- D7 SAR beat's in-situ pairing (GDP `drifter_6h`, HF radar overlay-only):
  `docs/research/remaining-research-checklist.md` § D7-best.

### Genuinely unknown

1. The actual URL the PS author intended for item d — the authority source does not contain it.
2. Whether item d meant the **INCOIS holdings index as a whole** (C1), a **specific**
   INCOIS in-situ platform, the **OMNI-RAMA joint portal** (C3), or an **external**
   aggregator (C5/C6/C7).
3. Whether item d is INCOIS-internal at all; the PS Background only names Argo and
   Gliders as instrument examples.
4. License, bbox, variables, temporal extent, and format for item d — unknowable without
   the URL.
5. Whether viz-only platforms (XBT/XCTD, Moored Buoy, Tide Gauges, Coastal ADCP, HF
   Radar) are in scope for item d, given F6 requires plugin-style ingestion of CTD,
   moorings, HF-radar, and ADCP, yet most carry "No download option" or "Registered
   access" and cannot be an automated fixture.
6. Which entity holds the missing link — SIH organizers, the MoES/INCOIS PS nodal
   officer, or the PS author. Both portal `contact` fields (authority and mirror) are blank.

---

## Why this stays unresolved

`ocean-dataset-provenance` rule: a blank slot in the canonical source list stays
UNKNOWN; a plausible candidate is not a source; only an authoritative link resolves it.
A portal listing many possible datasets (C1) proves options exist, not which one was meant.
No fixture, demo beat, or citation may call any candidate here "the source".

## Recommended next action (to resolve with SIH organizers)

1. **Ask SIH/INCOIS for the missing item-d URL.** Both the authority modal and the mirror
   have an empty contact field; route the request through the SIH 2026 portal contact and
   the MoES/INCOIS problem-statement nodal officer, citing PS ID SIH26067 and quoting the
   verbatim `Dataset Link` block above (the blank is reproducible at
   `https://sih.gov.in/sih2026PS` → modal `#ViewProblemStatement26067`).
2. **Fail closed until answered.** Treat item d as BLOCKED, not as "use the INCOIS
   holdings page". Do not wire any d-specific fixture.
3. **Proceed on the covered sources.** For in-situ co-visualization (F2) the demo can rely
   on the already-carded sources: `Indian_ARGO_Floats` (ERDDAP tabledap) + the Argo/Glider
   GDACs, plus GDP drifters for the SAR beat. These satisfy the PS's named instruments
   (Argo, Glider, CTD/BGC) without needing item d.
4. **If item d is later confirmed as the INCOIS holdings index (C1):** the remaining work
   is to promote `incois-las.md`'s holdings section into a full card, and to record per-
   platform access at that time. Even then, most platforms are viz-only with no download,
   so they remain reference-only, not fixtures.

---

## Assumptions

1. The pasted problem statement and the `sih.gov.in/sih2026PS` modal are authoritative;
   the `sih2026.vuce.in` mirror is corroborating only. Both show item d blank at
   `scraped_at 2026-09-03` / retrieval 2026-09-10.
2. The mirror's attached `SIH26066.pdf` is not evidence for SIH26067 and is deliberately
   not adopted.
3. Candidate rankings reflect source-page content (holdings index C1 is the broadest
   INCOIS in-situ surface) and are reasoning, not provenance.
4. No gateway used — `$NINEROUTER_KEY` absent in tool shell (length 0, never printed);
   direct `curl -k` / Exa used. INCOIS TLS needs `-k` on this network (cert chain).
5. Access date 2026-09-10 applies to every URL probed above.
