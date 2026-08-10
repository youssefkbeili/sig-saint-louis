"""
Wave 4C — structured PCU/PCUI content.

Full audit method and source traceability are in PCU_CONTENT_BASELINE.md.
Headline finding: no dedicated PCU/PCUI document (rapport de présentation,
zonage réglementaire, règlement, EES, or atlas) exists in the delivered
material for any commune. The only real, usable content found is:
  - a small planning-orientation GIS layer for Gandon ("Zone d'extension
    futur/en cours"), explicitly NOT presented as official zoning
  - SVD-roadmap "Priorité / Projet structurant" tables per commune, which
    the SVD text itself connects to the term "Projets d'Investissement
    Prioritaires (PIP)" — used here for the PIP section, with only the
    3 fields that actually exist (priorité, nom, portée stratégique)

Nothing here was fabricated. Every status below is either MISSING or
PARTIAL — never presented as if it were AVAILABLE/complete when it isn't.
"""

PCU_SECTION_ORDER = ["rapport-presentation", "zonage", "pip", "reglement", "ees", "atlas"]

PCU_SECTION_META = {
    "rapport-presentation": {"label": "Rapport de présentation"},
    "zonage": {"label": "Zonage"},
    "pip": {"label": "PIP"},
    "reglement": {"label": "Règlement d'urbanisme"},
    "ees": {"label": "Évaluation environnementale stratégique"},
    "atlas": {"label": "Atlas cartographique"},
}

_MISSING_GENERIC = {
    "status": "MISSING",
    "note": "Aucun document n'a été livré pour cette section à ce jour. Rien n'a été inventé ici — la section sera complétée dès réception d'un document validé par le client.",
}

