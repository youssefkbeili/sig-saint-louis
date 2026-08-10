# PHASE3_WAVE2_REPORT.md — Wave 2: GIS Data Integration

Baseline: `PROJECT_ANALYSIS.md`, `REPLY_CLIENT.md`, `PHASE3_WAVE1_REPORT.md`. Wave 1 was not redone. No Wave 3+ work (villages, bassins versants, énergie/économie layers, corridors, commune architecture, PostGIS, buffer/spatial tools) was started. **All original client GIS source files in `reply client/` were only read, never modified.**

---

## Source data used

| Dataset | Source path | CRS | Characteristics | Original size |
|---|---|---|---|---|
| Occupation du sol 2020 | `reply client/occupation du sol 2020 SL/Occupation du sol 2020.shp` | EPSG:32628 (confirmed) | 575 features (571 Polygon + 4 MultiPolygon), 17 `NOM` classes, `.cpg` declares UTF-8 but actual bytes are cp1252 (confirmed) | `.shp` 9.3 MB, `.dbf` 418 KB |
| MNT (raw) | `reply client/Carte_MNT_Topographie/Carte_MNT_Topographie/MNT.tif` | EPSG:32628 | 712×1140 px, 32-bit float, ~30.19 m resolution, NoData `-1000000000` | 3.25 MB |
| MNT (filled) | `.../MNT_filled.tif` | EPSG:32628 | Same dimensions, NoData tag `-99999`, valid elevation −4.8 to 36.8 m after masking | 3.25 MB |
| CN_5m contours | `.../Courbes_de_niveau/CN_5m.shp` | EPSG:32628 (confirmed) | 8,519 LineString features, fields `ID`/`ELEV` | `.shp` 3.33 MB |

**Correction to `REPLY_CLIENT.md`, discovered during "verify the source again":** the Occupation du sol 2020 shapefile's true bounding box (confirmed independently via `fiona`'s own `.bounds`, not just the conversion code) is lon [-17.00, -16.00], lat [15.00, 16.56] — **substantially larger than the 3-commune study zone** (lon [-16.53, -16.33], lat [15.83, 16.14]). The earlier Phase 2A note that its extent was "consistent with the 3-commune study area" was an assumption based on feature count alone, never numerically checked — now corrected. This doesn't block integration (the layer still displays correctly, showing extra surrounding context), but it's a materially different fact than previously stated.

---

## Conversion performed

