"""
Wave 4A — per-commune Diagnostic content and data-coverage configuration.

Kept separate from communes.py to keep that router file readable: this module is
pure configuration (mirrors the pattern already used for diagnostic.py's SECTIONS
dict, one level deeper to account for per-commune variation).

Layer lists below were built from real, verified data only:
- geologie / conservation / risques / topographie / urbanisation / transport / occupation-sol-2020:
  spatially clipped from the existing global layers to each commune's own boundary
  (app/static/data/base/limite-communale.geojson), via shapely, in this wave.
  Layers that clip to zero features for a given commune are simply not listed for
  that commune (confirmed programmatically before writing this file, not guessed).
- habitat / foncier / économie / énergie / corridors: reused directly from Wave 3
  and this wave's own commune-native shapefile conversions (Gandon/Ndiébène Gandiol
  only — no equivalent client data exists for Saint-Louis).
- démographie: reuses the existing Saint-Louis quartier polygons and Wave 3's
  Gandon/Gandiol quartier points.
- enjeux: reuses the existing, already-vetted `COMMUNES[slug]["enjeux"]` list from
  communes.py — no new content invented here.

COVERAGE values: COMPLETE / PARTIAL / GLOBAL_CONTEXT / MISSING (never fabricated;
directly reflects whether real, clipped/commune-specific data exists).
"""

DIAGNOSTIC_SECTION_ORDER = [
    "milieu-physique", "demographie", "urbain-mobilite",
    "habitat-foncier", "economie-energie", "enjeux",
]

DIAGNOSTIC_SECTION_META = {
    "milieu-physique": {"label": "Milieu physique et risques", "icon": "mountain"},
    "demographie": {"label": "Démographie", "icon": "users"},
    "urbain-mobilite": {"label": "Développement urbain et mobilité", "icon": "road"},
    "habitat-foncier": {"label": "Habitat et foncier", "icon": "building"},
    "economie-energie": {"label": "Activités économiques et énergie", "icon": "chart"},
    "enjeux": {"label": "Enjeux et problématiques", "icon": "alert"},
}

_D = "app/static/data"  # not used directly (paths below are web paths under /static/data/), kept for readability only


def _layers_milieu_physique(slug, geologie, conservation, risques, topo):
    layers = []
    for key, name, color in geologie:
        layers.append({"file": f"communes/{slug}/geologie-{key}.geojson", "name": name, "color": color})
    if conservation:
        layers.append({
            "file": f"communes/{slug}/conservation-zones.geojson", "name": "Zones de conservation",
            "color": "#2e7d32", "categoryField": "categorie",
            "categoryColors": {"Protection Naturel": "#2e7d32", "Protection Patrimoinel": "#8e44ad"},
        })
    for key, name, color, gtype in risques:
        layers.append({"file": f"communes/{slug}/risques-{key}.geojson", "name": name, "color": color, "type": gtype})
    for key, name, color in topo:
        layers.append({"file": f"communes/{slug}/topo-{key}.geojson", "name": name, "color": color, "type": "line"})
    layers.append({
        "name": "Relief ombré (MNT) — contexte régional", "type": "image",
        "url": "/static/img/topographie/hillshade-mnt.png",
        "bounds": [[15.828733, -16.530742], [16.141098, -16.327712]],
        "imageOpacity": 0.5, "color": "#555555",
        "coverage": "Contexte régional (MNT non découpé par commune)",
    })
    return layers


