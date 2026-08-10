# REPLY_CLIENT.md — Phase 2: Official Client Requirements & New GIS Data Baseline

Supersedes `CLIENT_UPDATE_PLAN.md` (renamed/restructured). Baseline architecture reference remains `PROJECT_ANALYSIS.md` (commit `d6a038f`). **No application code was modified in producing this document.**

---

## Sourcing note — read before using this document

`Commentaires_SIG WEB.docx` is an **external client document**, provided outside this repository. It is not expected to be present locally, and its absence from the repo/`reply client/` folder is not a data gap — Remarks 1–7 below have already been transcribed from it into this baseline and are treated as confirmed client requirements.

Separately, three other real DOCX files were provided and are available locally in `reply client/`:

| File | Content |
|---|---|
| `Commentaires Livrable SVD GTO COMETE LJ_avril26.docx` | GTO committee comments on the **SVD/PCUI report** (urbanism methodology) |
| `OBSERVATIONS DU CONSULTANT1.docx` | ADM consultant's comments on **SVD report structure** — corroborates the Diagnostic→SVD→PCU/PCUI pyramid used below |
| `QUESTIONS_POUR_AVANCER_TY.docx` | A website-specific Q&A with the client |
| `SVD_Saint-Louis_12-05.docx`, `SVD_Gandon 12-05 1.docx`, `SDV Gandiole 12-05.docx` | Full SVD narrative reports per commune (50–63 MB each) — not opened; relevant later as raw content source for the SVD section of the commune redesign |

Every requirement in this document is tagged with its actual origin, using these categories:

- **[CLIENT-DOC-EXTERNAL]** — requirement explicitly supplied from the client's external feedback document (`Commentaires_SIG WEB.docx`).
- **[DOCX-CONFIRMED]** — independently verified in a locally available client DOCX (`QUESTIONS_POUR_AVANCER_TY.docx`, `OBSERVATIONS DU CONSULTANT1.docx`, or the SVD-comments docx).
- **[DATA-CONFIRMED]** — verified directly from delivered GIS data (shapefiles/rasters actually inspected).
- **[INFERRED]** — a technical interpretation or recommendation, not an explicit client instruction.
- **[MISSING-DATA]** — required data not currently available.

---

## Confirmed Client Requests

### From `QUESTIONS_POUR_AVANCER_TY.docx` — [DOCX-CONFIRMED]

