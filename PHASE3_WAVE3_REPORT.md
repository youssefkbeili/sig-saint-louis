# PHASE3_WAVE3_REPORT.md — Wave 3: New GIS Themes

Baseline: `PROJECT_ANALYSIS.md`, `REPLY_CLIENT.md`, `PHASE3_WAVE1_REPORT.md`, `PHASE3_WAVE2_REPORT.md`. Waves 1–2 were not redone. Commune architecture (Wave 4) and advanced GIS analysis (Wave 5) were not started. **All original client GIS source files in `reply client/` were only read, never modified.**

`REPLY_CLIENT.md` was corrected per task §0 — only the Occupation du sol 2020 extent statement was rewritten (now reflects the true, larger-than-3-communes extent verified in Wave 2); every other technical finding in that file is untouched.

---

## A discovery that reshapes this report: two distinct, unrelated encoding problems in the same delivery

Before converting anything, every source file's *actual* text encoding was verified byte-for-byte (not assumed from its `.cpg` file, and not trusted from printed terminal output — see below). Two independent problems were found:

1. **The already-known bug** (Wave 2, `PROJECT_ANALYSIS.md` R5 family): `Occupation du sol 2020.shp` and its 2 source national tiles declare UTF-8 in their `.cpg` but are actually cp1252. This is still the case and was handled the same way as before.
2. **A new, opposite-direction mistake made and caught during this wave**: every *other* Wave 3 source file (`localite.shp`, `Quartier Gandon.shp`, the Gandiol `Quartiers.shp`, and all the économie/énergie project shapefiles) is **genuinely, correctly UTF-8 encoded**, matching their `.cpg`. The first conversion pass wrongly applied the same `cp1252` override to all of them (extrapolating from problem #1), which **double-mangled** already-correct text (e.g. "Ndiébène Gandiol" → corrupted double-encoded bytes). This was caught by inspecting raw `.dbf` bytes directly (`\xc3\xa9` = correct UTF-8 "é") before shipping, and every affected file was reconverted with the correct per-file encoding.

**A related tooling pitfall, documented so it doesn't cost time again**: this session's bash/Windows-console pipeline visually garbles some correctly-encoded UTF-8 text when printed to the terminal (e.g., a perfectly correct "à" byte sequence prints as "�"). This looked exactly like real corruption and briefly caused a false read of the encoding problem in the wrong direction. The only reliable verification methods used from that point on were **raw byte inspection** (`open(path, 'rb').read()`) and **reading the actual output file directly** — never trusting a terminal `print()` of French text in this environment.

A third, smaller issue was found and fixed the same way: `Quartier Gandon.shp`'s `Commune` field is Unicode-NFD-normalized while ordinary Python string literals are NFC, so a naive `==` comparison against a typed-out commune name silently returns zero matches even on correctly-decoded text. Fixed by using `unicodedata.normalize("NFC", ...)` on every text property during conversion, and by writing comparisons that don't depend on retyping the accented literal (`!= "Gandon"` instead of `== "Ndiébène Gandiol"`).

---

## Themes implemented

### 1. Peuplement (new section, placed before Population)

| | |
|---|---|
| Client requirement | Quartiers + villages/localités, positioned before Population in the diagnostic nav; keep peuplement (spatial structure) distinct from population (demographic stats) |
| Source datasets | `localite.shp` (372, whole region); `Nouveau dossier/Gandon/Quartier Gandon.shp` (36, mixed communes); `Nouveau dossier/Ndiebene Gandiol/Quartiers.shp` (23); existing `population/quartiers-polygones.geojson` (33, Saint-Louis, reused unchanged) |
| Geographic scope | See coverage matrix below — each layer's true scope is stated in its own UI caption |
| Files generated | `app/static/data/peuplement/localites.geojson`, `.../quartiers-gandon.geojson`, `.../quartiers-gandiol.geojson` |
| Application files changed | `app/routers/diagnostic.py` (new `peuplement` section + `SECTION_ORDER`), `app/templates/diagnostic_unified.html` (coverage-caption UI) |

**Important discovery, correcting `REPLY_CLIENT.md`'s "MISSING" classification:** `Quartier Gandon.shp` was expected to be Gandon-only and unnamed. Inspection found it actually contains **36 named quartiers with real population figures** and, unexpectedly, **3 of those 36 belong to Ndiébène Gandiol, not Gandon** (`Mbambara`, `Gantour`, `Keur Barka` — none of which duplicate the separate 23-feature Gandiol file, confirmed by name comparison). Population-by-quartier for Gandon (33 quartiers) and most of Gandiol (23+3=26 quartiers) **is available**, contrary to `REPLY_CLIENT.md`'s prior "MISSING" note — that note is now outdated for this specific data, though it was accurate at the time it was written (the file's true content wasn't inspected until this wave). Per the task's instruction to keep Peuplement and Population conceptually distinct, this population figure is shown as a popup attribute on each quartier (since it's a real, connected value on that exact feature) but was **not** used to alter the separate "Population" theme's own aggregate stats/charts — that reconciliation is deferred, not done here.

