# CLIENT_REMARK4_RISQUES_NATURELS_REPORT.md — Add the two client-provided cartographic maps

## Client remark

`Dans la rubrique risque naturel, tu n'as pas mis les cartes (deux cartes) comme dans les autres rubriques` — the Diagnostic → Risques naturels page had title/text/key-points but no cartographic map image, unlike every other diagnostic theme (which each show one static thematic map).

## Source folders inspected

Both folders contained exactly one PDF + one TIFF (a QGIS print-layout export in both formats) — no PNG/JPG, no extraneous or temporary files.

### Inondation

`.../Cartographie inondation et vulnerabilite/Inondation/Carte/` → **`Alea.tif`** (6614×4677 px, 400 DPI, 4.19 MB) + `Alea.pdf` (1 page, A3, 853 KB).

**Content verified visually, not assumed from the filename**: the map's own title block reads **"Carte des aléas naturels"**, dated 17/10/2025, format A3, ADM/COMETE letterhead. Its primary legend is "Hauteur de submersion pour crue centennale" (4 classes: >2m Très fort, 1–2m Fort, 0.5–1m Moyen, <0.5m Faible) — this is the flood-hazard content the client is referring to as "risque d'inondation." The sheet *also* carries a secondary legend, "Risque d'érosion côtière" (Fort/Moyen), on the same single image — this was not stripped out or hidden, since altering the client's original map would be inappropriate; it is disclosed here and in the site's own field note.

### Vulnérabilité

`.../Cartographie inondation et vulnerabilite/Vulnerabilite/Carte/` → **`vulnerabilite.tif`** (4677×3307 px, 400 DPI, 2.53 MB) + `Vulnerabilite.pdf` (1 page, A4, 2.93 MB).

**Content verified visually**: title block reads **"Carte de la vulnérabilité"**, dated 16/10/2025, format A4, same letterhead. Legend: "Vulnérabilité" (4 classes: Extrême >2m, Haute 1–2m, Moyenne 0.5–1m, Faible <0.5m) plus a secondary "Risque inondation" legend (Très fort/Fort/Moyen/Faible) on the same sheet — again disclosed, not hidden.

Neither file was a raw GIS layer, a legend-only export, a QGIS project, or a map belonging to another theme — both are genuine, complete, dated cartographic print layouts matching the requested themes.

## Integration

- **`app/routers/diagnostic.py`**: added a new `"cartes"` list to the `"risques"` section — 2 entries (title, image, image_alt, pdf, interactive_link), reusing the site's public French labels `"Carte du risque d'inondation"` and `"Carte de vulnérabilité"` exactly as the client requested. No Windows path, temporary filename, or `(nouvelle donnée)` wording is exposed anywhere.
- **`app/templates/diagnostic_unified.html`**: added a new template block ("Cartographie des risques") rendered only when `data.cartes` is present (every other section is unaffected, since none of them define this field). Each map reuses the site's **existing** click-to-enlarge lightbox (`class="lightbox-img"`, the same site-wide mechanism in `base.html` already used for every other theme's single image — no new JS library, no redesign), plus a "Télécharger le PDF" link to the original, untouched PDF and an "Explorer la carte interactive →" link to the matching existing route.
- **Flood map → `/risques/inondation`**, **Vulnerability map → `/risques/vulnerabilite`** — both routes already existed and remain unmodified; no duplicate route was created.

## Preparing the web-safe copies

