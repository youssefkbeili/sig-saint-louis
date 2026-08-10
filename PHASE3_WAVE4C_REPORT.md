# PHASE3_WAVE4C_REPORT.md — Wave 4C: PCU/PCUI Material Audit + Safe Integration

Baseline: `PROJECT_ANALYSIS.md`, `REPLY_CLIENT.md`, `SVD_CONTENT_BASELINE.md`, `PHASE3_WAVE1_REPORT.md`–`PHASE3_WAVE4B_REPORT.md`. Waves 1–4B were not redone. No advanced GIS tooling was built. **All client source files were only read, never modified.**

Full audit detail, including the per-section per-commune tables and the GIS layer classification, lives in `PCU_CONTENT_BASELINE.md` (created before any website change, per instruction). This report summarizes the findings and the implementation built on top of them.

---

## PCU material discovered

- **No dedicated PCU/PCUI document exists anywhere in the delivery** — confirmed by an exhaustive filename search (zero matches for PCU/PCUI/PUD/zonage/règlement/PIP/EES/atlas/ZAC/ZAD/servitude) and a full-text search of all 3 SVD `.docx` reports. The SVD reports are strategy documents, not regulatory PCU/PCUI documents, and say so themselves ("Le PCU/PCUI... assure la traduction spatiale, réglementaire et opérationnelle des orientations... définies par la SVD" — i.e., the PCU/PCUI is described as a *future* deliverable).
- **A genuine, small planning-orientation GIS layer for Gandon**: `Nouveau dossier/Gandon/pp.shp`, 3 polygons with `Nom` = "Zone d'extension futur ( MT, LT)" ×2 and "Zone d'extension en cours (CT)" — real court/medium/long-term urban-extension planning vocabulary, found only by inspecting attributes (the filename `pp.shp` gave no hint). No legal reference or approval status exists in the data, so this is published as a planning-orientation layer, explicitly **not** as approved zoning.
- **SVD-roadmap "Priorité / Projet structurant" tables**, one set per commune (15 ranked projects for Saint-Louis, 15 for Gandon, 6 for Ndiébène Gandiole), which the SVD text itself explicitly connects to "Projets d'Investissement Prioritaires (PIP)." Only 3 real fields exist per project (priorité, nom, portée stratégique) — no cost, schedule, responsible entity, or status anywhere in the source.
- **A citation only, not a deliverable**: the SVD text cites a 2006 "Plan de sauvegarde et de mise en valeur de l'île de Saint-Louis — Rapport de présentation" as the source of some of its maps. That 2006 document was never delivered to us and cannot be published.
- **An intercommunal (not commune-specific) phasing table** (court/moyen/long terme × actions × bassins versants × responsables), found in Saint-Louis's document but explicitly spanning all 3 watersheds and multiple communes — correctly excluded from any single commune's page to avoid misrepresenting its scope.

## PCU material missing

Règlement d'urbanisme, Évaluation environnementale stratégique (EES), and Atlas cartographique: **zero mentions found anywhere** in any of the 3 SVD documents or any delivered file, for any commune. Zonage réglementaire (an approved, legally-referenced zoning map): **not found for any commune** — the closest candidate (Gandon's `pp.shp`) is a planning-orientation sketch, not confirmed regulatory zoning.

Two previously-uncharacterized shapefiles were investigated and excluded: `L.shp` (Gandon) shares an identical bounding box with the already-integrated `Lotissements autorisés.shp` and is very likely a duplicate/earlier export — not published, to avoid presenting probable duplicate data as new. `2.shp`/`3.shp` (root folder) turned out to be OSM-derived road-attribute exports, unrelated to zoning — noted as a possible future transport-layer enrichment, out of scope here.

---

## Per-commune implementation

### Saint-Louis
1. Rapport de présentation — **MISSING**, honest note shown (mentions the uncited-but-unavailable 2006 document for transparency).
2. Zonage — **MISSING**, no layer of any kind (Saint-Louis already has no habitat/foncier data either, per Wave 4A).
3. PIP — **PARTIAL**, 3 grouped tables (15 projects) with priorité/nom/portée stratégique, explicit caveat about missing fields.
4. Règlement d'urbanisme — **MISSING**.
5. EES — **MISSING**.
6. Atlas cartographique — **MISSING**.

### Gandon
1. Rapport de présentation — **MISSING**.
2. Zonage — **PARTIAL** — the "Zone d'extension" layer, rendered as an interactive map with a 2-category legend and an explicit "orientation, non approuvée" label directly in the layer name.
3. PIP — **PARTIAL**, 3 grouped tables (15 projects).
4. Règlement d'urbanisme — **MISSING**.
5. EES — **MISSING**.
6. Atlas cartographique — **MISSING**.

