# PHASE3_WAVE4A_REPORT.md — Wave 4A: Commune Architecture + Diagnostic

Baseline: `PROJECT_ANALYSIS.md`, `REPLY_CLIENT.md`, `PHASE3_WAVE1_REPORT.md`–`PHASE3_WAVE3_REPORT.md`. Waves 1–3 were not redone. SVD content (4B), PCU/PCUI (4C), and advanced GIS tools (Wave 5) were **not** implemented — only clearly-marked placeholders exist for SVD/PCU. **All original client GIS source files in `reply client/` were only read, never modified.**

`REPLY_CLIENT.md` was corrected per task §0 — only the Gandon/Gandiol population/quartier note was rewritten to record that `Quartier Gandon.shp` contains named quartiers, real population figures, and 3 embedded Ndiébène Gandiol records; nothing else in that file was touched.

---

## Architecture implemented

```
/communes/                                    (existing — unchanged: 3 commune cards)
/communes/{slug}                              (redesigned landing page — see below)
/communes/{slug}/diagnostic                   (NEW — index of 6 subsections, coverage badges)
/communes/{slug}/diagnostic/{section}         (NEW — one of 6 sections, per commune)
/communes/{slug}/svd                          (NEW — placeholder, "Contenu en cours d'intégration")
/communes/{slug}/pcu                          (NEW — placeholder, same)
```
`{section}` ∈ `milieu-physique`, `demographie`, `urbain-mobilite`, `habitat-foncier`, `economie-energie`, `enjeux`.

**Design decision, as invited by the task brief:** routes were added directly onto the existing `communes.py` router (same file, same `router` object, same `/communes` prefix already applied in `app/main.py`) rather than a separate router module, since FastAPI path matching already disambiguates `/communes/{slug}` (exactly one segment) from `/communes/{slug}/diagnostic` (two segments) with zero risk of collision — no routing complexity was needed. The large per-commune content/layer configuration was, however, split into its own file (`app/routers/commune_diagnostic_data.py`) purely to keep `communes.py` readable, mirroring how `diagnostic.py` already keeps its own large `SECTIONS` dict.

