from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")

# ── Each section = its own page with its own map, image, and dashboard ──

SECTIONS = {
    "geologie": {
        "label": "Géologie",
        "title": "Le sous-sol et les formations naturelles",
        "subtitle": "Géologie — Formations du Quaternaire",
        "image": "/static/img/cartes/geologie.jpg",
        "image_alt": "Carte géologique de l'agglomération de Saint-Louis",
        "content": "La zone d'étude présente des formations géologiques variées datant du Quaternaire : cordons littoraux et dunes jaunes, dunes vives, dunes littorales semi-fixées, cuvettes argileuses de décantation, levées deltaïques, levées sub-actuelles, remaniement de dunes rouges, terrasses marines sableuses et vasières.",
        "messages": [
            "9 formations géologiques identifiées sur le territoire",
            "Prédominance des dunes et cordons littoraux côté océan",
            "Vasières et levées deltaïques le long du fleuve Sénégal",
        ],
        "layers": [
            {"file": "diagnostic/geologie/cordons-littoraux.geojson", "name": "Cordons littoraux", "color": "#f4d03f"},
            {"file": "diagnostic/geologie/dunes-semi-fixees.geojson", "name": "Dunes semi-fixées", "color": "#e67e22"},
            {"file": "diagnostic/geologie/dunes-rouges.geojson", "name": "Dunes rouges", "color": "#c0392b"},
            {"file": "diagnostic/geologie/cuvettes-argileuses.geojson", "name": "Cuvettes argileuses", "color": "#7f8c8d"},
            {"file": "diagnostic/geologie/levees-deltaiques.geojson", "name": "Levées deltaïques", "color": "#27ae60"},
            {"file": "diagnostic/geologie/levees-sub-actuelles.geojson", "name": "Levées sub-actuelles", "color": "#2ecc71"},
            {"file": "diagnostic/geologie/terrasse-marine.geojson", "name": "Terrasse marine", "color": "#3498db"},
            {"file": "diagnostic/geologie/vasieres.geojson", "name": "Vasières", "color": "#1abc9c"},
        ],
        "stats": [
            {"value": "8", "label": "Formations géologiques", "icon": "layers"},
            {"value": "96 km²", "label": "Vasières cartographiées", "icon": "water"},
            {"value": "24 km²", "label": "Cordons littoraux", "icon": "mountain"},
            {"value": "Quaternaire", "label": "Période géologique", "icon": "clock"},
        ],
    },
    "pedologie": {
        "label": "Pédologie",
        "title": "Les types de sols",
        "subtitle": "Pédologie — Classification des sols",
        "image": "/static/img/cartes/pedologie.jpg",
        "image_alt": "Carte pédologique de l'agglomération de Saint-Louis",
        "content": "Les sols de l'agglomération se répartissent en plusieurs types : sols minéraux bruts, sols isohumiques sur sable silicieux, sols halomorphes (salés) et sols d'alluvions fluviatiles. Cette diversité conditionne les possibilités d'urbanisation et d'agriculture.",
        "messages": [
            "4 grands types de sols identifiés",
            "Sols salés (halomorphes) près de la côte, limitant la construction",
            "Sols alluviaux fertiles le long du fleuve, propices à l'agriculture",
        ],
        "layers": [],
        "stats": [
            {"value": "4", "label": "Types de sols", "icon": "layers"},
            {"value": "Salés", "label": "Sols côtiers dominants", "icon": "alert"},
            {"value": "Fertiles", "label": "Sols fluviaux", "icon": "leaf"},
            {"value": "Variable", "label": "Aptitude à l'urbanisation", "icon": "building"},
        ],
    },
    "topographie": {
        "label": "Topographie",
        "title": "Le relief et les altitudes",
        "subtitle": "Topographie — Courbes de niveau",
        "image": None,
        "content": "Le relief est globalement plat avec des altitudes très faibles (0 à 10 mètres). Cette topographie basse contribue directement à la vulnérabilité face aux inondations. Les zones les plus basses se concentrent le long du fleuve et sur l'île de Saint-Louis.",
        "messages": [
            "Altitude moyenne inférieure à 5 mètres sur toute la zone",
            "Relief plat favorisant la stagnation des eaux pluviales",
            "13 762 courbes de niveau cartographiées",
        ],
        "layers": [
            {"file": "diagnostic/topographie/courbes-niveau.geojson", "name": "Courbes de niveau", "color": "#8B4513", "type": "line"},
        ],
        "stats": [
            {"value": "0–10 m", "label": "Altitude du territoire", "icon": "mountain"},
            {"value": "< 5 m", "label": "Altitude moyenne", "icon": "arrow-down"},
            {"value": "13 762", "label": "Courbes de niveau", "icon": "layers"},
            {"value": "Plat", "label": "Type de relief", "icon": "map"},
        ],
    },
    "occupation": {
        "label": "Occupation du sol",
        "title": "Comment le territoire est utilisé",
        "subtitle": "Occupation du sol — 14 catégories",
        "image": "/static/img/cartes/occupation-sol.jpg",
        "image_alt": "Carte d'occupation du sol de l'agglomération de Saint-Louis",
        "content": "Le territoire présente une grande diversité d'occupations du sol : zones urbaines, cultures maraîchères et irriguées, cultures pluviales, plantations forestières, mangrove, savanes (arbustive, boisée), steppes, sols nus (dunaire, inondable), et canaux d'irrigation.",
        "messages": [
            "14 catégories d'occupation du sol cartographiées",
            "L'urbain s'étend progressivement sur les espaces naturels",
            "La mangrove et les savanes occupent encore de vastes étendues",
        ],
        "layers": [
            {"file": "occupation-sol/empreinte-urbaine.geojson", "name": "Empreinte urbaine", "color": "#e74c3c"},
            {"file": "occupation-sol/culture-pluviale.geojson", "name": "Culture pluviale", "color": "#f1c40f"},
            {"file": "occupation-sol/plantation-forestiere.geojson", "name": "Plantation forestière", "color": "#27ae60"},
            {"file": "occupation-sol/mangrove.geojson", "name": "Mangrove", "color": "#1abc9c"},
            {"file": "occupation-sol/savane-arbustive.geojson", "name": "Savane arbustive", "color": "#8e44ad"},
            {"file": "occupation-sol/savane-boisee.geojson", "name": "Savane boisée", "color": "#6c3483"},
            {"file": "occupation-sol/steppe.geojson", "name": "Steppe", "color": "#d4a574"},
            {"file": "occupation-sol/sol-nu-dunaire.geojson", "name": "Sol nu dunaire", "color": "#f0e68c"},
            {"file": "occupation-sol/sol-nu-inondable.geojson", "name": "Sol nu inondable", "color": "#87ceeb"},
            {"file": "occupation-sol/canal-irrigation.geojson", "name": "Canal d'irrigation", "color": "#2980b9", "type": "line"},
        ],
        "stats": [
            {"value": "14", "label": "Catégories de sol", "icon": "layers"},
            {"value": "407 ha", "label": "Empreinte urbaine", "icon": "building"},
            {"value": "84 ha", "label": "Mangrove", "icon": "leaf"},
            {"value": "1 765 ha", "label": "Culture maraîchère", "icon": "plant"},
        ],
    },
    "urbanisation": {
        "label": "Urbanisation",
        "title": "Comment la ville s'est agrandie",
        "subtitle": "Évolution de la tache urbaine 2017 – 2024",
        "image": "/static/img/cartes/evolution-urbaine.jpg",
        "image_alt": "Carte d'évolution de la tache urbaine 2017-2024",
        "content": "Entre 2017 et 2024, l'agglomération de Saint-Louis a connu une croissance urbaine significative, mise en évidence par photo-interprétation d'images Sentinel-2. Trois empreintes urbaines (2017, 2020, 2024) permettent de visualiser cette expansion et de la comparer aux lotissements planifiés. La pression démographique se traduit par une augmentation continue des besoins en logements et infrastructures.",
        "messages": [
            "3 périodes d'observation : 2017, 2020, 2024",
            "Expansion principalement vers Gandon et les zones périurbaines",
            "Décalage entre urbanisation réelle et lotissements planifiés",
        ],
        "layers": [
            {"file": "evolution/empreinte-2017.geojson", "name": "Empreinte 2017", "color": "#8B4513"},
            {"file": "evolution/empreinte-2020.geojson", "name": "Empreinte 2020", "color": "#e67e22"},
            {"file": "evolution/empreinte-2024.geojson", "name": "Empreinte 2024", "color": "#e91e63"},
            {"file": "evolution/lotissements.geojson", "name": "Lotissements planifiés", "color": "#3498db"},
        ],
        "stats": [
            {"value": "195", "label": "Zones urbaines 2017", "icon": "building"},
            {"value": "202", "label": "Zones urbaines 2020", "icon": "building"},
            {"value": "215", "label": "Zones urbaines 2024", "icon": "building"},
            {"value": "4", "label": "Lotissements planifiés", "icon": "map"},
        ],
    },
    "risques": {
        "label": "Risques naturels",
        "title": "Zones exposées aux risques",
        "subtitle": "Inondation, vulnérabilité et érosion côtière",
        "image": None,
        "content": "Saint-Louis fait face à des risques naturels majeurs : inondations liées à la topographie basse et au fonctionnement hydraulique du territoire, vulnérabilité des populations urbaines, érosion côtière menaçant la Langue de Barbarie, et intrusion saline. Les zones les plus exposées se situent sur l'île de Saint-Louis et dans la partie côtière de Gandon et Ndiébène Gandiole, où se concentrent les infrastructures essentielles.",
        "messages": [
            "147 zones de risque d'inondation cartographiées",
            "1 058 zones de vulnérabilité identifiées",
            "3 zones d'érosion côtière sur le littoral",
            "Gor, Guet Ndar et Pikine parmi les plus vulnérables",
        ],
        "layers": [
            {"file": "risques/risque-inondation.geojson", "name": "Risque d'inondation", "color": "#e74c3c"},
            {"file": "risques/vulnerabilite.geojson", "name": "Vulnérabilité", "color": "#e67e22"},
            {"file": "risques/erosion.geojson", "name": "Érosion côtière", "color": "#8B0000"},
        ],
        "stats": [
            {"value": "147", "label": "Zones d'inondation", "icon": "water"},
            {"value": "1 058", "label": "Zones vulnérables", "icon": "alert"},
            {"value": "3", "label": "Zones d'érosion", "icon": "mountain"},
            {"value": "4", "label": "Niveaux de risque", "icon": "layers"},
        ],
    },
    "transport": {
        "label": "Transport",
        "title": "Les infrastructures de transport",
        "subtitle": "Réseau routier et ferroviaire",
        "image": "/static/img/cartes/transport.jpg",
        "image_alt": "Carte des infrastructures de transport de Saint-Louis",
        "content": "Le réseau de transport de l'agglomération comprend des routes nationales, locales, résidentielles, des pistes, et une voie de chemin de fer historique. L'accessibilité varie fortement entre Saint-Louis et les communes périphériques.",
        "messages": [
            "7 catégories de voies de circulation cartographiées",
            "Réseau de pistes important dans les zones rurales",
            "Chemin de fer historique Saint-Louis – Dakar",
        ],
        "layers": [
            {"file": "transport/route-locale.geojson", "name": "Routes locales", "color": "#e67e22", "type": "line"},
            {"file": "transport/route-residentielle.geojson", "name": "Routes résidentielles", "color": "#95a5a6", "type": "line"},
            {"file": "transport/route-tertiaire.geojson", "name": "Routes tertiaires", "color": "#f39c12", "type": "line"},
            {"file": "transport/route-construction.geojson", "name": "Routes en construction", "color": "#e74c3c", "type": "line"},
            {"file": "transport/piste.geojson", "name": "Pistes", "color": "#d4a574", "type": "line"},
            {"file": "transport/chemin-fer.geojson", "name": "Chemin de fer", "color": "#2c3e50", "type": "line"},
            {"file": "transport/route-acces.geojson", "name": "Routes d'accès", "color": "#16a085", "type": "line"},
        ],
        "stats": [
            {"value": "7", "label": "Types de voies", "icon": "road"},
            {"value": "226 km", "label": "Routes locales", "icon": "road"},
            {"value": "361 km", "label": "Pistes", "icon": "road"},
            {"value": "9 km", "label": "Chemin de fer", "icon": "train"},
        ],
    },
    "population": {
        "label": "Population",
        "title": "Répartition de la population",
        "subtitle": "Quartiers et données démographiques",
        "image": "/static/img/cartes/population.jpg",
        "image_alt": "Carte de répartition de la population de Saint-Louis",
        "content": "La population de l'agglomération regroupe plus de 350 000 habitants en 2023 (RGPH-5), caractérisée par une croissance soutenue entre 2% et 4% par an et une structure démographique très jeune. Saint-Louis concentre environ 72% de la population totale, confirmant son rôle de pôle urbain central, tandis que Gandon et Ndiébène Gandiole présentent des profils ruraux et périurbains en forte mutation.",
        "messages": [
            "350 000+ habitants recensés en 2023 (RGPH-5)",
            "Saint-Louis concentre 72% de la population totale",
            "Croissance démographique entre 2% et 4% par an",
            "Projections démographiques à l'horizon 2050 disponibles",
        ],
        "layers": [
            {"file": "population/quartiers-polygones.geojson", "name": "Quartiers", "color": "#3498db"},
            {"file": "population/population-quartiers.geojson", "name": "Points de population", "color": "#e74c3c", "type": "point"},
        ],
        "stats": [
            {"value": "350 000+", "label": "Habitants (RGPH 2023)", "icon": "users"},
            {"value": "72%", "label": "Population à Saint-Louis", "icon": "building"},
            {"value": "2-4%", "label": "Croissance annuelle", "icon": "arrow-up"},
            {"value": "2050", "label": "Horizon de projection", "icon": "clock"},
        ],
    },
    "equipements": {
        "label": "Équipements",
        "title": "Équipements et services par commune",
        "subtitle": "Santé, éducation, culture, sport, tourisme",
        "image": None,
        "content": "L'inventaire des équipements socio-collectifs couvre plusieurs secteurs : santé (hôpital, postes de santé), éducation (écoles, lycées), culture (musées, bibliothèques), économie et tourisme (hôtels, marchés), sport (stades, terrains). La répartition est inégale entre les 3 communes.",
        "messages": [
            "98 couches d'équipements converties pour les 3 communes",
            "Saint-Louis concentre la majorité des services publics",
            "Gandon et Gandiol manquent d'équipements de santé et d'éducation",
        ],
        "layers": [
            {"file": "equipements/education/ecole-élémentaire.geojson", "name": "Écoles élémentaires", "color": "#3498db", "type": "point"},
            {"file": "equipements/education/cem.geojson", "name": "CEM (collèges)", "color": "#2980b9", "type": "point"},
            {"file": "equipements/education/lycée.geojson", "name": "Lycées", "color": "#1a5276", "type": "point"},
            {"file": "equipements/sante/hôpital-régional-de-saint-louis.geojson", "name": "Hôpital", "color": "#e74c3c", "type": "point"},
            {"file": "equipements/sport/terrain-de-sport.geojson", "name": "Terrains de sport", "color": "#27ae60", "type": "point"},
            {"file": "equipements/culture/musée.geojson", "name": "Musées", "color": "#8e44ad", "type": "point"},
            {"file": "equipements/economie/marché-permanent.geojson", "name": "Marchés", "color": "#f39c12", "type": "point"},
            {"file": "equipements/economie/hôtel.geojson", "name": "Hôtels", "color": "#e67e22", "type": "point"},
        ],
        "stats": [
            {"value": "57+", "label": "Écoles élémentaires", "icon": "school"},
            {"value": "11", "label": "CEM / collèges", "icon": "school"},
            {"value": "1", "label": "Hôpital régional", "icon": "hospital"},
            {"value": "10+", "label": "Terrains de sport", "icon": "sport"},
        ],
    },
}

