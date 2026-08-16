"""
Phase 5 — minimal smoke-test suite.

The project had zero automated tests before this. These tests are deliberately
simple: for every route that matters, assert the expected HTTP status, that no
unhandled server exception occurred (TestClient raises those by default), and
that a few identity-confirming strings are present (e.g. the right commune name
on the right page) to catch cross-commune data leakage.

Run with:  pytest tests/ -v
Requires (test-only, NOT part of the deployed app): pytest, httpx — see
requirements-dev.txt. The application itself has no test-time dependency.
"""
import json
import os

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

COMMUNES = ["saint-louis", "gandon", "gandiole"]
COMMUNE_NAMES = {
    "saint-louis": "Saint-Louis",
    "gandon": "Gandon",
    "gandiole": "Ndiébène Gandiole",
}
DIAGNOSTIC_SECTIONS = [
    "milieu-physique", "demographie", "urbain-mobilite",
    "habitat-foncier", "economie-energie", "enjeux",
]
GLOBAL_DIAGNOSTIC_SECTIONS = [
    "geologie", "pedologie", "topographie", "occupation", "urbanisation",
    "risques", "transport", "peuplement", "population", "equipements",
    "economie_energie", "gouvernance",
]
EQUIPEMENT_COMMUNES = ["saint-louis", "gandon", "gandiol"]  # equipements.py uses "gandiol", not "gandiole"


# ---- Core global pages ----

@pytest.mark.parametrize("path", ["/", "/projet", "/ressources", "/carte/", "/communes/"])
def test_global_pages_ok(path):
    r = client.get(path)
    assert r.status_code == 200


def test_diagnostic_default_redirects_and_resolves():
    r = client.get("/diagnostic", follow_redirects=True)
    assert r.status_code == 200


@pytest.mark.parametrize("section", GLOBAL_DIAGNOSTIC_SECTIONS)
def test_global_diagnostic_sections_ok(section):
    r = client.get(f"/diagnostic?section={section}", follow_redirects=True)
    assert r.status_code == 200


def test_diagnostic_invalid_section_falls_back_not_500():
    r = client.get("/diagnostic?section=doesnotexist", follow_redirects=True)
    assert r.status_code == 200


# ---- Legacy redirects (must keep working, per PROJECT_ANALYSIS.md) ----

@pytest.mark.parametrize("path", [
    "/a-propos", "/telechargements", "/contact",
    "/diagnostic/situation", "/diagnostic/geologie", "/diagnostic/pedologie",
    "/diagnostic/topographie", "/diagnostic/occupation-du-sol", "/diagnostic/evolution-urbaine",
])
def test_legacy_redirects_resolve(path):
    r = client.get(path, follow_redirects=True)
    assert r.status_code == 200


# ---- Risk pages ----

@pytest.mark.parametrize("path", ["/risques/inondation", "/risques/vulnerabilite", "/risques/erosion"])
def test_risk_pages_ok(path):
    r = client.get(path)
    assert r.status_code == 200


@pytest.mark.parametrize("path,geojson", [
    ("/risques/vulnerabilite", "vulnerabilite.geojson"),
    ("/risques/erosion", "erosion.geojson"),
])
def test_risk_pages_load_their_data_layer(path, geojson):
    """Regression test for a Phase 5 fix: these 2 pages previously rendered a
    basemap with no data layer at all (PROJECT_ANALYSIS.md R3)."""
    r = client.get(path)
    assert geojson in r.text


# ---- Equipment pages ----

@pytest.mark.parametrize("slug", EQUIPEMENT_COMMUNES)
def test_equipement_pages_ok(slug):
    r = client.get(f"/equipements/{slug}")
    assert r.status_code == 200


# ---- Commune landing pages: correct identity, no cross-commune leakage ----

@pytest.mark.parametrize("slug", COMMUNES)
def test_commune_landing_page_identity(slug):
    r = client.get(f"/communes/{slug}")
    assert r.status_code == 200
    assert COMMUNE_NAMES[slug] in r.text
    # the 3 nav cards to Diagnostic/SVD/PCU must be present
    assert f"/communes/{slug}/diagnostic" in r.text
    assert f"/communes/{slug}/svd" in r.text
    assert f"/communes/{slug}/pcu" in r.text


def test_commune_invalid_slug_redirects():
    r = client.get("/communes/nonexistent", follow_redirects=False)
    assert r.status_code == 302