The global study-wide `/diagnostic` (all 9 existing + Wave 3's 2 new sections) is completely untouched and remains the default "whole study area" experience, exactly as required. The new commune-level Diagnostic is additional, not a replacement.

---

## Commune pages

### Landing page (`/communes/{slug}`) — redesigned

**Kept:** header (name + population/superficie/densité badges), "Présentation" text, "Chiffres clés" stats, the full "Enjeux principaux" list, the SVD photo gallery, prev/next commune navigation. Nothing was deleted.

**Removed:** the single generic Leaflet map that previously showed a fixed 2–3-layer mix (commune boundary + Saint-Louis quartiers + 2024 urban footprint) regardless of what a visitor actually wanted to see — **this was the literal source of the client's complaint** ("a commune page contains information/maps for all 3 communes" — more precisely, one fixed, un-scoped map bundle reused with only the underlying data swapped per commune, never actually letting the visitor choose what to view). It has been replaced by proper, purpose-built maps inside each Diagnostic subsection.

**Added:** a prominent 3-card navigation block (Diagnostic / SVD / PCU-PCUI) directly under the header, establishing the hierarchy the task asked for before any other content.

### Gandon and Ndiébène Gandiol

Same template, same structural change — no per-commune template duplication. Content differences are entirely data-driven (population figures, enjeux text, and Diagnostic layer availability), matching the existing `COMMUNES` dict pattern already used since Phase 1.

---

## Diagnostic sections

### 1. Milieu physique et risques environnementaux
- **Content used:** géologie (formations that spatially intersect the commune only), zones de conservation (spatially clipped), risques (inondation/vulnérabilité/érosion, clipped), courbes de niveau (both the existing 13,762-feature layer and Wave 2's 5 m layer, clipped), and the Wave 2 MNT hillshade shown as regional context (rasters cannot be meaningfully clipped without real raster processing, which was intentionally not introduced this wave).
- **Layers:** all spatially derived via real `shapely` intersection against `app/static/data/base/limite-communale.geojson` (see "GIS conversions" below) — not filename tricks, not fake scoping.
- **Coverage:** COMPLETE for all 3 communes. Where a géologie formation or `risques-vulnerabilite` clips to zero features for a commune (e.g. Saint-Louis has no dune formations; Ndiébène Gandiol has zero `vulnerabilite` features), that layer is simply **not listed** for that commune — confirmed programmatically before writing the config, not guessed, and explained as a real absence, not a data gap, in each commune's note.

### 2. Démographie
- **Saint-Louis:** existing `population/quartiers-polygones.geojson` (33 quartiers, already carrying a `POPULATION` field, newly noticed this wave). COMPLETE.
- **Gandon:** Wave 3's `peuplement/quartiers-gandon.geojson` (33 named quartiers with real population). COMPLETE.
- **Ndiébène Gandiol:** Wave 3's merged `peuplement/quartiers-gandiol.geojson` (26 quartiers; 7 have no population value in the source). PARTIAL, stated explicitly.
- The 372 unnamed `localités` from Wave 3 are **deliberately excluded** from Démographie, per the explicit instruction not to present them as named villages — they remain only under the global "Peuplement" theme (Wave 3) where their true nature (unnamed regional footprints) is already disclosed.

### 3. Développement urbain et mobilité
- Urbanisation empreintes 2017/2020/2024 — **Wave 1's blue-family, no-transparency styling preserved exactly** (same hex values, same `fillOpacity: 1`), now on commune-clipped subsets.
- Occupation du sol 2020: Gandon and Ndiébène Gandiol use the client's **own** pre-clipped per-commune files (`occupation du sol Gandon.shp`, `Occupation du sol final NG.shp`) — more authoritative than a derived clip. Saint-Louis has no equivalent client file, so its version was derived by clipping the Wave 2 global layer — **labeled as such** in its `coverage` caption, so the two provenances are never conflated.
- Transport layers (up to 7 per commune) — clipped from the existing global transport layers.
- Future autoroute (Wave 3) — included for Gandon only, where it actually exists.
- **A filename/attribute mismatch was found and corrected here, not silently accepted:** the file named `"Zone d'habitation (ZH).shp"` (which sounds like a foncier/zoning layer) actually carries the attribute `Nature = "Empreinte urbaine"` (Gandon) or `NOM = "Empreinte urbaine"` (Gandiol) — i.e., it is factually an urban-footprint dataset, not a housing-zone designation. It was placed under **Développement urbain**, not Habitat et foncier, and this reclassification is explained inline in its own layer label and `coverage` note.
- **Coverage:** COMPLETE for all 3 communes.

### 4. Habitat et foncier
- **Saint-Louis:** MISSING — confirmed, no client file of this kind exists for Saint-Louis at all. Stated plainly, not worked around.
- **Gandon:** `Lotissements autorisés` (874 individual approved plots — a genuine foncier/subdivision dataset, kept as-is) plus ZAPA/ZAPE/ZP. PARTIAL.
- **Ndiébène Gandiol:** ZAPA/ZAPE/ZP/ZPE (no lotissements-equivalent file exists for this commune). PARTIAL.
- **A second filename/attribute mismatch, disclosed rather than hidden:** ZAPA/ZAPE/ZP ("Zone agro-pastorale à priorité agricole/élevage," "Zone pastorale") sound like formal agro-pastoral zoning codes, but their actual attribute in every one of these files is the same `NOM` occupation-du-sol category field used elsewhere in the project (e.g. "Culture maraîchère," "Steppe," "Mangrove") — there is no distinct zoning code anywhere in the data. Every one of these layers is labeled "— voir note" and the section's `note` field explains this plainly. No zoning code was invented to fill the gap.

### 5. Activités économiques et énergie
- Direct reuse of Wave 3's already-commune-scoped, already-coverage-disclosed layers (`economie-gandon`, `energie-gandon`, `gazoduc-gandon` for Gandon; `economie-gandiol`, `usine-zircon-gandiol` for Ndiébène Gandiol). No reconversion needed.
- **Saint-Louis:** MISSING — same as Wave 3, unchanged, still true.
- **Coverage:** PARTIAL for Gandon and Ndiébène Gandiol (isolated project markers, not exhaustive economic coverage — worded identically to Wave 3's own honest framing).

### 6. Enjeux et problématiques
- Reuses `COMMUNES[slug]["enjeux"]` verbatim — the same already-vetted list already shown on the (now-shorter) landing page. No new planning conclusions were written; nothing was derived from GIS layers alone, per the explicit instruction. COMPLETE for all 3 (this content already existed and was already trusted).

---

## Data coverage matrix

| Diagnostic area | Saint-Louis | Gandon | Ndiébène Gandiol |
|---|---|---|---|
| Milieu physique et risques | COMPLETE | COMPLETE | COMPLETE |
| Démographie | COMPLETE | COMPLETE | PARTIAL (7/26 quartiers missing population) |
| Développement urbain et mobilité | COMPLETE | COMPLETE | COMPLETE |
| Habitat et foncier | MISSING | PARTIAL | PARTIAL |
| Activités économiques et énergie | MISSING | PARTIAL | PARTIAL |
| Enjeux et problématiques | COMPLETE | COMPLETE | COMPLETE |
| Topographie/MNT (within Milieu physique) | GLOBAL CONTEXT (hillshade only — raster not clipped) | GLOBAL CONTEXT (same) | GLOBAL CONTEXT (same) |

---

## GIS conversions (this wave)

All clipping was done with `shapely.intersection()` against the 3 polygons in `app/static/data/base/limite-communale.geojson` — no PostGIS, no new backend service, matching the "simplest safe approach" instruction.

| Layer group | Source | Method | Communes | Notes |
|---|---|---|---|---|
| Géologie (8 layers) | Existing global GeoJSON | Clip | All 3 | Several formations clip to 0 features for Saint-Louis/Gandiol — correctly omitted, not padded |
| Zones de conservation | Wave 3 global (44 features) | Clip | All 3 | Gives the per-commune attribution Wave 3 couldn't determine from attributes alone (13/23/15 features respectively) |
| Risques (3 layers) | Existing global GeoJSON | Clip | All 3 | `risques-vulnerabilite` clips to 0 for Ndiébène Gandiol |
| Topographie (2 layers) | Existing global + Wave 2 | Clip | All 3 | Gandon's clipped files are the largest (2.1 MB + 2.7 MB) — Gandon is by far the largest commune by area |
| Urbanisation empreintes + lotissements | Wave 1-styled global GeoJSON | Clip | All 3 | Wave 1 colors/opacity preserved exactly |
| Transport (7 layers) | Existing global GeoJSON | Clip | All 3 | Some route types clip to 0 for smaller communes |
| Occupation du sol 2020 | Wave 2 global (Saint-Louis: clipped here); client's own Gandon/Gandiol per-commune files (reused, not reclipped) | Clip (SL) / direct (Gandon, Gandiol) | All 3 | Provenance difference explicitly labeled |
| Habitat/foncier (Lotissements, ZAPA, ZAPE, ZP, ZPE) | Client's own per-commune shapefiles | Direct convert (already commune-scoped) + simplify | Gandon, Gandiol | Simplified (~0.0001° ≈ 11 m tolerance, same as Wave 2's approved tolerance) — 81–87% size reduction, no meaningful accuracy loss |

**Total new/generated files this wave:** 88 GeoJSON files under `app/static/data/communes/{slug}/` (~10.4 MB combined across all 3 communes — Saint-Louis 1.8 MB, Gandon 6.7 MB, Gandiol 1.9 MB), none loaded except when its own Diagnostic subsection page is opened (theme-scoped lazy loading, matching the site's existing pattern — nothing was added to the homepage or to `/carte/`).

**Validation performed:** every generated/clipped file was checked for geometry validity; 3 minor self-intersections (2 in the habitat layers, reintroduced by simplification, matching a pattern already seen and fixed in Waves 2–3) were repaired with `buffer(0)` before shipping. Final invalid-geometry count across all 88 files: **0**.

---

## UX decisions

- **Navigation:** every commune diagnostic page shows a breadcrumb (Accueil › Communes › {commune} › Diagnostic › {section}) plus a horizontally-scrollable section-tab row (mobile-safe) plus prev/next links — three redundant ways to always know commune + branch + subsection, per the task's explicit requirement.
- **Coverage badges:** each Diagnostic subsection card and page carries a colored badge (green=Complete, amber=Partial, blue=Global context, gray=Missing) so a user never has to infer completeness from silence.
- **No empty controls:** sections with `coverage: MISSING` (Saint-Louis's habitat-foncier and économie-énergie) show a plain, honest message instead of an empty map or empty layer list.
- **SVD/PCU exposed, but only as placeholders:** the task allowed choosing not to expose these branches at all if doing so would mislead. The chosen middle ground: the tabs/cards are visible (so the *information architecture* — the point of Wave 4A — is fully legible) but every SVD/PCU page shows a single, honest "Contenu en cours d'intégration" state and nothing else. No fake report text, GIS layers, PIP data, or règlement content was created.

## Shared components introduced

- **One** new template, `communes/diagnostic_section.html`, serves all 18 commune×section combinations (data-driven, mirroring the existing `diagnostic_unified.html` pattern) — not 18 separate files.
- **One** new template, `communes/diagnostic_index.html`, serves all 3 communes' overview pages.
- **One** new template, `communes/branch_placeholder.html`, serves both SVD and PCU placeholders for all 3 communes (6 pages, 1 file).
- **Explicit decision against a deeper refactor:** `diagnostic_section.html`'s map-rendering JS is self-contained rather than extracted into a shared include with the already-shipped `diagnostic_unified.html`. Extracting a shared partial was considered (and would remove some code similarity) but was judged to add regression risk to Waves 1–3's already-verified code for a modest gain, which the task explicitly discouraged ("do NOT perform a full frontend refactor"). This is documented here as a deliberate tradeoff, not an oversight.

---

## Tests

| Test | Result |
|---|---|
| All 3 commune landing pages (`/communes/{slug}`) | PASS (200), 3-way nav cards confirmed present, old unscoped map confirmed removed |
| All 3 `/communes/{slug}/diagnostic` index pages | PASS (200) — caught and fixed a 500 error here first (see Problems below) |
| All 18 `/communes/{slug}/diagnostic/{section}` combinations | PASS (200) after the fix |
| All 6 `/communes/{slug}/svd` and `/pcu` placeholders | PASS (200), no fabricated content confirmed by direct inspection |
| Reclassified "Zone d'habitation" layer appears under Développement urbain, not Habitat et foncier | PASS — confirmed by direct content search in both pages |
| Geometry validity across all 88 new files | PASS — 0 invalid after repair |
| Regression: `/`, `/projet`, `/ressources`, `/carte/`, `/communes/` | PASS |
| Regression: all 11 global `/diagnostic` sections (incl. Wave 3's Peuplement/Économie-Énergie) | PASS |
| Regression: `/equipements/{saint-louis,gandon,gandiol}` | PASS |
| Regression: `/risques/{inondation,vulnerabilite,erosion}` | PASS |
| Server log across every request in this wave | Clean after the fix — zero unhandled errors |
| `app.main:app` import | Clean |

No headless browser was available; verification was via server-rendered HTML/JSON inspection, consistent with every prior wave.

---

## Problems / missing data (not hidden)

- **A real bug was caught during testing, not before shipping:** the "Enjeux et problématiques" section was completely missing from the initial data config (`commune_diagnostic_data.py` only had 5 of 6 sections), causing a 500 error on every commune's diagnostic index and every commune's `/diagnostic/enjeux` page. Fixed by building that section's data on the fly from the existing `COMMUNES[slug]["enjeux"]` list (avoiding a circular import between `communes.py` and `commune_diagnostic_data.py`), then re-tested clean across all 21 combinations (3 index pages + 18 sections).
- Saint-Louis has zero habitat/foncier and zero économie/énergie data — stated plainly in the UI, not worked around.
- The ZAPA/ZAPE/ZP filename-vs-attribute mismatch (documented above) means these 3 layer types don't actually carry the zoning information their names imply — the client may want to supply real zoning codes for these later.
- Ndiébène Gandiol: 7 of 26 quartiers have no population figure in the source data.
- Occupation du sol 2020's regional (larger-than-3-communes) extent, discovered in Wave 3, is why the Saint-Louis version required a derived clip rather than a client-supplied one — documented for transparency, not hidden behind a uniform label.

---

## Files changed

**Modified:**
- `app/routers/communes.py` — 5 new routes, new imports, `_enjeux_section_data`/`_commune_sections` helpers
- `app/templates/commune_detail.html` — redesigned (nav cards added, old unscoped map removed, everything else preserved)
- `REPLY_CLIENT.md` — one factual correction (Gandon/Gandiol population), nothing else

**New:**
- `app/routers/commune_diagnostic_data.py`
- `app/templates/communes/diagnostic_index.html`
- `app/templates/communes/diagnostic_section.html`
- `app/templates/communes/branch_placeholder.html`
- 88 new files under `app/static/data/communes/{saint-louis,gandon,gandiole}/*.geojson`
- `PHASE3_WAVE4A_REPORT.md` (this file)

No files under `reply client/` were modified. No orphaned templates were touched. No PostGIS, authentication, or admin system was introduced.

---

## Deferred to Wave 4B (SVD)

- Extraction of real content from the 3 large SVD `.docx` reports (Saint-Louis, Gandon, Gandiole — 50–63 MB each, still unopened).
- Vision territoriale et principes directeurs, Axes stratégiques, Programmes de développement — per commune.
- Any real replacement of the current `Contenu en cours d'intégration` placeholder.

## Deferred to Wave 4C (PCU/PCUI)

- Rapport de présentation, Zonage (interactive), PIP, Règlement d'urbanisme, Évaluation environnementale stratégique, Atlas cartographique — all still MISSING/not fabricated, per instruction.

## Also still deferred (Wave 5+, unchanged from earlier waves)

- Bassins versants (still blocked on missing data).
- Buffer/query/spatial-analysis/export tooling, PostGIS, authentication, Wolof translation, PWA conversion — none started, per explicit instruction.

---

## Result

`WAVE 4A COMPLETE — READY FOR REVIEW`

The commune information architecture (Diagnostic → SVD → PCU/PCUI) is live for all 3 communes, with the Diagnostic branch fully implemented across all 6 subsections using only real, verified, and — where global data had to be reused — genuinely spatially-clipped, commune-specific data. The client's core complaint (one undifferentiated 3-commune map reused everywhere) is directly addressed: every commune's Diagnostic pages now show only what actually applies to that commune, with honest coverage disclosure wherever data is incomplete. Existing URLs and all prior-wave functionality remain intact. Stopping here per instructions; not proceeding to Wave 4B automatically.