GEOLOGIE_ALL = [
    ("cordons-littoraux", "Cordons littoraux", "#f4d03f"),
    ("dunes-semi-fixees", "Dunes semi-fixées", "#e67e22"),
    ("dunes-rouges", "Dunes rouges", "#c0392b"),
    ("cuvettes-argileuses", "Cuvettes argileuses", "#7f8c8d"),
    ("levees-deltaiques", "Levées deltaïques", "#27ae60"),
    ("levees-sub-actuelles", "Levées sub-actuelles", "#2ecc71"),
    ("terrasse-marine", "Terrasse marine", "#3498db"),
    ("vasieres", "Vasières", "#1abc9c"),
]
RISQUES_ALL = [
    ("inondation", "Risque d'inondation", "#e74c3c", "polygon"),
    ("vulnerabilite", "Vulnérabilité", "#e67e22", "polygon"),
    ("erosion", "Érosion côtière", "#8B0000", "line"),
]
TOPO_ALL = [
    ("courbes-niveau", "Courbes de niveau", "#8B4513"),
    ("courbes-niveau-5m", "Courbes de niveau 5 m", "#a0522d"),
]

OCCSOL_2020_CATEGORY_COLORS = {
    "Mare": "#3498db", "Lac": "#2980b9", "Cours d'eau": "#1abc9c", "Plaine inondable": "#85c1e9",
    "Vasière": "#a9946c", "Mangrove": "#16a085", "Prairie aquatique": "#48c9b0", "Tanne": "#f7dc6f",
    "Steppe": "#d4a574", "Savane": "#8e44ad", "Sol nu": "#f0e68c", "Dune": "#e67e22",
    "Culture pluviale": "#f1c40f", "Culture irriguée": "#27ae60", "Culture maraichère": "#58d68d",
    "Plantation forestière": "#196f3d", "Carrière Mine Infrastructure": "#7f8c8d", "Empreinte urbaine": "#e74c3c",
}


