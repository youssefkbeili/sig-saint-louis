"""
Wave 4B — structured SVD (Stratégie de Ville Durable) content, extracted from the
three official commune SVD reports:

  - reply client/SVD_Saint-Louis_12-05.docx
  - reply client/SVD_Gandon 12-05 1.docx
  - reply client/SDV Gandiole 12-05.docx

Every string below is a faithful summary or direct quote of source text — nothing
here was invented. Full source traceability (paragraph index, heading, page-area)
is recorded in SVD_CONTENT_BASELINE.md, not duplicated inline here to keep this
module focused on what the website actually renders.

Structure mirrors commune_diagnostic_data.py's pattern:
COMMUNE -> Vision -> Principes directeurs -> Axes stratégiques -> Programmes de développement.

IMPORTANT — shared vs. commune-specific:
The Vision (2050 formulation), the 5 "Principes directeurs," and the 7 "Axes
stratégiques" are near word-for-word IDENTICAL across all 3 source documents —
they describe ONE intercommunal strategy for the whole agglomeration. They are
stored ONCE below (VISION_INTERCOMMUNALE, PRINCIPES_DIRECTEURS, AXES_STRATEGIQUES)
and labeled "Vision intercommunale" on the website, per the explicit instruction
not to present shared content as if it were commune-specific.

Each commune ALSO has its own distinct Vision statement (confirmed different
wording per commune, not shared) and its own "Programmes de développement"
content — that part IS commune-specific and is stored per-commune below.
"""

VISION_INTERCOMMUNALE = {
    "text": (
        "Produire un cadre de vie bâti durable, résilient et inclusif, fondé sur la coopération "
        "intercommunale et la valorisation de la diversité territoriale."
    ),
    "context": (
        "Formulation retenue à l'horizon 2050 dans l'architecture de la Stratégie de Ville Durable (SVD), "
        "reprenant et actualisant la vision originelle du Plan Directeur d'Urbanisme (PDU) : « Produire un "
        "cadre de vie bâti durable, basé sur la coopération entre les différentes échelles et la diversité "
        "du territoire, partant de l'intercommunalité au niveau local »."
    ),
}

PRINCIPES_DIRECTEURS = [
    {
        "titre": "Un cadre de vie salubre et digne pour l'ensemble des populations",
        "resume": "Réduire les disparités entre quartiers et communes ; garantir un accès équitable à l'habitat, aux infrastructures et aux services urbains essentiels.",
    },
    {
        "titre": "Capacité du territoire à s'adapter aux défis climatiques et environnementaux",
        "resume": "Planifier en tenant compte des risques d'inondation, d'érosion côtière et de submersion, tout en protégeant les écosystèmes et zones humides.",
    },
    {
        "titre": "Planification de l'espace face à la croissance démographique",
        "resume": "Anticiper les besoins futurs en orientant les développements vers des espaces sécurisés, accessibles et bien structurés.",
    },
    {
        "titre": "Accompagner le développement économique et l'emploi",
        "resume": "Structurer une économie territoriale durable, inclusive et créatrice de valeur, appuyée sur les filières locales.",
    },
    {
        "titre": "Gouvernance territoriale efficace, décentralisée et participative",
        "resume": "Coordination entre acteurs institutionnels, implication des collectivités, participation des populations aux décisions.",
    },
]
PRINCIPES_DIRECTEURS_NOTE = (
    "Un sixième principe, transversal, porte sur l'organisation efficace des mobilités et de l'accessibilité, "
    "condition de mise en œuvre des cinq principes ci-dessus."
)

