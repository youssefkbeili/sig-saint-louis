# CLIENT_INTERACTIVE_MAP_REMARKS_REPORT.md — Interactive Map Remarks + Data Gap Classification

Baseline: `PROJECT_ANALYSIS.md`, `REPLY_CLIENT.md`, `REPLY_CLIENT_REQUEST.md`, `PHASE5_STABILIZATION_REPORT.md`. `DERIVED_GIS_DATA_BASELINE.md` and `INTERNAL_GIS_PRODUCTION_REPORT.md` do not exist in this project — confirmed before starting, not assumed.

## 0. Audit summary (before any change)

- `/carte/` (`app/routers/carte.py` + `app/templates/carte.html`) was a flat, auto-discovered layer registry (`LAYER_GROUPS`) with generic checkbox toggles, a single flat color per layer, and no support for categorized styling, image overlays, filters, or deterministic stacking — unlike `diagnostic_unified.html`, which already had categorized/image-layer support from Wave 2/3.
- The évolution urbaine blue palette (`#93c5fd`/`#2563eb`/`#1e3a5f`) was duplicated in **4 places**: `carte.py`, `diagnostic.py`'s `urbanisation` section, and all 3 communes' `urbain-mobilite` subsection in `commune_diagnostic_data.py` — all needed updating for consistency.
- Occupation du sol 2020, the MNT hillshade, and the CN_5m contours already existed and were validated (Wave 2/Phase 5) — reusable as-is, no new GIS conversion needed.
- Équipements data exists as 40 small GeoJSON files across 5 sectors (santé, éducation, culture, économie, sport), already used by the existing `/equipements/{commune}` pages — but it is a heterogeneous, OSM+official-source merge, not a clean per-commune split (byte-level check: of 398 total features, only 7 are tagged "Gandon", 49 have no commune tag at all, and the rest use 4 different spelling variants of "Saint-Louis"/"Ndiébène Gandiole"). Building a new per-commune filter on top of this inconsistent tagging was judged out of scope and unreliable — see §"Équipements" below for the honest alternative implemented instead.
- The real source field for the flood-risk category is **`Categorie`** (no accent) — the client wrote "Catégorie". The real source field for vulnerability is **`indice`** (lowercase) — the client wrote "Indice". Both were verified at the byte level (not by terminal printing, which is known to garble accented French text in this environment) before writing any code. Source attributes were never renamed; only the UI-facing filter labels use the client's preferred spelling.

---

## Client requests

### Remark 1 — Évolution urbaine

**Status: IMPLEMENTED**

- Red family: `#7f1d1d` (2017, darkest), `#dc2626` (2020, medium), `#fca5a5` (2024, lightest), `fillOpacity: 1` on all three (no transparency used as differentiator) — applied in `carte.py`, `diagnostic.py`, and all 3 communes in `commune_diagnostic_data.py`.
- Deterministic layer order: implemented via dedicated Leaflet panes (`empreinte2017Pane`/`zIndex 403`, `empreinte2020Pane`/402, `empreinte2024Pane`/401) created once at map init and referenced by every empreinte layer's Leaflet constructor (`L.geoJSON`, `L.circleMarker`, `L.imageOverlay` all accept `pane`). This does not depend on fetch order, toggle order, or add sequence — 2017 always renders above 2020, always above 2024.
- Files changed: `app/routers/carte.py`, `app/routers/diagnostic.py`, `app/routers/commune_diagnostic_data.py`, `app/templates/carte.html`, `app/templates/diagnostic_unified.html`, `app/templates/communes/diagnostic_section.html`.

### Remark 2 — New rubriques

**Occupation du sol: IMPLEMENTED** — reuses the existing validated `occupation-du-sol-2020.geojson` (17 categories, `categoryField: "categorie"`), same `categoryColors` dict as `diagnostic.py`'s occupation section (copied, not re-derived, to avoid any risk of re-introducing the double-encoding bug fixed in Phase 5). Public label: "Occupation du sol — 2020", with an explicit coverage note that it is a 2020 dataset, not current land cover.

**Relief: IMPLEMENTED** — reuses the existing hillshade image (`hillshade-mnt.png`, labeled "Relief ombré (MNT)") and the CN_5m contour line layer, both explicitly labeled as derived from/transmitted alongside the client's MNT. Slope, elevation classes, and watershed delineation do **not** yet exist anywhere in the project (confirmed by search) and were **not generated** for this task — generating them was judged out of scope for "add the rubrique" and is recorded below as producible-but-not-yet-produced, per the instruction not to create data just to close a blocker.

**Équipements: IMPLEMENTED, with an honest coverage caveat instead of a per-commune split** — reuses the 5 existing sector files (santé/éducation/culture/économie/sport) via a new on-demand merge endpoint (`GET /carte/data/equipements/{sector}`), so no duplicate GeoJSON was written to disk. Given the underlying data's inconsistent commune tagging (see audit above), this rubrique is presented as one intercommunal layer per sector rather than three fragile per-commune layers built on unreliable tags. Its coverage note states plainly that the dataset is an aggregated, non-commune-structured dataset and that no dedicated Gandon equipment dataset has been supplied — matching the already-tracked gap in `REPLY_CLIENT_REQUEST.md`. No `0 équipement` figure is shown anywhere for Gandon; no per-commune count is fabricated at all for this rubrique.

