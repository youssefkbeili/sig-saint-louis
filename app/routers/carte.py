from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pathlib import Path
import json

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")

DATA_DIR = Path(__file__).resolve().parent.parent / "static" / "data"
IMG_DIR = Path(__file__).resolve().parent.parent / "static" / "img"

# Reused verbatim from app/routers/diagnostic.py's "occupation" section (Wave 2/Phase 5) —
# do not fork this dict, the values were byte-verified against the source shapefile there.
OCCSOL_2020_CATEGORY_COLORS = {
    "Mare": "#3498db",
    "Lac": "#2980b9",
    "Cours d'eau": "#1abc9c",
    "Plaine inondable": "#85c1e9",
    "Vasière": "#a9946c",
    "Mangrove": "#16a085",
    "Prairie aquatique": "#48c9b0",
    "Tanne": "#f7dc6f",
    "Steppe": "#d4a574",
    "Savane": "#8e44ad",
    "Sol nu": "#f0e68c",
    "Dune": "#e67e22",
    "Culture pluviale": "#f1c40f",
    "Culture irriguée": "#27ae60",
    "Culture maraichère": "#58d68d",
    "Plantation forestière": "#196f3d",
    "Carrière Mine Infrastructure": "#7f8c8d",
}

# Équipements sectors reused verbatim from app/routers/equipements.py's SECTOR_LABELS —
# each sector folder holds several small heterogeneous GeoJSON files (official + OSM-derived),
# merged on demand by /carte/data/equipements/{sector} rather than duplicated on disk.
EQUIPEMENTS_SECTORS = {
    "sante": {"label": "Équipements — Santé", "color": "#e74c3c"},
    "education": {"label": "Équipements — Éducation", "color": "#3498db"},
    "culture": {"label": "Équipements — Culture & Loisirs", "color": "#9b59b6"},
    "economie": {"label": "Équipements — Économie & Tourisme", "color": "#f39c12"},
    "sport": {"label": "Équipements — Sport", "color": "#27ae60"},
}

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
            "risque-inondation": {
                "label": "Risque inondation", "color": "#e74c3c", "type": "polygon",
                "filter": {
                    "field": "Categorie", "uiLabel": "Catégorie",
                    "options": ["Risque très fort", "Risque fort", "Risque moyen", "Risque faible"],
                },
            },
            "vulnerabilite": {
                "label": "Vulnérabilité", "color": "#e67e22", "type": "polygon",
                "filter": {
                    "field": "indice", "uiLabel": "Indice",
                    "options": [1, 2, 3, 4], "numeric": True,
                },
            },
            "erosion": {"label": "Érosion", "color": "#ff69b4", "type": "polygon"},
        },
    },
    "evolution": {
        "label": "Évolution urbaine",
        "layers": {
            # Client remark (interactive-map): red family, 2017 = darkest/foreground,
            # 2024 = lightest/background. Deterministic stacking via dedicated Leaflet
            # panes (see carte.html) — do not rely on fetch/toggle order.
            "empreinte-2017": {"label": "Empreinte 2017", "color": "#7f1d1d", "type": "polygon", "fillOpacity": 1, "pane": "empreinte2017Pane", "paneZIndex": 403},
            "empreinte-2020": {"label": "Empreinte 2020", "color": "#dc2626", "type": "polygon", "fillOpacity": 1, "pane": "empreinte2020Pane", "paneZIndex": 402},
            "empreinte-2024": {"label": "Empreinte 2024", "color": "#fca5a5", "type": "polygon", "fillOpacity": 1, "pane": "empreinte2024Pane", "paneZIndex": 401},
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
    "occupation": {
        "label": "Occupation du sol",
        "layers": {
            # Reuses the validated Wave 2/Phase 5 layer as-is — no duplicate GeoJSON generated.
            "occupation-du-sol-2020": {
                "label": "Occupation du sol — 2020", "color": "#7f8c8d", "type": "polygon",
                "categoryField": "categorie", "categoryColors": OCCSOL_2020_CATEGORY_COLORS,
                "coverage": "Donnée 2020 (17 classes) — ne représente pas l'occupation du sol actuelle",
            },
        },
    },
    "relief": {
        "label": "Relief",
        "layers": {
            "hillshade-mnt": {
                "label": "Relief ombré (MNT)", "type": "image", "color": "#555555",
                "url": "/static/img/topographie/hillshade-mnt.png",
                "bounds": [[15.828733, -16.530742], [16.141098, -16.327712]],
                "imageOpacity": 0.6,
                "coverage": "Donnée dérivée du MNT fourni par le client",
            },
            "courbes-niveau-5m": {
                "label": "Courbes de niveau 5 m", "color": "#a0522d", "type": "line",
                "coverage": "Donnée transmise par le client",
            },
        },
    },
    "equipements": {
        "label": "Équipements",
        "layers": {
            f"equip-{sector}": {
                "label": info["label"], "color": info["color"], "type": "point",
                "sector": sector,
                "coverage": (
                    "Couverture intercommunale agrégée (sources officielles + OpenStreetMap) — "
                    "non structurée de façon fiable par commune ; aucun jeu de données équipements "
                    "dédié n'a été transmis pour Gandon à ce jour"
                ),
            }
            for sector, info in EQUIPEMENTS_SECTORS.items()
        },
    },
}


def _resolve_layer_url(layer_id: str, layer_info: dict):
    """Return the URL to fetch this layer's data from, or None if unavailable."""
    if layer_info.get("type") == "image":
        # Image overlays are static files, not GeoJSON — check existence directly.
        rel = layer_info["url"].removeprefix("/static/")
        if (Path(__file__).resolve().parent.parent / "static" / rel).exists():
            return layer_info["url"]
        return None

    if "sector" in layer_info:
        # Équipements layers are merged on demand from several small files — always
        # "available" if the sector folder exists and holds at least one file.
        sector_dir = DATA_DIR / "equipements" / layer_info["sector"]
        if sector_dir.exists() and any(sector_dir.glob("*.geojson")):
            return f"/carte/data/equipements/{layer_info['sector']}"
        return None

    for subdir in DATA_DIR.rglob(f"{layer_id}.geojson"):
        return f"/static/data/{subdir.relative_to(DATA_DIR)}"
    return None


@router.get("/", name="carte_interactive")
async def carte_page(request: Request):
    # Scan available layers (GeoJSON on disk, image overlays, or on-demand équipements merges)
    available_layers = {}
    for group_id, group in LAYER_GROUPS.items():
        available = {}
        for layer_id, layer_info in group["layers"].items():
            url = _resolve_layer_url(layer_id, layer_info)
            if url:
                available[layer_id] = {**layer_info, "url": url}
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


@router.get("/data/equipements/{sector}", name="carte_equipements_sector")
async def equipements_sector_geojson(sector: str):
    """Merge a sector's already-validated GeoJSON files into one FeatureCollection,
    computed in memory on first request — no new file is written to disk."""
    if sector not in EQUIPEMENTS_SECTORS:
        return JSONResponse({"type": "FeatureCollection", "features": []}, status_code=404)

    sector_dir = DATA_DIR / "equipements" / sector
    features = []
    if sector_dir.exists():
        for geojson_path in sorted(sector_dir.glob("*.geojson")):
            try:
                with open(geojson_path, encoding="utf-8") as fh:
                    data = json.load(fh)
                features.extend(data.get("features", []))
            except (json.JSONDecodeError, OSError):
                continue

    return JSONResponse({"type": "FeatureCollection", "features": features})