COMMUNE_DIAGNOSTIC = {
    "saint-louis": {
        "milieu-physique": {
            "coverage": "COMPLETE",
            "note": "Données découpées sur le territoire communal. Certaines formations géologiques n'existent pas sur ce territoire (île/presqu'île) — leur absence reflète la réalité du terrain, pas une donnée manquante.",
            "layers": _layers_milieu_physique(
                "saint-louis",
                [g for g in GEOLOGIE_ALL if g[0] in ("cordons-littoraux", "vasieres")],
                True,
                RISQUES_ALL,
                TOPO_ALL,
            ),
        },
        "demographie": {
            "coverage": "COMPLETE",
            "note": "33 quartiers avec population par quartier (donnée déjà présente dans le projet).",
            "layers": [
                {"file": "population/quartiers-polygones.geojson", "name": "Quartiers de Saint-Louis (avec population)", "color": "#3498db"},
            ],
        },
        "urbain-mobilite": {
            "coverage": "COMPLETE",
            "note": None,
            "layers": [
                {"file": "communes/saint-louis/urbanisation-empreinte-2017.geojson", "name": "Empreinte urbaine 2017", "color": "#7f1d1d", "fillOpacity": 1, "pane": "empreinte2017Pane", "paneZIndex": 403},
                {"file": "communes/saint-louis/urbanisation-empreinte-2020.geojson", "name": "Empreinte urbaine 2020", "color": "#dc2626", "fillOpacity": 1, "pane": "empreinte2020Pane", "paneZIndex": 402},
                {"file": "communes/saint-louis/urbanisation-empreinte-2024.geojson", "name": "Empreinte urbaine 2024", "color": "#fca5a5", "fillOpacity": 1, "pane": "empreinte2024Pane", "paneZIndex": 401},
                {"file": "communes/saint-louis/urbanisation-lotissements.geojson", "name": "Lotissements planifiés", "color": "#3498db"},
                {"file": "communes/saint-louis/occupation-sol-2020.geojson", "name": "Occupation du sol 2020 (découpage dérivé, voir note)", "color": "#7f8c8d", "categoryField": "categorie", "categoryColors": OCCSOL_2020_CATEGORY_COLORS,
                 "coverage": "Découpage réalisé pour ce projet à partir de la couche régionale — Gandon/Gandiol utilisent un découpage fourni directement par le client"},
                {"file": "communes/saint-louis/transport-route-locale.geojson", "name": "Routes locales", "color": "#e67e22", "type": "line"},
                {"file": "communes/saint-louis/transport-route-tertiaire.geojson", "name": "Routes tertiaires", "color": "#f39c12", "type": "line"},
                {"file": "communes/saint-louis/transport-route-construction.geojson", "name": "Routes en construction", "color": "#e74c3c", "type": "line"},
                {"file": "communes/saint-louis/transport-piste.geojson", "name": "Pistes", "color": "#d4a574", "type": "line"},
                {"file": "communes/saint-louis/transport-chemin-fer.geojson", "name": "Chemin de fer", "color": "#2c3e50", "type": "line"},
                {"file": "communes/saint-louis/transport-route-acces.geojson", "name": "Routes d'accès", "color": "#16a085", "type": "line"},
            ],
        },
        "habitat-foncier": {
            "coverage": "MISSING",
            "note": "Aucune donnée foncière/habitat spécifique à Saint-Louis n'a été livrée par le client (contrairement à Gandon et Ndiébène Gandiol, qui disposent de couches ZAPA/ZAPE/ZP/lotissements). Non inventé ici.",
            "layers": [],
        },
        "economie-energie": {
            "coverage": "MISSING",
            "note": "Aucune donnée d'activité économique ou d'infrastructure énergétique spécifique à Saint-Louis n'a été livrée (contrairement à Gandon et Ndiébène Gandiol).",
            "layers": [],
        },
    },
    "gandon": {
        "milieu-physique": {
            "coverage": "COMPLETE",
            "note": None,
            "layers": _layers_milieu_physique("gandon", GEOLOGIE_ALL, True, RISQUES_ALL, TOPO_ALL),
        },
        "demographie": {
            "coverage": "COMPLETE",
            "note": "33 quartiers nommés avec population, issus de la donnée client vérifiée en Wave 3.",
            "layers": [
                {"file": "peuplement/quartiers-gandon.geojson", "name": "Quartiers de Gandon (avec population)", "color": "#16a34a", "type": "point"},
            ],
        },
        "urbain-mobilite": {
            "coverage": "COMPLETE",
            "note": None,
            "layers": [
                {"file": "communes/gandon/urbanisation-empreinte-2017.geojson", "name": "Empreinte urbaine 2017", "color": "#7f1d1d", "fillOpacity": 1, "pane": "empreinte2017Pane", "paneZIndex": 403},
                {"file": "communes/gandon/urbanisation-empreinte-2020.geojson", "name": "Empreinte urbaine 2020", "color": "#dc2626", "fillOpacity": 1, "pane": "empreinte2020Pane", "paneZIndex": 402},
                {"file": "communes/gandon/urbanisation-empreinte-2024.geojson", "name": "Empreinte urbaine 2024", "color": "#fca5a5", "fillOpacity": 1, "pane": "empreinte2024Pane", "paneZIndex": 401},
                {"file": "communes/gandon/urbanisation-lotissements.geojson", "name": "Lotissements planifiés", "color": "#3498db"},
                {"file": "communes/gandon/urbain-zone-habitation-empreinte.geojson", "name": "Empreinte urbaine détaillée (reclassée depuis « Zone d'habitation »)", "color": "#e74c3c",
                 "coverage": "Reclassée ici : le fichier source nommé « Zone d'habitation (ZH) » contient en réalité un attribut « Empreinte urbaine », pas un zonage d'habitat — voir rapport"},
                {"file": "communes/gandon/occupation-sol-2020.geojson", "name": "Occupation du sol 2020 (découpage fourni par le client)", "color": "#7f8c8d", "categoryField": "categorie", "categoryColors": OCCSOL_2020_CATEGORY_COLORS},
                {"file": "economie/future-autoroute.geojson", "name": "Corridor structurant — Future autoroute (projeté)", "color": "#34495e"},
                {"file": "communes/gandon/transport-route-locale.geojson", "name": "Routes locales", "color": "#e67e22", "type": "line"},
                {"file": "communes/gandon/transport-route-residentielle.geojson", "name": "Routes résidentielles", "color": "#95a5a6", "type": "line"},
                {"file": "communes/gandon/transport-route-tertiaire.geojson", "name": "Routes tertiaires", "color": "#f39c12", "type": "line"},
                {"file": "communes/gandon/transport-route-construction.geojson", "name": "Routes en construction", "color": "#e74c3c", "type": "line"},
                {"file": "communes/gandon/transport-piste.geojson", "name": "Pistes", "color": "#d4a574", "type": "line"},
                {"file": "communes/gandon/transport-chemin-fer.geojson", "name": "Chemin de fer", "color": "#2c3e50", "type": "line"},
                {"file": "communes/gandon/transport-route-acces.geojson", "name": "Routes d'accès", "color": "#16a085", "type": "line"},
            ],
        },
        "habitat-foncier": {
            "coverage": "PARTIAL",
            "note": "Les couches ZAPA/ZAPE/ZP portent un nom de zonage agro-pastoral, mais leurs attributs réels sont des catégories d'occupation du sol (ex. « Culture maraîchère », « Steppe »), pas un code de zonage distinct — affiché tel quel, sans invention d'un code de zonage qui n'existe pas dans la donnée.",
            "layers": [
                {"file": "communes/gandon/habitat-lotissements-autorises.geojson", "name": "Lotissements autorisés (parcelles)", "color": "#3498db"},
                {"file": "communes/gandon/habitat-zapa.geojson", "name": "Zone agro-pastorale à priorité agricole (ZAPA) — voir note", "color": "#f1c40f", "categoryField": "categorie", "categoryColors": OCCSOL_2020_CATEGORY_COLORS},
                {"file": "communes/gandon/habitat-zape.geojson", "name": "Zone agro-pastorale à priorité élevage (ZAPE) — voir note", "color": "#d4a574", "categoryField": "categorie", "categoryColors": OCCSOL_2020_CATEGORY_COLORS},
                {"file": "communes/gandon/habitat-zp.geojson", "name": "Zone pastorale (ZP) — voir note", "color": "#8e44ad", "categoryField": "categorie", "categoryColors": OCCSOL_2020_CATEGORY_COLORS},
            ],
        },
        "economie-energie": {
            "coverage": "PARTIAL",
            "note": "Sites/projets isolés uniquement — pas une couverture économique exhaustive de la commune.",
            "layers": [
                {"file": "economie/economie-gandon.geojson", "name": "Zones et projets économiques", "color": "#f39c12"},
                {"file": "energie/energie-gandon.geojson", "name": "Infrastructures énergétiques (centrale à gaz, poste Senelec)", "color": "#d35400", "type": "point"},
                {"file": "energie/gazoduc-gandon.geojson", "name": "Corridor énergétique — Tracé Gazoduc RGS", "color": "#c0392b", "type": "line"},
            ],
        },
    },
    "gandiole": {
        "milieu-physique": {
            "coverage": "COMPLETE",
            "note": "Certaines formations géologiques et la vulnérabilité aux inondations ne concernent pas ce territoire d'après la donnée découpée — absence réelle, pas une lacune.",
            "layers": _layers_milieu_physique(
                "gandiole",
                [g for g in GEOLOGIE_ALL if g[0] not in ("cuvettes-argileuses", "levees-deltaiques", "levees-sub-actuelles", "terrasse-marine")],
                True,
                [r for r in RISQUES_ALL if r[0] != "vulnerabilite"],
                TOPO_ALL,
            ),
        },
        "demographie": {
            "coverage": "PARTIAL",
            "note": "26 quartiers nommés (3 issus du fichier Gandon + 23 d'un fichier dédié) ; 7 d'entre eux n'ont pas de population renseignée dans la donnée source — non estimée ici.",
            "layers": [
                {"file": "peuplement/quartiers-gandiol.geojson", "name": "Quartiers de Ndiébène Gandiol (avec population, partielle)", "color": "#d97706", "type": "point"},
            ],
        },
        "urbain-mobilite": {
            "coverage": "COMPLETE",
            "note": None,
            "layers": [
                {"file": "communes/gandiole/urbanisation-empreinte-2017.geojson", "name": "Empreinte urbaine 2017", "color": "#7f1d1d", "fillOpacity": 1, "pane": "empreinte2017Pane", "paneZIndex": 403},
                {"file": "communes/gandiole/urbanisation-empreinte-2020.geojson", "name": "Empreinte urbaine 2020", "color": "#dc2626", "fillOpacity": 1, "pane": "empreinte2020Pane", "paneZIndex": 402},
                {"file": "communes/gandiole/urbanisation-empreinte-2024.geojson", "name": "Empreinte urbaine 2024", "color": "#fca5a5", "fillOpacity": 1, "pane": "empreinte2024Pane", "paneZIndex": 401},
                {"file": "communes/gandiole/urbain-zone-habitation-empreinte.geojson", "name": "Empreinte urbaine détaillée (reclassée depuis « Zone d'habitation »)", "color": "#e74c3c",
                 "coverage": "Reclassée ici : le fichier source nommé « Zone d'habitation (ZH) » contient en réalité une catégorie « Empreinte urbaine », pas un zonage d'habitat — voir rapport"},
                {"file": "communes/gandiole/occupation-sol-2020.geojson", "name": "Occupation du sol 2020 (découpage fourni par le client)", "color": "#7f8c8d", "categoryField": "categorie", "categoryColors": OCCSOL_2020_CATEGORY_COLORS},
                {"file": "communes/gandiole/transport-route-locale.geojson", "name": "Routes locales", "color": "#e67e22", "type": "line"},
                {"file": "communes/gandiole/transport-route-tertiaire.geojson", "name": "Routes tertiaires", "color": "#f39c12", "type": "line"},
                {"file": "communes/gandiole/transport-piste.geojson", "name": "Pistes", "color": "#d4a574", "type": "line"},
                {"file": "communes/gandiole/transport-route-acces.geojson", "name": "Routes d'accès", "color": "#16a085", "type": "line"},
            ],
        },
        "habitat-foncier": {
            "coverage": "PARTIAL",
            "note": "Mêmes réserves que pour Gandon : les couches ZAPA/ZAPE/ZP portent un nom de zonage mais leurs attributs réels sont des catégories d'occupation du sol. Aucun équivalent « lotissements autorisés » n'a été livré pour cette commune.",
            "layers": [
                {"file": "communes/gandiole/habitat-zapa.geojson", "name": "Zone agro-pastorale à priorité agricole (ZAPA) — voir note", "color": "#f1c40f", "categoryField": "categorie", "categoryColors": OCCSOL_2020_CATEGORY_COLORS},
                {"file": "communes/gandiole/habitat-zape.geojson", "name": "Zone agro-pastorale à priorité élevage (ZAPE) — voir note", "color": "#d4a574", "categoryField": "categorie", "categoryColors": OCCSOL_2020_CATEGORY_COLORS},
                {"file": "communes/gandiole/habitat-zp.geojson", "name": "Zone pastorale (ZP) — voir note", "color": "#8e44ad", "categoryField": "categorie", "categoryColors": OCCSOL_2020_CATEGORY_COLORS},
                {"file": "communes/gandiole/habitat-zpe.geojson", "name": "Zone de protection écologique (ZPE)", "color": "#2e7d32"},
            ],
        },
        "economie-energie": {
            "coverage": "PARTIAL",
            "note": "Sites/projets isolés uniquement — pas une couverture économique exhaustive de la commune. Aucune donnée énergétique n'a été livrée pour cette commune.",
            "layers": [
                {"file": "economie/economie-gandiol.geojson", "name": "Projets économiques, agricoles & équipements", "color": "#e67e22"},
                {"file": "economie/usine-zircon-gandiol.geojson", "name": "Usine d'exploitation du Zircon (CEN_HMC)", "color": "#8B4513", "type": "point"},
            ],
        },
    },
}
