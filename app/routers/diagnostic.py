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
            "Nouveau : 44 zones de conservation (protection naturelle et patrimoniale)",
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
            {
                "file": "conservation/zones-conservation.geojson",
                "name": "Zones de conservation (nouvelle donnée)",
                "color": "#2e7d32",
                "categoryField": "categorie",
                "categoryColors": {
                    "Protection Naturel": "#2e7d32",
                    "Protection Patrimoinel": "#8e44ad",
                },
            },
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
        "subtitle": "Topographie — Relief (MNT), courbes de niveau",
        "image": None,
        "content": "Le relief est globalement plat avec des altitudes très faibles (0 à 10 mètres). Cette topographie basse contribue directement à la vulnérabilité face aux inondations. Les zones les plus basses se concentrent le long du fleuve et sur l'île de Saint-Louis. Un modèle numérique de terrain (MNT) et des courbes de niveau au pas de 5 m sont désormais disponibles en complément des courbes existantes.",
        "messages": [
            "Altitude moyenne inférieure à 5 mètres sur toute la zone",
            "Relief plat favorisant la stagnation des eaux pluviales",
            "13 762 courbes de niveau cartographiées (pas variable)",
            "Nouveau : relief ombré (MNT) et courbes de niveau au pas de 5 m",
        ],
        "layers": [
            {"file": "diagnostic/topographie/courbes-niveau.geojson", "name": "Courbes de niveau", "color": "#8B4513", "type": "line"},
            {
                "name": "Relief ombré (MNT)",
                "type": "image",
                "url": "/static/img/topographie/hillshade-mnt.png",
                "bounds": [[15.828733, -16.530742], [16.141098, -16.327712]],
                "imageOpacity": 0.6,
                "color": "#555555",
            },
            {"file": "diagnostic/topographie/courbes-niveau-5m.geojson", "name": "Courbes de niveau 5 m (nouvelle donnée)", "color": "#a0522d", "type": "line"},
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
            "Nouvelle couche 2020 disponible : 17 classes, couvrant une zone plus large que l'agglomération",
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
            {
                "file": "occupation-sol-2020/occupation-du-sol-2020.geojson",
                "name": "Occupation du sol 2020 (nouvelle donnée)",
                "color": "#7f8c8d",
                "categoryField": "categorie",
                "categoryColors": {
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
                },
            },
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
            {"file": "evolution/empreinte-2017.geojson", "name": "Empreinte 2017", "color": "#7f1d1d", "fillOpacity": 1, "pane": "empreinte2017Pane", "paneZIndex": 403},
            {"file": "evolution/empreinte-2020.geojson", "name": "Empreinte 2020", "color": "#dc2626", "fillOpacity": 1, "pane": "empreinte2020Pane", "paneZIndex": 402},
            {"file": "evolution/empreinte-2024.geojson", "name": "Empreinte 2024", "color": "#fca5a5", "fillOpacity": 1, "pane": "empreinte2024Pane", "paneZIndex": 401},
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
    "peuplement": {
        "label": "Peuplement",
        "title": "Peuplement — quartiers et localités",
        "subtitle": "Structure spatiale de l'habitat : quartiers et localités/villages",
        "image": None,
        "content": "Cette carte présente la structure spatiale du peuplement de l'agglomération : quartiers urbains et localités/villages. Elle décrit où les populations sont implantées, avant le détail démographique présenté dans le thème « Population ». La couverture réelle de chaque couche est indiquée : certaines données ne couvrent pas encore les 3 communes.",
        "messages": [
            "Quartiers de Saint-Louis (33), Gandon (33) et Ndiébène Gandiol (26) avec nom et population par quartier",
            "372 localités/villages recensés sur une zone plus large que l'agglomération — sans nom individuel disponible",
            "Les noms de villages de la couche « Localités » ne sont pas disponibles dans la donnée source — non inventés ici",
        ],
        "layers": [
            {"file": "population/quartiers-polygones.geojson", "name": "Quartiers — Saint-Louis", "color": "#3498db", "coverage": "Couverture : Saint-Louis uniquement"},
            {"file": "peuplement/quartiers-gandon.geojson", "name": "Quartiers — Gandon", "color": "#16a34a", "type": "point", "coverage": "Couverture : Gandon uniquement"},
            {"file": "peuplement/quartiers-gandiol.geojson", "name": "Quartiers — Ndiébène Gandiol", "color": "#d97706", "type": "point", "coverage": "Couverture : Ndiébène Gandiol uniquement"},
            {"file": "peuplement/localites.geojson", "name": "Localités / villages (sans nom, nouvelle donnée)", "color": "#7f8c8d", "coverage": "Couverture : zone régionale plus large que l'agglomération — noms de villages non disponibles"},
        ],
        "stats": [
            {"value": "33+33+26", "label": "Quartiers nommés (SL / Gandon / Gandiol)", "icon": "map"},
            {"value": "372", "label": "Localités/villages (footprints, sans nom)", "icon": "layers"},
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
    "economie_energie": {
        "label": "Économie & Énergie",
        "title": "Développement économique & énergie",
        "subtitle": "Activités économiques diversifiées, transition énergétique et corridors structurants",
        "image": None,
        "content": "Ce thème présente les activités économiques du territoire ainsi que les enjeux de transition énergétique de l'agglomération de Saint-Louis. Les données actuellement disponibles ne couvrent pas encore les 3 communes de façon égale : la couverture réelle de chaque couche est indiquée sous son nom, et aucune donnée de Gandon n'a été dupliquée vers les autres communes.",
        "messages": [
            "Activités économiques diversifiées",
            "Transition énergétique",
            "Couverture actuelle : Gandon (économie + énergie) et Ndiébène Gandiol (économie) — Saint-Louis non couvert par ces nouvelles données",
        ],
        "layers": [
            {"file": "economie/economie-gandon.geojson", "name": "Zones et projets économiques — Gandon", "color": "#f39c12", "coverage": "Couverture : Gandon uniquement"},
            {"file": "economie/economie-gandiol.geojson", "name": "Projets économiques, agricoles & équipements — Ndiébène Gandiol", "color": "#e67e22", "coverage": "Couverture : Ndiébène Gandiol uniquement"},
            {"file": "economie/usine-zircon-gandiol.geojson", "name": "Usine d'exploitation du Zircon (CEN_HMC) — Ndiébène Gandiol", "color": "#8B4513", "type": "point", "coverage": "Couverture : Ndiébène Gandiol uniquement (site unique)"},
            {"file": "energie/energie-gandon.geojson", "name": "Infrastructures énergétiques — Gandon (centrale à gaz, poste Senelec)", "color": "#d35400", "type": "point", "coverage": "Couverture : Gandon uniquement"},
            {"file": "energie/gazoduc-gandon.geojson", "name": "Corridor énergétique — Tracé Gazoduc RGS (Gandon)", "color": "#c0392b", "type": "line", "coverage": "Couverture : Gandon uniquement"},
            {"file": "economie/future-autoroute.geojson", "name": "Corridor structurant — Future autoroute (projeté)", "color": "#34495e", "coverage": "Couverture : tracé projeté, emprise partielle disponible"},
        ],
        "stats": [
            {"value": "4", "label": "Zones/projets économiques — Gandon", "icon": "building"},
            {"value": "14", "label": "Projets économiques/équipements — Gandiol", "icon": "building"},
            {"value": "2", "label": "Infrastructures énergétiques — Gandon", "icon": "layers"},
            {"value": "2", "label": "Corridors structurants identifiés", "icon": "road"},
        ],
    },
    "gouvernance": {
        "label": "Gouvernance",
        "title": "Gouvernance et intercommunalité",
        "subtitle": "Coopération entre les communes de l'agglomération",
        "image": None,
        "content": "Ce thème présente les enjeux de gouvernance et de coopération intercommunale entre les communes de Saint-Louis, Gandon et Ndiébène Gandiol.",
        "messages": [
            "Coopération entre les communes de Saint-Louis, Gandon et Ndiébène Gandiol",
        ],
        "layers": [],
        "stats": [],
    },
}

# Order of sections for navigation
SECTION_ORDER = [
    "geologie", "pedologie", "topographie", "occupation",
    "urbanisation", "risques", "transport", "peuplement", "population", "equipements",
    "economie_energie", "gouvernance",
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
