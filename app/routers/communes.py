from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pathlib import Path

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