# ---- Commune Diagnostic: all 6 sections x 3 communes ----

@pytest.mark.parametrize("slug", COMMUNES)
def test_commune_diagnostic_index(slug):
    r = client.get(f"/communes/{slug}/diagnostic")
    assert r.status_code == 200
    assert COMMUNE_NAMES[slug] in r.text


@pytest.mark.parametrize("slug", COMMUNES)
@pytest.mark.parametrize("section", DIAGNOSTIC_SECTIONS)
def test_commune_diagnostic_section(slug, section):
    r = client.get(f"/communes/{slug}/diagnostic/{section}")
    assert r.status_code == 200
    assert COMMUNE_NAMES[slug] in r.text


def test_commune_diagnostic_invalid_section_redirects():
    r = client.get("/communes/gandon/diagnostic/doesnotexist", follow_redirects=False)
    assert r.status_code == 302


# ---- Commune SVD: identity + shared-vs-specific labeling present ----

@pytest.mark.parametrize("slug", COMMUNES)
def test_commune_svd_page(slug):
    r = client.get(f"/communes/{slug}/svd")
    assert r.status_code == 200
    assert COMMUNE_NAMES[slug] in r.text
    assert "Vision intercommunale" in r.text  # shared content must always be labeled as such
    assert "Spécifique à" in r.text


def test_svd_vision_not_cross_commune():
    """Each commune's own vision quote must appear on its own page and not be
    silently swapped for another commune's (guards against a copy/paste bug)."""
    gandon = client.get("/communes/gandon/svd").text
    gandiole = client.get("/communes/gandiole/svd").text
    assert "Faire de Gandon un territoire viable" in gandon
    assert "Faire de Gandon un territoire viable" not in gandiole
    assert "Produire un territoire attractif et émergent" in gandiole
    assert "Produire un territoire attractif et émergent" not in gandon


# ---- Commune PCU: honest statuses, no fabricated content ----

@pytest.mark.parametrize("slug", COMMUNES)
def test_commune_pcu_page(slug):
    r = client.get(f"/communes/{slug}/pcu")
    assert r.status_code == 200
    assert COMMUNE_NAMES[slug] in r.text


def test_pcu_never_claims_fully_available():
    """No commune has an approved rapport de présentation, règlement, EES, or
    atlas yet (see PCU_CONTENT_BASELINE.md) — the page must never show the
    'Disponible' badge, only 'Partiel' or 'En attente de données client'."""
    for slug in COMMUNES:
        r = client.get(f"/communes/{slug}/pcu")
        assert "Disponible</span>" not in r.text


def test_gandon_zonage_labeled_as_orientation_not_official():
    r = client.get("/communes/gandon/pcu")
    assert "non approuvée" in r.text or "orientation" in r.text.lower()


# ---- GIS data encoding regression (Phase 5 found and fixed a real double-encoding bug) ----

def test_occupation_sol_2020_categories_not_double_encoded():
    r = client.get("/static/data/occupation-sol-2020/occupation-du-sol-2020.geojson")
    assert r.status_code == 200
    assert "Culture maraichère" in r.text  # correct single-encoded "è"
    assert "Ã" not in r.text  # double-encoding marker (mojibake "Ã")


# ---- Contact form ----

def test_contact_form_get_ok():
    r = client.get("/ressources")
    assert r.status_code == 200


def test_contact_form_post_does_not_500():
    r = client.post("/ressources", data={"name": "Test", "email": "test@example.com", "message": "Hello"})
    assert r.status_code == 200


# ---- /api/log ----

def test_api_log_accepts_valid_payload():
    r = client.post("/api/log", json={"level": "info", "message": "test", "page": "/"})
    assert r.status_code == 200


def test_api_log_rejects_malformed_json_gracefully():
    r = client.post("/api/log", content=b"not json", headers={"Content-Type": "application/json"})
    assert r.status_code in (400, 422)


# ---- Interactive map (/carte/) — client remarks: red évolution palette, new rubriques, filters ----

def _extract_available_layers_json(html):
    """The page also embeds base.html's unrelated Tailwind color scale, which happens to
    reuse some of the same old blue hex codes — scope palette checks to just the layer
    config payload so that shared site theming doesn't produce a false positive/negative."""
    start = html.index("const availableLayers = ") + len("const availableLayers = ")
    end = html.index(";\n", start)
    return html[start:end]


