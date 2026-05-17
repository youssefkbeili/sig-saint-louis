from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get("/inondation", name="inondation")
async def inondation_page(request: Request):
    return templates.TemplateResponse(request, "risques/inondation.html", {
        "page_title": "Risques d'inondation",
    })


@router.get("/vulnerabilite", name="vulnerabilite")
async def vulnerabilite_page(request: Request):
    return templates.TemplateResponse(request, "risques/vulnerabilite.html", {
        "page_title": "Vulnérabilité",
    })


@router.get("/erosion", name="erosion")
async def erosion_page(request: Request):
    return templates.TemplateResponse(request, "risques/erosion.html", {
        "page_title": "Érosion côtière",
    })
