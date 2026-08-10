# PHASE3_WAVE4B_REPORT.md — Wave 4B: SVD Content Extraction + Integration

Baseline: `PROJECT_ANALYSIS.md`, `REPLY_CLIENT.md`, `PHASE3_WAVE1_REPORT.md`–`PHASE3_WAVE4A_REPORT.md`. Wave 4A was not redone. PCU/PCUI (`/communes/{slug}/pcu`) remains the honest Wave 4A placeholder, untouched. No advanced GIS functionality was implemented. **All 3 SVD source `.docx` files were only read, never modified.**

---

## 0. Deployment safety check

Wave 4A used `shapely`/`fiona`/`pyproj` for one-time spatial clipping, but **these are not runtime dependencies of the deployed application** — confirmed by:
1. `grep`-ing every `import`/`from` statement across `app/` — zero matches for `shapely`, `fiona`, or `pyproj`. The app only imports `fastapi`/`starlette` and Python stdlib.
2. Creating a genuinely clean virtual environment, installing **only** `requirements.txt`, and confirming `app.main:app` imports cleanly, the server starts, and it correctly serves the Wave 4A commune pages plus the raw clipped GeoJSON files (all 200 OK, zero errors).
3. Total `app/static/` size is 129 MB, well under `vercel.json`'s already-configured `maxLambdaSize: 250mb`.

**Conclusion: no `requirements.txt` change was needed or made.** Shapely/fiona/pyproj were data-preparation tools used locally to pre-generate static GeoJSON files that are committed as ordinary static assets — the exact same category as the site's existing hand-converted GeoJSON files from Waves 2–3. Adding them to `requirements.txt` would be incorrect (they'd be unused, dead weight on every Vercel cold start) rather than a fix for a real gap. This is the accurate, verified answer, not an assumption.

---

## 1–3. Source documents analyzed

| File | Commune | Extraction | Sections used |
|---|---|---|---|
| `SVD_Saint-Louis_12-05.docx` | Saint-Louis | 2,487 paragraphs, 45 tables (full text extracted via `python-docx`, ~278K characters — most of the 53MB file size is embedded images, not text) | Vision (§1086), Axes stratégiques (§1221–1308), Programme de développement (§1474–2224) |
| `SVD_Gandon 12-05 1.docx` | Gandon | Similar scale | Vision + Principes directeurs (§1013–1037), Axes (§1147–1235), Programme (§1396–2328) |
| `SDV Gandiole 12-05.docx` | Ndiébène Gandiole | Similar scale | Vision + Principes directeurs (§1163–1187), Axes (shared), Programme (§1555–2209) |

**Key structural finding (drove the whole implementation):** the Vision (2050 formulation), the 5 Principes directeurs, and the 7 Axes stratégiques are word-for-word identical (or trivially reworded) across all 3 documents — they describe **one** intercommunal strategy. Each commune's document, however, has its **own distinct Vision quote** and its **own Programme de développement chapter** — genuinely commune-specific content. This shared-vs-specific split is the structural backbone of everything built this wave, and is fully documented with exact paragraph references in `SVD_CONTENT_BASELINE.md`.

---

## Content extracted (per commune summary)

**Saint-Louis:** adopts the intercommunal/PDU vision as its own (no distinct commune vision found — confirmed absent, not a gap). 4 programmes: Environnement (with a genuine Saint-Louis-specific state-of-play: drainage saturation, submersion/erosion/salinization vulnerability, named quartiers Ngallèle/Bango/Maka Toubé Sor/Langue de Barbarie), Urbanisme (BV3 coastal/estuarine watershed, "climate urbanism pilot" positioning), Économie et société (consolidate fishing + diversify to tertiary/innovation/digital/energy), Gouvernance (position as intercommunal piloting hub).

**Gandon:** own vision — «Faire de Gandon un territoire viable, attractif et compétitif, porteur d'un développement durable.» 4 programmes: Environnement (shared framing only, no distinct Gandon state-of-play found), Urbanisme (hinge territory Saint-Louis↔delta, land-pressure narrative, ZES + logistics platform), Économie et société (agro-pastoral potential positioned as complementary to Saint-Louis's fishing economy), Gouvernance (same 4-objective structure as Saint-Louis, Gandon-specific wording).