def test_carte_evolution_urbaine_uses_red_family_not_blue():
    """Client remark: replace the blue gradient with a red one for évolution urbaine."""
    r = client.get("/carte/")
    assert r.status_code == 200
    layers_json = _extract_available_layers_json(r.text)
    assert "#7f1d1d" in layers_json and "#dc2626" in layers_json and "#fca5a5" in layers_json
    assert "#93c5fd" not in layers_json and "#2563eb" not in layers_json and "#1e3a5f" not in layers_json


def test_carte_evolution_urbaine_color_intensity_inverted_stacking_unchanged():
    """Client remark 3: color INTENSITY inverted (2017 light -> 2024 dark) while pane
    zIndex stacking (2017 foreground -> 2024 background) must stay exactly as before —
    the two are easy to confuse but must not move together."""
    r = client.get("/carte/")
    evolution = json.loads(_extract_available_layers_json(r.text))["evolution"]["layers"]
    assert evolution["empreinte-2017"]["color"] == "#fca5a5"  # light
    assert evolution["empreinte-2020"]["color"] == "#dc2626"  # medium
    assert evolution["empreinte-2024"]["color"] == "#7f1d1d"  # dark
    assert evolution["empreinte-2017"]["paneZIndex"] > evolution["empreinte-2020"]["paneZIndex"] > evolution["empreinte-2024"]["paneZIndex"]


def test_carte_evolution_urbaine_has_deterministic_panes():
    """2017 must always render above 2020, above 2024 — not left to fetch/toggle order."""
    r = client.get("/carte/")
    assert "empreinte2017Pane" in r.text
    assert "empreinte2020Pane" in r.text
    assert "empreinte2024Pane" in r.text
    assert "paneZIndex" in r.text


def test_carte_has_new_rubriques():
    r = client.get("/carte/")
    assert "Occupation du sol" in r.text
    assert "Relief" in r.text
    assert "occupation-du-sol-2020" in r.text
    assert "hillshade-mnt.png" in r.text
    assert "courbes-niveau-5m" in r.text


def test_carte_flood_filter_uses_real_field_name_and_client_values():
    """Real source field is 'Categorie' (no accent); client-facing label stays 'Catégorie'."""
    r = client.get("/carte/")
    assert "applyFilter('risque-inondation'" in r.text
    assert '"field": "Categorie"' in r.text
    for value in ["Risque très fort", "Risque fort", "Risque moyen", "Risque faible"]:
        assert value in r.text


def test_carte_vulnerability_filter_uses_real_field_name_and_client_values():
    """Real source field is 'indice' (lowercase); client-facing label stays 'Indice'."""
    r = client.get("/carte/")
    assert "applyFilter('vulnerabilite'" in r.text
    assert '"field": "indice"' in r.text
    for value in ["1", "2", "3", "4"]:
        assert f">{value}<" in r.text


def test_carte_equipements_group_present_for_all_sectors():
    r = client.get("/carte/")
    for sector in ["sante", "education", "culture", "economie", "sport"]:
        assert f"equip-{sector}" in r.text


def test_carte_equipements_sector_endpoint_merges_real_files():
    r = client.get("/carte/data/equipements/sante")
    assert r.status_code == 200
    data = r.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) >= 1


def test_carte_equipements_sector_endpoint_unknown_sector_404():
    r = client.get("/carte/data/equipements/doesnotexist")
    assert r.status_code == 404


def _extract_cfgs_json(html):
    """Same rationale as _extract_available_layers_json: base.html's Tailwind color
    scale shares hex codes with the old urbanisation palette, so scope to the payload."""
    start = html.index("const cfgs = ") + len("const cfgs = ")
    end = html.index(";\n", start)
    return html[start:end]


def test_diagnostic_urbanisation_uses_red_family_not_blue():
    """Same red family must be applied on the global Diagnostic urbanisation theme too."""
    r = client.get("/diagnostic?section=urbanisation")
    assert r.status_code == 200
    cfgs_json = _extract_cfgs_json(r.text)
    assert "#7f1d1d" in cfgs_json and "#dc2626" in cfgs_json and "#fca5a5" in cfgs_json
    assert "#93c5fd" not in cfgs_json and "#2563eb" not in cfgs_json


