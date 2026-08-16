# CLIENT_REMARK2_OCCUPATION_SOL_REPORT.md — Occupation du sol 2020 selectable classes

## Client remark

`Tu peux supprimer occupation 2020 ou bien insérer des couches séparées` — the combined "Occupation du sol 2020 (nouvelle donnée)" checkbox showed a static, non-interactive 17-class legend underneath several already-selectable standalone land-cover layers, creating a confusing interface where the client could not tell what the extra control did or select individual classes from it.

## Decision

**Option B — separate selectable 2020 classes — was implemented**, not deletion, per the task's explicit preference. The 2020 dataset (`occupation-du-sol-2020.geojson`, 575 features, 17 real classes, byte-verified) is valid, already-validated client data; discarding it to simplify the UI would have thrown away real information rather than fixing the actual usability problem, which was interactivity, not the data's existence.

## Current-data audit

| Layer | Source file | Year/date | Attribute/class | Feature count | Currently separate? | Part of 2020 dataset? | Duplicates another layer? |
|---|---|---|---|---|---|---|---|
| Empreinte urbaine | `occupation-sol/empreinte-urbaine.geojson` | Not dated in data | — (single class per file) | Not re-counted (unchanged) | Yes | No | No |
| Culture pluviale | `occupation-sol/culture-pluviale.geojson` | Not dated | — | — | Yes | No | No — also a 2020 class, but distinct file/provenance |
| Plantation forestière | `occupation-sol/plantation-forestiere.geojson` | Not dated | — | — | Yes | No | No — also a 2020 class, distinct provenance |
| Mangrove | `occupation-sol/mangrove.geojson` | Not dated | — | — | Yes | No | **Unclear/likely** — a 2020 class is also named "Mangrove"; no documented date exists to disambiguate further than "existing site layer" vs "2020 dataset" — addressed via grouping, not renaming (see below) |
| Savane arbustive / Savane boisée | `occupation-sol/savane-{arbustive,boisee}.geojson` | Not dated | — | — | Yes | No | Unclear vs. the 2020 dataset's single combined "Savane" class (not split arbustive/boisée there) |
| Steppe | `occupation-sol/steppe.geojson` | Not dated | — | — | Yes | No | Unclear — a 2020 class is also named "Steppe" |
| Sol nu dunaire / Sol nu inondable | `occupation-sol/sol-nu-{dunaire,inondable}.geojson` | Not dated | — | — | Yes | No | Unclear vs. the 2020 dataset's single combined "Sol nu" class |
| Canal d'irrigation | `occupation-sol/canal-irrigation.geojson` | Not dated | — | — | Yes | No | No |
| **17 classes (Mare, Lac, Cours d'eau, Plaine inondable, Vasière, Mangrove, Prairie aquatique, Tanne, Steppe, Savane, Sol nu, Dune, Culture pluviale, Culture irriguée, Culture maraichère, Plantation forestière, Carrière Mine Infrastructure)** | `occupation-sol-2020/occupation-du-sol-2020.geojson` | 2020 | `categorie` field, byte-verified against the actual source file (not from memory) | 575 total, distributed across 17 values | **Now yes** (was: one combined layer) | Yes, this **is** the 2020 dataset | Several class names overlap with the "existantes" standalone layers above (Mangrove, Steppe, Culture pluviale, Plantation forestière) or partially overlap (Savane, Sol nu) |

**Per instruction, no fake "historique"/year label was invented** for the old standalone layers (no source document establishes their exact date). The overlap is instead resolved by **grouping/heading**, not renaming: the sidebar now shows "Occupation du sol — couches existantes" (10 layers, unchanged, expanded by default) and a separate, collapsible "Occupation du sol — 2020" (17 layers, collapsed/unchecked by default) — exactly the "safer UI" pattern suggested in the task.

## Implementation

**One source dataset, one fetch, per-category virtual sublayers** — implemented identically on both pages:

- **`app/routers/diagnostic.py`**: extracted the previously-inline `categoryColors` dict into a module-level `OCCSOL_2020_CATEGORY_COLORS` constant (byte-verified against the source file before use), then generated `OCCSOL_2020_CLASS_LAYERS` — a list of 17 layer configs, each pointing at the **same** `occupation-sol-2020/occupation-du-sol-2020.geojson` file with its own `categoryFilter` value, `group: "occ2020"`, and `defaultChecked: False`. The 10 existing standalone layers were tagged `group: "existantes"` (first one carries `groupOpen: True`). The old single combined entry and its `(nouvelle donnée)` label are gone.
- **`app/routers/carte.py`**: added support for an explicit `"file"` override in `_resolve_layer_url()` (needed because several `layer_id`s now share one physical file, which the old filename-stem `rglob` lookup couldn't express), then replaced the single combined `occupation-du-sol-2020` entry with 17 dict entries (`occ2020-0` … `occ2020-16`), each with its own `categoryFilter`. The group itself is now `"collapsible": True`.
- **`app/templates/diagnostic_unified.html`**: added group-transition detection in the sidebar loop (Jinja `namespace`, matching the existing prev/next-nav pattern already used in this file) to render a `<details>` block with a group label and "Tout afficher"/"Tout masquer" buttons whenever consecutive layers share a `group`. Checkboxes gained `data-layer-index`/`data-layer-group` attributes. A `fetchFile(file)` helper caches the parsed GeoJSON **by file path**, so all 17 category configs share exactly one network request. Feature filtering by `categoryFilter` builds a **new** array (`sharedGeojson.features.filter(...)`) rather than mutating the cached object, since 16 other configs depend on the same cached data staying intact. **Loading is lazy**: layers that start unchecked (`defaultChecked: False`) are not fetched at page load at all — `toggleLayer()` now triggers the fetch+build on first activation, matching `/carte/`'s existing pattern and genuinely honoring "2020 group initially OFF" rather than fetching everything anyway just to leave it un-rendered.
- **`app/templates/carte.html`**: `layerCache` changed from being keyed by `layerId` to being keyed by **resolved URL**, storing the fetch **promise** (not just the resolved data) so concurrent activations (e.g. clicking "Tout afficher", which toggles all 17 checkboxes near-simultaneously) can never trigger more than one network request for the same file — a plain "skip if cached" check would have raced under concurrent async calls. Added the same collapsible-group rendering (`group.collapsible`) and `toggleGroup()` mechanism as the diagnostic page.
- **Popups**: added an optional `popupHeader` field (set to `"Occupation du sol 2020"` for all 17 classes) so a feature's popup shows which dataset it came from, without fabricating any new attribute — the underlying data only ever had the one `categorie` field.

No 17-file duplication was created anywhere; both routers' `OCCSOL_2020_CATEGORY_COLORS`/class-layer generation reference the same single validated GeoJSON.

## New client data relevance

Re-examined for this specific remark (Occupation du sol), reusing Remark 1's inventory of `C:\Users\ykbeili\OneDrive - Vermeg\Desktop\taher\Base de donnees SIG Senegal\DIAGNOSTIC\couches nouvelles\couches nouvelles`:

- **`bati`**: **NO** — 15,481 building-footprint polygons with a single `Id` attribute field; no land-cover classification of any kind.
- **`quartier_saint_louis`**: **NO** — 33 named-quartier points with `POPULATION`, `superficie`, `type_zone`, `type_activ` attributes; these describe administrative/urban-network zoning concepts (e.g. "zoneconect"/"dens_branch"), not land-cover categories comparable to Mare/Mangrove/Steppe/etc. Neither dataset was forced into this page; both remain available for a future habitat/bâti or population/quartiers remark.

## Browser validation

Performed with Playwright + headless Chromium against the running dev server, on both `/diagnostic?section=occupation` and `/carte/`.

- **Single class (Mangrove only)**: **PASS** — only the Mangrove-2020 polygon rendered in addition to the unaffected "existantes" layers; screenshot-verified.
- **Multiple classes (Steppe + Mare simultaneously)**: **PASS** — both rendered together, no interference.
- **All classes ("Tout afficher")**: **PASS** — all 17 categories rendered simultaneously with correct, distinct colors on both pages (screenshot-verified on `/carte/`, showing the full regional extent of the 2020 dataset).
- **Toggle repeatedly (Mare OFF→ON→OFF→ON)**: **PASS** — `layers`/`activeLayers` count stayed exactly consistent throughout (11→13→13 as expected), no duplicate layers, no extra fetch.
- **`/carte/`**: **PASS** — same 17-class model, same collapsible group, same "Tout afficher"/"Tout masquer" controls; red évolution urbaine palette, Relief, Équipements, and both risk filters all confirmed still present and unaffected (regression-tested).
- **Mobile (390px)**: **PASS** — collapsible group readable, checkboxes clickable, panel scrolls independently, no horizontal page overflow.
- **Console**: **PASS** — zero `pageerror` events across every scenario.

## Performance

- **Number of GeoJSON fetches for `occupation-du-sol-2020.geojson` per page load with nothing checked: 0** (previously this file was being fetched unconditionally on every page load even though "2020 group initially OFF" was the intent — caught and fixed during this task's own testing, not left as a residual issue).
- **After activating any single 2020 class: exactly 1 fetch.** After then toggling more classes, swapping classes, or clicking "Tout afficher" (which checks all 17 near-simultaneously): **still exactly 1 fetch total**, verified via a live network-request counter in the browser test — the promise-based cache correctly de-duplicates even concurrent activations, not just sequential ones.
- **Duplicate fetches: NO.**

## Automated tests

**102 PASS / 0 FAIL** (`pytest tests/ -q`) — 93 pre-existing (unaffected) + 9 new:
- `test_occupation_no_nouvelle_donnee_wording`
- `test_occupation_2020_classes_are_individually_selectable` (all 17 `categoryFilter` values present, one shared source file)
- `test_occupation_2020_classes_default_unchecked`
- `test_occupation_existing_layers_unaffected`
- `test_carte_occupation_group_is_17_individual_classes`
- `test_carte_still_has_red_evolution_palette_and_filters` (regression guard for prior remarks)
- `test_commune_occupation_sol_2020_no_nouvelle_donnee` (×3 communes)

No existing test was weakened. (Two of the new tests initially failed against Jinja's own HTML/JSON escaping of apostrophes and accented characters in `Cours d'eau`/`Vasière`/etc. — fixed in the test assertions themselves, not a product bug; verified against the actual rendered bytes before concluding this.)

## Client input required

`NONE FOR THIS REMARK`

## Files changed

- `app/routers/diagnostic.py`
- `app/routers/carte.py`
- `app/templates/diagnostic_unified.html`
- `app/templates/carte.html`
- `tests/test_routes.py`
- `REPLY_CLIENT_REQUEST.md` (new §M, recap table row)
- `CLIENT_REMARK2_OCCUPATION_SOL_REPORT.md` (new, this file)

## Result

`CLIENT REMARK 2 OCCUPATION DU SOL COMPLETE`
