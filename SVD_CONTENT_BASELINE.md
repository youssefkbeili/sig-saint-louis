# SVD_CONTENT_BASELINE.md — Source-of-Truth for Extracted SVD Content

Source documents (all in `reply client/`, read-only, never modified):
- `SVD_Saint-Louis_12-05.docx` — 2,487 paragraphs, 45 tables, ~278K characters of text (most of the 53MB file size is embedded images, not extracted here)
- `SVD_Gandon 12-05 1.docx` — similar scale
- `SDV Gandiole 12-05.docx` — similar scale

Extraction method: full paragraph + table text extracted via `python-docx`, preserving paragraph style names (Heading 1–4, Normal, List Paragraph) and original paragraph order, to a plain-text working file per document (not committed — a working artifact of this analysis, not a project file). Every quote below was verified against that extraction; direct quotes are marked with «guillemets» exactly as they appear in the source.

**Cross-cutting finding, applies to all 3 communes:** the Vision (2050 formulation), the 5 Principes directeurs, and the 7 Axes stratégiques are **word-for-word identical** (or trivially reworded) across all 3 documents — confirmed by direct comparison. They describe ONE intercommunal strategy for the whole agglomeration of Saint-Louis, Gandon, and Ndiébène Gandiole. They are documented ONCE below under "Shared / Intercommunal Content" and are **not** duplicated as if commune-specific on the website (labeled "Vision intercommunale" there instead).

---

## Shared / Intercommunal Content (applies to all 3 communes)

### Vision territoriale (2050 formulation)
**CONFIRMED FROM SOURCE** (direct quote, found near-identically in all 3 documents, e.g. Saint-Louis §[1240], Gandon §[1240], Gandiole §[1244] approx.):
> « Produire un cadre de vie bâti durable, résilient et inclusif, fondé sur la coopération intercommunale et la valorisation de la diversité territoriale. »

Also quoted in all 3 documents as the original PDU-level formulation (e.g. Saint-Louis §[842], §[1086]):
> « Produire un cadre de vie bâti durable, basé sur la coopération entre les différentes échelles et la diversité du territoire, partant de l'intercommunalité au niveau local. »

### Principes directeurs (5, + 1 transversal)
**CONFIRMED FROM SOURCE** — word-for-word identical text found in Gandon §[1021]–[1037] and Ndiébène Gandiole §[1171]–[1187], only the introductory sentence changes commune name. Not independently re-verified against Saint-Louis's exact paragraph numbers, but the same 5 principles are referenced there too.
1. Un cadre de vie salubre et digne pour l'ensemble des populations
2. Capacité du territoire à s'adapter aux défis climatiques et environnementaux
3. Planification de l'espace face à la croissance démographique
4. Accompagner le développement économique et l'emploi
5. Gouvernance territoriale efficace, décentralisée et participative
6. (transversal) Organisation efficace des mobilités et de l'accessibilité

### Axes stratégiques (7)
**CONFIRMED FROM SOURCE** — Saint-Louis §[1226]–[1308] (most detailed articulation, used as the canonical text). Gandon confirms "y compris la Commune de Gandon" applies the same 7 axes (§[1165]). Ndiébène Gandiole confirms the same framing (line ~1141 of its extraction).
1. Résilience climatique, environnementale et ville compatible avec l'eau
2. Urbanisation maîtrisée, structuration spatiale et armature territoriale
3. Habitat, cadre de vie, services urbains et cohésion sociale
4. Mobilité durable, accessibilité et structuration des corridors
5. Développement économique local, économie durable et valorisation territoriale
6. Transition énergétique, sécurité énergétique et ville à financements verts
7. Gouvernance territoriale, pilotage stratégique et innovation institutionnelle

**UNCLEAR / NOT SURFACED ON WEBSITE:** all 3 documents also contain a separate, earlier "5 orientations stratégiques" list (e.g. Gandon §[1043]–[1101]: "Protéger durablement le littoral," "Maîtriser l'expansion urbaine," "Préserver et valoriser les terres agricoles," "Structurer un développement économique," "Renforcer la gouvernance intercommunale") that appears to be an earlier or complementary layer, not the same as the 7 axes. Not featured on the website to avoid presenting two overlapping strategic frameworks side by side — flagged here for the client to clarify which is authoritative if a future revision needs it.

