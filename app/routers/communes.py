from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pathlib import Path

from app.routers.commune_diagnostic_data import (
    COMMUNE_DIAGNOSTIC,
    DIAGNOSTIC_SECTION_ORDER,
    DIAGNOSTIC_SECTION_META,
)
from app.routers.commune_svd_data import (
    COMMUNE_SVD,
    VISION_INTERCOMMUNALE,
    PRINCIPES_DIRECTEURS,
    PRINCIPES_DIRECTEURS_NOTE,
    AXES_STRATEGIQUES,
    PROGRAMME_CATEGORY_LABELS,
)
from app.routers.commune_pcu_data import (
    COMMUNE_PCU,
    PCU_SECTION_ORDER,
    PCU_SECTION_META,
)

SVD_PDF_BY_SLUG = {
    "saint-louis": "/static/docs/SVD_Saint-Louis.pdf",
    "gandon": "/static/docs/SVD_Gandon.pdf",
    "gandiole": "/static/docs/SVD_Gandiole.pdf",
}

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")

# ── Commune data: overview + key stats from SVD / RGPH 2023 ──

COMMUNES = {
    "saint-louis": {
        "name": "Saint-Louis",
        "slug": "saint-louis",
        "population": "237 000",
        "superficie": "4 579 ha",
        "densite": "51,8 hab/ha",
        "quartiers": 33,
        "description": (
            "Capitale de la région nord du Sénégal, Saint-Louis est une ville historique inscrite "
            "au patrimoine mondial de l'UNESCO. L'île de Saint-Louis constitue le centre historique "
            "et administratif, tandis que Sor et la Langue de Barbarie accueillent l'essentiel de la "
            "population. La commune concentre 72% de la population de l'agglomération et l'essentiel "
            "des équipements publics (santé, éducation, culture, administration)."
        ),
        "enjeux": [
            "Vulnérabilité aux inondations (topographie basse, île de Saint-Louis)",
            "Érosion côtière menaçant la Langue de Barbarie",
            "Densité élevée et pression foncière sur l'île",
            "Patrimoine historique UNESCO à préserver",
            "Concentration des équipements — besoin de rééquilibrage",
        ],
        "center": [16.02, -16.50],
        "zoom": 13,
        "images": "/static/img/svd/saint-louis/",
        "layers": [
            {"file": "base/limite-communale.geojson", "name": "Limite communale", "color": "#e74c3c", "type": "line"},
            {"file": "population/quartiers-polygones.geojson", "name": "Quartiers", "color": "#3498db"},
            {"file": "evolution/empreinte-2024.geojson", "name": "Empreinte urbaine 2024", "color": "#f39c12"},
        ],
        "stats": [
            {"value": "237 000", "label": "Habitants (RGPH 2023)", "icon": "users"},
            {"value": "33", "label": "Quartiers", "icon": "map"},
            {"value": "72%", "label": "Population agglomération", "icon": "chart"},
            {"value": "UNESCO", "label": "Patrimoine mondial", "icon": "globe"},
        ],
    },
    "gandon": {
        "name": "Gandon",
        "slug": "gandon",
        "population": "78 000",
        "superficie": "34 500 ha",
        "densite": "2,3 hab/ha",
        "quartiers": 0,
        "description": (
            "Commune périurbaine en forte croissance, Gandon se situe à l'est et au nord de Saint-Louis. "
            "Son territoire essentiellement rural connaît une urbanisation rapide le long de la RN2 et "
            "de la route de Gandiol. L'agriculture irriguée (riz, maraîchage) et l'élevage restent des "
            "activités économiques majeures. La commune accueille une part croissante de la population "
            "qui ne trouve plus de logements abordables à Saint-Louis."
        ),
        "enjeux": [
            "Urbanisation rapide et non planifiée",
            "Consommation de terres agricoles par l'étalement urbain",
            "Déficit d'équipements publics (santé, éducation)",
            "Gestion des eaux pluviales et risque d'inondation",
            "Connexion insuffisante avec Saint-Louis (transport)",
        ],
        "center": [16.10, -16.42],
        "zoom": 12,
        "images": "/static/img/svd/gandon/",
        "layers": [
            {"file": "base/limite-communale.geojson", "name": "Limite communale", "color": "#e74c3c", "type": "line"},
            {"file": "evolution/empreinte-2024.geojson", "name": "Empreinte urbaine 2024", "color": "#f39c12"},
        ],
        "stats": [
            {"value": "78 000", "label": "Habitants (RGPH 2023)", "icon": "users"},
            {"value": "34 500 ha", "label": "Superficie", "icon": "map"},
            {"value": "2-4%", "label": "Croissance annuelle", "icon": "arrow-up"},
            {"value": "Rural", "label": "Profil dominant", "icon": "tree"},
        ],
    },
    "gandiole": {
        "name": "Ndiébène Gandiole",
        "slug": "gandiole",
        "population": "35 000",
        "superficie": "19 200 ha",
        "densite": "1,8 hab/ha",
        "quartiers": 0,
        "description": (
            "Commune côtière au sud de l'agglomération, Ndiébène Gandiole est bordée par l'océan Atlantique "
            "à l'ouest et le fleuve Sénégal à l'est. Son économie repose sur la pêche artisanale, le "
            "maraîchage et le tourisme (Parc National de la Langue de Barbarie). La commune est "
            "particulièrement exposée aux risques côtiers : érosion, submersion marine et intrusion saline "
            "qui menacent les infrastructures et les activités économiques."
        ),
        "enjeux": [
            "Érosion côtière sévère (recul du trait de côte)",
            "Intrusion saline menaçant les terres agricoles",
            "Isolement et déficit de transport",
            "Vulnérabilité de la pêche artisanale",
            "Potentiel touristique sous-exploité (Parc National)",
        ],
        "center": [15.92, -16.52],
        "zoom": 12,
        "images": "/static/img/svd/gandiole/",
        "layers": [
            {"file": "base/limite-communale.geojson", "name": "Limite communale", "color": "#e74c3c", "type": "line"},
            {"file": "evolution/empreinte-2024.geojson", "name": "Empreinte urbaine 2024", "color": "#f39c12"},
        ],
        "stats": [
            {"value": "35 000", "label": "Habitants (RGPH 2023)", "icon": "users"},
            {"value": "19 200 ha", "label": "Superficie", "icon": "map"},
            {"value": "Côtière", "label": "Position géographique", "icon": "water"},
            {"value": "Pêche", "label": "Activité dominante", "icon": "anchor"},
        ],
    },
}

