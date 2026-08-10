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
