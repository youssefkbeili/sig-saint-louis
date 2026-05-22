from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")

STATS = [
    {"value": 3, "label": "Communes"},
    {"value": "350 000+", "label": "Habitants (RGPH 2023)"},
    {"value": 78, "label": "Couches cartographiques"},
    {"value": 9, "label": "Thèmes d'analyse"},
]


@router.get("/", name="home")
async def home_page(request: Request):
    return templates.TemplateResponse(request, "home.html", {
        "stats": STATS,
        "page_title": "Accueil",
    })


@router.get("/projet", name="projet")
async def projet_page(request: Request):
    return templates.TemplateResponse(request, "projet.html", {
        "page_title": "Le projet",
    })


@router.get("/ressources", name="ressources")
async def ressources_page(request: Request):
    return templates.TemplateResponse(request, "ressources.html", {
        "page_title": "Ressources",
        "success_message": None,
    })


@router.post("/ressources", name="ressources_submit")
async def ressources_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
):
    # TODO: In production, send email or store in database
    return templates.TemplateResponse(request, "ressources.html", {
        "page_title": "Ressources",
        "success_message": "Votre message a bien été envoyé. Nous vous répondrons dans les meilleurs délais.",
    })


# Backward compatibility redirects
@router.get("/a-propos")
async def about_redirect():
    return RedirectResponse(url="/projet", status_code=301)


@router.get("/telechargements")
async def downloads_redirect():
    return RedirectResponse(url="/ressources", status_code=301)


@router.get("/contact")
async def contact_redirect():
    return RedirectResponse(url="/ressources", status_code=301)