COMMUNE_ORDER = ["saint-louis", "gandon", "gandiole"]


@router.get("/", name="communes_index")
async def communes_index(request: Request):
    """Overview page: 3 commune cards → click to go to detail"""
    communes_list = [COMMUNES[k] for k in COMMUNE_ORDER]
    return templates.TemplateResponse(request, "communes.html", {
        "page_title": "Communes",
        "communes": communes_list,
    })


@router.get("/{slug}", name="commune_detail")
async def commune_detail(request: Request, slug: str):
    """Detail page for a single commune"""
    if slug not in COMMUNES:
        return RedirectResponse(url="/communes/", status_code=302)

    commune = COMMUNES[slug]

    # Determine prev/next
    idx = COMMUNE_ORDER.index(slug)
    prev_commune = COMMUNES[COMMUNE_ORDER[idx - 1]] if idx > 0 else None
    next_commune = COMMUNES[COMMUNE_ORDER[idx + 1]] if idx < len(COMMUNE_ORDER) - 1 else None

    # Collect SVD images for gallery
    img_dir = Path(__file__).resolve().parent.parent / "static" / "img" / "svd" / slug
    svd_images = []
    if img_dir.exists():
        for f in sorted(img_dir.iterdir()):
            if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif"):
                svd_images.append(f"/static/img/svd/{slug}/{f.name}")

    return templates.TemplateResponse(request, "commune_detail.html", {
        "page_title": commune["name"],
        "commune": commune,
        "prev_commune": prev_commune,
        "next_commune": next_commune,
        "svd_images": svd_images[:20],  # Limit to 20 best images
    })


