# PCU_CONTENT_BASELINE.md — PCU/PCUI Material Audit

Audit method: full filename search across `reply client/` for PCU/PCUI/PUD/zonage/règlement/PIP/EES/atlas/ZAC/ZAD/servitude keywords (zero filename matches); full-text search of all 3 SVD `.docx` extractions (from Wave 4B) for the same concepts; direct inspection (via `fiona`) of every previously-uncharacterized shapefile in `reply client/occupation du sol 2020 SL/` to check attributes rather than trust filenames, per instruction. **No website files were changed during this audit.**

**Headline finding: no dedicated PCU/PCUI document (rapport de présentation, zonage réglementaire, règlement, PIP, EES, or atlas) exists anywhere in the delivered materials.** The 3 SVD reports are strategy documents, not regulatory PCU/PCUI documents — confirmed by their own text, which repeatedly describes the PCU/PCUI as a *future* deliverable that will "translate" the SVD ("Le PCU/PCUI... assure la traduction spatiale, réglementaire et opérationnelle des orientations stratégiques définies par la SVD"). This matches `QUESTIONS_POUR_AVANCER_TY.docx`'s own admission (Phase 2A) that more maps and plans were still being produced as of the client conversation. What DOES exist: (1) a handful of small, genuine planning-adjacent GIS layers, found by inspecting attributes rather than filenames, and (2) explicit SVD-roadmap tables that name and rank "Projets structurants" per commune, which the SVD text itself connects to the term "Projets d'Investissement Prioritaires (PIP)."

---

## Candidate records found

