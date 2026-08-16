# CLIENT_REMARK1_TOPOGRAPHY_REPORT.md — Topographie Map Not Displaying Data

## Client remark

1. `Pourquoi aucune donnée ne s'affiche sur la carte` — the Topographie map (`/diagnostic?section=topographie`) showed checked layers (Courbes de niveau, Relief ombré (MNT), Courbes de niveau 5 m) but no visible topographic information.
2. `Pourquoi la troisième couche tu l'as appelée (nouvelle donnée)` — why the "Courbes de niveau 5 m" layer carried the implementation-history label "(nouvelle donnée)".

## Root cause

**A genuine JavaScript crash**, reproduced in a real headless Chromium browser (Playwright), not a styling/color/opacity issue.

`app/templates/diagnostic_unified.html` (and identically `communes/diagnostic_section.html`, `carte.html`) passed `pane: cfg.pane || undefined` into every Leaflet layer constructor — a pattern introduced in the prior "interactive map remarks" task to support deterministic stacking for the évolution urbaine layers. For layers that don't declare a pane (which is every Topographie layer today), this evaluates to `pane: undefined`.

In JavaScript, `{ pane: undefined }` is **not the same as omitting the key**: Leaflet's option-merging (`L.Util.setOptions`) copies `undefined` as an *own property*, which shadows the class's default `pane: 'overlayPane'` on the prototype. `L.GeoJSON`/`L.Polyline` tolerate this silently (verified — they fall back safely), but **`L.ImageOverlay.onAdd()` does not** — it calls `this._map.getPane(this.options.pane).appendChild(this._image)` directly, and `getPane(undefined)` returns `undefined`, so `.appendChild` throws:

```
Uncaught TypeError: Cannot read properties of undefined (reading 'appendChild')
```

This was confirmed with an isolated minimal reproduction (`L.imageOverlay(url, bounds, {pane: undefined})` throws this exact error; `L.geoJSON(data, {pane: undefined})` does not).

**Why this looked like "no data at all":** the Topographie layer array is `[courbes-niveau (line), Relief ombré (image), courbes-niveau-5m (line)]`. The image-overlay crash happens **synchronously inside the `forEach` loop** that creates all three layers — an uncaught exception there aborts every loop iteration after it. So:
- Layer 0 (Courbes de niveau) had already been queued for fetch before the crash and loaded fine.
- Layer 1 (Relief ombré) crashed — it was still registered in `map._layers` (Leaflet adds to that registry *before* calling `onAdd()`, so `map.hasLayer()` misleadingly reported `true`), but the image element was never actually inserted into the DOM, so nothing was visible.
- **Layer 2 (Courbes de niveau 5 m) never even started fetching** — the crash in the image branch aborted the `forEach` before that iteration ran.

This fully explains the client's report: only 1 of 3 layers was actually rendering, and the newest layer they specifically asked about never loaded at all.

A secondary, much smaller factor was also found and addressed: the page's `fitBounds()` call used whichever layer happened to be at array index 0 — for Topographie that's the *older*, non-clipped `courbes-niveau.geojson`, whose extent is somewhat larger than the hillshade/5m-contour study area. This is not a bug (Leaflet correctly computes the mathematically-tightest zoom for the given bounds and container aspect ratio — confirmed by testing with animation disabled to rule out a mid-animation read), but it meant the default view showed more surrounding context than necessary. Fixed to prefer the image layer's known bounds when present.

## Existing data used

All three Topographie layers already existed and needed no new data — verified directly, not assumed:

| Layer | File | Format | Features/size | CRS check |
|---|---|---|---|---|
| Courbes de niveau | `app/static/data/diagnostic/topographie/courbes-niveau.geojson` | GeoJSON LineString | 13,762 features, 5.81 MB | Coordinates confirmed valid WGS84 lon/lat (lon −16.53…−16.14, lat 15.83…16.14) |
| Relief ombré (MNT) | `app/static/img/topographie/hillshade-mnt.png` | PNG image overlay | 0.84 MB | Bounds `[[15.828733,-16.530742],[16.141098,-16.327712]]` confirmed to overlap the study area |
| Courbes de niveau 5 m | `app/static/data/diagnostic/topographie/courbes-niveau-5m.geojson` | GeoJSON LineString | 8,519 features, 3.49 MB | Coordinates confirmed valid WGS84 (lon −16.53…−16.33, lat 15.83…16.14) |

**Real finding on the two contour layers:** inspecting the `Contour` field (older file) and `elevation` field (newer file) across every feature shows **both use the exact same 5 m step** (`-10, -5, 0, 5, 10, 15, 20, 25, 30, 35`). The older layer's key message text ("13 762 courbes de niveau cartographiées **(pas variable)**") was factually incorrect — it is not a variable interval, it's the same fixed 5 m step as the newer layer. Corrected to "(pas de 5 m)". The two layers therefore appear substantially redundant (same interval, overlapping area, different vertex density/vintage) — **not deleted**, documented instead (see `REPLY_CLIENT_REQUEST.md` §L), with a client clarification question on whether to keep both or retain only one.

## New client data inspected

Location: `C:\Users\ykbeili\OneDrive - Vermeg\Desktop\taher\Base de donnees SIG Senegal\DIAGNOSTIC\couches nouvelles\couches nouvelles`

