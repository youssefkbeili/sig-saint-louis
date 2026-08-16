# CLIENT_REMARK5_PEUPLEMENT_REPORT.md — Replace Saint-Louis quartiers + unnamed localities with new client data

## Client remark

1. Replace `Quartiers — Saint-Louis` (old polygon layer) with the new client dataset `quartier_saint_louis`, displayed as **implantation ponctuelle** (points).
2. Replace `Localités / villages (sans nom, nouvelle donnée)` with `bati.shp`.

## New source audit

### `quartier_saint_louis`

| | |
|---|---|
| Geometry | **Point** (already — no polygon-to-point conversion needed) |
| CRS | **EPSG:32628**, declared in `.prj` (confirmed, not assumed) |
| Feature count | 33 |
| Fields | `Id`, `Nom_quarti`, `superficie`, `type_activ`, `type_zone`, `coord`, `x_coord`, `y_coor`, `y_coor_1`, `Nom_zone`, `NumeroTF`, `Nom_TF`, `POPULATION` |
| Name field | `Nom_quarti` |
| Population field | `POPULATION` (present for all 33) |
| Encoding | `.cpg` declares `1252`. One name (`Cité Niakh`) contains an accented character — GDAL/fiona's **default** read decoded it correctly (verified at the codepoint level: `name == 'Cité Niakh'` is `True`); the visually "broken" printed output in this terminal was, once again, this environment's known display artifact, not a real decode error — confirmed by comparing actual Unicode codepoints, not printed text, before trusting it. |
| Point-conversion method | **N/A** — source is already Point geometry, used as-is per instruction ("if source is already Point/MultiPoint: use the real points") |

**Old vs. new comparison** (done before replacing anything): the currently-active `population/quartiers-polygones.geojson` (33 Polygon features) has the **exact same** `Nom_quarti`/`POPULATION` schema and values as the new point dataset — same 33 names, zero population differences, verified by a full name-by-name and population-by-population diff. The only actual difference is geometry type (Polygon → Point). This is a clean, risk-free replacement — no data was gained or lost besides the geometry representation itself.

### `bati`

| | |
|---|---|
| Geometry | **Polygon** |
| CRS | **Not declared** (no `.prj`; `.qmd` also has an empty `<crs>` block) — see the CRS verification below |
| Feature count | 15,481 |
| Fields | `Id` only, and it is **not informative** (every one of the 15,481 features has `Id = 0`) |
| QGIS metadata | `.qmd` `<title>`/`<identifier>` = **"Tissu poly"** — a standard French GIS/urbanism term for a building-footprint ("urban fabric") polygon layer |
| Geometry validity | 15,473 valid, 8 invalid (0.05%) — repaired via `shapely.validation.make_valid()` in the derived copy only; 0 dropped (all 8 repaired successfully) |
| Area distribution | median 368.5 m², p10 35.1 m², p90 2,754.7 m², max 147,630 m² — a size spread consistent with individual building footprints (small huts through larger institutional buildings), not a uniform parcel/lot layer |

**Interpretation, not assumed from the filename**: the combination of (a) Polygon geometry, (b) the QGIS metadata title "Tissu poly" (urban building fabric), and (c) a building-scale area distribution is conclusive: **`bati.shp` represents building footprints.** Public label used: **"Bâtiments"** — not "Localités / villages", since the source data does not represent villages/localities at all.

**CRS verification (no `.prj` present)** — per the explicit safety protocol, the CRS was **not** blindly assumed:
1. `bati.shp`'s raw coordinate values (range: X 337,821–376,664, Y 1,750,912–1,781,873) are in the same numeric magnitude as every other confirmed-EPSG:32628 layer in this project (UTM 28N meters).
2. Reprojecting those raw bounds from EPSG:32628 → EPSG:4326 produces lon **-16.514 to -16.153**, lat **15.832 to 16.114** — landing almost exactly inside this project's already-documented agglomeration bounding box (lon [-16.53, -16.33], lat [15.83, 16.14]), with only a modest eastward extension.
3. Six sample building centroids, individually reprojected the same way, all land at real, geographically coherent points along the Saint-Louis coast (lat ~15.83–16.07) — not in the ocean, not on another continent, not at inverted/nonsensical coordinates. If the CRS assumption were wrong, this would not happen.
4. The confirmed-EPSG:32628 `quartier_saint_louis` point set (33 points) falls entirely *inside* `bati`'s reprojected extent — exactly the spatial relationship expected if both datasets share the same real-world area and the same CRS.