AXES_STRATEGIQUES = [
    {
        "numero": 1,
        "titre": "Résilience climatique, environnementale et ville compatible avec l'eau",
        "resume": "Protection du littoral et des zones vulnérables, gestion durable des inondations, infrastructures vertes, adaptation au changement climatique.",
    },
    {
        "numero": 2,
        "titre": "Urbanisation maîtrisée, structuration spatiale et armature territoriale",
        "resume": "Renforcement des centralités urbaines, planification foncière, densification maîtrisée, lutte contre l'étalement urbain.",
    },
    {
        "numero": 3,
        "titre": "Habitat, cadre de vie, services urbains et cohésion sociale",
        "resume": "Requalification des quartiers existants, renforcement des services urbains de base, développement des équipements publics.",
    },
    {
        "numero": 4,
        "titre": "Mobilité durable, accessibilité et structuration des corridors",
        "resume": "Transport collectif performant, corridors de mobilité intercommunaux, mobilités douces, accessibilité renforcée.",
    },
    {
        "numero": 5,
        "titre": "Développement économique local, économie durable et valorisation territoriale",
        "resume": "Zones d'activités économiques (dont la ZES), valorisation des filières locales, modernisation de la pêche, tourisme durable, emploi.",
    },
    {
        "numero": 6,
        "titre": "Transition énergétique, sécurité énergétique et ville à financements verts",
        "resume": "Sécurisation de l'approvisionnement énergétique, intégration maîtrisée de la nouvelle centrale à gaz de Gandon, énergies renouvelables, financements verts.",
    },
    {
        "numero": 7,
        "titre": "Gouvernance territoriale, pilotage stratégique et innovation institutionnelle",
        "resume": "Coopération intercommunale, transparence et redevabilité, participation citoyenne, observatoire territorial, suivi-évaluation.",
    },
]

PROGRAMME_CATEGORY_LABELS = {
    "environnement": "Environnement",
    "urbanisme": "Urbanisme",
    "economie_societe": "Économie et société",
    "gouvernance": "Gouvernance et intercommunalité",
}