COMMUNE_PCU = {
    "saint-louis": {
        "rapport-presentation": dict(_MISSING_GENERIC, note=(
            "Aucun rapport de présentation du PCU/PCUI n'a été livré. Le rapport SVD cite, comme source de "
            "certaines cartes, un document distinct et plus ancien (« Plan de sauvegarde et de mise en valeur "
            "de l'île de Saint-Louis — Rapport de présentation », 2006), mais ce document n'a pas été fourni "
            "et ne peut donc pas être publié ici."
        )),
        "zonage": dict(_MISSING_GENERIC, layers=[], note=(
            "Aucune donnée de zonage réglementaire n'a été livrée pour Saint-Louis. Les couches déjà publiées "
            "sous « Diagnostic » (occupation du sol, habitat) sont des données d'observation du territoire, "
            "pas un zonage PCU/PCUI approuvé — elles ne sont pas dupliquées ici sous cette étiquette."
        )),
        "pip": {
            "status": "PARTIAL",
            "note": (
                "Aucun document PIP formel n'a été livré séparément. Le rapport SVD identifie cependant des "
                "« Projets structurants » classés par ordre de priorité et les relie explicitement au principe "
                "des Projets d'Investissement Prioritaires (PIP). Seuls les champs réellement présents dans la "
                "source sont affichés : priorité, nom du projet, portée stratégique — ni coût, ni calendrier, "
                "ni entité responsable, ni statut ne sont disponibles dans le document source."
            ),
            "groups": [
                {
                    "theme": "Résilience climatique et littoral",
                    "projets": [
                        {"priorite": 1, "nom": "Sécurisation de la brèche et protection du littoral", "portee": "Projet vital pour la protection de la ville contre l'érosion et la submersion marine"},
                        {"priorite": 2, "nom": "Programme intégré mangroves – récifs – lutte contre la salinisation", "portee": "Solution fondée sur la nature pour restaurer les écosystèmes et protéger le littoral"},
                        {"priorite": 3, "nom": "Extension du réseau de drainage et gestion des eaux pluviales", "portee": "Réduction des inondations urbaines et amélioration de la résilience climatique"},
                        {"priorite": 4, "nom": "Renforcement des digues et ouvrages hydrauliques", "portee": "Protection des zones urbaines basses et du front fluvial"},
                        {"priorite": 5, "nom": "Plan intégré de gestion du littoral et observatoire du trait de côte", "portee": "Outil stratégique de gouvernance et de suivi des risques"},
                    ],
                },
                {
                    "theme": "Développement urbain et mobilité",
                    "projets": [
                        {"priorite": 1, "nom": "Construction d'un deuxième pont reliant Sor, l'île et la Langue de Barbarie", "portee": "Infrastructure majeure pour la mobilité et la décongestion du centre-ville"},
                        {"priorite": 2, "nom": "Restructuration des quartiers irréguliers et programme de logements adaptés", "portee": "Amélioration durable du cadre de vie et réduction de la vulnérabilité urbaine"},
                        {"priorite": 3, "nom": "Élaboration et mise en œuvre d'un plan de déplacement urbain", "portee": "Organisation durable des mobilités et réduction de la congestion"},
                        {"priorite": 4, "nom": "Modernisation des marchés structurants (marché de Sor notamment)", "portee": "Renforcement des centralités urbaines et dynamisation des activités locales"},
                        {"priorite": 5, "nom": "Densification et modernisation du réseau de voirie urbaine", "portee": "Amélioration de l'accessibilité et structuration du développement urbain"},
                    ],
                },
                {
                    "theme": "Développement économique",
                    "projets": [
                        {"priorite": 1, "nom": "Réhabilitation et modernisation du port de pêche et des quais", "portee": "Projet clé pour la filière halieutique et l'économie locale"},
                        {"priorite": 2, "nom": "Création d'une zone économique spéciale sur le corridor Ngallèle – Gandon", "portee": "Levier majeur pour l'investissement et l'industrialisation territoriale"},
                        {"priorite": 3, "nom": "Création d'un marché moderne de poissons avec chaîne du froid", "portee": "Structuration de la commercialisation des produits halieutiques"},
                        {"priorite": 4, "nom": "Création d'un centre de formation halieutique et agricole", "portee": "Renforcement du capital humain et de l'emploi local"},
                        {"priorite": 5, "nom": "Réhabilitation du centre historique et développement du tourisme culturel", "portee": "Valorisation du patrimoine et diversification de l'économie"},
                    ],
                },
            ],
        },
        "reglement": dict(_MISSING_GENERIC),
        "ees": dict(_MISSING_GENERIC),
        "atlas": dict(_MISSING_GENERIC, note=(
            "Aucun atlas cartographique groupé n'a été livré. Les cartes déjà publiées sur le site "
            "(Diagnostic, carte interactive) ne sont pas repackagées ici en « atlas » sans confirmation "
            "explicite du client sur cette interprétation."
        )),
    },
    "gandon": {
        "rapport-presentation": dict(_MISSING_GENERIC),
        "zonage": {
            "status": "PARTIAL",
            "note": (
                "Une seule couche a été identifiée comme potentiellement liée au zonage : « Zone d'extension "
                "futur / en cours », utilisant un vocabulaire de planification authentique (court/moyen/long "
                "terme). Elle est publiée ici comme une orientation de planification, PAS comme un zonage "
                "réglementaire approuvé — aucune référence légale, code de zone ou statut d'approbation "
                "n'existe dans la donnée source."
            ),
            "layers": [
                {"file": "pcu/gandon/zone-extension-planifiee.geojson", "name": "Zones d'extension planifiées (CT/MT/LT) — orientation, non approuvée", "color": "#9b59b6", "categoryField": "nom",
                 "categoryColors": {"Zone d'extension futur ( MT, LT)": "#9b59b6", "Zone d'extension en cours  (CT)": "#e67e22"}},
            ],
        },
        "pip": {
            "status": "PARTIAL",
            "note": (
                "Mêmes réserves que pour Saint-Louis : données issues des tableaux de priorisation du rapport "
                "SVD, pas d'un document PIP formel distinct. Seuls priorité, nom et portée stratégique existent."
            ),
            "groups": [
                {
                    "theme": "Résilience climatique et agricole",
                    "projets": [
                        {"priorite": 1, "nom": "Programme de résilience agropastorale (500 ha + 100 forages solaires)", "portee": "Projet pivot économie + climat"},
                        {"priorite": 2, "nom": "Aménagement des cuvettes agricoles (Djeuss / Gueumbeul)", "portee": "Sécurisation production maraîchère"},
                        {"priorite": 3, "nom": "Plan intégré de gestion des risques (CPRC + littoral)", "portee": "Gouvernance climatique"},
                        {"priorite": 4, "nom": "Restauration écosystèmes (Delta SAED / PNUD)", "portee": "Solution fondée sur la nature"},
                        {"priorite": 5, "nom": "Infrastructures d'appui (stockage, vaccination)", "portee": "Résilience productive"},
                    ],
                },
                {
                    "theme": "Structuration urbaine et intercommunale",
                    "projets": [
                        {"priorite": 1, "nom": "Aménagement 100 ha relogement + urbanisation maîtrisée", "portee": "Projet structurant majeur PCUi"},
                        {"priorite": 2, "nom": "Corridor Ngallèle – Gandon", "portee": "Structuration intercommunale"},
                        {"priorite": 3, "nom": "100 km pistes rurales productives", "portee": "Désenclavement économique"},
                        {"priorite": 4, "nom": "Restructuration Ngallèle – Khor", "portee": "Projet intercommunal critique"},
                        {"priorite": 5, "nom": "Mobilité multimodale (fluvial + ligne)", "portee": "Accessibilité territoriale"},
                    ],
                },
                {
                    "theme": "Développement économique",
                    "projets": [
                        {"priorite": 1, "nom": "ZES Ngallèle – Gandon", "portee": "Transformation économique majeure"},
                        {"priorite": 2, "nom": "Agropole", "portee": "Sécurisation production agricole"},
                        {"priorite": 3, "nom": "Modernisation quai + filière halieutique", "portee": "Chaîne de valeur pêche"},
                        {"priorite": 4, "nom": "Électrification solaire productive", "portee": "Transition énergétique"},
                        {"priorite": 5, "nom": "Maisons emploi + fonds GIE", "portee": "Inclusion socio-économique"},
                    ],
                },
            ],
        },
        "reglement": dict(_MISSING_GENERIC),
        "ees": dict(_MISSING_GENERIC),
        "atlas": dict(_MISSING_GENERIC),
    },
    "gandiole": {
        "rapport-presentation": dict(_MISSING_GENERIC),
        "zonage": dict(_MISSING_GENERIC, layers=[], note=(
            "Aucune couche de zonage ou d'orientation de planification propre à Ndiébène Gandiole n'a été "
            "identifiée dans cet audit (contrairement à Gandon, qui dispose d'une couche d'orientation limitée)."
        )),
        "pip": {
            "status": "PARTIAL",
            "note": (
                "Mêmes réserves que pour les deux autres communes : données issues des tableaux de "
                "priorisation du rapport SVD, pas d'un document PIP formel distinct."
            ),
            "groups": [
                {
                    "theme": "Projets structurants",
                    "projets": [
                        {"priorite": 1, "nom": "Poste de santé avec chaîne du froid", "portee": "Urgence sociale et inclusion territoriale"},
                        {"priorite": 2, "nom": "Marché intercommunal aux poissons", "portee": "Structuration de la filière bleue et sécurité alimentaire"},
                        {"priorite": 3, "nom": "Forages solaires et bassins maraîchers", "portee": "Résilience productive et sécurité alimentaire"},
                        {"priorite": 4, "nom": "Centre de formation aux métiers halieutiques et touristiques", "portee": "Renforcement du capital humain et employabilité"},
                        {"priorite": 5, "nom": "Circuits écotouristiques littoraux", "portee": "Diversification économique et valorisation patrimoniale"},
                        {"priorite": 6, "nom": "Programme « Mangroves & récifs »", "portee": "Protection écosystémique et résilience climatique"},
                    ],
                },
            ],
        },
        "reglement": dict(_MISSING_GENERIC),
        "ees": dict(_MISSING_GENERIC),
        "atlas": dict(_MISSING_GENERIC),
    },
}