**CONFIRMED SOURCE ERROR (not corrected, documented instead):** the Ndiébène Gandiole document, at the "orientations stratégiques" intro (§[1192] of its extraction), literally says "...pour encadrer et organiser la transformation durable de **la ville de Saint-Louis**" — an apparent copy-paste artifact from the Saint-Louis document, since the surrounding text and heading are otherwise about Ndiébène Gandiole. Not used on the website (that whole "orientations stratégiques" layer wasn't surfaced, per above), but flagged here since it's evidence of a real drafting inconsistency in the client's source material.

---

# Saint-Louis

## Vision
**CONFIRMED FROM SOURCE** — Saint-Louis's document doesn't articulate a distinct commune-only vision; it explicitly adopts the PDU/intercommunal vision as its own (§[1086]: "Identification de la vision" → quotes the PDU vision verbatim).

## Principes directeurs
Shared — see above. Not re-stated per commune on the website.

## Axes stratégiques
Shared — see above.

## Programmes de développement
**SUMMARY OF SOURCE**, from `PARTIE IV : PROGRAMME DE DEVELOPPEMENT` (§[1474]–[2224]):
- **Environnement** — "Programme d'adaptation et d'atténuation des risques environnementaux et climatiques" (§[1487]). Saint-Louis-specific state-of-play (§[1513]–[1521], Heading 4 "Stratégie environnementale de la commune de Saint-Louis"): saturation of drainage networks in heavy rain, high vulnerability to marine submersion/coastal erosion/salinization, dense urbanization between ocean and river. Named quartiers: Ngallèle, Bango, Maka Toubé Sor, Langue de Barbarie.
- **Urbanisme** — "Programme de développement urbain durable et résiliente" (§[1681]). Saint-Louis corresponds to the downstream coastal/estuarine watershed (BV3): historic urban center, dense population, high exposure to flooding/erosion/submersion. Strategy: reorganize the city, adapted building typologies (amphibious housing, porous infrastructure), position Saint-Louis as a "climate urbanism pilot territory."
- **Économie et société** — "Programme de développement économique et social" (§[2001]). Double ambition: consolidate historic activities (artisanal fishing) and diversify toward higher-value sectors (advanced tertiary, innovation, digital, energy); some economic functions to be deployed intercommunally on Gandon to reduce land pressure on the city center.
- **Gouvernance et intercommunalité** — "Programme de bonne gouvernance territoriale et institutionnelle : Commune de Saint-Louis" (§[2224]). General objective: performant, transparent, results-oriented governance, positioning Saint-Louis as the intercommunal piloting hub.

## Source references
- File: `SVD_Saint-Louis_12-05.docx`
- Key sections used: §[1086] (vision), §[1221]–[1308] (axes), §[1474]–[2224] (programmes)

## Missing / unclear information
- No distinct Saint-Louis-only vision statement exists — confirmed absent, not an extraction gap.
- Full "leviers" detail beyond the environmental programme was summarized at the section-intro level rather than transcribed in full (documents run to ~870 lines for this section alone) — a fuller extraction is possible later if the client wants more granularity.

---

# Gandon

## Vision
**CONFIRMED FROM SOURCE**, direct quote (§[1013]):
> « Faire de Gandon un territoire viable, attractif et compétitif, porteur d'un développement durable. »

Distinct from the intercommunal vision — this is Gandon's own, described as built "à partir des échanges avec l'exécutif communal et les acteurs locaux."

## Principes directeurs
Shared — see above (confirmed identical wording found directly in this document, §[1021]–[1037]).

## Axes stratégiques
Shared — see above.

## Programmes de développement
**SUMMARY OF SOURCE**, from `PARTIE IV : PROGRAMME DE DEVELOPPEMENT` (§[1396]–[2328]):
- **Environnement** — "Le programme d'adaptation et d'atténuation des risques environnementaux et climatiques" (§[1409]). **UNCLEAR/MISSING:** unlike Saint-Louis, this document does not include a distinct Gandon-only environmental state-of-play paragraph in this section — content here largely mirrors the shared 5-principle framing.
- **Urbanisme** — "Programme de développement urbain durable et résilient" (§[1479]). Gandon-specific: described as a hinge territory between Saint-Louis's urban agglomeration and the delta's rural/agricultural spaces, at the crossroads of logistics corridors (highway, RN2, Dakar link). Growing urban/land pressure from Saint-Louis's proximity — habitat extension, conversion of farmland, unplanned urbanization. Must also accommodate a Special Economic Zone and a logistics platform.
- **Économie et société** — "Programme de développement économique et social" (§[2115]). Gandon-specific: unlike Saint-Louis (fishing-dominated), Gandon has strong agro-pastoral potential, strategic land reserves, and capacity to host structuring economic functions (activity zones, logistics, services) — positioned as complementary to Saint-Louis.
- **Gouvernance et intercommunalité** — "Programme de bonne gouvernance territoriale et institutionnelle" (§[2328]). General objective: efficient, transparent, results-oriented intercommunal governance for PCUi piloting.

## Source references
- File: `SVD_Gandon 12-05 1.docx`
- Key sections used: §[1013]–[1037] (vision + principes), §[1147]–[1235] (axes), §[1396]–[2328] (programmes)

## Missing / unclear information
- No distinct Gandon-only environmental state-of-play was found in the environmental programme section (present for Saint-Louis, absent/generic for Gandon) — noted as a genuine content asymmetry between the 3 documents, not an extraction error (confirmed by reading the full section).

---

# Ndiébène Gandiole

## Vision
**CONFIRMED FROM SOURCE**, direct quote (§[1166]):
> « Produire un territoire attractif et émergent dans un cadre de vie durable. »

Distinct from the intercommunal vision; the document explicitly notes it is "en parfaite harmonie" with the PDU vision (also quoted immediately after, §[1168]).

## Principes directeurs
Shared — see above (confirmed identical wording found directly in this document, §[1171]–[1187]).

## Axes stratégiques
Shared — see above.

## Programmes de développement
**SUMMARY OF SOURCE**, from `PARTIE IV : PROGRAMME DE DEVELOPPEMENT` (§[1555]–[2209]):
- **Environnement** — "Programme d'adaptation et d'atténuation des risques environnementaux et climatiques" (§[1569]). Same caveat as Gandon: no distinct commune-only environmental state-of-play paragraph found in this exact section; environmental context (wetlands, coastline, salinization) is instead developed under the Urbanisme heading below.
- **Urbanisme** — **UNCLEAR HEADING MATCH:** this document does not have a section literally titled "Programme de développement urbain durable," unlike Saint-Louis and Gandon. The equivalent content exists under "Stratégies de production urbaine résiliente de la commune de Ndiébène Gandiole" (§[1630]). Kept under this original heading on the website rather than renamed, per instruction to preserve source terminology. Content: territory with strong habitat/agriculture/wetland/coastal interaction, exposed to seasonal flooding and soil salinization; strategy organizes urbanization into 4 hierarchical "unités de voisinage" levels from the main communal center outward.
- **Économie et société** — "Programme de développement économique et social" (§[2035]). Positions Ndiébène Gandiole as a "pôle littoral écologique et productif" complementary to Saint-Louis and Gandon: economic ambition (artisanal fishing, food-crop farming, agri-food/fishery processing, eco-tourism) and social ambition (equitable access to essential services, social cohesion, housing, territorial inclusion).
- **Gouvernance et intercommunalité** — "Programme de bonne gouvernance territoriale et institutionnelle-Commune de Ndiébène Gandiole" (§[2209]). Context: weak institutional structuring, dispersed settlements, strong dependence on natural resources, high climate vulnerability. Objective: inclusive, transparent governance ensuring equitable investment, particularly for rural/vulnerable areas.

## Source references
- File: `SDV Gandiole 12-05.docx`
- Key sections used: §[1163]–[1187] (vision + principes), §[1147]-equivalent (axes, same shared text), §[1555]–[2209] (programmes)

## Missing / unclear information
- No section titled exactly "Programme de développement urbain durable" — content exists under a different heading, used as-is (see above).
- No distinct commune-only environmental state-of-play paragraph, same caveat as Gandon.
- The "orientations stratégiques" copy-paste artifact referencing "la ville de Saint-Louis" (see Shared Content section above) originates in this document specifically.

---

## How to use this document

When the client requests a correction to SVD content on the website:
1. Find the relevant commune section above.
2. Check the "Source references" paragraph indices against the original `.docx` (reopen with `python-docx`, paragraph index matches `document.paragraphs[i]`).
3. Update `app/routers/commune_svd_data.py` directly — it is the single source the website renders from.
4. If the correction reveals the source itself is wrong (like the Ndiébène Gandiole copy-paste artifact above), flag it back to the client rather than silently "fixing" the website to say something the report doesn't.