### Ndiébène Gandiole
1. Rapport de présentation — **MISSING**.
2. Zonage — **MISSING** (no equivalent orientation layer found for this commune).
3. PIP — **PARTIAL**, 1 table (6 projects).
4. Règlement d'urbanisme — **MISSING**.
5. EES — **MISSING**.
6. Atlas cartographique — **MISSING**.

---

## Six-section availability matrix

| Section | Saint-Louis | Gandon | Ndiébène Gandiol |
|---|---|---|---|
| Rapport de présentation | MISSING | MISSING | MISSING |
| Zonage | MISSING | PARTIAL | MISSING |
| PIP | PARTIAL | PARTIAL | PARTIAL |
| Règlement d'urbanisme | MISSING | MISSING | MISSING |
| EES | MISSING | MISSING | MISSING |
| Atlas cartographique | MISSING | MISSING | MISSING |

(No section reached AVAILABLE or INTERCOMMUNAL status for any commune on the public page — the one genuinely intercommunal item found, the phasing table, was deliberately not surfaced under any single commune to avoid misrepresenting its scope; see `PCU_CONTENT_BASELINE.md`.)

---

## GIS layers classified

| Layer | Classification |
|---|---|
| `pp.shp` (Gandon, "Zone d'extension") | **PLANNING / PROJECT LAYER** — not official zoning |
| ZAPA / ZAPE / ZP (Gandon, Gandiole) | **LAND USE** (confirmed in Wave 4A — occupation-du-sol categories, not zoning codes) |
| `Zone d'habitation (ZH)` | **LAND USE** (urban footprint, confirmed in Wave 4A) |
| `zone de conservation.shp` | **PROTECTION / CONSTRAINT** |
| `Lotissements autorisés.shp` | **PLANNING / PROJECT LAYER** (individual approved plots, not a zoning map) |
| ZES / économie layers (Wave 3) | **ECONOMIC ZONE** |
| `Future autoroute.shp` | **PLANNING / PROJECT LAYER** (corridor) |
| `L.shp` | **UNCLEAR** — likely duplicate of Lotissements autorisés, not used |
| `2.shp` / `3.shp` | **UNCLEAR relative to PCU** — actually transport/road data, not zoning |
| Anything matching "official zoning" | **NONE FOUND** |

---

## Documents published

- No new documents were published (none exist). The PCU page for every commune links to that commune's existing SVD page/PDF as the closest available official material, with a clear label that no PCU/PCUI document exists yet.

## Files changed

**New:**
- `app/routers/commune_pcu_data.py`
- `app/templates/communes/pcu.html`
- `app/static/data/pcu/gandon/zone-extension-planifiee.geojson` (3 features, converted from `pp.shp`: reprojected EPSG:32628→EPSG:4326, encoding-verified, 0 invalid geometries)
- `PCU_CONTENT_BASELINE.md`
- `PHASE3_WAVE4C_REPORT.md`

**Modified:**
- `app/routers/communes.py` — added `commune_pcu_data` imports, rewrote `commune_pcu_page()` to render `communes/pcu.html` with the real audit-backed data instead of `branch_placeholder.html`.

**Now orphaned (not deleted, flagged for awareness):** `app/templates/communes/branch_placeholder.html` is no longer used by any route — both `/svd` (Wave 4B) and `/pcu` (this wave) now render their own dedicated templates. Left in place rather than deleted, consistent with this project's established convention (per `PROJECT_ANALYSIS.md` R9) of not removing files without being asked.

---

## Tests

| Test | Result |
|---|---|
| All 3 `/communes/{slug}/pcu` pages load | PASS (200) |
| Six sections visible with correct status badges (Disponible/Partiel/En attente de données client) | PASS — verified via direct content search, not terminal print |
| Gandon's PIP table shows correct 15 named projects across 3 groups | PASS |
| Gandon's zonage map loads the "Zone d'extension" layer with working legend | PASS |
| Saint-Louis and Ndiébène Gandiole correctly show no zonage map (MISSING, no empty map shown) | PASS |
| No document assigned to the wrong commune | PASS — verified each commune's PIP list matches its own SVD document's tables |
| Regression: `/`, `/projet`, `/ressources`, `/carte/`, `/communes/` | PASS |
| Regression: all 3 commune landing pages, all 18 Diagnostic subsections, all 3 SVD pages | PASS |
| Regression: Wave 1 urbanisation styling, Wave 2 MNT/Occupation 2020, Wave 3 themes, Wave 4A clipping | PASS — untouched |
| Server log across every request this wave | Clean |
| `app.main:app` import | Clean |