**Conclusion, recorded per instruction:** `SOURCE CRS NOT DECLARED — WORKING CRS INFERRED AS EPSG:32628 FROM VERIFIED SPATIAL OVERLAP`. No `.prj` was created or altered in the client's original folder — the CRS was only assumed inside this session's own conversion script, applied to a derived copy.

## Old layers replaced

- `population/quartiers-polygones.geojson` (Saint-Louis quartiers, Polygon) — **no longer used in the Peuplement page or Saint-Louis's commune Démographie page.** File left on disk untouched (still actively used by the separate, out-of-scope "Population" theme page — see below).
- `peuplement/localites.geojson` (372 unnamed locality footprints) — **deactivated from the Peuplement map.** File left on disk untouched; confirmed via a full codebase search that no route/template references it anymore.

## New active layers

- `app/static/data/peuplement/quartiers-saint-louis.geojson` (new, 33 Point features, EPSG:4326, properties: `Nom_quartier`, `Commune`, `Population`) — used by:
  - `app/routers/diagnostic.py` → global Diagnostic → Peuplement ("Quartiers — Saint-Louis", point, default ON)
  - `app/routers/commune_diagnostic_data.py` → Saint-Louis commune → Démographie ("Quartiers de Saint-Louis (avec population)", point) — updated for consistency, per instruction, since it represents the exact same settlement information; Gandon/Gandiol were **not** touched.
- `app/static/data/peuplement/batiments.geojson` (new, 15,481 Polygon features, EPSG:4326, no informative attributes preserved beyond geometry) — used by `app/routers/diagnostic.py` → global Diagnostic → Peuplement ("Bâtiments", default **OFF**, lazy-loaded).

## Saint-Louis point implementation

Not needed — the source (`quartier_saint_louis.shp`) is **already Point geometry**, so no centroid/representative-point derivation was performed. Had the source been Polygon, the instruction to prefer a representative/point-on-surface method over a raw centroid would have applied; it did not arise here.

## Deliberately out of scope (documented, not changed)

- **`app/routers/diagnostic.py`'s separate "Population" theme** (a different page from "Peuplement") still uses `population/quartiers-polygones.geojson` (polygon) alongside a second, already-existing synthetic point layer (`population/population-quartiers.geojson`, derived in an earlier wave from the same quartiers' embedded `x_coord`/`y_coor` attributes). The client's remark is specifically about the **Peuplement** page; "Population" is a distinct theme not mentioned in this remark, and it already has its own point representation for a different purpose (population-weighted display). Left untouched — this is also why the old polygon file could not simply be deleted from the repository.
- **`/carte/`** does not currently expose any Peuplement-equivalent group at all (confirmed by search — its only related group is the same separate "Population" group described above, using the same two files as the "Population" theme, not "Peuplement"). Per instruction to "only change views that actually expose the same data," no changes were made to `carte.py`.
- **`app/routers/communes.py`'s `COMMUNES["saint-louis"]["layers"]`** list (line 63) still references the old `population/quartiers-polygones.geojson`, but this list is dead configuration — confirmed via search that `commune_detail.html` never reads `commune.layers` at all (it was superseded by the Wave 4A Diagnostic/SVD/PCU redesign). Left untouched since it has zero runtime effect either way; noted here for completeness.
- **Gandon and Ndiébène Gandiol's own quartier layers** were not modified at all.
- No population/household/dwelling/occupancy/equipment figures were derived from the building-footprint layer, per explicit instruction — `bati`'s only real attribute (`Id`) is a constant, uninformative value, and no other number was invented.

## Browser validation

Performed with Playwright + headless Chromium against the running dev server.

