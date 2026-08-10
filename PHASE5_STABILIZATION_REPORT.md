# PHASE5_STABILIZATION_REPORT.md — Stabilization, Testing & Delivery Readiness

Baseline: all prior reports (`PROJECT_ANALYSIS.md` through `PHASE3_WAVE4C_REPORT.md`), `REPLY_CLIENT.md`, `REPLY_CLIENT_REQUEST.md`. No new features were built this phase — this was testing, bug-fixing, and readiness work only.

## Executive result

**PASS WITH CLIENT BLOCKERS**

The application is functionally stable, has a real automated test suite for the first time (76 tests, all passing), and 3 genuine bugs were found and fixed. Remaining gaps are entirely client-data blockers already tracked in `REPLY_CLIENT_REQUEST.md` (PCU/PCUI documents, contact-form email delivery), not code defects.

---

## 0. REPLY_CLIENT_REQUEST.md correction

Removed the requests for homepage title, introduction text, and the "Thèmes du diagnostic" replacement label (already supplied by the client) from §3 and the recap table. Only genuinely open visual items remain: the equipment-map symbol to remove, the RINA logo, and confirmation of the already-applied urbanisation color palette. No other part of the document was rewritten.

---

## 1. Route inventory (testing checklist)

| Route | Purpose | Scope | Status |
|---|---|---|---|
| `/`, `/projet`, `/ressources` (GET/POST) | Homepage, about, resources+contact | Global | 200 |
| `/diagnostic?section=...` (12 sections) | Global territorial diagnostic | Global | 200 |
| `/carte/` | Flagship interactive map | Global | 200 |
| `/communes/` | Commune index | Global | 200 |
| `/communes/{slug}` | Commune landing (3 communes) | Commune | 200 |
| `/communes/{slug}/diagnostic` | Commune diagnostic index | Commune | 200 |
| `/communes/{slug}/diagnostic/{section}` (6 sections × 3) | Commune diagnostic detail | Commune | 200 |
| `/communes/{slug}/svd` | SVD content | Commune | 200 |
| `/communes/{slug}/pcu` | PCU/PCUI content | Commune | 200 |
| `/equipements/{commune}` (3 communes) | Equipment maps | Commune | 200 |
| `/risques/{inondation,vulnerabilite,erosion}` | Risk theme pages | Global | 200 (all 3 now load their data — see §7) |
| `/a-propos`, `/telechargements`, `/contact`, `/diagnostic/{situation,geologie,pedologie,topographie,occupation-du-sol,evolution-urbaine}` | Legacy redirects | Global | 301→200 |
| `/api/log` (POST) | Frontend telemetry | Global | 200 (400 on malformed input — see §11) |

This table became the basis for `tests/test_routes.py`.

---

## 2. Automated tests

**Created from zero** (the project had no test suite before this phase): `tests/test_routes.py`, using `pytest` + FastAPI's `TestClient`. Test-only dependencies (`pytest`, `httpx`) were placed in a new `requirements-dev.txt`, kept separate from `requirements.txt` so the deployed Vercel function gains no new dependency.

**76 tests / 76 passed / 0 failed** (1 failed on first run, fixed — see §11).