`localite.shp`'s 372 footprints still have **no individual village name** anywhere in the source (confirmed again this wave) — displayed as an unnamed "Localité" category, not fabricated.

### 2. Zones de conservation

| | |
|---|---|
| Client requirement | Integrate `zone de conservation.shp` (44 features: 43 Protection Naturel, 1 Protection Patrimoniel) with a clear legend |
| Source dataset | `zone de conservation.shp`, EPSG:32628, field `Categorie` (plain ASCII values, no accents, no encoding ambiguity) |
| Geographic scope | Bounding box spans roughly the same longitude/latitude range as the full study zone, but **no `Commune` attribute exists on this file** to attribute individual features to Saint-Louis/Gandon/Gandiol — stated honestly as "whole-zone scope, per-commune breakdown not determinable without a spatial join," which this wave does not perform |
| Placement decision | Added as an additional layer inside the existing **"Géologie"** theme (milieu physique), rather than a new top-level theme — closest existing architectural fit for "natural/physical characteristics of the territory," per the task's explicit allowance to use "a dedicated conservation layer" only if it doesn't require a major new system. A brand-new top-level theme for one 44-feature layer was judged unnecessary complexity. |
| Files generated | `app/static/data/conservation/zones-conservation.geojson` |
| Application files changed | `app/routers/diagnostic.py` (`geologie` section) |

Categorized styling + a 2-item legend (Protection Naturel / Protection Patrimoniel) uses the same mechanism built in Wave 2 for Occupation du sol 2020 — no new JS was needed.

### 3. Énergie (Gandon only)

| | |
|---|---|
| Client requirement | Integrate available energy infrastructure without implying coverage that doesn't exist |
| Source datasets | `Nouvelle Centrale a Gaz.shp` (1), `Substation Senelec.shp` (1), `Tracé Gazoduc RGS.shp` (1, KML-derived) — all Gandon only |
| Geographic scope | **Gandon only** — no Saint-Louis or Ndiébène Gandiol energy data exists anywhere in the delivery, confirmed again this wave |
| Files generated | `app/static/data/energie/energie-gandon.geojson` (2 points), `app/static/data/energie/gazoduc-gandon.geojson` (1 line) |
| Application files changed | `app/routers/diagnostic.py` (`economie_energie` section) |

The gas-pipeline KML import carried 11 KML-artifact fields (`descriptio`, `timestamp`, `altitudeMo`, `tessellate`, `extrude`, `visibility`, `drawOrder`, `icon`, etc.) — all dropped, keeping only the one meaningful field (`Name` → `nom`), per the instruction not to expose meaningless GIS fields in popups.

### 4. Activités économiques