- Commissioning organization: **Agence de Développement Municipal (ADM)**, for the PCU/PCUI project under SERRP.
- Logos: ADM and COMETE confirmed as the right ones to use; a graphic charter proposal was "provisionally validated."
- No domain name or hosting reserved yet — open for recommendation.
- Site objective: an online-consultable version of the diagnostic/PUD, per the ToR ("Une version consultable en ligne du PUD devra être proposée").
- Audience: the 3 communes (Saint-Louis, Gandon, Ndiébène Gandiole), ADM, ADC (Agence de Développement Communal de Saint-Louis), and deconcentrated technical services.
- Site will be **entirely public**, no authentication.
- Content will receive **regular updates**, not a frozen one-time publication.
- Language: **French, and Wolof if possible** — not French-only as currently built.
- Raw data downloads wanted: **both PDF and shapefiles**, not PDF-only.
- A statistics/indicators dashboard is explicitly wanted.
- A contact form is wanted — specifically **to let visitors request additional information and layers**, not just general contact.
- Commune structure confirmed: **"une page globale après on pourra basculer dans les communes avec section dédiée pour chacune des trois communes"** — i.e., one global page, then dedicated per-commune sections. This directly confirms the population-structure request (Remark 6 below).
- Official CRS confirmed: **WGS_1984_UTM_Zone_28N (EPSG:32628)**; a second, incorrect CRS present in some of the client's own files was acknowledged as unintentional and to be corrected.
- Known file-hygiene issues acknowledged by the client: duplicate shapefiles elsewhere in their archive, and stray ArcGIS `.sr.lock` files safe to delete.
- Missing topographie PDF and incomplete equipment PDFs acknowledged — client will supply/generate them.
- Urban-footprint areas (ha) for 2017/2020/2024 will be supplied.
- Equipment shapefiles' attribute richness (school capacity, hospital beds, etc.) is **not guaranteed** ("on n'a pas forcément toutes les infos").
- Site must perform acceptably on **slow mobile connections** (Senegalese context) and ideally as a **PWA**.
- Client wants, eventually, as many urbanism-plan layers displayable simultaneously as possible, in the spirit of a PAU (plan d'aménagement urbain).
- Statistical charts (bar/pie) are explicitly wanted alongside maps.
- **The full source code will be delivered to the end client** — this is a handoff deliverable, not just a hosted service.
- Sentinel-2 imagery's open-license status was **not** formally confirmed by the client ("Non") — a latent caution for anything derived from it, though this predates the current site.
- TIN/raster topography files should be converted into a usable DEM and shown as an online relief map; the raw raster itself only needs to be **downloadable**, not necessarily rendered live.

### From the client's external feedback document (`Commentaires_SIG WEB.docx`) — [CLIENT-DOC-EXTERNAL]

| # | Remark | Detail |
|---|---|---|
| R1 | Homepage title / description | **[IMPLEMENTED]** Exact new H1 confirmed by the client: "ÉLABORATION DE TROIS PLANS INTERCOMMUNAUX D'URBANISME DANS L'AGGLOMÉRATION DE SAINT-LOUIS DANS LE CADRE DU SERRP : SAINT-LOUIS, GANDON ET NDIEBENE GANDIOLE" (verbatim, including the client's "NDIEBENE GANDIOLE" spelling without accent). Also confirmed and implemented in an earlier turn: the hero subtitle/description paragraph. See `CLIENT_REMARK1_IMPLEMENTATION_REPORT.md` for full detail, including a note on the hero kicker line's wording. |
| R2 | Rename "Thèmes du diagnostic" | **[IMPLEMENTED]** New label confirmed by the client: "Thèmes des plans intercommunaux". Also confirmed alongside this remark: two new rubriques ("Développement économique & énergie" and "Gouvernance et intercommunalité"), both already implemented (see `CLIENT_REMARK3_IMPLEMENTATION_REPORT.md`). The accompanying phrase "Ajouter aussi à la rubrique urbanisation" remains **[CLIENT CLARIFICATION REQUIRED]** — its intended meaning could not be determined unambiguously; existing Urbanisation content was preserved unchanged. Note: the client's own document numbers this remark "3"; it was transcribed as R2 in this table during the original Phase 2A pass — see the implementation report for detail. |
| R3 | Logo order | Sénégal flag → ADM → COMETE → RINA. Current site shows only ADM, COMETE, Sénégal (no RINA). RINA is confirmed as a real partner ("RINA Consulting S.p.A.", per `OBSERVATIONS DU CONSULTANT1.docx` letterhead — **[DOCX-CONFIRMED]** cross-reference), but no RINA logo file has been supplied yet **[MISSING-DATA]**. |
| R4 | Remove an equipment-map symbol | A specific symbol on the equipment map should be removed. Which one, to be confirmed by the client. |
| R5 | Urbanisation empreinte styling | The 2017/2020/2024 urban-footprint layers should use 3 highly contrasted shades of **one** color family, with **no transparency**. Current styling uses 3 unrelated hues (brown/orange/pink) with `fillOpacity` 0.3–0.45 **[DATA-CONFIRMED, current-state]**. |
| R6 | Population structure | One global population map for all 3 communes, then per-commune maps within each commune section. **Also independently confirmed [DOCX-CONFIRMED]** by `QUESTIONS_POUR_AVANCER_TY.docx` — already close to a match architecturally; the gap is data completeness (Gandon/Gandiol lack population figures **[MISSING-DATA]**), not structure. |
| R7 | Commune architecture redesign | Each commune page restructured into **I. Diagnostic → II. SVD → III. PCU/PCUI**, each with detailed sub-sections. **Also structurally corroborated [DOCX-CONFIRMED]** by `OBSERVATIONS DU CONSULTANT1.docx`, which independently describes the same diagnostic → vision → axes stratégiques → programmes de développement pyramid for SVD documents in general. |
| Group C | New themes | Carte de peuplement (quartiers + villages), bassins versants, énergie, activités économiques et corridors, occupation du sol 2020, topographie/MNT. |

---

## New Data Provided

All items below are **[DATA-CONFIRMED]** — directly inspected, not assumed — unless marked **[INFERRED]**.

### Occupation du sol 2020 SL

- **"SL" verified = "Saint-Louis" (the study zone)** **[DATA-CONFIRMED]**, not guessed: the file sits alongside two national map-sheet tiles it was clearly clipped from (`occsol_2020_LOUGA_ND-28-XX`, 678 features; `occsol_2020_SAINT-LOUIS_NE-28-II`, 291 features), and its own 575-feature count is consistent with a merge of those two tiles.
- Format: ESRI Shapefile + `.qgz` QGIS project. `.shp` 9.3 MB, `.dbf` 418 KB.
- CRS: **EPSG:32628** (confirmed, matches client's official CRS).
- Geometry: 571 Polygon + 4 MultiPolygon = 575 features.
- Category field `NOM`, 17 classes: Mare, Steppe, Culture maraîchère, Plaine inondable, Sol nu, Culture pluviale, Mangrove, Culture irriguée, Prairie aquatique, Dune, Tanne, Carrière/Mine/Infrastructure, Plantation forestière, Vasière, Savane, Lac, Cours d'eau.
- **Encoding bug confirmed**: `.cpg` declares `UTF-8`, but the actual `.dbf` bytes are Windows-1252/Latin-1 — any UTF-8-trusting reader (including this analysis) garbles accented values (e.g. "Culture maraîchère" → "Culture maraich�re"). Same root-cause family as the encoding bug already tracked as R5 in `PROJECT_ANALYSIS.md`. **Conversion must force `encoding='cp1252'`, ignoring the incorrect `.cpg`.**
- No invalid/null geometries detected.
- Scope: **[DATA-CONFIRMED — corrected in Wave 2]** cross-checked directly via `fiona`'s own bounding-box computation (independent of any conversion code): the true extent is lon [-17.00, -16.00], lat [15.00, 16.56] — **substantially larger than the 3-commune study zone** (lon [-16.53, -16.33], lat [15.83, 16.14]), not tightly clipped to it as originally assumed here. It behaves as a regional map-sheet-scale extract rather than a commune-clipped one; the "SL" naming still correctly refers to Saint-Louis as the study area this extract was prepared for, but the polygon data itself extends well beyond the 3 communes.
- Uses a **different classification scheme** (17 `NOM` categories) than the current site's occupation-du-sol data (14–18 categories depending which page you read — see `PROJECT_ANALYSIS.md` R9). Not a 1:1 replacement.
- **[INFERRED] Recommendation:** add as a new dated layer ("Occupation du sol 2020"), enabling a future occupation-du-sol time comparison — same pattern the site already uses for urban footprint (2017/2020/2024).

### Carte_MNT_Topographie

| Property | `MNT.tif` | `MNT_filled.tif` |
|---|---|---|
| Type | Raster DEM, single band, 32-bit float | Void-filled DEM |
| Dimensions | 712 × 1140 px | Same |
| Resolution | ~30.19 m × 30.19 m **[DATA-CONFIRMED: pixel scale]** / **[INFERRED: source]** consistent with a public ~30 m DEM (e.g. SRTM/ASTER), resampled — not a bespoke survey | Same |
| CRS | **EPSG:32628** (GeoKeyDirectory present, tiepoint origin 336321.2, 1785001.7 — UTM 28N meters) | Same |
| Extent | ~21.5 km × 34.4 km — consistent with the client's statement that the source TIN covers the whole Département de Saint-Louis (5 communes) | Same |
| NoData | `-1000000000` sentinel | Same convention |
| Elevation range | **-6 m to 32 m** (mean 6.4 m, 68% valid pixels) | **0 m to 31.5 m** (mean 7.0 m, 68.75% valid), negatives clipped and gaps filled |
| File size | 3.25 MB | 3.25 MB |
| Leaflet-compatible? | **No** — raw `.tif` cannot be used directly in Leaflet |
| Preprocessing needed | Hillshade image (fastest, matches the site's existing static-image pattern) or elevation-class GeoJSON polygons; full tile pyramid is likely overkill at this extent |

Also delivered: `Courbes_de_niveau/CN_1m.shp` (43,624 features), `CN_5m.shp` (8,519 features, clean, `ID`/`ELEV` fields only), `CN_10m.shp` (**broken — see Missing/Broken Data below**). All readable files confirmed **EPSG:32628** — not affected by the geographic-degrees/UTM mismatch the client flagged for a different, older contour file.

**[DOCX-CONFIRMED] + [INFERRED] Recommendation:** publish the raw `.tif` files as downloads (client confirmed via `QUESTIONS_POUR_AVANCER_TY.docx` this is sufficient — "téléchargeable"), build the interactive relief view from a hillshade image, and add `CN_5m` as a cleaner alternative to the existing 13,762-feature contour layer (`CN_1m` is likely too dense for client-side Leaflet without simplification — **[INFERRED]**).

### Bonus data (found during inspection, directly relevant to Group C themes)

| File | Features | Notes |
|---|---|---|
| `localite.shp` | 372 | Village/settlement footprints, whole study zone. All labeled generically `NOM = "Localité"` — **no individual village name field**. |
| `zone de conservation.shp` | 44 | `Categorie`: "Protection Naturel" (43), "Protection Patrimoniel" (1, likely the UNESCO Saint-Louis island zone). Entirely new theme, not on the site today. |
| `Nouveau dossier/Gandon/*.shp` (22 files) | varies | `occupation du sol Gandon.shp` (144), `Quartier Gandon.shp` (36 named points), `Lotissements autorisés.shp` (874), `Zone d'habitation (ZH)` (142), `Zone pastorale (ZP)` (36), `ZAPA`/`ZAPE` (45/66). **Energy/infrastructure**: `Nouvelle Centrale a Gaz`, `Substation Senelec`, `Tracé Gazoduc RGS`. **Economic**: `ZES`, `Future Zone Economique Specialisée`, `Projets Économiques`, `Projets Immobiliers, Hôteliers`. Plus `Réserve spéciale de faune de Guembeul` (×2), `Forêt classée de Rao`, `Fleuve`, `Canal du Gandiolais`. |
| `Nouveau dossier/Ndiebene Gandiol/*.shp` (11 files) | varies | `Occupation du sol final NG.shp` (151), `Quartiers.shp` (23 named points), `ZH`/`ZP`/`ZAPA`/`ZAPE`, `Zone de protection Ecologique (ZPE)`, `Usine d'exploitation du Zircon CEN_HMC` (mining), `Projets Économiques, Agricoles & Agro-industriels` (7), `Projets Équipements & Services` (4). |
| `Equipements socio economiques/Ndiebene Gandiol/Equipements.shp` | 50 | Real, **commune-specific** equipment data with rich categories (École, Case de santé, Mosquée, Marché, Lycée, etc.) — directly usable to fix the equipment data-integrity bug already tracked as **R4 in `PROJECT_ANALYSIS.md`**, at least for this commune. |
| `Occupation du sol 2024.shp` | 916 | `DN`/`Nature` fields typical of raster→vector conversion; only 343/916 features have `Nature` populated — see Missing/Broken Data. |
| `Zone d'habitation existante.shp` / `...2025.shp` | 563 / 556 | Fully populated `Nature = "Empreinte urbaine"` — possible replacement candidates for the current `evolution/empreinte-2024.geojson` (215 features), pending client confirmation of which is authoritative. |
| `Future autoroute.shp` | 1 | Opens correctly — a planned highway corridor. |

---

## Missing / Broken Data

| Item | Status |
|---|---|
| Bassins versants | **MISSING** — not found anywhere in the delivery |
| Village names for `localite.shp`'s 372 features | **MISSING** — only a generic category label exists, no per-feature name |
| Population/quartier figures for Gandon and Gandiol | **[DATA-CONFIRMED — corrected in Wave 3]** No longer missing for most of it: `Nouveau dossier/Gandon/Quartier Gandon.shp` (36 features) actually contains named quartiers **with real population figures** — 33 for Gandon, plus 3 unexpected Ndiébène Gandiol records (`Mbambara`, `Gantour`, `Keur Barka`, none duplicating the separate 23-feature Gandiol `Quartiers.shp`). Combined with that standalone file, Gandiol has 26 named quartiers total, 7 of which still have a null population value. Saint-Louis's `population/quartiers-polygones.geojson` was also found to already carry a `POPULATION` field per quartier, previously unnoted. Remaining gap: none of the underlying source files' geometry types match across communes (Saint-Louis = polygons, Gandon/Gandiol = points). |
| Équipements socio-économiques for Gandon | **MISSING** — the delivered folder (`Equipements socio economiques/Gandon/`) is **confirmed empty**, 0 files |
| Full énergie coverage for Saint-Louis and Gandiol | **MISSING** — only 3 point features exist, Gandon commune only |
| Full activités économiques coverage for Saint-Louis | **MISSING** — project footprints exist for Gandon and Gandiol only |
| Working `Boucle de Gandiolais.shp` | **BROKEN, both delivered copies** — root copy missing `.shx`/`.prj`/`.cpg`; `Nouveau dossier` copy has a corrupted `.dbf` header. Needs re-export. |
| Complete `CN_10m.shp` | **BROKEN** — `.shp`/`.dbf` present, but no `.shx`/`.prj`/`.cpg`. Unreadable as delivered. Needs re-export. |
| `Occupation du sol 2024.shp` full attribution | **PARTIALLY BROKEN** — 573 of 916 features have null `Nature`/`DN`; needs client clarification before use |
| PCU/PCUI zonage | **MISSING** |
| PIP (programme d'investissement prioritaire) | **MISSING** |
| ZAC/ZAD | **MISSING** (not the same as the ZES/ZAPA/ZAPE zones that were supplied) |
| Servitudes | **MISSING** |
| Règlement d'urbanisme | **MISSING** |
| Évaluation environnementale stratégique (EES) | **MISSING** |
| Atlas cartographique | **MISSING** |
| SVD content (vision/axes/programmes), web-ready | **MISSING as structured content** — raw narrative likely exists inside the 3 large SVD `.docx` reports (50–63 MB each), not yet extracted |
| RINA logo file | **MISSING** |
| Exact new homepage title/description text (R1) | **RESOLVED** — client-confirmed wording received and implemented |
| New label to replace "Thèmes du diagnostic" (R2) | **MISSING** |
| Specification of which equipment symbol to remove (R4) | **MISSING** |
| `Commentaires_SIG WEB.docx` itself | **MISSING** — see Sourcing note at top |

Known duplicate/ambiguous files acknowledged by the client already (Terrase/Terrasse marine sableuse, Eaux_permanentes variants, Sur_sable_silicieux variants, stray `.sr.lock` files) — cleanup already authorized by the client, not blocked on a question.

---

## Questions for Client

1. ~~Exact new homepage title and description text (R1)?~~ **ANSWERED** — implemented, see R1 row above.
2. Exact new label to replace "Thèmes du diagnostic" (R2)?
3. Please supply the official RINA logo file (R3)?
4. Which specific equipment-map symbol should be removed (R4)?
5. Confirm the target color family for the urbanisation empreinte layers (R5) — a hex reference, or should 3 shades be proposed for approval?
6. Should "Carte de peuplement" be a new top-level nav item, or folded into the existing Diagnostic → Population theme?
7. Full village-name list for the 372 `localite.shp` features, or a corrected shapefile with names attached?
8. Population/quartier figures for Gandon and Gandiol (currently Saint-Louis only)?
9. Does bassins versants data exist anywhere, or does it need to be derived from the MNT?
10. Complete énergie/infrastructure coverage for Saint-Louis and Gandiol (currently Gandon-only)?
11. Can the empty Gandon équipements folder be filled in?
12. A working, uncorrupted `Boucle de Gandiolais.shp` and a complete `CN_10m` (with `.shx`/`.prj`/`.cpg`)?
13. Which is authoritative: `evolution/empreinte-2024.geojson` (existing, 215 features) or `Zone d'habitation existante.shp`/`...2025.shp` (556/563 features)?
14. For the commune architecture redesign (R7): all 3 communes at once, or incrementally? Can SVD narrative content be extracted from the existing large docx reports, or will separate web-ready summaries be provided?
15. Is the French+Wolof bilingual requirement still current, and at what priority?
16. Which specific "advanced GIS" operations are actually required (search is clearly wanted; buffer/servitude/export need explicit confirmation before any backend architecture work begins)?

---

## Implementation Plan

### Wave 1 — Safe visible corrections
R1–R5: title/description text, section rename, logo reorder (+ RINA asset once supplied), equipment symbol removal (once specified), empreinte color/opacity fix. All **Low risk**. Ship everything not blocked by a missing text/asset now; patch the remaining 3 items in as a fast-follow once Questions 1–4 are answered.

### Wave 2 — New verified GIS data
Occupation du sol 2020 (after the confirmed encoding fix), MNT hillshade image, `CN_5m` contours. Technically ready today.

### Wave 3 — New map themes
Zones de conservation (ready now). Peuplement, énergie, activités économiques/corridors — ship incrementally as each commune's data arrives rather than waiting for full 3-commune coverage. Bassins versants blocked entirely pending Question 9.

### Wave 4 — Commune architecture (R7)
Build the new `/communes/{slug}/diagnostic|svd|pcu` route tree incrementally:
- **Diagnostic** branch first — highest data readiness, maps closely onto existing themes.
- **SVD** branch — needs narrative extraction from the 3 large docx reports (Question 14).
- **PCU/PCUI** branch — almost entirely missing data today; gate behind Questions 11–13, 16.
Preserve all currently-working URLs (`/communes/{slug}` keeps working) — add new sub-trees rather than replacing the existing page, to minimize regression risk.

### Wave 5 — Advanced GIS capabilities
Search/query/layer-toggle are **already implemented** today. Buffer, servitude-zone analysis, and general spatial operations require a new backend architecture (PostGIS or equivalent) that does not exist in the current static FastAPI+Leaflet stack — **do not build this speculatively**. Only start after Question 16 is answered with specific required operations.

### Wave 6 — Testing (continuous, not a single end phase)
Every route, every map (existing and new), all 3 communes, mobile/desktop, Vercel compatibility. Fix and verify the two pre-existing functional bugs already tracked in `PROJECT_ANALYSIS.md` (R3: vulnerabilite/erosion maps not loading; R4: equipment counts identical across communes) as part of Wave 1's testing pass, since they're cheap to fix now and unrelated to waiting on client data.

---

**No application code was modified during this analysis.**