---

## Client data still required

| ITEM | COMMUNE / SCOPE | WHY NEEDED | TARGET SECTION | BLOCKS IMPLEMENTATION |
|---|---|---|---|---|
| PCU/PCUI rapport de présentation | All 3 + intercommunal | No such document exists yet in any delivery | Rapport de présentation | YES |
| Approved zonage réglementaire (with legal reference / zone codes) | All 3 | Only one small, unapproved planning-orientation sketch exists (Gandon only) | Zonage | YES |
| Confirmation of what "Zone d'extension futur/en cours" (Gandon) actually represents — an approved planning intention or a working sketch? | Gandon | Determines whether it can ever be relabeled "official zoning" | Zonage | NO (already shown, honestly labeled) |
| Formal PIP with cost, schedule, responsible entity, and status per project | All 3 | Only priority rank + name + rationale exist today | PIP | NO (already shown partially) |
| Règlement d'urbanisme document | All 3 + intercommunal | Zero content exists | Règlement d'urbanisme | YES |
| Évaluation environnementale stratégique (EES) | All 3 or intercommunal (client to clarify scope) | Zero content exists | EES | YES |
| Atlas cartographique (a real, approved map-book deliverable) | All 3 | Zero such document exists; client must confirm whether website maps may be repackaged as one, or a real atlas will be delivered | Atlas cartographique | YES |
| The 2006 "Plan de sauvegarde..." rapport de présentation, if the client wants it referenced/linked | Saint-Louis | Currently only cited inside the SVD text, never delivered as a file | Rapport de présentation | NO |
| Clarification of the intercommunal phasing table's intended publication scope | Intercommunal | Currently excluded from all commune pages to avoid scope misrepresentation | PIP (potentially a future intercommunal view) | NO |

---

## Advanced GIS readiness

| Capability | Data ready? | Frontend-only possible? | Backend required? | Client clarification required? |
|---|---|---|---|---|
| Buffer analysis | No confirmed zoning/servitude geometry to buffer against | Approximate buffer possible client-side (Turf.js) once real zoning exists | Exact buffer at scale needs backend processing | Yes — need real zoning data first |
| Spatial intersection / servitude analysis | No servitude data exists at all | No | Yes — needs a real spatial engine | Yes — no servitude data has been delivered for any commune |
| Arbitrary layer extraction / export | Existing GeoJSON layers could technically be exported as-is | Yes, for already-published layers (simple file download) | No, for simple whole-layer export; yes for filtered/clipped export-on-demand | No, but scope (which layers, what format) needs confirming |
| Shapefile generation from web selections | Not built | No | Yes | Yes |
| Drawing/editing tools | Not built, no editing workflow exists anywhere in the project | Yes, Leaflet.Draw could add sketch tools | Yes, if edits must persist | Yes — persistence/authorization model undefined |
| PostGIS / GeoServer | Not introduced, per every wave's explicit instruction | — | Would be required for true spatial-query tooling | Yes — this is a significant architecture decision, not to be made unilaterally |

**Summary:** the current static FastAPI + Leaflet architecture can support simple, already-published-layer downloads today. Everything else in this list (buffer, servitude analysis, drawing, generation) requires either data that doesn't exist yet (servitudes, approved zoning) or backend/architecture decisions (PostGIS) that are explicitly out of scope until the client confirms real requirements. Nothing here was built this wave.

---

## Deferred work

- Everything in "Client data still required" above — cannot be safely implemented without real client-supplied material.
- Advanced GIS tooling (§ above) — architecture decision, not attempted.
- Reconciling the intercommunal phasing table into a dedicated intercommunal PIP/roadmap view — a reasonable future addition, not built this wave since no such page currently exists in the site's information architecture.

---

## Result

`WAVE 4C PARTIALLY COMPLETE — CLIENT DATA REQUIRED`

The PCU/PCUI branch is now live for all 3 communes with an honest, audited representation of what actually exists: real (if partial) PIP content for all 3 communes, a real (if unapproved) zoning-orientation layer for Gandon, and clear "en attente de données client" messaging — never an empty-feeling page — for every one of the 12 remaining MISSING sections. No planning content was fabricated, no GIS layer was misclassified as official zoning, and no document was assigned to the wrong commune. The client data list above is ready to drive the next reply to the client. Stopping here; not starting advanced GIS work automatically.
