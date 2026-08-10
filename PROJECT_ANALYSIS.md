# PROJECT_ANALYSIS.md — SIG Saint-Louis

Baseline architecture documentation. Produced from a full Phase 1 read-only analysis of the repository (commit `d6a038f`, branch `main`, clean tree). Treat this file as the reference baseline for all future work — compare every future client request against it before touching code.

**Verification depth:** every active template read in full, all inline JavaScript inspected, `style.css` read in full, all 78 GeoJSON files validated programmatically (structure, feature counts, geometry types, encoding), every static asset reference checked against disk, every route traced end-to-end to its template and data sources. Unless a line below is explicitly marked INFERRED or UNKNOWN, it is CONFIRMED by direct inspection of the code/data at commit `d6a038f`.

*This revision supersedes all prior versions of this file — 9 new issues were found during this deep pass, including two functional bugs (R3, R4 below) that silently break real user-facing behavior. No application code was modified while producing this document.*

---

## 1. Project Objective

**CONFIRMED:**
- FastAPI app metadata (`app/main.py`): *"Diagnostic Territorial de l'Agglomération de Saint-Louis du Sénégal"*.
- Footer/`projet.html` branding: **ADM — Agence de Développement Municipal** (maître d'ouvrage), **Programme SERRP**, produced by **COMETE International / RINA Consulting**. Full program name found in `projet.html`: *"Projet de Relèvement d'Urgence et de Résilience à Saint-Louis"*.
- Purpose stated in `projet.html`: elaboration of three communal/intercommunal urbanism plans (**PCU/PCUI**) for the Saint-Louis agglomeration. The **SVD** ("Stratégie de Ville Durable") is the strategic document this diagnostic feeds into, aligned with ODD (SDGs), "Sénégal 2050," and international climate conventions.
- Public, French-language site covering 3 communes — **Saint-Louis, Gandon, Ndiébène Gandiol** — across 9 diagnostic themes (géologie, pédologie, topographie, occupation du sol, urbanisation 2017–2024, risques naturels, transport, population, équipements).
- Backed by real data: 78 GeoJSON files (~25,000 total features), RGPH-5 2023 census figures, 196 commune photos, 3 downloadable PDF "SVD" reports (one per commune).

**INFERRED:** audience is municipal planners and ADM/SERRP/COMETE stakeholders, secondarily the general public. No login/editing exists, so it reads as a communication/diagnostic deliverable, not a working GIS editor.

**UNKNOWN:**
- Whether site content is expected to change often (would justify externalizing config) or is frozen for this study.
- Origin/pipeline of the GeoJSON datasets (relevant to fixing encoding bugs at the source vs. downstream).
- Whether the numeric mismatches found in §10 (14 vs. 18 "catégories," hardcoded homepage chart data) reflect stale content from an earlier data cut, or were simply never reconciled.

---

## 2. Technology Stack

**Languages:** Python (backend), Jinja2/HTML (views), inline JavaScript (no build step), CSS, GeoJSON (all data).

**Backend**
- FastAPI ≥0.111 — sole framework; `app/main.py` + 6 routers, no separate service/repository layer.
- Uvicorn ≥0.30 — local dev only (`uvicorn app.main:app`, confirmed no Procfile/run-script exists — this is a manual developer command); Vercel's own runtime serves production.
- Starlette (transitive) — `GZipMiddleware`, `StaticFiles`.
- `python-multipart` — required for the one `Form(...)` handler (contact form).
- No ORM, no database driver, no auth library.

**Frontend**
- Tailwind CSS via CDN `<script src="https://cdn.tailwindcss.com">` (JIT runtime build, not compiled/purged), custom `primary`/`accent`/`danger` palette configured inline in `base.html`.
- Leaflet 1.9.4 (CDN/unpkg) — all interactive maps, **4 independent hand-rolled implementations** (see §8.2).
- Chart.js 4.4.7 (CDN/jsdelivr) — 4 homepage charts, built from hardcoded JS arrays disconnected from all backend data (see §10.1).
- One hand-written stylesheet: `app/static/css/style.css`, 96 lines, read in full (see §8.3).
- No JS framework, no bundler, no `package.json`.

**Database:** None. All "data" = hardcoded Python dicts in router files + static `.geojson` files read from disk.

**DevOps / Infrastructure**
- Vercel is the sole deployment target. `vercel.json` routes **all** paths — including `/static/*` — through one Python serverless function (`api/index.py`, `@vercel/python`, `maxLambdaSize: 250mb`, raised specifically for the bundled images/GeoJSON per commit `d6a038f`). See §11 for the implication of this.
- No Docker, no Kubernetes, no CI/CD (no `.github/workflows` or any CI config).
- Custom file-logging, environment-aware (`VERCEL=1` → `/tmp/logs`, ephemeral; local → `<repo>/logs`).
- No APM/monitoring integration.

**Testing:** None. No test files, no test framework dependency, no `tests/` directory.

### 2.1 Dependency Classification (`requirements.txt`)

| Package | Classification | Evidence |
|---|---|---|
| `fastapi` | **Used — core** | App framework, all routers |
| `uvicorn` | **Used — dev only** | Manual local run command; not invoked anywhere in production path |
| `jinja2` | **Used — core** | `Jinja2Templates` in every router |
| `python-multipart` | **Used — core** | Required transitively by `Form(...)` in `home.py`'s contact handler |
| `aiofiles` | **Unused — dead** | Zero `import aiofiles` anywhere in the codebase; confirmed via full-repo search |

---

## 3. Repository Structure

```
api/index.py                — Vercel entry point (2 lines, re-exports app)
app/main.py                  — FastAPI app, middleware, logging, router registration
app/routers/                 — 6 routers = the entire backend "controller" layer
  home.py, diagnostic.py, risques.py, equipements.py, communes.py, carte.py
app/templates/                — 23 template files total: 13 active, 10 orphaned (see §8.1)
app/static/
  css/style.css              — one stylesheet, 96 lines
  data/**/*.geojson (78)     — all geographic content, ~25,000 features total, 14 MB
  img/svd/**/*.jpg (196)     — per-commune photo galleries, part of 47 MB img/
  img/cartes, img/logos      — static map images (8 files, all referenced), partner logos
  docs/*.pdf (3)             — one SVD report per commune, 45 MB total
vercel.json, requirements.txt, README.md (1 line, no content)
```
Total `app/static/`: **106 MB** (14 MB data + 45 MB docs + 47 MB img) — see §11 for the deployment implication.

---

## 4. Architecture

**Pattern:** a flat, **router-per-feature monolith with server-side template rendering** — routers act as controllers, Jinja templates as views, hardcoded Python dicts as an inline "model." There is **no distinct Service layer or Repository layer**.

```
Browser (Leaflet / Chart.js / Tailwind, inline JS only)
   ↓ HTTP GET/POST
Vercel routing (vercel.json — every path, including /static/*, → one function)
   ↓
api/index.py  (2 lines: re-exports the ASGI app)
   ↓
app/main.py  (FastAPI app: GZip + logging middleware, StaticFiles mount, 6 routers)
   ↓
app/routers/{home,diagnostic,risques,equipements,communes,carte}.py
   │  — hardcoded Python dicts (content/config)
   │  — direct filesystem reads (Path.glob/rglob/json.load) of app/static/data/**/*.geojson
   ↓
Jinja2Templates.TemplateResponse → app/templates/**/*.html
   ↓
HTML response → browser JS fetches raw GeoJSON via /static/data/... for client-side Leaflet rendering
```

Appropriate for the project's current scope (a ~10-endpoint informational GIS microsite) but would need a real data/service layer if content starts changing frequently or grows substantially.

---

## 5. Design Patterns Identified

| Pattern | Where | Notes |
|---|---|---|
| Front Controller / Router-per-feature | `app/main.py` `include_router` × 6 | Idiomatic FastAPI usage |
| Template View | Every router → `templates.TemplateResponse(...)` | Correctly applied; "model" is inline dict literals |
| Configuration-as-code dict | `SECTIONS` (`diagnostic.py`), `COMMUNES`/`SECTOR_LABELS` (`equipements.py`, `communes.py`), `LAYER_GROUPS` (`carte.py`) | Works at current scale; every content edit requires a code deploy |
| Template Inheritance (`extends`/`block`) | `base.html` → `diagnostic/base_theme.html` (unused branch), `risques/base_risk.html` (active) | Consistently applied in the active template tree; see §8.1 for the dead branch |
| Legacy redirect shim | `home.py`, `diagnostic.py` — multiple 301 `RedirectResponse` | Evidence of a prior URL-structure migration, handled cleanly |

**Not present:** Repository, Dependency Injection (`Depends()`), Pydantic request/response DTOs, Unit of Work, Factory, Strategy, Observer, CQRS. No business-rule complexity currently warrants them.

---

## 6. Routes — Full Cross-Check

Every route traced end-to-end (Route → Router → Function → Template → Data/assets). All referenced templates and data files were confirmed to exist; no broken references found anywhere.

| Route | Method | Function | Template | Data / assets used |
|---|---|---|---|---|
| `/` | GET | `home.home_page` | `home.html` | Hardcoded `STATS` (accurate — see §10.1) + 4 hardcoded Chart.js datasets (inaccurate — see §10.1) |
| `/projet` | GET | `home.projet_page` | `projet.html` | Static content, no data |
| `/ressources` | GET/POST | `home.ressources_page` / `ressources_submit` | `ressources.html` | Static PDF/image download links (all verified to exist) + contact form (POST discards input) |
| `/diagnostic?section=` | GET | `diagnostic.diagnostic_page` | `diagnostic_unified.html` | `SECTIONS` dict — all 27 referenced layer files confirmed to exist on disk |
| `/risques/inondation` | GET | `risques.inondation_page` | `risques/inondation.html` | Loads `risques/risque-inondation.geojson` (147 features) — **works correctly** |
| `/risques/vulnerabilite` | GET | `risques.vulnerabilite_page` | `risques/vulnerabilite.html` | `risques/vulnerabilite.geojson` exists (1,058 features) but **is never fetched — see R3** |
| `/risques/erosion` | GET | `risques.erosion_page` | `risques/erosion.html` | `risques/erosion.geojson` exists (3 features) but **is never fetched — see R3** |
| `/equipements/{commune}` | GET | `equipements.equipements_page` | `equipements/commune.html` | Sector GeoJSON — **not commune-specific, see R4** |
| `/communes/`, `/communes/{slug}` | GET | `communes.communes_index` / `commune_detail` | `communes.html`, `commune_detail.html` | Hardcoded `COMMUNES` dict + dynamically globbed SVD images (verified: 65/69/62 images exist for the 3 communes, capped to 20 shown) |
| `/carte/` | GET | `carte.carte_page` | `carte.html` | `LAYER_GROUPS` — only 5 of 9 diagnostic themes represented, see R10 |
| `/api/log` | POST | `frontend_log` | — | Writes client JSON straight into server logs, no auth (R2) |
| `/a-propos`, `/telechargements`, `/contact`, `/diagnostic/{situation,geologie,pedologie,topographie,occupation-du-sol,evolution-urbaine}` | GET | various `redir_*` | — | 301 redirects to current routes — all confirmed to point at real, working destinations |

No unreachable pages, no broken links, no dangling redirects were found. The only "obsolete" surface is the orphaned template files in §8.1, which have no route pointing at them at all (not even a broken one).

---

## 7. Backend Analysis

Each router owns its own `Jinja2Templates` instance (redundant — `main.py` also creates one that's never used). `equipements.py`, `communes.py`, `carte.py` do **synchronous** `Path.glob`/`json.load` filesystem I/O inside `async def` handlers. No controller contains business logic complex enough to warrant a service layer — except `equipements.py`, which has a genuine correctness bug (R4, below): it does per-sector filesystem globbing but the sector directories are shared across **all** communes, so it silently returns identical counts and file lists regardless of which commune was requested.

---

## 8. Frontend Analysis

### 8.1 Templates — active vs. orphaned (23 total, all read in full)

**13 active** (each confirmed rendered by at least one router): `base.html`, `home.html`, `projet.html`, `ressources.html`, `diagnostic_unified.html`, `carte.html`, `communes.html`, `commune_detail.html`, `equipements/commune.html`, `risques/base_risk.html`, `risques/inondation.html`, `risques/vulnerabilite.html`, `risques/erosion.html`.

**10 orphaned** (no router renders them; confirmed via cross-check of every `TemplateResponse(...)` call against the full file list): `about.html`, `contact.html`, `downloads.html`, `diagnostic/base_theme.html` and its 6 children (`geologie.html`, `pedologie.html`, `topographie.html`, `occupation.html`, `evolution.html`, `situation.html`). These predate the diagnostic-theme unification into `diagnostic_unified.html` and the about/contact/downloads → `/projet`/`/ressources` rename. All still `{% extends %}` correctly and would render if hit directly, but nothing links to them.

### 8.2 JavaScript — four independent Leaflet implementations

Every map-bearing template hand-rolls its own Leaflet setup with no shared JS module (no bundler exists to support one):

| Template | Fetches | Popup field filtering | Failure UX |
|---|---|---|---|
| `diagnostic_unified.html` | Per-theme layers via `{{ data.layers | tojson }}` | None — shows all raw properties | Silent (`FLog.error` only, no user-visible message) |
| `carte.html` | On-demand per checkbox toggle, with a `layerCache` | Filters `FID`/`OBJECTID` | **Only page with a real user-facing error** (`showNotification`) |
| `commune_detail.html` | Commune's `layers` list via `L.control.layers` | None — shows all raw properties | Silent (`console.warn` + `FLog.error`) |
| `equipements/commune.html` | Every sector file individually | Filters `FID`/`OBJECTID`/`Shape_Leng`/`Shape_Area` | Silent (`.catch(() => {})`, no logging at all) |

All four correctly filter out features with `null`/missing geometry before rendering (a real defensive pattern, consistently duplicated). `base.html`'s `FLog` object (`/api/log` POST) is the one shared piece of frontend infrastructure and is used consistently for page-load and JS-error telemetry.

**risques/base_risk.html** defines two overridable blocks, `risk_description` and `risk_layers`. Only `risques/inondation.html` overrides both. `vulnerabilite.html` and `erosion.html` override only `risk_description` — see **R3**.

### 8.3 CSS — `style.css` (96 lines, read in full)

Six small, well-scoped component classes: `.nav-link`/`.mobile-link` (nav styling + `.active` state), `.theme-card` (homepage theme grid), `.stat-card` (padding only), Leaflet popup overrides (`.leaflet-popup-content-wrapper/-content`), a custom scrollbar for `.layer-panel`, and `.prose h2/p` for text blocks. No unused selectors detected (all six are referenced by at least one active template), no conflicts with Tailwind observed, no duplication within the file. Low risk, low maintenance burden.

---

## 9. GeoJSON / Data Verification

All 78 files were parsed and validated programmatically. **Zero invalid JSON, zero malformed FeatureCollections, zero empty datasets, zero null/missing geometries** — the geodata itself is structurally solid.

| Folder | Files | Features | Notes |
|---|---|---|---|
| `base/` | 2 | 57 | Polygons only |
| `diagnostic/geologie/` | 8 | 56 | Matches `diagnostic.py`'s 8 wired layers exactly |
| `diagnostic/topographie/` | 1 | 13,762 | `courbes-niveau.geojson` — by far the densest single file |
| `equipements/culture/` | 5 | 12 | Points |
| `equipements/economie/` | 16 | 173 | Points + polygons; **1 mojibake file** (below) |
| `equipements/education/` | 13 | 154 | Points |
| `equipements/sante/` | 1 | 1 | Single hospital point |
| `equipements/sport/` | 5 | 58 | Points |
| `evolution/` | 4 | 616 | Urban footprint polygons, 2017/2020/2024 + lotissements |
| `occupation-sol/` | 11 | 6,104 | **`culture-maraichere.geojson` alone = 3,649 features, wired into zero layer lists — see R8** |
| `population/` | 2 | 66 | Points + polygons |
| `risques/` | 3 | 1,208 | `vulnerabilite.geojson` (1,058 features) and `erosion.geojson` (3 features) are real and complete — confirms **R3** is a display bug, not a missing-data issue |
| `transport/` | 7 | 2,737 | **1 mojibake file** (below), otherwise clean |

**Encoding issues confirmed in 2 files** (both are genuine mojibake — UTF-8 bytes re-decoded as Latin-1 — not a terminal display artifact):
- `transport/route-tertiaire.geojson` — pervasive; corrupted substrings (e.g. `"Ã‰tat de s"`, `"RÃ©fÃ©renc"`) detected across nearly all 127 features.
- `equipements/economie/site-touristique-général.geojson` — same corruption pattern, ~19 occurrences across its 8 features. **(Newly found in this pass — not previously documented.)**

No other files show encoding problems. All accented filenames (é, è, etc.) are correctly UTF-8 encoded at the filesystem level — they only render as `�` in this session's Windows terminal, which is a terminal-encoding artifact, not a data defect.

---

## 10. Cross-Check: Duplicated / Inconsistent Data

Three genuine, confirmed data-consistency problems were found by comparing the same real-world facts across Python dicts, templates, and JS:

### 10.1 Homepage Chart.js numbers are fabricated, not computed
`home.html`'s 4 charts are hardcoded JS arrays with no connection to any backend data:
- **Population chart** — 237,000 / 78,000 / 35,000 — happens to **match** `communes.py`'s real population figures exactly. ✅ Consistent (likely copied by hand at some point).
- **Urbanisation chart** — per-commune hectare figures (e.g. Saint-Louis 3200→3450→3800 ha) — measures something entirely different from `diagnostic.py`'s "urbanisation" stats (zone *counts*: 195→202→215), and neither is derived from the actual `evolution/empreinte-*.geojson` polygon areas.
- **Équipements chart** — e.g. "Saint-Louis: 82 écoles" — does not match the real on-disk total for the `education` sector (154 features across all communes combined, since equipment data isn't split by commune at all — see R4). This number appears to be invented, not computed.
- **Risques chart** — percentages (35/30/25/10%) for 4 risk levels — doesn't correspond to `diagnostic.py`'s risk stats (147 flood zones / 1,058 vulnerability zones / 3 erosion zones), a different unit entirely with no stated source.

### 10.2 "Occupation du sol" category count contradicts itself
- `diagnostic.py`: subtitle *"Occupation du sol — 14 catégories"*, content text *"14 catégories d'occupation du sol cartographiées"*, and stats value `"14"`.
- `home.html` and `ressources.html`: both independently state *"18 catégories d'utilisation du territoire"*.
- Neither number matches the 11 actual `.geojson` files present in `occupation-sol/`. This is a direct textual contradiction between three source files, not just a stale-vs-fresh issue.

### 10.3 `equipements.py` doesn't actually vary by commune
Confirmed by reading the code: `sector_dir = data_dir / sector` always resolves to the same shared directory (`app/static/data/equipements/{sector}/`) regardless of which commune was requested. There is no per-commune subfolder and no geographic/property-based filtering anywhere in the function. **Every commune that lists a given sector in `COMMUNES[slug]["sectors"]` displays the exact same total count and exact same file list for that sector.** For example, both Saint-Louis and Gandon list `"education"`, so `/equipements/saint-louis` and `/equipements/gandon` render identical education numbers and identical school names, even though they are different territories. This is a data-integrity bug, not just a display inconsistency — see **R4**.

---

## 11. Deployment Analysis

- **Local:** `uvicorn app.main:app` serves directly from the filesystem; no read-only constraints, logs go to `<repo>/logs`.
- **Vercel:** `vercel.json` routes **every** path — including `/static/*` — through the single `api/index.py` function. This means the entire `app/static/` tree (**106 MB**: 14 MB geodata + 45 MB PDFs + 47 MB images) is packaged into and served through the Python serverless function itself, rather than through Vercel's dedicated static-asset CDN layer. `maxLambdaSize` was already raised to 250 MB specifically to fit this (per commit `d6a038f`, "perf: compress SVD images for Vercel bundle size limit") — confirming the project has already once bumped against a platform ceiling because of this routing choice. Every image, PDF, or GeoJSON fetch round-trips through the Python runtime instead of a CDN edge, adding latency and leaving less headroom before the next size-limit crisis if more photos/reports/data are added. **(New finding — see R16.)**
- Logging is Vercel-aware (`try/except OSError` guard around `/tmp/logs`), correctly handling the read-only production filesystem.
- No environment variables, secrets, or per-environment config files exist beyond the single `VERCEL=1` flag check.

---

## 12. Security Issues

| Severity | Issue | Evidence |
|---|---|---|
| **HIGH** | `POST /api/log` — unauthenticated, unvalidated, unrate-limited write into server logs | `app/main.py` |
| **MEDIUM** | No CORS policy configured anywhere | repo-wide grep, zero `CORSMiddleware` matches |
| **MEDIUM** | Contact form has no server-side validation, no CSRF protection | `home.py` (low real risk since nothing is persisted) |
| **LOW** | Visitor IP logged in plaintext with no retention/redaction policy | `app/main.py` |
| **LOW** | CDN scripts (Tailwind/Leaflet/Chart.js) loaded with no Subresource Integrity | `base.html` |
| — | No secrets/API keys/credentials found anywhere | confirmed |
| — | No auth system exists — every route public (appropriate for this use case) | confirmed |

No CRITICAL issues — there is no auth to break and no database to inject into.

---

## 13. Testing Strategy

None exists. No test files, no framework dependency, no `tests/` directory, no CI. Given the two functional bugs found in this pass (R3, R4) were both silent — no error, no 500, no visible symptom short of manually comparing pages — a handful of smoke tests asserting "this page's map actually receives N features" or "these two communes' equipment counts differ" would have caught both immediately.

---

## 14. Code Quality, Dead Code & Technical Debt

- Content/config (`SECTIONS`, `COMMUNES`, `SECTOR_LABELS`, `LAYER_GROUPS`) hardcoded inside router files — couples every content edit to a code deploy.
- Duplicate, unused `Jinja2Templates` instantiation in `main.py`.
- Duplicated Leaflet/GeoJSON-fetch JS boilerplate across 4 templates, each with subtly different behavior (§8.2) — this divergence is itself a maintenance risk (a fix applied to one map's popup filtering won't propagate to the other three).
- `aiofiles` declared but dead.
- Contact form is an unfinished feature (explicit TODO).
- 10 orphaned template files (§8.1).
- `img/cartes/geologie-detail.jpg` — exists on disk, never referenced anywhere (confirmed via full repo grep). **(New finding.)**
- `occupation-sol/culture-maraichere.geojson` (largest dataset in the project) is orphaned from every layer configuration (§9, R8).

---

## 15. What the Project Does Well

1. Right-sized architecture — no over-engineering for a ~10-page informational GIS site.
2. Consistent, DRY Jinja template inheritance across the *active* template tree.
3. Environment-aware logging correctly handles Vercel's read-only filesystem.
4. Legacy URL redirect shims show deliberate care during a prior refactor — confirmed zero broken links or dangling redirects across the entire route surface (§6).
5. Client-side error telemetry (`FLog`) gives real visibility with zero APM tooling.
6. Defensive GeoJSON parsing (`try/except` around file reads, null-geometry filtering duplicated consistently across all 4 map implementations) — a malformed or incomplete feature can't crash a page.
7. The GeoJSON data itself is structurally clean: 78/78 files are valid FeatureCollections with zero corrupt JSON, zero empty datasets, zero null geometries.
8. Rich, well-organized real-world domain data (78 GeoJSON layers, ~25,000 features, 3 commune PDFs, 196 photos, all correctly cross-referenced against disk with zero missing files).
9. `home.py`'s "78 couches cartographiques" stat is exactly accurate against the real file count — a small but real sign of care taken when it was written.

---

## 16. Problems and Risks (Full, Updated)

| ID | Severity | Area | Problem | Evidence | Impact |
|---|---|---|---|---|---|
| R1 | **P1** | Functional | Contact form silently discards every submission | `home.py` TODO comment | Visitors believe their message was sent; ADM/SERRP never receives it |
| R2 | **P1** | Security | `POST /api/log` has zero auth/validation/rate-limiting | `app/main.py` | Anyone can write arbitrary strings into server log files |
| R3 | **P1** | Functional (NEW) | `/risques/vulnerabilite` and `/risques/erosion` never load their map layer — both pages only override `risk_description`, never `risk_layers`, so real, existing data (1,058 and 3 features respectively) is never fetched or shown | `risques/vulnerabilite.html`, `risques/erosion.html` vs. `risques/base_risk.html` | 2 of the 3 dedicated risk pages show a blank map with zero data — a real, silent functional bug |
| R4 | **P1** | Data integrity (NEW) | `equipements.py` never filters by commune — every commune sharing a sector shows identical counts/lists for that sector | `equipements.py` — `sector_dir = data_dir / sector` is commune-independent | Equipment numbers/lists shown per commune are factually wrong for every commune except (at best) one |
| R5 | **P2** | Data quality | Mojibake encoding in 2 files, not 1: `transport/route-tertiaire.geojson` (pervasive) and `equipements/economie/site-touristique-général.geojson` (new finding) | Programmatic validation of all 78 files | Garbled French labels if shown in a popup |
| R6 | **P2** | Code quality | Blocking synchronous file I/O inside `async def` route handlers | `equipements.py`, `communes.py`, `carte.py` | Minor perf inconsistency |
| R7 | **P2** | Testing | Zero automated test coverage | No test files exist | R3/R4 above went undetected because nothing asserts expected behavior |
| R8 | **P2** | Data completeness (NEW) | `occupation-sol/culture-maraichere.geojson` (3,649 features — largest dataset in the project) is wired into zero layer lists anywhere | `diagnostic.py`'s `occupation` layers vs. on-disk file list; `carte.py`'s `LAYER_GROUPS` | Over half of the occupation-sol theme's data is invisible on every map |
| R9 | **P2** | Content inconsistency (NEW) | "Occupation du sol" is "14 catégories" per `diagnostic.py` but "18 catégories" per `home.html`/`ressources.html`; neither matches the 11 files on disk | Direct text comparison across 3 files | Visible, citable factual contradiction on a public site |
| R10 | **P2** | Scope gap (NEW) | The flagship `/carte/` interactive map covers only 5 of 9 diagnostic themes (missing géologie, pédologie, topographie, occupation du sol, équipements) | `carte.py`'s `LAYER_GROUPS` | Contradicts the homepage's explicit promise: *"Explorez toutes les données sur une seule carte"* |
| R11 | **P3** | Data consistency | Homepage Chart.js numbers for urbanisation/équipements/risques are hardcoded and don't correspond to any real computed source | `home.html` vs. `diagnostic.py`/`equipements.py` (§10.1) | Numbers a visitor can screenshot don't match numbers elsewhere on the same site |
| R12 | **P3** | Dependency hygiene | `aiofiles` declared but never used | `requirements.txt` | Minor — unnecessary install |
| R13 | **P3** | Observability | Vercel logs written to ephemeral `/tmp`, no retrieval mechanism | `app/main.py` | Effectively no production log visibility |
| R14 | **P3** | Dead code | 10 orphaned template files never rendered by any router | §8.1 | Confusing for a new maintainer; risk of "fixing" a page nothing links to |
| R15 | **P3** | UX inconsistency (NEW) | 4 independent Leaflet implementations differ in popup field-filtering and failure UX; only `carte.html` shows the user an error when a layer fails to load | §8.2 | Inconsistent polish; a fix to one map won't propagate to the others |
| R16 | **P3** | Deployment/perf (NEW) | Entire 106 MB static tree served through the single Python serverless function, not a CDN; `maxLambdaSize` already raised once to cope | `vercel.json`, commit `d6a038f` | Added latency per static request; recurring risk of hitting platform size limits again as content grows |
| R17 | **P3** | Dead asset (NEW) | `img/cartes/geologie-detail.jpg` exists but is referenced nowhere | Full-repo grep | Negligible — orphaned file only |

No P0 (blocking/critical) issues found.

---

## 17. Important Files

| Path | Purpose | Why it matters |
|---|---|---|
| `api/index.py` | Vercel serverless entry point | Single point of entry into the whole app |
| `app/main.py` | FastAPI instantiation, middleware, logging, static mount, router registration | A mistake here breaks the entire site |
| `app/routers/home.py` | `/`, `/projet`, `/ressources` (+POST) | Homepage + contact form (unfinished, R1) + inconsistent chart data (R11) |
| `app/routers/diagnostic.py` | `/diagnostic?section=...` — 9-section `SECTIONS` dict | Largest single source of business content; source of the 14-vs-18 contradiction (R9) |
| `app/routers/risques.py` + `app/templates/risques/*.html` | 3 risk-theme pages | 2 of 3 have a silent map-loading bug (R3) |
| `app/routers/equipements.py` | `/equipements/{commune}` | Has the per-commune data-integrity bug (R4) |
| `app/routers/communes.py` | `/communes`, `/communes/{slug}` | Drives commune detail pages; verified against real image counts |
| `app/routers/carte.py` | `/carte` — `LAYER_GROUPS` registry | Controls the flagship map; missing 5 of 9 themes (R10) |
| `app/templates/base.html` | Site-wide layout, nav, CDN loading, `FLog` telemetry | Touch point for any global UI/library change |
| `app/templates/diagnostic_unified.html` | Richest data-bound template | Most complex Jinja logic in the project |
| `app/static/data/**/*.geojson` (78 files, ~25,000 features) | All geographic content | Source of truth for every map; validated clean except R5 |
| `app/static/data/occupation-sol/culture-maraichere.geojson` | Largest single dataset (3,649 features) | Orphaned from every layer config (R8) |
| `app/static/img/svd/**` (196 images) + `app/static/docs/*.pdf` (3 files) | Per-commune galleries/reports | All verified present on disk |
| `vercel.json` | Deployment routing (all paths → one function) | Root cause of R16 |
| `requirements.txt` | Python dependencies | `aiofiles` unused (R12) |

---

## 18. Application Flow (key traces)

- **Startup:** `api/index.py` imports `app` → instantiation in `main.py` → `@app.on_event("startup")` logs a GeoJSON/image inventory banner (Vercel-safe).
- **Homepage:** `GET /` → `home.py` → `home.html` renders accurate `STATS` but fabricated Chart.js numbers (§10.1).
- **Diagnostic theme page:** `GET /diagnostic?section=risques` → validated against `SECTIONS` (invalid → silent fallback to `"geologie"`, no 404) → `diagnostic_unified.html` → backend never parses GeoJSON; browser fetches `/static/data/...` directly.
- **Risk page (broken for 2 of 3):** `GET /risques/vulnerabilite` → renders a real Leaflet map with basemap tiles, but the `risk_layers` block that would fetch `vulnerabilite.geojson` is never overridden → **map shows no data** (R3).
- **Equipment page (data-integrity bug):** `GET /equipements/gandon` → globs the *same shared* sector directories used by every other commune → returns numbers/lists identical to any other commune sharing that sector (R4) → client separately re-fetches the same files for map rendering (a pre-existing double-read noted before, still present).
- **Contact form:** `POST /ressources` → parses form fields → discards them → renders a canned success message.
- **Error handling:** invalid `section`/`commune`/`slug` never raises `HTTPException`; always falls back or redirects. No global exception handler; unhandled errors surface as FastAPI's default 500.

---

## 19. Change Safety Map

- **LOW RISK:** template styling/copy edits, adding new static assets, README.
- **MEDIUM RISK:** router dict content (`SECTIONS`, `COMMUNES`, `LAYER_GROUPS`) — affects rendered pages, low blast radius.
- **HIGH RISK:** `main.py` (global middleware/logging/router registration), `vercel.json` (all routing), `equipements.py` (any fix to R4 touches the one place with real, if buggy, logic).
- **VERY HIGH RISK:** none identified — no auth, no financial logic, no migrations, no shared external contracts exist in this project.

---

## 20. Unknown / Uncertain Areas

- Meaning of "SVD" is now confirmed (§1: Stratégie de Ville Durable); "SERRP" is confirmed too (Projet de Relèvement d'Urgence et de Résilience). No longer unknown.
- Whether the 14-vs-18 "catégories" contradiction (R9) reflects an intentional recount that only updated some pages, or a simple copy-paste error.
- Whether `culture-maraichere.geojson` (R8) was deliberately excluded from the map (e.g., performance concerns given its 3,649 features) or simply forgotten.
- Whether the `/risques/vulnerabilite` and `/risques/erosion` empty-map bug (R3) was ever noticed by a real user, or whether these pages have gone unused since launch.
- Whether the 10 orphaned templates (§8.1) are safe to delete or intentionally kept as a rollback reference.
- Origin/pipeline of the GeoJSON datasets, relevant to fixing the two mojibake files at the source.

---

## 21. Recommended Next Steps

**Immediate — real, user-facing bugs, worth fixing before anything else:**
- Fix `/risques/vulnerabilite` and `/risques/erosion` to actually load their GeoJSON (R3) — likely a one-block-per-file fix in each template, mirroring `inondation.html`.
- Decide the equipment-per-commune data problem (R4): either split the underlying GeoJSON by commune (if a commune property exists in the source data) or clearly relabel the numbers as agglomeration-wide until real per-commune data exists.
- Decide the contact form's fate (R1) — wire it up for real, or stop implying success.

**Content accuracy — cheap to fix, currently visibly wrong to any careful reader:**
- Reconcile "14" vs. "18" catégories d'occupation du sol (R9) — pick the correct number and apply it in all 3 places.
- Wire `culture-maraichere.geojson` into the occupation-sol layer list (R8) — currently the largest dataset in the project is invisible.
- Reconcile or remove the fabricated homepage Chart.js numbers (R11).

**Low-effort, opportunistic (do when touching adjacent code):**
- Fix both mojibake files at the source (R5).
- Remove the unused `aiofiles` dependency (R12).
- Add basic validation/size limits to `/api/log` (R2).
- Confirm and remove the 10 orphaned templates (R14) and the orphaned `geologie-detail.jpg` (R17).

**Structural, only if scope grows:**
- Extract `SECTIONS`/`COMMUNES`/`LAYER_GROUPS` into a dedicated config/data module if content-edit frequency increases.
- Add smoke tests per route (R7) — would have caught R3 and R4 immediately.
- Consider serving `app/static/` via Vercel's static hosting instead of the Python function (R16), if the project keeps growing in asset size.
- Either complete `/carte/`'s `LAYER_GROUPS` to cover all 9 themes, or adjust the homepage copy to stop promising "toutes les données" (R10).
- Unify the 4 Leaflet implementations into one shared client-side module for consistent popup filtering and failure UX (R15) — only worth it if a build step is ever introduced.

**Explicitly deferred:** no rewrite, no framework change, no database introduction is currently justified — the architecture is appropriate for its scope.

---

## Continuation Protocol

This file is the baseline. For every future client request:
1. Compare the request against this document.
2. Identify impacted routers/templates/data files.
3. Identify regression risk using the Problems/Risks table (§16).
4. Propose the safest implementation before touching code.
5. Implement only what's necessary.
6. Validate existing functionality remains intact.
7. Update this file if new information changes any assumption above.
