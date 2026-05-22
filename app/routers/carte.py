from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")

DATA_DIR = Path(__file__).resolve().parent.parent / "static" / "data"

LAYER_GROUPS = {
    "base": {
        "label": "Fond de plan",
        "layers": {
            "limite-communale": {"label": "Limite communale", "color": "#2c3e50", "type": "polygon"},
            "eaux-permanentes": {"label": "Eaux permanentes", "color": "#3498db", "type": "polygon"},
        },
    },
    "risques": {
        "label": "Risques naturels",
        "layers": {
            "risque-inondation": {"label": "Risque inondation", "color": "#e74c3c", "type": "polygon"},
            "vulnerabilite": {"label": "Vulnérabilité", "color": "#e67e22", "type": "polygon"},
            "erosion": {"label": "Érosion", "color": "#ff69b4", "type": "polygon"},
        },
    },
    "evolution": {
        "label": "Évolution urbaine",
        "layers": {
            "empreinte-2017": {"label": "Empreinte 2017", "color": "#8B4513", "type": "polygon"},
            "empreinte-2020": {"label": "Empreinte 2020", "color": "#e67e22", "type": "polygon"},
            "empreinte-2024": {"label": "Empreinte 2024", "color": "#e91e63", "type": "polygon"},
        },
    },
    "transport": {
        "label": "Transport",
        "layers": {
            "route-acces": {"label": "Routes d'accès", "color": "#e74c3c", "type": "line"},
            "route-locale": {"label": "Route locale", "color": "#f39c12", "type": "line"},
            "route-tertiaire": {"label": "Route tertiaire", "color": "#95a5a6", "type": "line"},
            "route-residentielle": {"label": "Route résidentielle", "color": "#bdc3c7", "type": "line"},
            "route-construction": {"label": "Route en construction", "color": "#e67e22", "type": "line"},
            "piste": {"label": "Piste", "color": "#d4a574", "type": "line"},
            "chemin-fer": {"label": "Chemin de fer", "color": "#2c3e50", "type": "line"},
        },
    },
    "population": {
        "label": "Population",
        "layers": {
            "quartiers-polygones": {"label": "Quartiers", "color": "#9b59b6", "type": "polygon"},
            "population-quartiers": {"label": "Population (points)", "color": "#8e44ad", "type": "point"},
        },
    },
}


@router.get("/", name="carte_interactive")
async def carte_page(request: Request):
    # Scan available GeoJSON files
    available_layers = {}
    for group_id, group in LAYER_GROUPS.items():
        available = {}
        for layer_id, layer_info in group["layers"].items():
            # Search in subfolders
            geojson_path = None
            for subdir in DATA_DIR.rglob(f"{layer_id}.geojson"):
                geojson_path = f"/static/data/{subdir.relative_to(DATA_DIR)}"
                break
            if geojson_path:
                available[layer_id] = {**layer_info, "url": geojson_path}
        if available:
            available_layers[group_id] = {
                "label": group["label"],
                "layers": available,
            }

    return templates.TemplateResponse(request, "carte.html", {
        "page_title": "Carte interactive",
        "layer_groups": available_layers,
        "all_groups": LAYER_GROUPS,
    })