| FILE | TYPE | COMMUNE | CONTENT | SOURCE | LIKELY PCU SECTION | CONFIDENCE | SAFE TO PUBLISH |
|---|---|---|---|---|---|---|---|
| `Nouveau dossier/Gandon/pp.shp` | Shapefile, 3 polygons | Gandon | Attributes: `Nom` = "Zone d'extension futur ( MT, LT)" (×2) and "Zone d'extension en cours (CT)" — genuine urbanism planning-horizon terminology (CT/MT/LT = court/moyen/long terme) | Client GIS delivery | Zonage (as a planning/project layer, not confirmed regulatory zoning) | Medium — real planning vocabulary, but no legal/approval reference, no zoning code nomenclature (no "UA"/"NC" etc.) | PARTIAL — publish as a labeled planning-orientation layer, not as "official zoning" |
| `Nouveau dossier/Gandon/L.shp` | Shapefile, 914 polygons | Gandon | Same schema and identical bounding box as the already-integrated `Lotissements autorisés.shp` (874 features) | Client GIS delivery | Habitat/foncier (already covered) | Low — appears to be a duplicate/earlier export of the same dataset | NO — not used, to avoid publishing a probable duplicate as if it were new data |
| `2.shp`, `3.shp` (root of `occupation du sol 2020 SL/`) | Shapefile, 12 and 11 features | Unspecified (regional extract) | OSM-derived road attributes (`osm_id`, surface, speed limit, lighting) — e.g. "Route Nationale 2," "Route de Rosso" | OpenStreetMap-derived export, French-translated tags | Not PCU material — general transport infrastructure | High confidence it's transport data, not zoning | NO — out of scope for PCU/PCUI; a possible future transport-layer enrichment, not pursued this wave |
| `occup.shp` (referenced in earlier phase notes) | — | — | File no longer present / never existed with valid companions — confirmed via direct filesystem check | — | — | — | N/A |
| SVD reports, "Priorité \|\| Projet structurant \|\| Portée/Lecture stratégique" tables (3 per commune in Saint-Louis's document; similar tables in Gandon's and Ndiébène Gandiole's) | DOCX tables | All 3 (separately, per-commune) | Ranked (1–5 or 1–6) named structuring projects with a one-line strategic rationale each | `SVD_*.docx`, "Feuille de route" section | PIP | High — the SVD text explicitly names "Projets d'Investissement Prioritaires (PIP)" as the concept these tables feed | PARTIAL — real data, but only 3 fields exist (priorité, nom du projet, portée stratégique); no cost, schedule, responsible entity, or status — must not be presented as a complete/finalized PIP |
| SVD reports, "Horizon \|\| Actions prioritaires \|\| Bassin(s) concerné(s) \|\| Responsables principaux" table (Saint-Louis document, §2764) | DOCX table | Intercommunal (explicitly spans BV1/BV2/BV3 and multiple communes) | Court/moyen/long-terme phasing of intercommunal actions with named responsible entities | `SVD_Saint-Louis_12-05.docx`, "Feuille de route" | PIP (intercommunal layer) | Medium — genuinely intercommunal, not commune-specific | NOT published on a single commune's page — would misrepresent scope if shown as commune-specific |
| Citation: "Plan de sauvegarde et de mise en valeur de l'île de Saint Louis... Rapport de présentation - 2006" | Citation only, not a delivered file | Saint-Louis (île) | A 2006 heritage-conservation planning report is cited as the *source* of some SVD maps/content | Referenced inside `SVD_Saint-Louis_12-05.docx`, not itself delivered | Rapport de présentation | Low — this is an older, unrelated document's title, not the current PCU/PCUI's rapport de présentation | NO — the file itself was never delivered; cannot be exposed |
| Règlement d'urbanisme | — | — | Zero mentions found anywhere in any of the 3 SVD documents' full text | — | Règlement d'urbanisme | — | MISSING |
| Évaluation environnementale stratégique (EES) | — | — | Zero mentions found | — | EES | — | MISSING |
| Atlas cartographique | — | — | Zero mentions found; no PDF map-book/atlas file exists anywhere in the delivery | — | Atlas cartographique | — | MISSING |
| ZAC / ZAD | — | — | "ZAC" appears only as a generic term inside SVD prose (e.g. "Lotissements planifiés et ZAC" in a phasing table, "ZAC et réserves foncières" in a governance table) — never as an actual delimited ZAC/ZAD dataset or document | `SVD_Saint-Louis_12-05.docx` | Zonage | Low — conceptual mention only, no boundary data | MISSING as a usable layer |

---

## Zonage layer classification (per instruction: attributes checked, not filenames)

| Layer | Classification | Why |
|---|---|---|
| `Nouveau dossier/Gandon/pp.shp` ("Zone d'extension futur/en cours") | **PLANNING / PROJECT LAYER** (not Official Zoning) | Real planning-horizon vocabulary, but no legal reference, no approval status, no zoning-code nomenclature |
| ZAPA / ZAPE / ZP (Gandon, Ndiébène Gandiole) — already integrated in Wave 4A | **LAND USE** (confirmed in Wave 4A, restated here) | Attributes are occupation-du-sol categories (Culture maraîchère, Steppe...), not zoning codes, despite zoning-sounding names |
| `Zone d'habitation (ZH)` (Gandon, Ndiébène Gandiole) — already reclassified in Wave 4A | **LAND USE** (urban footprint, not zoning) | Attribute is literally "Empreinte urbaine," confirmed in Wave 4A |
| `zone de conservation.shp` — already integrated in Wave 4A/3 | **PROTECTION / CONSTRAINT** | Categories are "Protection Naturel"/"Protection Patrimoniel" |
| `Lotissements autorisés.shp` (Gandon) | **PLANNING / PROJECT LAYER** | Individual approved-subdivision plots — genuine foncier/urbanism content, but not a zoning map (no zone-wide regulatory classes) |
| ZES / économie layers (Wave 3) | **ECONOMIC ZONE** | Confirmed in Wave 3 |
| `Future autoroute.shp` | **PLANNING / PROJECT LAYER** (corridor) | Confirmed in Wave 3 |
| Any layer literally named "Zonage PCU," "Plan de zonage," or similar | **NONE FOUND** | Zero such file or attribute exists anywhere in the delivery |

**Conclusion: no layer qualifies as OFFICIAL ZONING.** The public "Zonage PCU/PCUI" section (as literally labeled) has nothing to show yet — this is stated honestly on the website rather than relabeling a land-use or planning-project layer as if it were approved zoning.

---

# Saint-Louis

## Rapport de présentation
Available: nothing.
Missing: the current PCU/PCUI's own rapport de présentation. A 2006 heritage-conservation report is cited as a source elsewhere in the SVD document but was never delivered to us.
Source files: none.

## Zonage
Available: nothing classified as official zoning.
Missing: any approved zonage réglementaire dataset or document.
GIS layers: none specific to Saint-Louis were found in this audit (Saint-Louis already has no habitat/foncier layer at all, confirmed in Wave 4A).
Source files: none.

## PIP
Available: 3 ranked "Priorité / Projet structurant / Portée stratégique" tables from the SVD roadmap (15 named projects total: littoral/resilience, urban/mobility, economic), explicitly connected by the source text to the PIP concept.
Missing: cost, schedule, responsible entity, and status fields — not present in the source for any project.
Source files: `SVD_Saint-Louis_12-05.docx`, "Feuille de route" section, Tables 21–23.

## Règlement d'urbanisme
Available: nothing. Missing entirely — `MISSING — CLIENT CONFIRMATION REQUIRED`.

## EES
Available: nothing. Missing entirely — `MISSING — CLIENT CONFIRMATION REQUIRED`.

## Atlas cartographique
Available: nothing. Missing entirely — `MISSING — CLIENT CONFIRMATION REQUIRED`. (The site's existing static theme images and the global `/carte/` page are not being repackaged as an "atlas" without explicit client approval, per instruction.)

---

# Gandon

## Rapport de présentation
Available: nothing. Missing: same as Saint-Louis.
Source files: none.

## Zonage
Available: `pp.shp` ("Zone d'extension futur/en cours," 3 features) — published as a labeled planning-orientation layer, not as confirmed official zoning.
Missing: any approved zonage document; `L.shp` not used (likely duplicate of `Lotissements autorisés.shp`, see above).
GIS layers: `pp.shp` (PARTIAL, see classification table); ZAPA/ZAPE/ZP/ZH already covered under Diagnostic > Habitat et foncier / Urbanisme (Wave 4A), not re-labeled as zoning here.
Source files: `Nouveau dossier/Gandon/pp.shp`.

## PIP
Available: 3 ranked project tables (environmental/resilience, urban/PCUi-structuring, economic — 15 named projects total, e.g. "Aménagement 100 ha relogement," "Corridor Ngallèle – Gandon," "ZES Ngallèle – Gandon").
Missing: same field gaps as Saint-Louis (no cost/schedule/responsible/status).
Source files: `SVD_Gandon 12-05 1.docx`, roadmap/annex tables (§2963–2985 of the extraction).

## Règlement d'urbanisme
`MISSING — CLIENT CONFIRMATION REQUIRED`.

## EES
`MISSING — CLIENT CONFIRMATION REQUIRED`.

## Atlas cartographique
`MISSING — CLIENT CONFIRMATION REQUIRED`.

---

# Ndiébène Gandiol

## Rapport de présentation
Available: nothing. Missing: same as the other 2 communes.
Source files: none.

## Zonage
Available: nothing classified as official zoning or even a planning-orientation layer specific to this commune (no `pp.shp`-equivalent found for Ndiébène Gandiole in this audit).
Missing: any zoning-adjacent dataset.
Source files: none.

## PIP
Available: at least 1 ranked project table found (6 named projects: poste de santé, marché intercommunal aux poissons, forages solaires, centre de formation, circuits écotouristiques, programme "Mangroves & récifs").
Missing: same field gaps as the other communes.
Source files: `SDV Gandiole 12-05.docx`, roadmap/annex tables (§2608–2614 of the extraction).

## Règlement d'urbanisme
`MISSING — CLIENT CONFIRMATION REQUIRED`.

## EES
`MISSING — CLIENT CONFIRMATION REQUIRED`.

## Atlas cartographique
`MISSING — CLIENT CONFIRMATION REQUIRED`.

---

## Intercommunal content found, not attributed to a single commune

The "Horizon (court/moyen/long terme) × Actions prioritaires × Bassins versants concernés × Responsables principaux" table (`SVD_Saint-Louis_12-05.docx`, §2764–2767) explicitly spans all 3 watersheds (BV1/BV2/BV3) and multiple communes' institutions. This is **intercommunal** planning-horizon content, not Saint-Louis-specific despite being physically located in Saint-Louis's own document. **Not published under any single commune's PIP page**, to avoid misrepresenting its scope — noted here for a possible future intercommunal-scope PIP view, which doesn't exist as a standalone page today.
