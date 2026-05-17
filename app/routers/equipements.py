from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")

COMMUNES = {
    "saint-louis": {
        "name": "Saint-Louis",
        "sectors": ["sante", "education", "culture", "economie", "sport"],
    },
    "gandon": {
        "name": "Gandon",
        "sectors": ["sante", "education", "economie", "sport"],
    },
    "gandiol": {
        "name": "Ndiébène Gandiol",
        "sectors": ["sante", "sport"],
    },
}

SECTOR_LABELS = {
    "sante": {"label": "Santé", "icon": "🏥", "color": "#e74c3c"},
    "education": {"label": "Éducation", "icon": "🎓", "color": "#3498db"},
    "culture": {"label": "Culture & Loisirs", "icon": "🎭", "color": "#9b59b6"},
    "economie": {"label": "Économie & Tourisme", "icon": "💼", "color": "#f39c12"},
    "sport": {"label": "Sport", "icon": "⚽", "color": "#27ae60"},
}


@router.get("/{commune}", name="equipements_commune")
async def equipements_page(request: Request, commune: str):
    if commune not in COMMUNES:
        commune = "saint-louis"

    commune_info = COMMUNES[commune]

    # Load GeoJSON data for each sector if available
    data_dir = Path(__file__).resolve().parent.parent / "static" / "data" / "equipements"
    sectors_data = {}
    for sector in commune_info["sectors"]:
        sector_dir = data_dir / sector
        geojson_files = list(sector_dir.glob("*.geojson")) if sector_dir.exists() else []
        sectors_data[sector] = {
            "info": SECTOR_LABELS.get(sector, {}),
            "files": [f.stem for f in geojson_files],
            "count": 0,
        }
        # Count features from GeoJSON files
        for gf in geojson_files:
            try:
                with open(gf) as fh:
                    data = json.load(fh)
                    sectors_data[sector]["count"] += len(data.get("features", []))
            except (json.JSONDecodeError, OSError):
                pass

    return templates.TemplateResponse(request, "equipements/commune.html", {
        "page_title": f"Équipements — {commune_info['name']}",
        "commune": commune,
        "commune_info": commune_info,
        "communes": COMMUNES,
        "sectors_data": sectors_data,
        "sector_labels": SECTOR_LABELS,
    })