### Remark 3 — Filters

**Flood risk (Catégorie): IMPLEMENTED** — real field `Categorie`, options exactly `Risque très fort` / `Risque fort` / `Risque moyen` / `Risque faible` (verified byte-for-byte against the source file, independently re-verified by the verification workflow below), plus `Tous`. UI label reads "Catégorie" (client's preferred accented spelling) while the code reads the real unaccented field — a label choice, not a data change.

**Vulnerability (Indice): IMPLEMENTED** — real field `indice` (lowercase, integer-typed), options `1`/`2`/`3`/`4` plus `Tous`.

Both filters: rebuild the Leaflet layer from the already-fetched, never-mutated cached GeoJSON (`layerCache`) on every filter change — no re-fetch, no duplicate layer left on the map (the previous instance is always removed before the filtered one is added), and the filter selection is remembered even if changed while the layer is toggled off.

---

## Data already available

- Occupation du sol 2020 (17 categories, validated encoding).
- MNT-derived hillshade image and CN_5m contours.
- Risque d'inondation (147 features, `Categorie` field, 4 real categories matching the client's request exactly) and Vulnérabilité (1,058 features, `indice` field, values 1–4 matching exactly) — both already existed, now exposed with real filters.
- Équipements: 5 sectors, 40 files, 398 features, already validated and in production use on `/equipements/{commune}`.

## Data produced internally

Nothing new was generated for this task — every new rubrique reuses an already-existing, already-validated file or a lightweight in-memory merge of already-existing files. No SOURCE/METHOD/PARAMETERS record is needed for this task since no new derived layer was created.

The following remain **producible but not yet produced** (would require a dedicated internal-production task, out of scope here):

| Product | Source | Method | Client validation required? |
|---|---|---|---|
| Pente (slope) | `MNT.tif` / `MNT_filled.tif` | Slope raster from DEM, standard GIS operation | No (purely technical, reproducible) |
| Classes d'altitude | `MNT.tif` / `MNT_filled.tif` | Reclassification into elevation bands | No (purely technical, reproducible) |
| Bassins versants | `MNT.tif` / `MNT_filled.tif` | Hydrological flow-direction/accumulation delineation | **Yes** — methodological choices affect the result; already flagged in `REPLY_CLIENT_REQUEST.md` §I, not produced without client sign-off |

## Missing data requiring the client

- Dedicated équipements dataset for Gandon (folder previously transmitted empty — unchanged since `REPLY_CLIENT_REQUEST.md` first flagged it).
- Confirmation of the authoritative empreinte urbaine dataset for 2024/2025 (multiple candidate files coexist — already tracked in `REPLY_CLIENT_REQUEST.md` §J, re-affirmed here since area/feature-count statistics computed from the currently-integrated 2017/2020/2024 layers must be labeled `Calcul technique à partir des couches actuellement intégrées`, not official, until this is resolved).
- Official bassins versants layer, or explicit approval to derive one from the MNT (methodological, not purely technical).

## Data NOT requested anymore because we can produce it

None newly removed from the client's list this round — Occupation du sol, Relief (hillshade/CN_5m), and Équipements were already marked "intégré" in `REPLY_CLIENT_REQUEST.md` before this task; this task exposed them on the interactive map, it didn't newly resolve a client-facing data gap that hadn't already been closed.

---

## Data status classification matrix

| Requirement | Current status | Existing source | Can create internally? | Client needed? |
|---|---|---|---|---|
| Empreinte urbaine 2017 | Available, on map (red, foreground) | `evolution/empreinte-2017.geojson` | — | No |
| Empreinte urbaine 2020 | Available, on map (red, middle) | `evolution/empreinte-2020.geojson` | — | No |
| Empreinte urbaine 2024 | Available, on map (red, background) | `evolution/empreinte-2024.geojson` | — | Confirm authoritative version (2024/2025 ambiguity) |
| Occupation du sol | Available, on map (categorized, 2020) | `occupation-du-sol-2020.geojson` | — | No (a fresher-than-2020 dataset would need the client) |
| Relief | Available, on map (hillshade + CN_5m) | `MNT.tif`/`MNT_filled.tif` (hillshade already derived) | Yes, for slope/elevation classes (not yet produced) | No for what's shown; methodological validation recommended if slope/classes are produced later |
| Équipements Saint-Louis | Available (aggregated, not commune-isolated) | `equipements/{sector}/*.geojson` | — | No |
| Équipements Gandon | Partial/unreliable (7 features loosely tagged; no dedicated dataset) | Same aggregate file set | No — cannot fabricate a dedicated dataset | **Yes** |
| Équipements Ndiébène Gandiol | Available (aggregated, not commune-isolated) | Same aggregate file set | — | No |
| Risque d'inondation | Available, on map, filterable | `risque-inondation.geojson` | — | No |
| Vulnérabilité | Available, on map, filterable | `vulnerabilite.geojson` | — | No |
| Bassins versants | Not available | `MNT.tif` | Yes, methodologically | **Yes** — approval required before deriving |
| Courbes de niveau | Available (5 m, under Relief) | `courbes-niveau-5m.geojson` | — | No |
| Altitude (classes) | Not available | `MNT.tif` | Yes | No, but validation recommended once produced |
| Pente | Not available | `MNT.tif` | Yes | No, but validation recommended once produced |