def _find_layer(cfgs_list, file_substring):
    for cfg in cfgs_list:
        if file_substring in cfg.get("file", ""):
            return cfg
    raise AssertionError(f"no layer config with file containing {file_substring!r}")


def test_diagnostic_urbanisation_color_intensity_inverted_stacking_unchanged():
    """Client remark 3: 2017 light -> 2024 dark; stacking (2017 foreground -> 2024
    background) must be unaffected by the color change."""
    r = client.get("/diagnostic?section=urbanisation")
    cfgs = json.loads(_extract_cfgs_json(r.text))
    e2017 = _find_layer(cfgs, "empreinte-2017")
    e2020 = _find_layer(cfgs, "empreinte-2020")
    e2024 = _find_layer(cfgs, "empreinte-2024")
    assert e2017["color"] == "#fca5a5"
    assert e2020["color"] == "#dc2626"
    assert e2024["color"] == "#7f1d1d"
    assert e2017["paneZIndex"] > e2020["paneZIndex"] > e2024["paneZIndex"]


def test_diagnostic_lotissements_planifies_is_black():
    """Client remark 3: 'Lotissements planifiés' must render in black, and above all
    3 empreinte panes so it's never hidden beneath whichever footprint is toggled on."""
    r = client.get("/diagnostic?section=urbanisation")
    cfgs = json.loads(_extract_cfgs_json(r.text))
    lotissements = _find_layer(cfgs, "lotissements")
    assert lotissements["color"] == "#000000"
    e2017 = _find_layer(cfgs, "empreinte-2017")
    assert lotissements["paneZIndex"] > e2017["paneZIndex"]


@pytest.mark.parametrize("slug", COMMUNES)
def test_commune_urbanisation_uses_red_family_not_blue(slug):
    """Same red family must be applied on every commune's urbain-mobilite subsection too."""
    r = client.get(f"/communes/{slug}/diagnostic/urbain-mobilite")
    assert r.status_code == 200
    cfgs_json = _extract_cfgs_json(r.text)
    assert "#7f1d1d" in cfgs_json and "#dc2626" in cfgs_json and "#fca5a5" in cfgs_json
    assert "#93c5fd" not in cfgs_json and "#2563eb" not in cfgs_json


@pytest.mark.parametrize("slug", COMMUNES)
def test_commune_urbanisation_color_intensity_inverted_stacking_unchanged(slug):
    r = client.get(f"/communes/{slug}/diagnostic/urbain-mobilite")
    cfgs = json.loads(_extract_cfgs_json(r.text))
    e2017 = _find_layer(cfgs, "empreinte-2017")
    e2020 = _find_layer(cfgs, "empreinte-2020")
    e2024 = _find_layer(cfgs, "empreinte-2024")
    assert e2017["color"] == "#fca5a5"
    assert e2020["color"] == "#dc2626"
    assert e2024["color"] == "#7f1d1d"
    assert e2017["paneZIndex"] > e2020["paneZIndex"] > e2024["paneZIndex"]


@pytest.mark.parametrize("slug", ["saint-louis", "gandon"])  # gandiole has no lotissements-planifies dataset
def test_commune_lotissements_planifies_is_black(slug):
    r = client.get(f"/communes/{slug}/diagnostic/urbain-mobilite")
    cfgs = json.loads(_extract_cfgs_json(r.text))
    lotissements = _find_layer(cfgs, "lotissements")
    assert lotissements["color"] == "#000000"


# ---- Topographie remark: pane crash fix, label correction, correct assets ----

def test_topographie_page_ok():
    r = client.get("/diagnostic?section=topographie")
    assert r.status_code == 200


def test_topographie_no_nouvelle_donnee_wording():
    """Client asked why the 5m contour layer was labelled '(nouvelle donnée)' —
    the site should describe what the data is, not when it was added."""
    r = client.get("/diagnostic?section=topographie")
    assert "Courbes de niveau 5 m</span>" in r.text or '"Courbes de niveau 5 m"' in r.text
    cfgs_json = _extract_cfgs_json(r.text)
    assert "nouvelle donn" not in cfgs_json.lower()