- **Saint-Louis points**: **PASS** — 33 blue circle markers render at correct real-world positions (screenshot-verified against recognizable landmarks: the island, Rond-point, the airport); a popup was opened programmatically on the first point and showed exactly `Nom_quartier: TENDJIGUENE`, `Commune: Saint-Louis`, `Population: 5558` — real attributes only, nothing fabricated.
- **Gandon**: **PASS** — unchanged, still renders as green points, no regression.
- **Ndiébène Gandiol**: **PASS** — unchanged, still renders as orange points, no regression.
- **Bâtiments**: **PASS** — dense dark-grey building footprints render correctly aligned with the basemap and with the quartier points/commune boundary once activated; correct public label "Bâtiments" (not "Localités / villages"); toggle works.
- **Old locality layer removed**: **PASS** — confirmed absent from the rendered layer config (`localites.geojson` does not appear anywhere in the page).
- **Mobile (390px)**: **PASS** — layer names readable, no horizontal overflow, checkboxes usable.
- **Toggle test** (Bâtiments OFF→ON→OFF→ON): **PASS** — exactly 1 network request total for `batiments.geojson` regardless of how many times it was toggled (fetch-once-cache pattern, already built in Remark 2's `loadAndBuildLayer`, reused here with no new JS needed); no duplicate layers; no console errors.

## Performance

`batiments.geojson` is **6.95 MB** (15,481 features, none dropped, 8 geometries repaired) — the single heaviest GIS file in the project. Per instruction, it is **not** loaded by default: `"defaultChecked": False` makes it lazy-load only on first activation, reusing the exact fetch-once/cache mechanism already built for Occupation du sol 2020 in the prior remark. No geometry simplification was applied — this keeps every building's real outline recognizable, and lazy-loading alone already prevents it from affecting the page's default load time, so simplification was judged not required (per instruction: "if geometry simplification is required" — it wasn't, since lazy-loading already solves the stated concern). This is documented here rather than applied silently.

## Automated tests

**124 PASS / 0 FAIL** (`pytest tests/ -q`) — 118 pre-existing (unaffected) + 6 new:
- `test_peuplement_old_localites_layer_removed`
- `test_peuplement_saint_louis_uses_new_point_source`
- `test_peuplement_batiments_present_and_lazy`
- `test_peuplement_gandon_gandiol_preserved`
- `test_peuplement_new_assets_exist_and_are_valid` (asserts exactly 33 Point features and exactly 15,481 building features on disk)
- `test_commune_saint_louis_demographie_uses_new_point_source`

No existing test was weakened.

## Client-request update

The previous request for "noms des localités/villages pour les 372 entités" (`REPLY_CLIENT_REQUEST.md` §J) has been **removed**, per instruction: the layer it supported (`peuplement/localites.geojson`) is no longer used anywhere in the active site (confirmed by a full codebase search before removing the request, not assumed). A new §P records the completed replacement and explicitly states this request is withdrawn because it no longer supports anything active — not because it was fulfilled. The unrelated, still-valid request for Ndiébène Gandiol's 7 missing quartier-population values (§J, recap table) was **kept**, since it concerns a completely different, still-active dataset.

## Client input required

`NONE FOR THIS REMARK` — both new datasets were successfully verified and integrated. `bati`'s CRS was inferred with very high confidence from multiple independent lines of spatial evidence, not guessed.

## Files changed

- `app/routers/diagnostic.py`
- `app/routers/commune_diagnostic_data.py`
- `app/static/data/peuplement/quartiers-saint-louis.geojson` (new)
- `app/static/data/peuplement/batiments.geojson` (new)
- `tests/test_routes.py`
- `REPLY_CLIENT_REQUEST.md` (new §P, §J bullet removed, recap table updated)
- `CLIENT_REMARK5_PEUPLEMENT_REPORT.md` (new, this file)

**Not deleted, left in place on disk (per instruction):** `app/static/data/population/quartiers-polygones.geojson` (still used by the separate Population theme), `app/static/data/peuplement/localites.geojson` (now genuinely orphaned — deactivated, not deleted).

## Result

`CLIENT REMARK 5 PEUPLEMENT COMPLETE`