**Ndiébène Gandiole:** own vision — «Produire un territoire attractif et émergent dans un cadre de vie durable.» 4 categories, one with a genuine heading mismatch: Environnement (shared framing only), **Urbanisme content exists under a differently-named heading** ("Stratégies de production urbaine résiliente...") rather than "Programme de développement urbain durable" — kept as-is, not renamed, per instruction to preserve source terminology, and flagged explicitly on the page itself. Économie et société ("pôle littoral écologique et productif" — fishing, food-crop farming, eco-tourism). Gouvernance (weak institutional structuring, dispersed settlements context, equity-of-investment objective).

---

## Website implementation

### New route content
`/communes/{slug}/svd` now renders real content (previously Wave 4A's honest placeholder). `/communes/{slug}/pcu` is untouched.

### Files created
- `app/routers/commune_svd_data.py` — structured Python data module: `VISION_INTERCOMMUNALE`, `PRINCIPES_DIRECTEURS` (+ note), `AXES_STRATEGIQUES` (7), `PROGRAMME_CATEGORY_LABELS`, and `COMMUNE_SVD` (per-commune vision + 4 programme categories). Mirrors the existing `commune_diagnostic_data.py` pattern — a plain Python dict module, no database or CMS introduced, per instruction.
- `app/templates/communes/svd.html` — one template serving all 3 communes (data-driven, same pattern as Wave 4A's `diagnostic_section.html`).
- `SVD_CONTENT_BASELINE.md` — full source map (see below).

### Files modified
- `app/routers/communes.py` — added `commune_svd_data` imports and a `SVD_PDF_BY_SLUG` lookup; rewrote `commune_svd_page()` to render `communes/svd.html` with real data instead of `branch_placeholder.html`.

### Web content design
- **Vision**: large pull-quote treatment.
- **Principes directeurs** and **Axes stratégiques**: both carry a visible "Vision intercommunale" badge (blue) so visitors understand this content is shared across the agglomeration, not unique to the commune they're viewing — directly implementing the "do not duplicate an intercommunal statement as if commune-specific" instruction. Axes are shown as a 7-card grid, principes as a 2-column list — no wall of text.
- **Programmes de développement**: shown as 4 collapsible `<details>` cards (one per category), carrying a green "Spécifique à {commune}" badge, each showing the *source's own programme title*, a faithful prose summary, and a bullet list of concrete levers/objectives where the source supports them — not exhaustive transcription (each source programme chapter runs 200–800+ lines; the page shows a faithful digest, consistent with "avoid a long wall of text").
- **Document download**: a "Consulter le rapport complet" button links to the existing, unmodified official PDF (`/static/docs/SVD_{Commune}.pdf`, already present since Phase 1) — the original reports remain the reference; nothing was regenerated.
- No new frontend framework, no new JS library — pure Jinja + Tailwind, consistent with Wave 4A's visual language.

---

## Source traceability

Every structured field in `commune_svd_data.py` traces back to a specific document, heading, and paragraph index — recorded in full in `SVD_CONTENT_BASELINE.md` (not exposed to public visitors, per instruction, but available for internal maintenance and future client corrections). The baseline document also explicitly separates three trust levels: **CONFIRMED FROM SOURCE** (direct quotes), **SUMMARY OF SOURCE** (faithful paraphrase), and **UNCLEAR/MISSING** (gaps or ambiguities in the source itself, never silently filled).

Two source-document problems were found and documented rather than hidden:
1. A genuine copy-paste artifact in the Ndiébène Gandiole document — one paragraph literally says "...pour...la transformation durable de **la ville de Saint-Louis**" in a section that is otherwise entirely about Ndiébène Gandiole. Not used on the website; flagged for the client.
2. Ndiébène Gandiole's document lacks a section titled "Programme de développement urbain durable" (present in the other two) — the equivalent content exists under a different heading and was used as-is, with an inline note on the page itself explaining the discrepancy.

---

## Validation

| Commune | Vision source-verified | Axes/Principes source-verified | Programmes source-verified | No cross-commune content reuse | Result |
|---|---|---|---|---|---|
| Saint-Louis | PASS (adopts PDU vision, confirmed absent of a distinct one) | PASS | PASS | PASS | PASS |
| Gandon | PASS (own quote confirmed via direct grep on rendered page) | PASS | PASS | PASS | PASS |
| Ndiébène Gandiole | PASS (own quote confirmed via direct grep on rendered page) | PASS | PASS (heading mismatch documented, not hidden) | PASS | PASS |

**Content correctness note:** French-text verification was done via `Grep` (which renders UTF-8 correctly) and the `Read` tool on the actual generated HTML — not by printing to this session's bash/Windows terminal, which was already confirmed in Wave 3 to visually garble correct UTF-8 text. All three communes' vision quotes were confirmed to render with correct accents in the final HTML output.

---

## Regression tests

| Area | Result |
|---|---|
| `/`, `/projet`, `/ressources`, `/carte/`, `/communes/` | PASS (200) |
| Global `/diagnostic` — all sections incl. Wave 3's Peuplement | PASS |
| All 3 commune landing pages | PASS |
| All 18 commune Diagnostic subsections (3 communes × 6 sections) | PASS |
| All 3 `/svd` pages (new real content) | PASS |
| All 3 `/pcu` pages (still Wave 4A placeholder) | PASS |
| `/equipements/{saint-louis,gandon,gandiol}` | PASS |
| `/risques/{inondation,vulnerabilite,erosion}` | PASS |
| Wave 1 urbanisation styling, Wave 2 MNT/Occupation 2020, Wave 3 themes, Wave 4A commune clipping | PASS — untouched, all still render correctly |
| Server log across every request this wave | Clean — zero errors |
| Clean-venv install + import + serve test (§0) | PASS |

---

## Missing / ambiguous SVD information

- No distinct Saint-Louis-only vision statement (confirmed absent from the source, not an extraction gap).
- No Gandon-specific or Ndiébène Gandiole-specific environmental state-of-play paragraph (present only for Saint-Louis) — a real asymmetry between the 3 documents, not something to invent symmetry for.
- Ndiébène Gandiole has no section titled "Programme de développement urbain durable" — equivalent content exists under a different heading, used as-is with a disclosure note.
- A second "5 orientations stratégiques" framework exists in all 3 documents alongside the 7 axes — not surfaced on the website (would create a confusing second, overlapping strategic taxonomy); flagged in `SVD_CONTENT_BASELINE.md` for the client to clarify if needed.
- A confirmed copy-paste error in the Ndiébène Gandiole source document (references "la ville de Saint-Louis" in a Gandiole-specific paragraph) — documented, not corrected on our end (it's the client's report, not ours to silently rewrite).
- Full "levier-by-levier" detail within each programme (each source chapter runs into the hundreds of lines) was summarized at a faithful digest level rather than fully transcribed — available for a deeper pass later if the client wants more granularity per programme.

---

## Deferred to Wave 4C (PCU/PCUI)

- Rapport de présentation, Zonage (interactive), PIP, Règlement d'urbanisme, Évaluation environnementale stratégique, Atlas cartographique — all still `MISSING`, no client material exists for any of these yet, `/pcu` remains an honest placeholder.
- ZAC/ZAD, servitudes — same status.

## Also still deferred (unchanged from earlier waves)

- Bassins versants (blocked on missing data).
- Buffer/query/spatial-analysis/export tooling, PostGIS, authentication, Wolof translation, PWA conversion.

---

## Result

`WAVE 4B COMPLETE — READY FOR REVIEW`

All 3 communes' SVD pages now show real, source-traceable content — vision, principes directeurs, and axes stratégiques correctly labeled as shared/intercommunal, and programmes de développement correctly presented as commune-specific, with two genuine source-document inconsistencies documented rather than silently smoothed over. The deployment safety check confirmed the Wave 4A GIS tooling introduces no actual dependency risk. Full regression across all prior waves is clean. Stopping here per instructions; not proceeding to Wave 4C automatically.