| | |
|---|---|
| Client requirement | Integrate verified economic/project layers, correct popups, no fake Saint-Louis coverage |
| Source datasets (Gandon) | `Projets Économiques.shp` (2) + `Projets Immobiliers, Hôteliers.shp` (2) = 4 |
| Source datasets (Gandiol) | `Projets Économiques, Agricoles & Agro-industriels.shp` (7) + `Projets Divers.shp` (2) + `Projets Équipements & Services...shp` (4) = 13, plus `Usine d'exploitation du Zircon CEN_HMC.shp` (1 point) |
| **Duplicate found and avoided** | `Future Zone Economique Specialisée.shp` (1 feature) and `ZES.shp` (1 feature) are **already merged** into `Projets Économiques.shp` (confirmed via that file's own `layer`/`path` provenance attributes, which name those two files as the source of its 2 records). Using the 2 standalone files *in addition to* `Projets Économiques.shp` would have double-counted them — only `Projets Économiques.shp` was used. |
| **Data-quality issue found, not silently fixed** | Within `Projets Économiques.shp`, both merged records carry the identical `Name` value "Future Zone Economique Specialisée" — the `ZES.shp`-sourced record's name field was apparently lost or mis-populated during the client's own merge. Per instruction not to silently correct client terminology, this duplicate label was kept as-is in the popup; documented here instead. |
| Geographic scope | Gandon layer = Gandon only; Gandiol layers = Ndiébène Gandiol only; **no Saint-Louis coverage exists** |
| Files generated | `app/static/data/economie/economie-gandon.geojson` (4), `.../economie-gandiol.geojson` (13), `.../usine-zircon-gandiol.geojson` (1) |
| Application files changed | `app/routers/diagnostic.py` (`economie_energie` section) |

Popups show only `nom` (the project/site name) — internal fields (`OBJECTID`, `Shape_Leng`, `Shape_Area`, `begin`, `end`, `layer`, `path`) were dropped during conversion.

### 5. Corridors / infrastructures structurantes

| | |
|---|---|
| Client requirement | Only classify something as a corridor if the data or terminology supports it |
| Classified as corridors | `Future autoroute.shp` (1 polygon — a planned highway right-of-way, genuinely corridor-shaped) and `Tracé Gazoduc RGS.shp` (cross-listed — it's fundamentally an energy asset, but its linear "corridor" character is also explicit in the task's own example list, so it's labeled "Corridor énergétique" in the économie/énergie theme rather than duplicated as a second file) |
| **Not classified as a corridor** | `Boucle de Gandiolais.shp` — still broken in both delivered copies (confirmed unusable again this wave, matching `REPLY_CLIENT.md`), so it was excluded rather than guessed at |
| Geographic scope | `Future autoroute`: Gandon area, single projected route segment. Gazoduc: Gandon only. |
| Files generated | `app/static/data/economie/future-autoroute.geojson` |
| Application files changed | `app/routers/diagnostic.py` (`economie_energie` section) |

---

## Dataset coverage matrix

| Theme / Layer | Saint-Louis | Gandon | Ndiébène Gandiol | Global (whole region) |
|---|---|---|---|---|
| Quartiers (named, with population) | AVAILABLE (33, polygons) | AVAILABLE (33, points) | AVAILABLE (26, points; 3 embedded in the Gandon file + 23 standalone) | NOT APPLICABLE |
| Localités / villages | NOT APPLICABLE (folded into the regional layer) | NOT APPLICABLE | NOT APPLICABLE | AVAILABLE (372, unnamed) |
| Zones de conservation | PARTIAL (bbox overlaps, no per-commune attribution possible) | PARTIAL (same) | PARTIAL (same) | AVAILABLE (44 total, commune breakdown not determinable) |
| Énergie | MISSING | AVAILABLE (3 features: 2 point + 1 line) | MISSING | NOT APPLICABLE |
| Activités économiques | MISSING | AVAILABLE (4 features) | AVAILABLE (14 features: 13 + 1 usine) | NOT APPLICABLE |
| Corridors | MISSING | AVAILABLE (2: gazoduc + future autoroute) | MISSING | NOT APPLICABLE |
| Bassins versants | MISSING | MISSING | MISSING | MISSING (blocked, see below) |

---

## GIS conversions

| Asset | Source CRS | Output CRS | Feature count | Original size | Output size | Optimization |
|---|---|---|---|---|---|---|
| `localites.geojson` | EPSG:32628 | EPSG:4326 | 372 (unchanged) | part of shared 9.3MB delivery folder | 1.18 MB | Coordinate rounding to 6 decimals only (no simplification needed at this size); 4 minor self-intersections repaired with `buffer(0)` before **and** after reprojection (rounding had reintroduced them once) |
| `quartiers-gandon.geojson` | EPSG:32628 | EPSG:4326 | 33 | negligible (points) | 5.2 KB | None needed |
| `quartiers-gandiol.geojson` | EPSG:32628 | EPSG:4326 | 26 (3+23 merged, confirmed no duplicate names) | negligible | 4.3 KB | None needed; one trailing-newline artifact in a source name field ("Tassinère\n") stripped as a display-hygiene cleanup |
| `zones-conservation.geojson` | EPSG:32628 | EPSG:4326 | 44 (unchanged) | small | 198 KB | None needed |
| `energie-gandon.geojson` | EPSG:32628 | EPSG:4326 | 2 | negligible | 0.5 KB | None needed |
| `gazoduc-gandon.geojson` | EPSG:32628 (3D/KML-derived, Z dropped) | EPSG:4326 | 1 | negligible | 0.5 KB | 11 KML-artifact fields dropped |
| `economie-gandon.geojson` | EPSG:32628 | EPSG:4326 | 4 | negligible | 1.5 KB | None needed |
| `economie-gandiol.geojson` | EPSG:32628 | EPSG:4326 | 13 | negligible | 3.5 KB | None needed |
| `usine-zircon-gandiol.geojson` | EPSG:32628 | EPSG:4326 | 1 | negligible | 0.2 KB | None needed |
| `future-autoroute.geojson` | EPSG:32628 | EPSG:4326 | 1 | negligible | 3.7 KB | None needed |

None of these needed simplification — all are small enough (largest is 1.18 MB) that further reduction wasn't warranted; every one is well under the site's own existing precedent (6 MB contour file, 1.8–5.5 MB theme images, Wave 2's 1.7–3.5 MB layers). No layer is auto-loaded outside its own theme page — each fetches only when its diagnostic section is opened, matching the site's existing lazy, theme-scoped loading pattern; nothing was added to the homepage.

---

## UX decisions

- **Layer organization**: Wave 3 layers were placed into *existing* sections (Géologie for conservation, Économie & Énergie for énergie/économie/corridors, and one new Peuplement section) rather than creating several new top-level themes, per the instruction to prefer the existing architecture.
- **Legends**: reused the categorized-styling + inline-legend mechanism built in Wave 2 (Occupation du sol 2020) for Zones de conservation's 2 categories — no new JS.
- **Popups**: every new layer's properties were reduced to only meaningful fields (`nom`, `categorie`, `commune`, `population` where genuinely present) — no `OBJECTID`, `Shape_Area`, KML artifacts, or other internal GIS fields are exposed.
- **Coverage warnings**: a new, lightweight per-layer `coverage` caption (small amber italic text under the layer's checkbox, e.g. "📍 Couverture : Gandon uniquement") was added to `diagnostic_unified.html` for every layer whose scope is not the full 3-commune agglomeration. This directly satisfies the task's "never suggest a complete three-commune dataset when only one or two communes are represented" requirement without adding visual weight — it's one small line, only shown when relevant.
- **Consistency between diagnostic maps and `/carte/`**: none of the Wave 3 layers were added to `/carte/` in this wave. `/carte/`'s `LAYER_GROUPS` has no existing "peuplement," "conservation," or "économie" group to extend (a pre-existing scope gap already tracked as R10 in `PROJECT_ANALYSIS.md`), and creating 3 new group categories there was judged a larger structural change than "integrate the new themes" calls for — consistent with the same reasoning already applied in Wave 2 for Occupation du sol 2020/MNT. No second, different Leaflet implementation was created; every new layer uses the exact same rendering path already used by every other diagnostic-theme layer.

---

## Blocked client requests

- **Bassins versants**: no basin/watershed dataset exists anywhere in the delivery (confirmed again this wave). Per explicit instruction, no hydrological derivation from the MNT was attempted without approval, and nothing was fabricated. **Kept out of the navigation entirely** — no empty "Bassins versants" page was added, since an empty page would mislead users into thinking the data exists. Still blocked, same as `REPLY_CLIENT.md` already stated.
- **Village names for `localite.shp`**: still not available anywhere in the source data or its lineage (confirmed via the `path` provenance field, which traces back to the same national land-cover tiles, never an individually-named village dataset). Not fabricated.
- **Missing commune coverage**: Saint-Louis has zero énergie/économie/corridor data; Gandiol has zero énergie data; conservation zones can't be attributed per-commune. All communicated via the new coverage captions rather than hidden or implied otherwise.
- **`Projets Économiques.shp`'s duplicate-name data-quality issue** (both merged records share one name) was documented, not silently corrected, per instruction.

---

## Tests

| Area | Test | Result |
|---|---|---|
| Peuplement | `/diagnostic?section=peuplement` loads | PASS (200) |
| Peuplement | Quartier layers (Gandon, Gandiol) load with correct names/population | PASS — verified via direct file read (not terminal print, per the encoding lesson above) |
| Peuplement | Localités load, no fabricated names | PASS — all 372 show only the generic "Localité" category |
| Peuplement | Boundaries align geographically | PASS — reprojected bboxes cross-checked against the site's known extent |
| Peuplement | Population theme remains untouched/separate | PASS — `population` section's own layers/stats unchanged |
| Conservation | 44 features represented correctly | PASS — feature count and both category labels verified |
| Conservation | Legend correct | PASS — 2-item legend renders in the Géologie theme |
| Énergie | Gandon data loads | PASS |
| Énergie | No false Saint-Louis/Gandiol coverage implied | PASS — coverage caption present on every énergie layer |
| Activités économiques | Gandon layers work | PASS |
| Activités économiques | Gandiol layers work | PASS |
| Activités économiques | Missing Saint-Louis coverage communicated | PASS — no Saint-Louis économie layer exists, and the theme's own content text says so explicitly |
| Corridors | Verified corridor features load, styling/popups correct | PASS |
| Regression: `/` | 200, Wave 1/2 changes intact | PASS |
| Regression: `/diagnostic` (all sections: geologie, pedologie, topographie, occupation, urbanisation, risques, transport, peuplement, population, equipements, economie_energie, gouvernance) | All 200 | PASS |
| Regression: `/carte/` | 200, unaffected | PASS |
| Regression: `/communes/`, all 3 commune pages | 200 | PASS |
| Regression: equipment pages (all 3 communes) | 200 | PASS |
| Regression: `/ressources` | 200, Wave 2 MNT downloads intact | PASS |
| Regression: all 10 new static GeoJSON files served | 200 | PASS |
| Server log across every request in this wave | Clean — zero errors/tracebacks | PASS |
| `app.main:app` import | Clean | PASS |

No headless browser was available in this environment; verification was done by rendering every page server-side and inspecting the exact emitted HTML/JSON, plus direct file reads for French-text correctness (the terminal-print pitfall described above made this the only reliable method).

---

## Files changed

**Application files modified:**
- `app/routers/diagnostic.py` — new `peuplement` section, `zones-conservation` layer added to `geologie`, all new layers added to `economie_energie`, `SECTION_ORDER` updated
- `app/templates/diagnostic_unified.html` — new `coverage` caption rendering (additive, no existing behavior changed)
- `REPLY_CLIENT.md` — one factual correction (Occupation du sol 2020 extent), nothing else changed

**New generated web assets:**
- `app/static/data/peuplement/localites.geojson`
- `app/static/data/peuplement/quartiers-gandon.geojson`
- `app/static/data/peuplement/quartiers-gandiol.geojson`
- `app/static/data/conservation/zones-conservation.geojson`
- `app/static/data/energie/energie-gandon.geojson`
- `app/static/data/energie/gazoduc-gandon.geojson`
- `app/static/data/economie/economie-gandon.geojson`
- `app/static/data/economie/economie-gandiol.geojson`
- `app/static/data/economie/usine-zircon-gandiol.geojson`
- `app/static/data/economie/future-autoroute.geojson`
- `PHASE3_WAVE3_REPORT.md` (this file)

No files under `reply client/` were modified. No orphaned templates were touched. No commune, equipment-page, or advanced-GIS code was touched.

---

## Deferred work (Wave 4/5, not started)

- Bassins versants (blocked on missing data, kept out of navigation).
- Full 3-commune coverage for énergie, activités économiques, and conservation zone attribution — blocked on missing client data.
- Reconciling Saint-Louis's existing per-quartier `POPULATION` attribute (discovered already present in `population/quartiers-polygones.geojson`) with the newly-discovered Gandon/Gandiol per-quartier population into one unified cross-commune population dataset/view — deliberately deferred rather than merged ad hoc, since that's a data-reconciliation decision better suited to the commune-architecture work (Wave 4) than a Wave 3 GIS-integration task.
- Adding a "peuplement"/"conservation"/"économie" group to `/carte/`'s `LAYER_GROUPS` (same pre-existing scope gap as Wave 2's occupation-sol/topographie note, R10 in `PROJECT_ANALYSIS.md`).
- Commune architecture redesign (Diagnostic → SVD → PCU/PCUI) — Wave 4.
- Buffer/query/spatial-analysis/export tooling — Wave 5.
- `Boucle de Gandiolais.shp` and `CN_10m` remain broken/unusable, unchanged from `REPLY_CLIENT.md`.

---

## Result

`WAVE 3 COMPLETE — READY FOR REVIEW`

All 5 named themes (Peuplement, Zones de conservation, Énergie, Activités économiques, Corridors) were implemented using only verified, real client data, with honest per-layer coverage disclosure everywhere data is incomplete. Bassins versants remains explicitly and visibly blocked rather than faked. A real encoding mistake (wrongly applying Wave 2's cp1252 fix to files that were already correctly UTF-8) was caught and corrected before shipping, together with a Unicode normalization pitfall — both documented above so they don't recur in Wave 4. Stopping here per instructions; not proceeding to Wave 4 automatically.