| Dataset | Format | Contents | Relevant to Remark 1? | Reason |
|---|---|---|---|---|
| `bati.shp`/.dbf/.shx/.cpg/.qmd | ESRI Shapefile, 15,481 Polygon features | Building footprints; single attribute field (`Id`, integer only); no `.prj` (CRS undeclared, coordinates in meters consistent with UTM 28N) | **NO** | Building footprints — not elevation/relief/contour data. Relevant to a future habitat/bâti remark, not Topographie. |
| `quartier_saint louis.shp`/.dbf/.prj/.shx/.cpg | ESRI Shapefile, EPSG:32628, 33 Point features | Named quartiers of Saint-Louis with `Nom_quarti`, `POPULATION`, `superficie`, `type_zone`, `NumeroTF`, etc. | **NO** | Quartier/population/administrative data — not elevation/relief/contour data. Relevant to a future population/quartiers remark, not Topographie. |

Per instruction, neither dataset was integrated into Topographie. Both are recorded here and in `REPLY_CLIENT_REQUEST.md` §L for a future remark. Source files were not modified.

## Fix implemented

1. **`app/templates/diagnostic_unified.html`, `app/templates/communes/diagnostic_section.html`, `app/templates/carte.html`** — replaced every `pane: cfg.pane || undefined` (5 occurrences in `diagnostic_unified.html`, 5 in `communes/diagnostic_section.html`, 3 in `carte.html`) with a `paneOpt(pane)` helper that only includes the `pane` key at all when a real pane name is set (`pane ? {pane} : {}`), spread via `...paneOpt(cfg.pane)`. This is the actual root-cause fix.
2. **`app/templates/diagnostic_unified.html`** — the initial `fitBounds()` now prefers an image layer's known bounds (available synchronously, no fetch needed) over whichever GeoJSON layer happens to resolve first at array index 0, avoiding an unnecessarily wide default view driven by a legacy, non-clipped layer.
3. **`app/templates/diagnostic_unified.html`** — added a minimal per-layer loading indicator ("Chargement…", shown only for GeoJSON-backed layers, removed once that layer's fetch settles, success or failure) so a checked-by-default multi-megabyte layer that's still loading doesn't look identical to an empty map.
4. **`app/routers/diagnostic.py`** — `"Courbes de niveau 5 m (nouvelle donnée)"` → `"Courbes de niveau 5 m"`. Corrected the factually-inaccurate `"(pas variable)"` message to `"(pas de 5 m)"`, matching the verified data.

**Not changed, per explicit scope:** the 3 other pre-existing `(nouvelle donnée)` occurrences in `diagnostic.py` (Zones de conservation, Occupation du sol 2020, Localités/villages) refer to different layers, not part of this remark — left untouched and flagged here for a possible future consistency pass, per the instruction to work only on this remark.

## Browser validation

Performed with Playwright + headless Chromium (installed for this task — no browser automation tool was previously available in this environment) against the running dev server.

- **Relief ombré (MNT) only**: **PASS** — visible grey/dark hillshade overlay over the terrain, confirmed via screenshot; `onMap: true`, no console error.
- **Courbes de niveau only**: **PASS** — visible brown contour lines over the coastal/island area; 13,762 features loaded.
- **Courbes de niveau 5 m only**: **PASS** — visible contour lines; 8,519 features loaded (this is the layer that previously never even started fetching).
- **Combined (hillshade + both contour layers)**: **PASS** — all three simultaneously visible, no layer obscuring another.
- **Toggle test (OFF → ON → OFF → ON, ×4 on one layer)**: **PASS** — `layers` array stayed at exactly 3 populated entries throughout, no duplicate layers, no error.
- **Zoom + pan**: **PASS** — no error, map remained responsive.
- **Mobile width (390px)**: **PASS** — no horizontal overflow, tab navigation wraps correctly, all 3 layers still toggleable.
- **Console**: **PASS** — zero `pageerror` events across every scenario after the fix (previously: one uncaught `TypeError` on every page load).
- **Network**: **PASS** — all 3 asset requests return 200 (previously: the 5m contour file was never even requested).
- **`/carte/` Relief**: **PASS** — hillshade and 5 m contours both render correctly together (screenshot-verified), consistent with the Topographie fix, since both pages share the same underlying pane-handling code pattern (now fixed identically in `carte.html`).

## Automated tests

**93 PASS / 0 FAIL** (`pytest tests/ -q`) — 88 pre-existing tests (unaffected) + 5 new targeted tests:
- `test_topographie_page_ok`
- `test_topographie_no_nouvelle_donnee_wording`
- `test_topographie_references_valid_assets` (existence of all 3 backing files + presence in rendered config)
- `test_topographie_layers_do_not_pass_undefined_pane` (regression guard against reintroducing the exact `|| undefined` pattern in any of the 3 affected templates)
- `test_carte_relief_layers_present_and_reachable`

No existing test was weakened.

## Files changed

- `app/templates/diagnostic_unified.html`
- `app/templates/communes/diagnostic_section.html`
- `app/templates/carte.html`
- `app/routers/diagnostic.py`
- `tests/test_routes.py`
- `REPLY_CLIENT_REQUEST.md` (new §L, recap table row)
- `CLIENT_REMARK1_TOPOGRAPHY_REPORT.md` (new, this file)

## Client input required

`NONE FOR THIS REMARK` (the display bug is fixed with existing data; no new file or confirmation is required to close it).

One **optional** clarification was raised as a byproduct of the audit, not a blocker: whether to keep both contour layers (same 5 m interval, partially redundant) or retain only one — recorded in `REPLY_CLIENT_REQUEST.md` §L as "Optionnelle" priority.

## Result

`CLIENT REMARK 1 TOPOGRAPHY COMPLETE`