### 1. Occupation du sol 2020
- Read via `fiona` with an explicit `encoding="cp1252"` override (ignoring the shapefile's incorrect `.cpg` declaration) — this alone fixed every accented category name (e.g. "Culture maraich�re" → "Culture maraichère").
- Reprojected every coordinate from EPSG:32628 to EPSG:4326 using `pyproj.Transformer` (`always_xy=True`), verified against an independent corner-coordinate cross-check before trusting the full conversion.
- Dropped all GIS-internal fields (`OBJECTID_1`, `OBJECTID`, `Shape_Leng`, `Shape_Area`, `PAYS`, `layer`, `path`); kept only `NOM` → renamed to `categorie`.
- **Problem found and fixed:** the first conversion attempt produced a 24.6 MB file — investigated and found the source polygons are extremely dense (~580,000 total vertices, one single feature has 85,594 points). Applied Douglas-Peucker simplification (`shapely.simplify`, tolerance 10 m, `preserve_topology=True`) in the original metric CRS *before* reprojecting, which is the geometrically correct order (simplification tolerance is meaningless in degrees). Verified area distortion from simplification is 0.0038% — negligible.
- 2 features had minor self-intersections after reprojection; repaired with `buffer(0)` (a standard, non-destructive topology fix). Final output has 0 invalid geometries.

### 2. MNT hillshade
- No GDAL/rasterio available in this environment — read the raw pixel array from `MNT_filled.tif` directly via PIL (confirmed it correctly reads the 32-bit float GeoTIFF band).
- Masked NoData (`< -1000`, safely covering both the `-99999` and `-1000000000` sentinel conventions found across the two files — real elevations never go below -13 m here).
- Computed a standard hillshade (azimuth 315°, altitude 45°) from numerical gradients using the raster's true pixel spacing (~30.19 m), with a 2nd–98th percentile contrast stretch applied only to display (this is flat coastal terrain, 0–32 m relief, so raw hillshade clusters in a narrow gray band — the stretch is a legibility enhancement, not a change to any underlying value).
- Output as an RGBA PNG with full transparency over NoData areas (so ocean/river doesn't render as an opaque block over the basemap).
- **Georeferencing approach (documented, as instructed, before proceeding):** no GDAL/rasterio means no true raster warp was performed. Instead, the 4 corners of the raster's UTM bounding box were each reprojected to lon/lat individually, and the enclosing axis-aligned box was used as a Leaflet `imageOverlay` bounds. This is a standard, well-understood simplification for a single static relief backdrop image (not a scientific measurement layer) — it introduces a small, documented approximation from UTM-zone convergence at this longitude, rather than a full pixel-by-pixel warp. **Validated:** the resulting bounds `[[15.828733, -16.530742], [16.141098, -16.327712]]` align almost exactly with the site's own existing `limite-communale.geojson` extent `[[15.8287, -16.5285], [16.1411, -16.3289]]` — confirming no meaningful shift.

### 3. CN_5m contours
- Reprojected EPSG:32628 → EPSG:4326 the same way as above, plus a light 2 m simplification tolerance (small relative to the 5 m contour interval).
- **Problem found and fixed:** rounding coordinates to 6 decimal places initially collapsed 1,301 of 8,519 lines to fewer than 2 distinct points. Fixed by rounding to 7 decimals with an automatic fallback to full precision for any feature that still degenerated.
- **Residual, investigated and accepted:** 411 of 8,519 features (4.8%) remain "invalid" per `shapely` even at full precision — investigated directly and confirmed every one of them is a genuine **zero-length degenerate artifact already present in the source data** (all coordinates in the line are identical, no NaN values). These render as an invisible point, not a visual defect, and were not dropped since removing data wasn't authorized and they cause no functional harm.
- `ELEV` values preserved exactly, renamed to `elevation` in the output property.

---

## Files added

- `app/static/data/occupation-sol-2020/occupation-du-sol-2020.geojson` (1.7 MB)
- `app/static/data/diagnostic/topographie/courbes-niveau-5m.geojson` (3.5 MB)
- `app/static/img/topographie/hillshade-mnt.png` (868 KB)
- `app/static/data/topographie-mnt/MNT.tif` (3.2 MB, copy of client original)
- `app/static/data/topographie-mnt/MNT_filled.tif` (3.2 MB, copy of client original)
- `PHASE3_WAVE2_REPORT.md` (this file)

## Files modified

- `app/routers/diagnostic.py` — added the new Occupation du sol 2020 layer (with `categoryField`/`categoryColors`) to the `occupation` section; added the hillshade image layer and CN_5m line layer to the `topographie` section; updated topographie's `subtitle`/`content`/`messages` to mention the new data (existing 13,762-feature contour layer and its content were **not removed**).
- `app/templates/diagnostic_unified.html` — added an `image` layer type (renders via `L.imageOverlay`, bypassing the GeoJSON fetch path entirely) and a `categorized` styling path (per-feature color lookup by a configurable property, used only when a layer defines `categoryColors`); added an inline legend block for any layer with `categoryColors`. Every other existing layer type (point/line/polygon with a single color) is rendered by the exact same code path as before — confirmed via the geologie/risques/transport theme pages, which have no `categoryColors`/`image` config and were unaffected.
- `app/templates/ressources.html` — added 2 new download entries (MNT raw + filled rasters) under a new "Modèle numérique de terrain (MNT)" subsection, following the exact existing download-button pattern.

No other application files were touched. No orphaned templates were deleted. No commune, equipment, or advanced-GIS code was touched.

---

## GIS integration — where each new layer appears

| New asset | Appears at |
|---|---|
| Occupation du sol 2020 (`occupation-du-sol-2020.geojson`) | `/diagnostic?section=occupation` — as an additional togglable layer in the existing "Occupation du sol" theme map, alongside (not replacing) the 10 existing per-category layers. Own inline 17-item legend. |
| Hillshade (`hillshade-mnt.png`) | `/diagnostic?section=topographie` — as a new togglable image overlay in the existing "Topographie" theme map, alongside the existing contour layer. |
| CN_5m contours (`courbes-niveau-5m.geojson`) | `/diagnostic?section=topographie` — as an additional togglable line layer in the same map. |
| MNT.tif / MNT_filled.tif (raw downloads) | `/ressources` — new "Modèle numérique de terrain (MNT)" download section, following the existing PDF/JPEG download pattern. |

**Not added to `/carte/`** in this wave — the task scope named `/diagnostic`, the Topographie/Occupation du sol themes, `/carte/`, legends, popups, and homepage as places to *check*, not necessarily to duplicate every new layer into. Since `/carte/`'s `LAYER_GROUPS` structure doesn't currently have an "occupation-sol" or "topographie" group at all (a pre-existing scope gap tracked as R10 in `PROJECT_ANALYSIS.md`), adding these 3 new layers there would have meant creating 2 new group categories on the flagship map — a larger structural change than "integrate the already-validated datasets" calls for. Deferred to whenever R10 itself is addressed, to avoid duplicating configuration in two places per the task's own "do not duplicate configuration unnecessarily" instruction.

---

## Performance

| Asset | Original source size | Generated web size | Feature count | Simplified? | Accuracy impact |
|---|---|---|---|---|---|
| Occupation du sol 2020 | 9.3 MB (`.shp`) | **1.7 MB** | 575 (unchanged) | Yes — 10 m tolerance in UTM meters | 0.0038% area change (negligible) |
| CN_5m contours | 3.33 MB (`.shp`) | **3.5 MB** | 8,519 (unchanged) | Yes — 2 m tolerance | Vertex count reduced from 178,434 to 112,496 (−37%); `ELEV` values exact, untouched |
| Hillshade | 3.25 MB (`.tif`, not directly comparable — raster vs. image) | **868 KB** (PNG) | — | Contrast-stretched for legibility (display-only) | No underlying data altered |
| MNT.tif / MNT_filled.tif (download only) | 3.25 MB each | 3.25 MB each (verbatim copies) | — | No — client explicitly said these only need to be downloadable | None — bit-identical to source |

**Context for "is this too big for mobile":** the site already serves a 6.08 MB GeoJSON (the existing `courbes-niveau.geojson`, 13,762 features) and static theme images ranging 1.8–5.5 MB each (`app/static/img/cartes/*.jpg`) without prior complaint. Every new asset in this wave (1.7 MB, 3.5 MB, 868 KB) is at or below that existing precedent — no asset introduced here is the heaviest thing the site serves.

---

## Validation

| Dataset | Result |
|---|---|
| **Occupation du sol 2020** — feature count preserved (575), 17 expected classes present, valid geometries (0 invalid after 2 minor buffer(0) repairs), correct French encoding (verified: "Culture maraichère", "Plantation forestière", "Vasière" all render correctly), correct geographic position (corner cross-check independent of conversion code) | **PASS** (with the corrected, wider-than-expected study-zone coverage noted above — not a defect, a corrected fact) |
| **MNT** — relief aligns geographically with the study zone (hillshade bounds match the site's own commune-boundary extent almost exactly), no obvious shift, elevation rendering sensible for known-flat terrain, NoData areas fully transparent | **PASS** (georeferencing approximation documented, not a full raster warp — see Conversion section) |
| **CN_5m** — contours align with the same source/CRS as the MNT (bbox matches to within thousandths of a degree), `ELEV` values preserved exactly, no coordinate shift, map remains usable at 3.5 MB | **PASS** (411/8,519 pre-existing zero-length degenerate artifacts documented and accepted as harmless, not fixed by inventing new coordinates) |

---

## Regression tests

| Route/page | Result |
|---|---|
| `GET /` | 200, Wave 1 homepage cards still present |
| `GET /diagnostic?section=occupation` | 200, all 10 existing category layers + new "Occupation du sol 2020" layer + 17-item legend, no JS errors in server log |
| `GET /diagnostic?section=topographie` | 200, existing 13,762-feature contour layer + new hillshade image overlay + new CN_5m layer, all present |
| `GET /diagnostic?section=urbanisation` | 200, Wave 1's blue-family empreinte styling still intact |
| `GET /carte/` | 200, unaffected by this wave |
| `GET /communes/`, `/communes/saint-louis` | 200 |
| `GET /equipements/gandon` | 200 |
| `GET /ressources` | 200, new MNT download links present alongside all pre-existing download links |
| `GET /risques/inondation` | 200 |
| `GET /static/data/occupation-sol-2020/occupation-du-sol-2020.geojson` | 200, served directly by the existing `StaticFiles` mount, no new backend route needed |
| `GET /static/data/diagnostic/topographie/courbes-niveau-5m.geojson` | 200 |
| `GET /static/img/topographie/hillshade-mnt.png` | 200 |
| `GET /static/data/topographie-mnt/MNT.tif` | 200 |
| Server log across all requests | Clean — zero errors/tracebacks |
| `app.main:app` import | Clean import after all `diagnostic.py` edits |

No headless browser was available in this environment to check the browser console directly; verification was done by rendering each page server-side and inspecting the exact emitted HTML/JS for the new code paths (confirmed present and syntactically consistent with the existing, already-working JS in the same file).

---

## Problems discovered

1. **Occupation du sol 2020's real extent is much larger than previously documented** (corrected above) — not a blocker, just a factual correction to `REPLY_CLIENT.md`.
2. **The source shapefile's `.cpg` encoding declaration is simply wrong** (says UTF-8, is actually cp1252) — already flagged in `REPLY_CLIENT.md`, now concretely worked around during conversion.
3. **Naive coordinate rounding can silently destroy line geometries** — discovered while converting CN_5m; fixed with a fallback mechanism, documented above so future conversions (Wave 3's other datasets) don't repeat it blind.
4. **411 zero-length degenerate line artifacts pre-exist in the CN_5m source data** — not introduced by this conversion, confirmed harmless, not silently dropped.
5. **No GDAL/rasterio available in this environment** — the hillshade georeferencing uses a documented corner-based approximation rather than a full raster warp; flagged as a limitation, not hidden.

---

## Deferred work (Wave 3+, not started)

- Adding occupation-du-sol/topographie groups to `/carte/`'s `LAYER_GROUPS` (would touch pre-existing scope gap R10 in `PROJECT_ANALYSIS.md`).
- `CN_1m` (too dense, per instructions) and `CN_10m` (broken/missing companion files, per `REPLY_CLIENT.md`) — neither was touched.
- Villages/localités, zones de conservation, énergie/économie project layers, corridors, bassins versants — all still pending client data completeness per `REPLY_CLIENT.md`.
- Commune architecture redesign (Diagnostic → SVD → PCU/PCUI).
- Buffer/query/spatial-analysis/export tooling.
- Reconciling the pre-existing "14 vs. 18 catégories" text inconsistency (R9 in `PROJECT_ANALYSIS.md`) — out of scope for this wave, not touched.

---

## Result

`WAVE 2 COMPLETE — READY FOR REVIEW`

All 3 named datasets (Occupation du sol 2020, MNT/hillshade, CN_5m) were converted, validated, integrated, and regression-tested with no blockers. All original client source files remain untouched in `reply client/`. Stopping here per instructions; not proceeding to Wave 3 automatically.