def test_topographie_references_valid_assets():
    """Regression guard for the pane:undefined crash — all 3 layers must still be
    present in the rendered config and their backing files must actually exist."""
    r = client.get("/diagnostic?section=topographie")
    cfgs_json = _extract_cfgs_json(r.text)
    assert "courbes-niveau.geojson" in cfgs_json
    assert "courbes-niveau-5m.geojson" in cfgs_json
    assert "hillshade-mnt.png" in cfgs_json
    for path in [
        "app/static/data/diagnostic/topographie/courbes-niveau.geojson",
        "app/static/data/diagnostic/topographie/courbes-niveau-5m.geojson",
        "app/static/img/topographie/hillshade-mnt.png",
    ]:
        assert os.path.isfile(path), path


def test_topographie_layers_do_not_pass_undefined_pane():
    """Regression guard for the exact root cause: passing {pane: undefined} into a
    Leaflet constructor crashes L.ImageOverlay.onAdd() and silently aborts every
    layer queued after it. None of the 3 affected templates may reintroduce this."""
    for path in [
        "app/templates/diagnostic_unified.html",
        "app/templates/communes/diagnostic_section.html",
        "app/templates/carte.html",
    ]:
        with open(path, encoding="utf-8") as f:
            content = f.read()
        assert "|| undefined" not in content, f"{path} still has the pane:undefined regression pattern"


def test_carte_relief_layers_present_and_reachable():
    """/carte/'s Relief rubrique must use the same hillshade + 5m contour assets,
    with no display regression there either."""
    r = client.get("/carte/")
    assert r.status_code == 200
    assert "hillshade-mnt" in r.text
    assert "courbes-niveau-5m" in r.text
    r2 = client.get("/carte/data/equipements/sante")
    assert r2.status_code == 200  # unrelated route sanity check: router still loads cleanly


# ---- Occupation du sol remark: 17 individually-selectable 2020 classes, no combined-legend confusion ----

OCCSOL_2020_CATEGORIES = [
    "Mare", "Lac", "Cours d'eau", "Plaine inondable", "Vasière", "Mangrove",
    "Prairie aquatique", "Tanne", "Steppe", "Savane", "Sol nu", "Dune",
    "Culture pluviale", "Culture irriguée", "Culture maraichère",
    "Plantation forestière", "Carrière Mine Infrastructure",
]


def test_occupation_no_nouvelle_donnee_wording():
    r = client.get("/diagnostic?section=occupation")
    assert r.status_code == 200
    assert "nouvelle donn" not in r.text.lower()


def _tojson_escaped(s):
    """Jinja's |tojson filter HTML-escapes non-ASCII and ' for safe <script> embedding
    (e.g. "Cours d'eau" -> "Cours d\\u0027eau", "Vasière" -> "Vasi\\u00e8re") — match that
    instead of the raw string."""
    inner = json.dumps(s)[1:-1]  # ensure_ascii=True handles accented chars; strip quotes
    return inner.replace("'", "\\u0027")


def test_occupation_2020_classes_are_individually_selectable():
    """Client remark: replace the single combined '2020 (nouvelle donnée)' checkbox
    with one real, independently-toggleable checkbox per class."""
    r = client.get("/diagnostic?section=occupation")
    cfgs_json = _extract_cfgs_json(r.text)
    for category in OCCSOL_2020_CATEGORIES:
        assert f'"categoryFilter": "{_tojson_escaped(category)}"' in cfgs_json, category
    # All share one source file — not 17 duplicate GeoJSON files
    assert cfgs_json.count("occupation-du-sol-2020.geojson") == len(OCCSOL_2020_CATEGORIES)


def test_occupation_2020_classes_default_unchecked():
    """The 2020 group must start OFF (client should never open the map and see
    17 overlapping layers with no explanation)."""
    r = client.get("/diagnostic?section=occupation")
    assert '"defaultChecked": false' in r.text


def test_occupation_existing_layers_unaffected():
    """The 10 pre-existing standalone land-cover layers must still be present and
    still default to visible, matching behavior before this remark."""
    r = client.get("/diagnostic?section=occupation")
    for name in ["Empreinte urbaine", "Culture pluviale", "Mangrove", "Savane arbustive",
                 "Savane boisée", "Steppe", "Sol nu dunaire", "Sol nu inondable"]:
        assert name in r.text
    assert "Canal d&#39;irrigation" in r.text  # Jinja HTML-escapes the apostrophe in plain text