COMMUNE_SVD = {
    "saint-louis": {
        "vision": {
            "text": (
                "Produire un cadre de vie bâti durable, basé sur la coopération entre les différentes "
                "échelles et la diversité du territoire, partant de l'intercommunalité au niveau local."
            ),
            "note": "Saint-Louis adopte explicitement la vision d'ensemble du PDU comme sa propre vision territoriale (le document ne formule pas de vision distincte propre à la commune).",
        },
        "programmes": {
            "environnement": {
                "titre_source": "Programme d'adaptation et d'atténuation des risques environnementaux et climatiques",
                "resume": (
                    "Constat propre à Saint-Louis : saturation récurrente des réseaux de drainage lors des fortes "
                    "pluies, forte vulnérabilité à la submersion marine, à l'érosion côtière et à la salinisation, "
                    "urbanisation dense entre océan et fleuve. Quartiers cités : Ngallèle, Bango, Maka Toubé Sor, "
                    "Langue de Barbarie."
                ),
                "leviers": [
                    "Connaissance et suivi des dynamiques littorales et fluviales",
                    "Urbanisme résilient adapté aux risques d'inondation et de submersion",
                    "Solutions fondées sur la nature (restauration des mangroves et zones humides)",
                    "Gouvernance intégrée entre littoral, fleuve et territoires amont",
                ],
            },
            "urbanisme": {
                "titre_source": "Programme de développement urbain durable et résiliente",
                "resume": (
                    "Saint-Louis correspond au bassin aval littoral et estuarien (BV3) : centre urbain historique et "
                    "littoral vulnérable, forte densité de population, exposition élevée aux inondations, érosion "
                    "côtière et submersion marine. La stratégie vise à réorganiser la ville et ses équipements, "
                    "développer des typologies bâties adaptées aux risques (habitat amphibie, infrastructures "
                    "poreuses), protéger les zones humides et littorales, et positionner Saint-Louis comme "
                    "territoire pilote en urbanisme climatique."
                ),
                "leviers": [],
            },
            "economie_societe": {
                "titre_source": "Programme de développement économique et social",
                "resume": (
                    "Double ambition : consolider les activités historiques — en particulier la pêche artisanale, "
                    "pilier socio-économique majeur — et diversifier vers des secteurs à plus forte valeur ajoutée "
                    "(tertiaire supérieur, innovation, numérique, énergie), tout en affirmant le rôle métropolitain "
                    "régional de Saint-Louis. Certaines fonctions économiques structurantes seront déployées à "
                    "l'échelle intercommunale, notamment sur Gandon, pour limiter la pression foncière sur la ville "
                    "centre."
                ),
                "leviers": [],
            },
            "gouvernance": {
                "titre_source": "Programme de bonne gouvernance territoriale et institutionnelle : Commune de Saint-Louis",
                "resume": (
                    "Objectif général : mettre en place un système de gouvernance performant, transparent et "
                    "orienté résultats, permettant à Saint-Louis d'assurer le pilotage stratégique du PCUi et de "
                    "renforcer son rôle de pôle urbain, institutionnel et économique de l'agglomération."
                ),
                "leviers": [
                    "Renforcer le rôle de Saint-Louis comme pôle de pilotage intercommunal",
                    "Assurer un pilotage stratégique et opérationnel du PCUi",
                    "Mettre en place un système de suivi-évaluation structuré",
                    "Améliorer la transparence et la participation citoyenne",
                    "Structurer les mécanismes de financement et d'investissement",
                ],
            },
        },
    },
    "gandon": {
        "vision": {
            "text": "Faire de Gandon un territoire viable, attractif et compétitif, porteur d'un développement durable.",
            "note": "Vision propre à la commune de Gandon, distincte de la vision intercommunale, construite avec l'exécutif communal et les acteurs locaux.",
        },
        "programmes": {
            "environnement": {
                "titre_source": "Programme d'adaptation et d'atténuation des risques environnementaux et climatiques",
                "resume": (
                    "Contenu partagé avec la trame intercommunale (mêmes 5 principes : approche par bassin "
                    "versant, prévention des risques, solutions fondées sur la nature, aménagement différencié, "
                    "gouvernance intercommunale de l'eau) — le document de Gandon ne détaille pas, à la différence "
                    "de Saint-Louis, un état des lieux environnemental propre à la commune dans cette section."
                ),
                "leviers": [],
            },
            "urbanisme": {
                "titre_source": "Programme de développement urbain durable et résilient",
                "resume": (
                    "Gandon est un territoire charnière entre l'agglomération de Saint-Louis et les espaces "
                    "ruraux/agricoles du delta, au carrefour des corridors logistiques (autoroute, RN2, liaison "
                    "Dakar). La proximité de Saint-Louis exerce une pression urbaine et foncière croissante : "
                    "extension de l'habitat, conversion de terres agricoles, urbanisation spontanée. Le territoire "
                    "doit aussi accueillir plusieurs projets structurants (zone économique spéciale, plateforme "
                    "logistique). La stratégie met l'accent sur la maîtrise foncière et la préservation des terres "
                    "agricoles."
                ),
                "leviers": [
                    "Maîtrise foncière",
                    "Préservation des espaces agricoles structurants",
                    "Organisation des zones de transition habitat–agriculture",
                    "Urbanisation maîtrisée compatible avec le fonctionnement du bassin versant",
                ],
            },
            "economie_societe": {
                "titre_source": "Programme de développement économique et social",
                "resume": (
                    "Contrairement à Saint-Louis où la pêche domine, Gandon se distingue par un potentiel "
                    "agro-pastoral important, des réserves foncières stratégiques et une capacité d'accueil pour "
                    "des fonctions économiques structurantes (zones d'activités, logistique, services). Ambition : "
                    "faire de Gandon un territoire d'équilibre, productif, attractif et résilient, complémentaire "
                    "de Saint-Louis."
                ),
                "leviers": [
                    "Développement d'un pôle agroéconomique structurant",
                    "Création de zones d'activités économiques",
                    "Développement des fonctions de portée intercommunale",
                    "Promotion de l'économie verte et territoriale",
                ],
            },
            "gouvernance": {
                "titre_source": "Programme de bonne gouvernance territoriale et institutionnelle",
                "resume": (
                    "Objectif général : mettre en place un système de gouvernance intercommunale efficace, "
                    "transparent et orienté résultats, capable d'assurer le pilotage stratégique du PCUi, la "
                    "coordination des acteurs et la mise en œuvre des projets structurants."
                ),
                "leviers": [
                    "Renforcer la coordination intercommunale entre Saint-Louis, Gandon et Ndiébène Gandiole",
                    "Assurer un pilotage stratégique et opérationnel du PCUi",
                    "Mettre en place un système de suivi-évaluation performant",
                    "Améliorer la transparence et la participation citoyenne",
                    "Structurer les mécanismes de financement et d'investissement",
                ],
            },
        },
    },
    "gandiole": {
        "vision": {
            "text": "Produire un territoire attractif et émergent dans un cadre de vie durable.",
            "note": "Vision propre à Ndiébène Gandiole, présentée dans le document comme étant en harmonie avec la vision du PDU (citée en complément).",
        },
        "programmes": {
            "environnement": {
                "titre_source": "Programme d'adaptation et d'atténuation des risques environnementaux et climatiques",
                "resume": (
                    "Contenu partagé avec la trame intercommunale (mêmes 5 principes que Saint-Louis et Gandon) — "
                    "le document de Ndiébène Gandiole ne détaille pas non plus un état des lieux environnemental "
                    "propre à la commune dans cette section précise ; le contexte environnemental communal (zones "
                    "humides, littoral, salinisation) est en revanche développé dans la section Urbanisme ci-dessous."
                ),
                "leviers": [],
            },
            "urbanisme": {
                "titre_source": "Stratégies de production urbaine résiliente de la commune de Ndiébène Gandiole",
                "titre_source_note": "Le document de Ndiébène Gandiole ne porte pas de titre « Programme de développement urbain durable » distinct comme les deux autres communes — le contenu équivalent existe sous cet intitulé différent, conservé tel quel plutôt que renommé.",
                "resume": (
                    "Territoire à forte interaction entre habitat, agriculture, zones humides et espaces "
                    "littoraux, exposé à des contraintes environnementales majeures (inondations saisonnières, "
                    "salinisation des sols). La stratégie vise à structurer l'urbanisation, consolider les noyaux "
                    "existants, organiser l'habitat diffus et encadrer les extensions futures, tout en préservant "
                    "les équilibres écologiques. Organisation en 4 niveaux hiérarchiques d'unités de voisinage, du "
                    "centre principal communal aux secteurs les plus périphériques."
                ),
                "leviers": [
                    "Densification contrôlée et restructuration du noyau ancien (centralité principale communale)",
                    "Hiérarchisation en 4 niveaux d'unités de voisinage selon centralité et densité",
                ],
            },
            "economie_societe": {
                "titre_source": "Programme de développement économique et social",
                "resume": (
                    "Positionnement comme pôle littoral écologique et productif, complémentaire de Saint-Louis et "
                    "Gandon. Double ambition économique (valoriser la pêche artisanale et l'agriculture vivrière, "
                    "développer la transformation agroalimentaire et halieutique, promouvoir l'écotourisme) et "
                    "sociale (accès équitable aux services essentiels, cohésion sociale, habitat, inclusion "
                    "territoriale)."
                ),
                "leviers": [
                    "Valorisation de la pêche artisanale et de l'agriculture vivrière",
                    "Développement de la transformation agroalimentaire et halieutique",
                    "Promotion du tourisme écologique et patrimonial",
                ],
            },
            "gouvernance": {
                "titre_source": "Programme de bonne gouvernance territoriale et institutionnelle - Commune de Ndiébène Gandiole",
                "resume": (
                    "Contexte marqué par une faible structuration institutionnelle, une dispersion des localités, "
                    "une forte dépendance aux ressources naturelles et une vulnérabilité accrue aux risques "
                    "climatiques. Objectif général : gouvernance territoriale inclusive, transparente et adaptée "
                    "aux réalités locales, garantissant une répartition équitable des investissements, en "
                    "particulier au profit des zones rurales et vulnérables."
                ),
                "leviers": [
                    "Mise en place d'un dispositif local de pilotage de la SVD/PCUI au niveau communal",
                    "Renforcement de la coordination avec Saint-Louis et Gandon pour les projets structurants",
                ],
            },
        },
    },
}