def _enjeux_section_data(commune: dict) -> dict:
    """The 'Enjeux et problématiques' subsection reuses the existing, already-vetted
    COMMUNES[slug]['enjeux'] list directly (no new content, no GIS layer needed) --
    built here rather than stored in commune_diagnostic_data.py to avoid a circular
    import (that module is imported by this one, not the other way around)."""
    return {"coverage": "COMPLETE", "note": None, "layers": [], "enjeux": commune["enjeux"]}


def _commune_sections(slug: str, commune: dict) -> dict:
    sections = dict(COMMUNE_DIAGNOSTIC[slug])
    sections["enjeux"] = _enjeux_section_data(commune)
    return sections


@router.get("/{slug}/diagnostic", name="commune_diagnostic_index")
async def commune_diagnostic_index(request: Request, slug: str):
    """Diagnostic overview for one commune: 6 subsections with coverage badges."""
    if slug not in COMMUNES:
        return RedirectResponse(url="/communes/", status_code=302)
    commune = COMMUNES[slug]
    return templates.TemplateResponse(request, "communes/diagnostic_index.html", {
        "page_title": f"Diagnostic — {commune['name']}",
        "commune": commune,
        "sections": _commune_sections(slug, commune),
        "section_order": DIAGNOSTIC_SECTION_ORDER,
        "all_section_meta": DIAGNOSTIC_SECTION_META,
    })


@router.get("/{slug}/diagnostic/{section}", name="commune_diagnostic_section")
async def commune_diagnostic_section_page(request: Request, slug: str, section: str):
    """One Diagnostic subsection for one commune (e.g. milieu-physique, demographie...)."""
    if slug not in COMMUNES:
        return RedirectResponse(url="/communes/", status_code=302)
    if section not in DIAGNOSTIC_SECTION_ORDER:
        return RedirectResponse(url=f"/communes/{slug}/diagnostic", status_code=302)

    commune = COMMUNES[slug]
    data = _enjeux_section_data(commune) if section == "enjeux" else COMMUNE_DIAGNOSTIC[slug][section]
    return templates.TemplateResponse(request, "communes/diagnostic_section.html", {
        "page_title": f"{DIAGNOSTIC_SECTION_META[section]['label']} — {commune['name']}",
        "commune": commune,
        "data": data,
        "active_section": section,
        "section_order": DIAGNOSTIC_SECTION_ORDER,
        "section_meta": DIAGNOSTIC_SECTION_META[section],
        "all_section_meta": DIAGNOSTIC_SECTION_META,
    })


@router.get("/{slug}/svd", name="commune_svd")
async def commune_svd_page(request: Request, slug: str):
    """SVD branch — Wave 4B: real content extracted from the official SVD reports
    (see SVD_CONTENT_BASELINE.md for full source traceability)."""
    if slug not in COMMUNES:
        return RedirectResponse(url="/communes/", status_code=302)
    commune = COMMUNES[slug]
    return templates.TemplateResponse(request, "communes/svd.html", {
        "page_title": f"SVD — {commune['name']}",
        "commune": commune,
        "svd": COMMUNE_SVD[slug],
        "principes": PRINCIPES_DIRECTEURS,
        "principes_note": PRINCIPES_DIRECTEURS_NOTE,
        "axes": AXES_STRATEGIQUES,
        "category_labels": PROGRAMME_CATEGORY_LABELS,
        "svd_pdf_url": SVD_PDF_BY_SLUG[slug],
    })


@router.get("/{slug}/pcu", name="commune_pcu")
async def commune_pcu_page(request: Request, slug: str):
    """PCU/PCUI branch — Wave 4C: only genuinely available material is shown
    (see PCU_CONTENT_BASELINE.md for the full audit); every other of the 6
    requested sections is honestly marked MISSING, never fabricated."""
    if slug not in COMMUNES:
        return RedirectResponse(url="/communes/", status_code=302)
    commune = COMMUNES[slug]
    return templates.TemplateResponse(request, "communes/pcu.html", {
        "page_title": f"PCU / PCUI — {commune['name']}",
        "commune": commune,
        "pcu": COMMUNE_PCU[slug],
        "section_order": PCU_SECTION_ORDER,
        "section_meta": PCU_SECTION_META,
    })