| | Flood ("Carte du risque d'inondation") | Vulnerability ("Carte de vulnérabilité") |
|---|---|---|
| Source file | `Alea.tif` | `vulnerabilite.tif` |
| Source size | 4.19 MB (6614×4677) | 2.53 MB (4677×3307) |
| Web derivative | `app/static/img/cartes/risque-inondation.jpg` | `app/static/img/cartes/vulnerabilite.jpg` |
| Web size | 1.93 MB (6614×4677, unchanged resolution) | 1.37 MB (4677×3307, unchanged resolution) |
| Transformation | TIFF → JPEG, quality 90, no resize | Same |
| Quality loss | Minor JPEG compression only; resolution kept at the source's native pixel size — matches this site's existing convention for thematic map images (e.g. `occupation-sol.jpg` is 4959×3509 at similar quality), so legend text/scale bar/labels remain fully readable, confirmed visually via the lightbox |
| Original preserved | `app/static/docs/Carte_Alea_Inondation_PUD.pdf` (853,720 bytes, byte-identical copy of the client's PDF) | `app/static/docs/Carte_Vulnerabilite_PUD.pdf` (2,932,914 bytes, byte-identical copy) |

The client's original source files (in `Base de donnees SIG Senegal\...`) were **not modified** — only read and copied from.

### Source traceability

| | Flood | Vulnerability |
|---|---|---|
| CLIENT SOURCE | `Cartographie inondation et vulnerabilite/Inondation/Carte/Alea.tif` | `.../Vulnerabilite/Carte/vulnerabilite.tif` |
| THEME | Risque/aléa d'inondation (+ érosion côtière, secondary) | Vulnérabilité (+ risque inondation, secondary) |
| SOURCE FILE | `Alea.tif` / `Alea.pdf` | `vulnerabilite.tif` / `Vulnerabilite.pdf` |
| WEB FILE | `risque-inondation.jpg` | `vulnerabilite.jpg` |
| FORMAT | JPEG (from TIFF) | JPEG (from TIFF) |
| DIMENSIONS | 6614×4677 | 4677×3307 |
| OPTIMIZATION | JPEG quality 90, no resize | JPEG quality 90, no resize |
| APP LOCATION | `app/static/img/cartes/risque-inondation.jpg` + `app/static/docs/Carte_Alea_Inondation_PUD.pdf` | `app/static/img/cartes/vulnerabilite.jpg` + `app/static/docs/Carte_Vulnerabilite_PUD.pdf` |

## Existing interactive GIS preserved

- **Inondation** (`/risques/inondation`): **PASS** — 200, still references `risque-inondation.geojson`.
- **Vulnérabilité** (`/risques/vulnerabilite`): **PASS** — 200, still references `vulnerabilite.geojson` (the Phase 5 fix for this page's data loading is untouched).
- **Érosion** (`/risques/erosion`): **PASS** — 200, still references `erosion.geojson` (same Phase 5 fix untouched). No third static erosion map was created for this remark, per instruction — erosion's interactive page is unchanged, and the incidental erosion legend baked into the flood TIFF was left as-is rather than extracted into a separate product.

## Browser validation

Performed with Playwright + headless Chromium against the running dev server.

- **Risk diagnostic page**: **PASS** — loads cleanly, no console errors.
- **Flood map visible**: **PASS** — 200, screenshot-verified, fully legible (title block, legend, scale bar all crisp).
- **Vulnerability map visible**: **PASS** — 200, screenshot-verified, fully legible.
- **Lightbox**: **PASS** — clicking either map opens the full-resolution image in the site's existing modal; `Escape` closes it.
- **Interactive links**: **PASS** — both `/risques/inondation` and `/risques/vulnerabilite` links present and resolve to 200.
- **PDF downloads**: **PASS** — both `/static/docs/Carte_Alea_Inondation_PUD.pdf` and `/static/docs/Carte_Vulnerabilite_PUD.pdf` resolve to 200.
- **Mobile (390px)**: **PASS** — the two-column grid collapses to a single column, both images fit within the viewport, no horizontal page overflow, links remain tappable.
- **No broken assets**: **PASS** — both map images return 200; the only failed network requests observed were background OpenStreetMap tile cancellations from the (unrelated, pre-existing) interactive Leaflet map further down the same page, a normal artifact of the test navigating away, not a broken asset.
- **No local filesystem reference**: **PASS** — confirmed no `C:\Users`, `C:/Users`, or `file:///` string appears anywhere in the rendered HTML.

## Performance

Both images total **3.30 MB** combined web weight (1.93 MB + 1.37 MB), each with `loading="lazy"` (so neither downloads until scrolled into view) — consistent with, and not heavier than, this site's existing per-theme map images (which range 1.7–5.4 MB each). No aggressive compression was applied, since legend/label readability was prioritized, per instruction — verified by inspecting both images at full size via the lightbox.

## New `couches nouvelles` relevance

- `bati`: **NOT RELEVANT** — building footprints, no connection to flood/vulnerability risk mapping.
- `quartier_saint_louis`: **NOT RELEVANT** — named quartiers/population, no connection to flood/vulnerability risk mapping.

Neither was integrated; both remain available for a future, actually-relevant remark.

## Automated tests

**118 PASS / 0 FAIL** (`pytest tests/ -q`) — 110 pre-existing (unaffected) + 8 new:
- `test_risques_page_has_both_client_maps`
- `test_risques_map_assets_exist_and_are_reachable`
- `test_risques_no_windows_path_exposed`
- `test_risques_interactive_links_point_to_existing_routes`
- `test_risques_interactive_gis_still_loads_data` (×3 — inondation/vulnerabilite/erosion, regression guard for the Phase 5 fix)
- `test_risques_stats_unchanged`

No existing test was weakened.

## Client input required

`NONE FOR THIS REMARK` — both cartographic maps were found, verified, and integrated successfully.

## Files changed

- `app/routers/diagnostic.py`
- `app/templates/diagnostic_unified.html`
- `app/static/img/cartes/risque-inondation.jpg` (new)
- `app/static/img/cartes/vulnerabilite.jpg` (new)
- `app/static/docs/Carte_Alea_Inondation_PUD.pdf` (new, untouched copy of client original)
- `app/static/docs/Carte_Vulnerabilite_PUD.pdf` (new, untouched copy of client original)
- `tests/test_routes.py`
- `REPLY_CLIENT_REQUEST.md` (new §O, recap table row)
- `CLIENT_REMARK4_RISQUES_NATURELS_REPORT.md` (new, this file)

## Result

`CLIENT REMARK 4 RISQUES NATURELS COMPLETE`