def test_carte_occupation_group_is_17_individual_classes():
    """/carte/'s Occupation du sol rubrique must expose the same 17 selectable
    classes, not the old single combined layer, and stay consistent with /diagnostic/."""
    r = client.get("/carte/")
    assert r.status_code == 200
    for category in OCCSOL_2020_CATEGORIES:
        assert f'"categoryFilter": "{_tojson_escaped(category)}"' in r.text, category
    # Each layer's resolved dict carries both "file" (relative) and "url" (resolved) keys,
    # both containing the filename — so 17 layers legitimately produce 34 substring hits.
    # What actually matters (one real source file, not 17 duplicates) is confirmed by the
    # 17 distinct categoryFilter values above plus a single file on disk (see
    # test_topographie_references_valid_assets-style checks elsewhere for that pattern).
    assert r.text.count("occupation-du-sol-2020.geojson") == 2 * len(OCCSOL_2020_CATEGORIES)
    assert os.path.isfile("app/static/data/occupation-sol-2020/occupation-du-sol-2020.geojson")


def test_carte_still_has_red_evolution_palette_and_filters():
    """Regression guard: adding per-class Occupation du sol selection must not break
    the previously-implemented red palette, Relief, Équipements, or risk filters."""
    r = client.get("/carte/")
    assert "#7f1d1d" in r.text and "#dc2626" in r.text and "#fca5a5" in r.text
    assert "hillshade-mnt" in r.text
    assert '"field": "Categorie"' in r.text
    assert '"field": "indice"' in r.text


@pytest.mark.parametrize("slug", COMMUNES)
def test_commune_occupation_sol_2020_no_nouvelle_donnee(slug):
    """Commune pages already use clean labels — confirm no regression introduced
    by this remark's shared OCCSOL_2020_CATEGORY_COLORS constant."""
    r = client.get(f"/communes/{slug}/diagnostic/milieu-physique")
    assert r.status_code == 200
    assert "nouvelle donn" not in r.text.lower()


# ---- Risques naturels remark: the 2 client-provided cartographic maps ----

def test_risques_page_has_both_client_maps():
    """Client remark: the two official cartographic maps (inondation, vulnérabilité)
    must be shown, with clean public labels."""
    r = client.get("/diagnostic?section=risques")
    assert r.status_code == 200
    assert "Carte du risque d&#39;inondation" in r.text or "Carte du risque d'inondation" in r.text
    assert "Carte de vulnérabilité" in r.text
    assert "/static/img/cartes/risque-inondation.jpg" in r.text
    assert "/static/img/cartes/vulnerabilite.jpg" in r.text
    assert "nouvelle donn" not in r.text.lower()


def test_risques_map_assets_exist_and_are_reachable():
    r = client.get("/diagnostic?section=risques")
    assert r.status_code == 200
    for path in [
        "app/static/img/cartes/risque-inondation.jpg",
        "app/static/img/cartes/vulnerabilite.jpg",
        "app/static/docs/Carte_Alea_Inondation_PUD.pdf",
        "app/static/docs/Carte_Vulnerabilite_PUD.pdf",
    ]:
        assert os.path.isfile(path), path
    for url in [
        "/static/img/cartes/risque-inondation.jpg",
        "/static/img/cartes/vulnerabilite.jpg",
        "/static/docs/Carte_Alea_Inondation_PUD.pdf",
        "/static/docs/Carte_Vulnerabilite_PUD.pdf",
    ]:
        assert client.get(url).status_code == 200, url


def test_risques_no_windows_path_exposed():
    r = client.get("/diagnostic?section=risques")
    lowered = r.text.lower()
    assert "c:\\users" not in lowered
    assert "c:/users" not in lowered
    assert "file:///" not in lowered


def test_risques_interactive_links_point_to_existing_routes():
    """The 'Explorer la carte interactive' links must point at real, still-working
    routes — not dead links, and not duplicating a new route."""
    r = client.get("/diagnostic?section=risques")
    assert "/risques/inondation" in r.text
    assert "/risques/vulnerabilite" in r.text
    for path in ["/risques/inondation", "/risques/vulnerabilite", "/risques/erosion"]:
        assert client.get(path).status_code == 200


@pytest.mark.parametrize("path,geojson", [
    ("/risques/inondation", "risque-inondation.geojson"),
    ("/risques/vulnerabilite", "vulnerabilite.geojson"),
    ("/risques/erosion", "erosion.geojson"),
])
def test_risques_interactive_gis_still_loads_data(path, geojson):
    """Regression guard: this remark adds static maps ALONGSIDE the interactive GIS —
    it must not disturb the Phase 5 fix that made these 3 pages load real data."""
    r = client.get(path)
    assert r.status_code == 200
    assert geojson in r.text


