# CLIENT_REMARK3_URBANISATION_REPORT.md — Invert red intensity + black lotissements

## Client remark

`Il faut inverser l'ordre des couleurs` — rouge clair pour Empreinte 2017, rouge intermédiaire pour Empreinte 2020, rouge foncé pour Empreinte 2024 — and `utiliser le noir pour lotissements planifiés`.

## Previous state

From the earlier interactive-map remark: Empreinte 2017 = `#7f1d1d` (dark, darkest/foreground), Empreinte 2020 = `#dc2626` (medium), Empreinte 2024 = `#fca5a5` (light, lightest/background) — chosen so the OLDEST year was darkest. Lotissements planifiés was `#3498db` (blue), and carried no explicit Leaflet pane (it defaulted into Leaflet's own `overlayPane` at zIndex 400 — below every empreinte pane, which sit at 401–403).

## Final palette

| Layer | Hex | Pane | paneZIndex |
|---|---|---|---|
| Empreinte 2017 | `#fca5a5` (light red) | `empreinte2017Pane` | 403 (unchanged) |
| Empreinte 2020 | `#dc2626` (medium red) | `empreinte2020Pane` | 402 (unchanged) |
| Empreinte 2024 | `#7f1d1d` (dark red) | `empreinte2024Pane` | 401 (unchanged) |
| Lotissements planifiés | `#000000` (black) | `lotissementsPane` (new) | 410 (new — above all 3 empreinte panes) |

Only the **`color`** values for 2017 and 2024 were swapped (2020's color and every `paneZIndex` value were left untouched). `fillOpacity: 1` was kept on all three empreinte layers, so transparency still plays no role in distinguishing the years — matching the standing R5 requirement.

## Layer stacking

**Confirmed unchanged and verified in a real browser**: 2017 remains foreground (highest pane zIndex, 403), 2020 remains middle (402), 2024 remains background (lowest, 401) — the color swap did not touch stacking. Lotissements planifiés was given a **new** dedicated pane at zIndex 410 (above all three empreinte panes): previously it had no pane at all and silently sat in Leaflet's default `overlayPane` (zIndex 400) — *below* every empreinte layer, meaning it could already have been hidden beneath urban footprints even before this remark. This was corrected as part of satisfying "ensure black geometry is not hidden behind urban footprints."

## Views updated

- `app/routers/carte.py` — `/carte/`'s `evolution` group (no `lotissements` layer exists there — `/carte/` never exposed this layer, so there was nothing to recolor black there; noted rather than invented).
- `app/routers/diagnostic.py` — global Diagnostic → Urbanisation (`evolution/empreinte-*.geojson` + `evolution/lotissements.geojson`).
- `app/routers/commune_diagnostic_data.py` — Saint-Louis, Gandon, and Ndiébène Gandiole's `urbain-mobilite` subsections (empreinte colors in all 3; lotissements color in Saint-Louis and Gandon, the only two communes that actually have a "Lotissements planifiés" dataset — **Ndiébène Gandiole has none**, confirmed by inspecting its `urbain-mobilite` layer list, not assumed).

**Explicitly left unchanged, out of scope:**
- Gandon's `habitat-lotissements-autorises.geojson` ("Lotissements autorisés (parcelles)") — a *different* layer, in the `habitat-foncier` subsection, with different wording ("autorisés" vs. the client's "planifiés"). Recoloring it would have been guessing at an equivalence the client didn't state.
- Gandon/Gandiole's "Empreinte urbaine détaillée (reclassée depuis « Zone d'habitation »)" (`#e74c3c`) — a distinct, non-dated detail layer, not part of the 2017/2020/2024 sequence.

## Browser validation

Performed with Playwright + headless Chromium against the running dev server.

- **Diagnostic Urbanisation**: **PASS** — legend swatches and rendered polygons both show light-pink 2017, medium-red 2020, dark-red 2024, black lotissements; screenshot-verified. Panes confirmed via `map.getPane(...)`: 403/402/401/410 exactly as intended.
- **`/carte/`**: **PASS** — same palette, same pane values; screenshot shows a clear "growth ring" pattern (light 2017 cores surrounded by darker 2020/2024 expansion rings), which is only legible *because* 2017 stays on top despite being the lightest color — direct visual proof the color/stacking distinction was preserved correctly.
- **Commune pages**: **PASS** (spot-checked Gandon) — same palette and pane values; the Remark 2 Occupation du sol 2020 collapsible group is also visibly intact and unaffected on the same page.
- **Overlapping polygons**: **PASS** — visually confirmed on `/carte/`'s wide view: light-red 2017 areas render above the darker 2020/2024 rings surrounding them, exactly matching the required stacking despite the color inversion.
- **Layer toggles (2017/2020/2024/Lotissements OFF→ON, all 4 layers)**: **PASS** — `layers` array stayed populated at 4 throughout, no duplicate layers, no console errors.
- **Mobile (390px)**: **PASS** — legend colors clearly visible, labels readable, checkboxes functional, no horizontal overflow.

## Automated tests

**110 PASS / 0 FAIL** (`pytest tests/ -q`) — 102 pre-existing + 8 new/updated:
- `test_carte_evolution_urbaine_color_intensity_inverted_stacking_unchanged`
- `test_diagnostic_urbanisation_color_intensity_inverted_stacking_unchanged`
- `test_diagnostic_lotissements_planifies_is_black`
- `test_commune_urbanisation_color_intensity_inverted_stacking_unchanged` (×3 communes)
- `test_commune_lotissements_planifies_is_black` (×2 communes — Saint-Louis, Gandon; Ndiébène Gandiole has no such dataset)

The 4 pre-existing "red family, not blue" tests were kept as-is (they still correctly pass, since the same 3 hex values are used, just reassigned) and supplemented — not replaced — with the new precise per-year assertions, since the old tests alone could not have caught a color/year mismatch. These new tests parse the actual JSON payload (`json.loads`) rather than doing loose substring matching, so they directly verify both the exact color-per-year mapping and the pane zIndex ordering in one assertion, per the task's explicit "do not confuse color order with stacking order" concern.

## New client data relevance

- `bati`: **NOT RELEVANT TO THIS REMARK** — building footprints, no styling connection to urbanisation evolution colors.
- `quartier_saint_louis`: **NOT RELEVANT TO THIS REMARK** — named quartiers/population, no styling connection to urbanisation evolution colors.

Neither was inspected further for this remark since it is a pure styling correction to already-integrated layers.

## Client input required

`NONE FOR THIS REMARK`

The separate authoritative 2024/2025 empreinte dataset question (tracked in `REPLY_CLIENT_REQUEST.md` §J/§K) remains open but is unaffected by and does not block this styling correction.

## Files changed

- `app/routers/carte.py`
- `app/routers/diagnostic.py`
- `app/routers/commune_diagnostic_data.py`
- `tests/test_routes.py`
- `REPLY_CLIENT_REQUEST.md` (new §N, recap table row)
- `CLIENT_REMARK3_URBANISATION_REPORT.md` (new, this file)

## Result

`CLIENT REMARK 3 URBANISATION COMPLETE`