# Order of sections for navigation
SECTION_ORDER = [
    "geologie", "pedologie", "topographie", "occupation",
    "urbanisation", "risques", "transport", "population", "equipements",
]


@router.get("/", name="diagnostic")
async def diagnostic_page(request: Request, section: str = "geologie"):
    if section not in SECTIONS:
        section = "geologie"
    return templates.TemplateResponse(request, "diagnostic_unified.html", {
        "page_title": SECTIONS[section]["title"],
        "sections": {k: SECTIONS[k] for k in SECTION_ORDER},
        "section_order": SECTION_ORDER,
        "active_section": section,
        "data": SECTIONS[section],
    })


# Backward compatibility redirects for old URLs
@router.get("/situation")
async def redir_situation():
    return RedirectResponse(url="/diagnostic?section=geologie", status_code=301)

@router.get("/geologie")
async def redir_geologie():
    return RedirectResponse(url="/diagnostic?section=geologie", status_code=301)

@router.get("/pedologie")
async def redir_pedologie():
    return RedirectResponse(url="/diagnostic?section=pedologie", status_code=301)

@router.get("/topographie")
async def redir_topographie():
    return RedirectResponse(url="/diagnostic?section=topographie", status_code=301)

@router.get("/occupation-du-sol")
async def redir_occupation():
    return RedirectResponse(url="/diagnostic?section=occupation", status_code=301)

@router.get("/evolution-urbaine")
async def redir_evolution():
    return RedirectResponse(url="/diagnostic?section=urbanisation", status_code=301)