def test_risques_stats_unchanged():
    """147/1058/3 were independently re-verified against the live GIS sources during
    this remark and found still accurate — they must not have been altered."""
    r = client.get("/diagnostic?section=risques")
    assert "147 zones de risque d&#39;inondation" in r.text or "147 zones de risque d'inondation" in r.text
    assert "1 058 zones de vulnérabilité" in r.text
    assert "3 zones d&#39;érosion côtière" in r.text or "3 zones d'érosion côtière" in r.text


# ---- Peuplement remark: new Saint-Louis quartiers (points) + bâtiments replacing localités ----

def test_peuplement_old_localites_layer_removed():
    r = client.get("/diagnostic?section=peuplement")
    assert r.status_code == 200
    assert "localites.geojson" not in r.text
    assert "nouvelle donn" not in r.text.lower()
    assert "sans nom" not in r.text.lower()


def test_peuplement_saint_louis_uses_new_point_source():
    """Client remark: Saint-Louis quartiers must come from the new client dataset and
    be displayed as points ('implantation ponctuelle'), not the old polygon layer."""
    r = client.get("/diagnostic?section=peuplement")
    cfgs = json.loads(_extract_cfgs_json(r.text))
    sl = _find_layer(cfgs, "quartiers-saint-louis.geojson")
    assert sl.get("type") == "point"
    assert "quartiers-polygones" not in json.dumps(cfgs)


def test_peuplement_batiments_present_and_lazy():
    r = client.get("/diagnostic?section=peuplement")
    cfgs = json.loads(_extract_cfgs_json(r.text))
    batiments = _find_layer(cfgs, "batiments.geojson")
    assert batiments["defaultChecked"] is False  # must not load 6.9 MB by default
    assert "Bâtiments" in r.text or "B\\u00e2timents" in r.text


def test_peuplement_gandon_gandiol_preserved():
    r = client.get("/diagnostic?section=peuplement")
    cfgs = json.loads(_extract_cfgs_json(r.text))
    gandon = _find_layer(cfgs, "quartiers-gandon.geojson")
    gandiol = _find_layer(cfgs, "quartiers-gandiol.geojson")
    assert gandon["type"] == "point"
    assert gandiol["type"] == "point"


def test_peuplement_new_assets_exist_and_are_valid():
    r = client.get("/diagnostic?section=peuplement")
    assert r.status_code == 200
    for path in [
        "app/static/data/peuplement/quartiers-saint-louis.geojson",
        "app/static/data/peuplement/batiments.geojson",
    ]:
        assert os.path.isfile(path), path
    with open("app/static/data/peuplement/quartiers-saint-louis.geojson", encoding="utf-8") as f:
        sl_data = json.load(f)
    assert len(sl_data["features"]) == 33
    assert all(f_["geometry"]["type"] == "Point" for f_ in sl_data["features"])
    with open("app/static/data/peuplement/batiments.geojson", encoding="utf-8") as f:
        bati_data = json.load(f)
    assert len(bati_data["features"]) == 15481


def test_commune_saint_louis_demographie_uses_new_point_source():
    r = client.get("/communes/saint-louis/diagnostic/demographie")
    assert r.status_code == 200
    cfgs = json.loads(_extract_cfgs_json(r.text))
    sl = _find_layer(cfgs, "quartiers-saint-louis.geojson")
    assert sl["type"] == "point"


# ---- Navbar brand remark: "SIG Saint-Louis" -> "SIG WEB Interactif" ----

@pytest.mark.parametrize("path", ["/", "/diagnostic", "/carte/", "/communes/"])
def test_navbar_brand_is_new_client_wording(path):
    r = client.get(path, follow_redirects=True)
    assert r.status_code == 200
    assert "SIG WEB Interactif" in r.text
    assert "SIG Saint-Louis" not in r.text


def test_homepage_h1_unaffected_by_navbar_brand_change():
    """Client remark 1's long H1 is a different piece of text from the small navbar
    brand — this remark must not touch it."""
    r = client.get("/")
    assert "ÉLABORATION DE TROIS PLANS INTERCOMMUNAUX" in r.text