---

## Tests

**Automated:** 88 PASS / 0 FAIL (76 pre-existing + 12 new, all passing — `pytest tests/ -q`). New tests cover: red palette present / blue absent in `carte.py`'s own layer config (scoped to avoid a false positive from `base.html`'s unrelated Tailwind color scale, which coincidentally reuses the same 3 hex codes for sitewide theming), pane/zIndex presence, new rubriques presence, both filters' real field names and exact client-requested values, the new équipements endpoint (happy path + unknown-sector 404), and red-palette parity on the global Diagnostic urbanisation page and all 3 communes' urbain-mobilite subsections.

**Adversarial verification (independent, automated):** a 4-agent verification pass re-derived every high-risk claim from scratch rather than trusting this report's draft:
1. **Palette & panes** — confirmed exact hex values, `fillOpacity`, pane names/zIndex ordering (2017>2020>2024), and that panes are genuinely wired into every Leaflet constructor across all 3 templates, not just present in the data. One transparency note, not a bug: `#1e3a5f` (one of the "banned" old blue codes) is still used for the unrelated commune-boundary dashed outline in `diagnostic_unified.html` and `communes/diagnostic_section.html` — a different layer entirely (not an empreinte year), kept visually distinct from the new red fills on purpose.
2. **Filter ground truth** — independently re-parsed both source GeoJSON files (byte-level, not printed) and confirmed `carte.py`'s live `LAYER_GROUPS` dict matches exactly: field `Categorie` with all 4 client-requested values and no extras/omissions; field `indice` (int) with values 1–4 and no extras/omissions.
3. **No fabrication / no duplication** — confirmed no new GeoJSON files were written anywhere (MD5 dedup scan across the static data tree found only pre-existing, unrelated duplicate pairs), the équipements endpoint only reads existing files, and the "coverage" text is honest and matches the real (very inconsistent) commune-tagging in the source data. One incidental, harmless finding unrelated to this task: a stray, already-gitignored `.claude/settings.local.json` file sits under `app/static/data/.claude/` (predates this session by several days) — noted, not removed.
4. **Regression & JS syntax** — fresh `pytest` run: 88/88 pass. Rendered `<script>` output for `/carte/`, `/diagnostic?section=urbanisation`, and `/communes/gandon/diagnostic/urbain-mobilite` extracted and checked with `node --check`: valid JavaScript on all 3 pages, no leftover unresolved Jinja syntax.

**Manual browser tests: NOT EXECUTED** — no live browser is available in this environment. The checks above (rendered-HTML string assertions plus independent `node --check` syntax validation of the actual rendered JS) are the closest verification achievable here; they confirm the code that would run in a browser is both present and syntactically valid, but do not confirm pixel-level visual rendering (e.g. that the red gradient reads as "coherent" to a human eye, or that filter `<select>` dropdowns look correct on a real mobile viewport). This is flagged honestly rather than claimed as verified.

## Files changed

- `app/routers/carte.py` (full rewrite: red palette+panes, occupation/relief/équipements groups, filters, new équipements merge endpoint)
- `app/templates/carte.html` (full rewrite: panes, categorized styling+legend, image overlay, filter UI+logic)
- `app/routers/diagnostic.py` (urbanisation layers: blue → red + panes)
- `app/routers/commune_diagnostic_data.py` (urbanisation layers × 3 communes: blue → red + panes)
- `app/templates/diagnostic_unified.html` (generic pane creation/wiring added)
- `app/templates/communes/diagnostic_section.html` (generic pane creation/wiring added)
- `tests/test_routes.py` (12 new targeted tests)
- `REPLY_CLIENT_REQUEST.md` (new §K, recap table row)
- `CLIENT_INTERACTIVE_MAP_REMARKS_REPORT.md` (new, this file)

## Remaining client clarification

- Dedicated équipements dataset for Gandon (existing tracked gap, re-affirmed).
- Authoritative empreinte urbaine 2024/2025 dataset confirmation (existing tracked gap, re-affirmed — directly relevant now that this data is more visually prominent with the new red palette).
- Approval to derive bassins versants from the MNT, if no official layer exists (existing tracked gap, re-affirmed).
- The client's ellipsis ("…") after the 3 named new rubriques was **not** interpreted or expanded — no additional rubrique was invented from it, per instruction.

## Final result

`INTERACTIVE MAP CLIENT REMARKS COMPLETE`