Coverage: every route in §1, all 6×3 commune diagnostic combinations, SVD cross-commune identity checks, PCU honesty checks (never shows "Disponible" for anything not actually available; Gandon's zonage layer is verifiably labeled as an orientation, not approved zoning), contact form, and `/api/log` including a malformed-input case.

Run with: `pip install -r requirements.txt -r requirements-dev.txt && pytest tests/ -v`

---

## 3. GIS asset validation

Built a validation script cross-checking every layer reference in `diagnostic.py`, `carte.py`, `commune_diagnostic_data.py`, and `commune_pcu_data.py` against the actual files on disk: existence, valid JSON, valid `FeatureCollection` structure, geometry presence, coordinate plausibility (within a generous Senegal bounding box), and — critically — that every `categoryColors` key actually matches a real value in the data.

**This caught two real, previously-invisible bugs (see §7 for detail):**
1. A genuine double-UTF-8-encoding bug in `occupation-du-sol-2020.geojson` affecting 5 of 17 land-cover categories.
2. A spelling mismatch (`Protection Patrimoniel` vs. the source's actual `Protection Patrimoinel`) causing 1 conservation-zone category to silently render in the wrong color.

Both are now fixed and the validation script reports **zero problems** across all 130 distinct referenced GIS files.

**Orphaned files found** (registered nowhere, not a bug — see §15 for the full list): 49 `.geojson` files, all either intentionally-excluded zero-feature commune clips (confirmed correct per Wave 4A), or pre-existing orphans already documented in `PROJECT_ANALYSIS.md`.

---

## 4. Commune data integrity

Manually cross-checked the 3 highest cross-contamination-risk sections (Démographie, Habitat et foncier, Activités économiques et énergie) across all 3 communes by inspecting the exact GeoJSON file paths each page's rendered HTML requests:

| Section | Saint-Louis | Gandon | Ndiébène Gandiole |
|---|---|---|---|
| Démographie | `population/quartiers-polygones.geojson` only | `peuplement/quartiers-gandon.geojson` only | `peuplement/quartiers-gandiol.geojson` only |
| Habitat et foncier | none (honest MISSING) | 4 files, all `communes/gandon/habitat-*.geojson` | 4 files, all `communes/gandiole/habitat-*.geojson` |
| Économie et énergie | none (honest MISSING) | 3 files, all `-gandon.geojson` | 2 files, all `-gandiol.geojson` |

**No cross-commune leakage found.** Every commune's diagnostic pages load only files scoped to that commune (or global-context layers explicitly labeled as such, e.g. the hillshade).

---

## 5. SVD content validation

Automated tests (`test_svd_vision_not_cross_commune`) confirm Gandon's vision quote never appears on Gandiole's page and vice versa. Manual spot-check confirms "Vision intercommunale" and "Spécifique à {commune}" badges render correctly on all 3 pages, matching `SVD_CONTENT_BASELINE.md`'s documented shared-vs-specific split. No source SVD `.docx` files were touched. **Result: PASS.**

---

## 6. PCU/PCUI validation

Automated test (`test_pcu_never_claims_fully_available`) confirms no commune's PCU page ever shows the "Disponible" badge — only "Partiel" (Zonage/PIP where real data exists) or "En attente de données client" (everything else), matching `PCU_CONTENT_BASELINE.md` exactly. A second test confirms Gandon's "Zone d'extension" layer is explicitly labeled as an orientation/non-approved layer, never as official zoning. **Result: PASS — honest completeness confirmed.**

---

## 7. JavaScript / maps — problems found and fixed

| Problem | Where | Severity | Fix |
|---|---|---|---|
| **Double-UTF-8-encoding bug**: 5 of 17 Occupation du sol 2020 categories (Carrière Mine Infrastructure, Culture irriguée, Culture maraichère, Plantation forestière, Vasière) were stored mojibake-corrupted in the generated GeoJSON, and — because the `categoryColors` JS lookup silently falls back to a default grey on a missed key — this was invisible as an "error," just wrong colors and (if ever inspected) garbled popup text. Root cause: my own Wave 2 conversion script wrongly forced `encoding="cp1252"` on a file whose `.cpg` declaration (`UTF-8`) was actually correct — a conclusion I'd reached by trusting a misleading terminal print in this environment, before I'd diagnosed that same rendering artifact properly in Wave 3. | `occupation-du-sol-2020.geojson` (+ its Saint-Louis-clipped copy) | **HIGH** (silent data corruption, user-visible garbled text) | Regenerated both files from the original client shapefile with the correct encoding; added a byte-level self-check (`assert b"\xc3\x83" not in raw`) to the regeneration script so this class of bug can't silently reappear; added a regression test. |
| **Spelling mismatch**: `categoryColors` dict used "Protection Patrimoniel" while the source data's actual (typo'd) value is "Protection Patrimoinel" | `diagnostic.py`, `commune_diagnostic_data.py` (Zones de conservation layer) | **MEDIUM** (1 feature always fell back to default grey) | Corrected both dicts to match the source's exact spelling. |
| **Risk maps never loaded their data**: `/risques/vulnerabilite` and `/risques/erosion` extended `base_risk.html` but never overrode the `risk_layers` block — both showed a bare basemap despite real data existing (1,058 and 3 features respectively) | `risques/vulnerabilite.html`, `risques/erosion.html` | **HIGH** (pre-existing bug tracked as R3 in `PROJECT_ANALYSIS.md` since Phase 1, never fixed until now) | Added the missing `risk_layers` block to both, following the working `inondation.html` pattern. Added a regression test for both. |

No JS syntax errors were found (verified with `node --check` across every inline `<script>` block on 19 representative pages). No duplicate layer IDs, no undefined-variable errors, no layer-control problems found in any template.

---

## 8. Performance audit

| Asset/Page | Size | Classification | Action |
|---|---|---|---|
| Global Topographie theme (`courbes-niveau.geojson` 6.1MB + `courbes-niveau-5m.geojson` 3.7MB + hillshade 0.9MB, all auto-loaded) | ~10.6MB uncompressed (GZip middleware reduces actual transfer significantly for the JSON portion) | **HIGH** | Documented, not silently changed — see recommendation below |
| Gandon's Milieu physique + Urbain/mobilité diagnostic pages (multiple clipped contour/geologie/risques layers) | ~5–8MB combined | **MEDIUM** | Documented |
| 3 SVD PDFs (14–16MB each) | Download-only, not auto-loaded | **LOW** | Appropriately gated behind an explicit "Consulter le rapport complet" click, no action needed |
| Diagnostic theme static images (situation.jpg, occupation-sol.jpg, etc., 1.8–5.5MB each) | Loaded on every relevant theme page view | **MEDIUM** | Applied `loading="lazy"` (zero-risk, native browser attribute, no file modified) |
| `occupation-sol/culture-maraichere.geojson` (1.8MB) | Not referenced anywhere (orphaned) | **LOW** | No active cost; listed in §15 |

**Recommendation, not applied (architectural, out of scope for a stabilization pass):** the Topographie theme's practice of auto-fetching every configured layer on page load, regardless of its checkbox state, means a visitor who unchecks a layer has already paid its download cost. Converting to fetch-on-first-enable (all layers start unchecked except a lightweight default) would meaningfully help the heaviest pages on slow connections. This is a real, worthwhile optimization but changes existing default behavior (which layers are visible on first paint), so it wasn't applied silently here — flagged as a recommendation for a future wave with explicit sign-off.

---

## 9. Mobile / responsive review

Reviewed the newest templates (built without live browser testing: `communes/pcu.html`, `communes/svd.html`, `communes/diagnostic_section.html`, `communes/diagnostic_index.html`) for the same responsive conventions already proven in Wave 1–4A:
- The PIP table is wrapped in `overflow-x-auto` (won't force horizontal page scroll on narrow screens).
- The section-tab navigation is wrapped in `overflow-x-auto` (many tabs scroll horizontally rather than wrapping awkwardly).
- All map+sidebar layouts use `grid lg:grid-cols-4` (mobile-first: stacks to a single column below the `lg` breakpoint, matching the pattern already used and working in `diagnostic_unified.html` since Wave 1).

**No responsive bugs found.** No redesign performed.

---

## 10. Accessibility / UX basics

- Every `<img>` tag across all templates has an `alt` attribute (verified across every template file).
- Headings follow a logical order in every page reviewed (h1 → h2 → h3).
- Missing-data states are never silent: every MISSING/PARTIAL PCU section and every incomplete-coverage GIS layer shows an explicit French-language note rather than an empty control (per Wave 3/4A/4C design decisions, re-verified here).
- No broken internal links found (every route in §1 resolves).

---

## 11. Security / robustness

| Issue | Status |
|---|---|
| `/api/log` crashed with an unhandled `JSONDecodeError` (raw stack trace) on malformed input | **FIXED** — wrapped in `try/except`, returns a clean `400`; also added payload-type checking, a 3-value allowlist for `level`, and truncation of `message`/`page` to 500 characters each (basic size/input hardening, addresses part of `PROJECT_ANALYSIS.md` R2) |
| Contact form has no server-side validation beyond FastAPI's required-field checking | Reviewed — low real risk since submitted data is never stored or reflected back to any page (confirmed: the success message is a static string, not a template of user input) — no XSS/injection surface exists today. No change made. |
| No authentication anywhere on the site | Confirmed intentional — the site is meant to stay fully public, per explicit instruction. Not changed. |
| `FastAPI()` instantiated without `debug=True` | Confirmed — unhandled exceptions return a generic 500, not an interactive traceback, in the current configuration. |
| Visitor IP logged in plaintext (pre-existing, `PROJECT_ANALYSIS.md` R8-adjacent) | Not changed — low priority, already documented, no retention policy exists but no PII beyond IP is logged. |

No authentication was introduced, per explicit instruction that the site must remain public.

---

## 12. Contact form

**Status: still a delivery blocker, not fixed, honestly documented — not pretended to work.**

The form still discards every submission (`app/routers/home.py`, explicit `# TODO` comment, unchanged). No SMTP credentials, email service, or storage backend exist anywhere in the project or its configuration, and none were invented. Per the two options given for this phase (A: implement if configuration already exists, B: document as a blocker requiring configuration) — option A does not apply since no email/service configuration exists anywhere in the codebase or environment. This is already listed as an open item in `REPLY_CLIENT_REQUEST.md`'s priority list (the client has confirmed they want this form to support information/layer requests) and remains flagged here as a **MUST COME FROM CLIENT** item (an email address or SMTP/service configuration to send to) before it can be safely implemented.

---

## 13. Clean install test

**PASS.** Created a genuinely fresh virtual environment, installed only `requirements.txt`, and confirmed: clean import, server starts, serves all tested routes (including the newest PCU/SVD/commune pages) with zero errors. Then installed `requirements-dev.txt` on top and confirmed all 76 tests pass identically in that clean environment — proving the project does not depend on anything installed globally on this machine.

---

## 14. Vercel readiness

- `api/index.py` and `vercel.json` reviewed — unchanged, both still correct and minimal.
- No hardcoded Windows-only paths found anywhere in `app/` (confirmed via full-codebase search) — every path uses `Path(__file__).resolve().parent...`, which is platform-independent.
- Total `app/static/` size: **130 MB**, comfortably under the `maxLambdaSize: 250mb` already configured (52% utilization — some headroom remains, but noticeably less than in earlier waves given how much GIS data has been added since; worth monitoring before adding much more).
- No Vercel CLI or account access was available in this environment.

**`LOCAL VERIFIED — VERCEL PREVIEW STILL REQUIRED`**

---

## 15. Dead / orphaned files — cleanup recommendation (nothing deleted)

| Item | Status | Recommendation |
|---|---|---|
| 10 orphaned templates (`about.html`, `contact.html`, `downloads.html`, `diagnostic/base_theme.html` + 6 children) | Unreferenced since before Phase 1 | Safe to delete at final delivery; kept until then per this project's established convention |
| `app/templates/communes/branch_placeholder.html` | Newly orphaned — both `/svd` (Wave 4B) and `/pcu` (Wave 4C) now use their own dedicated templates | Safe to delete at final delivery |
| `aiofiles` in `requirements.txt` | Still never imported anywhere | Safe to remove at final delivery |
| `app/static/img/cartes/geologie-detail.jpg` | Still never referenced | Safe to delete at final delivery |
| 49 orphaned `.geojson` files | Mostly correct-by-design (zero-feature commune clips, intentionally excluded) or pre-existing (mojibake-named equipment files, `culture-maraichere.geojson`) | No action — documented, not a bug |

Per instruction, nothing was deleted this phase — recommendation only, deferred to final delivery.

---

## 16. Client-dependent blockers

### MUST COME FROM CLIENT
- Official PCU/PCUI rapport de présentation, approved zonage, formal PIP (cost/schedule/responsible/status fields), règlement d'urbanisme, EES, atlas cartographique — all per `PCU_CONTENT_BASELINE.md`.
- RINA logo file.
- Confirmation of the Gandon "Zone d'extension" layer's actual status (orientation sketch vs. approved).
- Email/SMTP or third-party service configuration for the contact form to actually send messages.
- Remaining GIS gaps already itemized in `REPLY_CLIENT_REQUEST.md` (village names, Gandon équipements, energy/economic coverage gaps, corrected `Boucle de Gandiolais`/`CN_10m`, authoritative urban-footprint dataset confirmation).

### CAN BE PRODUCED INTERNALLY AFTER CLIENT APPROVAL
- Bassins versants derived from the existing MNT (explicitly not attempted without approval, per every prior wave's instruction).
- Any GIS layer export/download tooling, once the client confirms which layers and formats are actually wanted.

### TECHNICAL WORK WE CAN COMPLETE OURSELVES
- Everything in this report (testing, the 3 bug fixes, performance/mobile/accessibility review, clean-install verification) — already done.
- The documented performance recommendation (lazy layer-fetch) — feasible in-house whenever prioritized.
- Migrating `@app.on_event` to FastAPI's newer lifespan-handler API (currently only a deprecation warning, not a functional problem) — low priority, not done this phase to avoid touching working startup/shutdown logic without cause.

---

## Bugs fixed (exact list)

1. `/api/log` — unhandled exception on malformed JSON → clean 400 + basic input hardening.
2. `occupation-du-sol-2020.geojson` (global + Saint-Louis-clipped copy) — double-UTF-8-encoding corrupting 5 of 17 category names.
3. `categoryColors` spelling mismatch ("Patrimoniel" vs. actual "Patrimoinel") in 2 files.
4. `/risques/vulnerabilite` and `/risques/erosion` — never loaded their data layer (pre-existing bug, tracked since Phase 1, fixed now).

## Files changed

- `app/main.py` (`/api/log` hardening)
- `app/routers/diagnostic.py` (categoryColors spelling fix)
- `app/routers/commune_diagnostic_data.py` (categoryColors spelling fix)
- `app/templates/risques/vulnerabilite.html` (added missing `risk_layers` block)
- `app/templates/risques/erosion.html` (added missing `risk_layers` block)
- `app/templates/diagnostic_unified.html` (added `loading="lazy"` to the theme image)
- `app/static/data/occupation-sol-2020/occupation-du-sol-2020.geojson` (regenerated with correct encoding)
- `app/static/data/communes/saint-louis/occupation-sol-2020.geojson` (re-clipped from the corrected file)
- `REPLY_CLIENT_REQUEST.md` (removed already-resolved items)

**New files:**
- `tests/__init__.py`, `tests/test_routes.py` (76 automated tests)
- `requirements-dev.txt` (test-only dependencies)
- `PHASE5_STABILIZATION_REPORT.md` (this file)

## Remaining technical work

- Apply the documented lazy layer-fetch optimization to the heaviest diagnostic pages (Topographie, Gandon's Milieu physique) — architectural, needs explicit go-ahead since it changes default on-load behavior.
- Migrate `@app.on_event` startup/shutdown handlers to FastAPI's lifespan API (cosmetic deprecation warning only).
- Delete the confirmed-dead files in §15 at final delivery.
- An actual Vercel preview deployment, once CLI/account access is available.

## Final recommendation

`READY FOR CLIENT PREVIEW`

The application is stable, tested, and free of the bugs found during this pass. What remains is exclusively client-supplied material (PCU/PCUI documents, logo, contact-form email configuration) already itemized in `REPLY_CLIENT_REQUEST.md`, plus one deployment step (an actual Vercel preview) that requires access not available in this environment. No further internal development is blocking a client preview.
