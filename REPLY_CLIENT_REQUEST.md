# Demande de compléments — Site SIG Saint-Louis

Note à l'attention de l'ADM / COMETE International

---

## 1. État d'avancement

Nous vous remercions pour l'ensemble des documents et données transmis. Voici où en est le site à ce jour :

- Le **Diagnostic** a été réorganisé par commune (Saint-Louis, Gandon, Ndiébène Gandiol), avec des cartes et des données propres à chaque territoire.
- Le contenu de la **SVD** (vision, principes directeurs, axes stratégiques, programmes de développement) a été intégré à partir des trois rapports SVD que vous nous avez transmis.
- L'ensemble des couches SIG que vous nous avez fournies et qui étaient exploitables ont été intégrées (occupation du sol, topographie, peuplement, zones de conservation, activités économiques, énergie, etc.).
- La section **PCU/PCUI** a été préparée avec la structure attendue (rapport de présentation, zonage, PIP, règlement, EES, atlas). Sa finalisation dépend cependant de documents complémentaires que nous n'avons pas encore reçus — détaillés ci-dessous.

L'objet de cette note est de lister précisément ce qu'il nous reste à recevoir ou à faire confirmer afin de finaliser le site.

---

## 2. Données et documents nécessaires

### A. PCU/PCUI — Rapport de présentation

Nous aurions besoin du rapport de présentation officiel du PCU/PCUI (version finale ou dernière version validée), pour :
- Saint-Louis
- Gandon
- Ndiébène Gandiol

Si ce rapport est unique et intercommunal plutôt que réalisé par commune, merci de nous le préciser.

Formats acceptés : PDF ou DOCX.

### B. Zonage PCU/PCUI

Nous aurions besoin des données de zonage officiel et validé, avec si possible :
- les fichiers de zonage (shapefile, GeoPackage ou GeoJSON) ;
- la nomenclature des zones ;
- la légende / symbologie associée, si elle existe ;
- la définition de chaque code de zone ;
- la commune ou le périmètre concerné ;
- le système de projection utilisé.

Nous travaillons avec le système EPSG:32628 / WGS 84 UTM Zone 28N, qui est aussi celui que vous nous avez confirmé comme officiel. Une autre projection ne pose pas de problème si elle est correctement identifiée — nous pourrons la convertir.

Point important à confirmer : la couche « Zone d'extension » actuellement disponible pour Gandon correspond-elle à une simple proposition d'orientation, ou fait-elle partie d'un zonage PCU/PCUI déjà approuvé ? Nous ne l'avons pas présentée comme un zonage officiel en l'absence de cette confirmation.

### C. PIP — Programme d'Investissement Prioritaire

Nous avons repéré, dans les rapports SVD, des tableaux de projets structurants classés par ordre de priorité, et nous les avons intégrés à titre provisoire dans la section PIP du site.

Afin de disposer d'un PIP officiel, merci de nous transmettre le tableau réel dont vous disposez, avec les champs disponibles parmi (liste non obligatoire — merci de nous envoyer ce qui existe, même incomplet) :
- intitulé du projet ;
- commune ;
- secteur ;
- localisation ;
- priorité ;
- coût estimatif ;
- calendrier ;
- maître d'ouvrage / responsable ;
- statut.

Formats acceptés : XLSX, CSV, DOCX ou PDF.

### D. Règlement d'urbanisme

Merci de nous transmettre le ou les documents de règlement d'urbanisme officiels. Merci de préciser s'il s'agit :
- d'un règlement intercommunal unique, ou
- d'un règlement propre à chaque commune.

Format préféré : PDF ou DOCX.

### E. Évaluation environnementale stratégique (EES)

Merci de nous transmettre la version finale/la plus récente de l'EES, ainsi que ses annexes et cartes associées si elles existent. Merci de préciser si l'EES est intercommunale ou propre à chaque commune.

### F. Atlas cartographique

Merci de nous transmettre l'atlas cartographique officiel du PCU/PCUI, de préférence au format PDF.

Si aucun atlas consolidé n'existe à ce jour, merci de nous confirmer si vous souhaitez qu'à titre d'alternative, le site rassemble des liens vers les cartes thématiques déjà validées individuellement. Nous ne mettrons pas en place cette alternative sans votre confirmation.

### G. Servitudes / contraintes réglementaires

Merci de nous transmettre, si elles existent, les couches SIG officielles concernant :
- les servitudes ;
- les reculs et emprises réglementaires ;
- les corridors protégés ;
- les zones de passage / droits de passage ;
- les restrictions liées aux zones inondables ;
- les périmètres de protection d'infrastructures ;
- toute autre contrainte réglementaire.

Merci d'y joindre la légende et la signification de chaque classe.

### H. ZAC / ZAD

Merci de nous transmettre, si elles existent et font partie du PCU/PCUI approuvé, les documents ou couches SIG relatives aux ZAC (zones d'aménagement concerté) ou ZAD (zones d'aménagement différé).

Pour information : les couches ZAPA/ZAPE/ZP déjà livrées ne sont pas présentées sur le site comme des ZAC/ZAD, leurs attributs ne permettant pas d'établir cette équivalence (elles correspondent en réalité à des catégories d'occupation du sol).

### I. Bassins versants

Cette thématique a été demandée mais aucune couche de bassins versants ne nous a été transmise à ce jour.
- Une couche officielle de bassins versants existe-t-elle déjà ? Si oui, merci de nous la transmettre.
- Si non, souhaitez-vous que nous la produisions à partir du MNT déjà fourni ? Nous ne le ferons pas sans votre accord préalable, ce type de traitement pouvant nécessiter des choix méthodologiques à valider avec vous.

### J. Autres compléments SIG en attente

Les éléments suivants restent à ce jour non résolus :
- Données d'équipements socio-économiques pour **Gandon** (le dossier transmis pour cette commune est vide, contrairement à celui de Ndiébène Gandiol) ;
- Population de 7 quartiers de Ndiébène Gandiol non renseignée dans le fichier transmis ;
- Couverture énergétique pour Saint-Louis et Ndiébène Gandiol (les seules données disponibles concernent Gandon) ;
- Couches d'activités économiques pour Saint-Louis, si elles existent ;
- Une nouvelle exportation du fichier « Boucle de Gandiolais » : le fichier transmis semble incomplet et nécessite une nouvelle exportation ;
- Une nouvelle exportation complète du fichier « CN_10m » (courbes de niveau), pour la même raison ;
- Confirmation du jeu de données d'empreinte urbaine à considérer comme référence (plusieurs versions semblent coexister pour 2024/2025).

### K. Carte interactive — remarques reçues

Vos remarques sur la carte interactive ont bien été prises en compte : dégradé rouge pour l'évolution urbaine (2017 au premier plan, 2020 intermédiaire, 2024 en arrière-plan), ajout des rubriques Occupation du sol, Relief et Équipements, et ajout de filtres pour les cartes de risque d'inondation (par Catégorie) et de vulnérabilité (par Indice). Ces éléments sont intégrés sur `/carte/` — voir `CLIENT_INTERACTIVE_MAP_REMARKS_REPORT.md` pour le détail technique complet.

Certaines couches demandées peuvent être produites directement à partir des données déjà transmises. C'est notamment le cas de plusieurs produits liés au relief (ombrage, pente, classes d'altitude, courbes de niveau et, sous réserve de validation méthodologique, bassins versants à partir du MNT). Ces éléments ne nécessitent donc pas nécessairement un nouveau fichier de votre part.

En revanche, les informations ayant une valeur officielle, réglementaire ou attributaire qui n'est pas présente dans les données disponibles ne seront pas reconstituées. Elles devront être transmises ou confirmées par vos soins — notamment : les équipements manquants de Gandon, les populations manquantes, le zonage réglementaire, les servitudes et les documents PCU/PCUI.

**Déjà disponible / intégré sur la carte interactive :**
- Occupation du sol 2020 (17 catégories, style et légende par catégorie) ;
- Relief ombré et courbes de niveau 5 m (dérivés du MNT que vous avez transmis) ;
- Équipements (santé, éducation, culture, économie/tourisme, sport) — jeu de données intercommunal existant, non structuré de façon fiable par commune à ce jour ;
- Risque d'inondation et Vulnérabilité, désormais avec filtres interactifs (Catégorie / Indice).

**Produit à partir des données existantes, sous réserve de validation méthodologique si nécessaire :**
- Pente et classes d'altitude (à partir du MNT) — pas encore produites, réalisables sur demande ;
- Bassins versants (à partir du MNT) — voir point I ci-dessus, ne sera pas produit sans votre accord préalable.

**Données toujours nécessaires de la part du client pour la carte interactive :**
- Jeu de données équipements dédié à Gandon (dossier transmis actuellement vide) ;
- Confirmation du jeu de données d'empreinte urbaine faisant référence pour 2024/2025 (voir point J).

### L. Carte de la Topographie — absence de données visibles à l'écran

Vous nous avez signalé que la carte de la rubrique Topographie n'affichait aucune donnée visible malgré des couches cochées, et vous avez demandé pourquoi la couche « Courbes de niveau 5 m » portait la mention « (nouvelle donnée) ».

Ces deux points sont désormais réglés :
- Il s'agissait d'un problème d'affichage (bug technique), pas d'un manque de données : le relief ombré, les courbes de niveau et les courbes de niveau 5 m que vous avez déjà transmis (ou pour lesquels le relief a été calculé à partir du MNT que vous avez transmis) s'affichent maintenant correctement.
- La mention « (nouvelle donnée) » a été retirée du libellé public de cette couche.

**Aucune nouvelle donnée n'est nécessaire de votre part pour ce point.** Les données existantes étaient suffisantes ; seul l'affichage devait être corrigé.

Par ailleurs, en vérifiant les deux couches de courbes de niveau, nous avons constaté qu'elles utilisent en réalité le même pas altimétrique (5 m), alors qu'elles proviennent de deux sources distinctes (l'ancienne couche historique du site et la nouvelle couche que vous avez transmise). Elles semblent donc en partie redondantes. Nous n'avons rien supprimé à ce stade ; merci de nous confirmer si vous souhaitez que nous conservions les deux couches ou que nous n'en gardions qu'une seule.

Enfin, deux jeux de données que vous nous avez transmis récemment (bâti et quartiers de Saint-Louis avec population) ont été examinés : ils ne concernent pas la Topographie et seront traités dans le cadre d'une prochaine remarque (habitat/bâti et population/quartiers).

### M. Occupation du sol — case « 2020 » confuse retirée

Vous nous avez signalé que la case « Occupation du sol 2020 (nouvelle donnée) », avec sa légende de 17 classes non cliquables, créait de la confusion à côté des couches existantes.

Plutôt que de supprimer les données 2020 (valides et déjà validées), nous avons choisi de les rendre utilisables : chacune des 17 classes est désormais une case à cocher indépendante, avec sa propre couleur, regroupée sous un intitulé dépliable « Occupation du sol — 2020 » (avec des liens « Tout afficher » / « Tout masquer »), séparé des couches existantes. La mention « (nouvelle donnée) » a été retirée. Une seule et même donnée source est utilisée (aucun fichier dupliqué), chargée une seule fois même si plusieurs classes sont affichées en même temps.

**Aucune nouvelle donnée n'est nécessaire de votre part pour ce point.**

Les jeux de données bâti et quartiers de Saint-Louis (voir point L) ont de nouveau été examinés pour cette remarque : ils ne contiennent aucun attribut de type occupation du sol et ne concernent donc pas cette rubrique non plus.

### N. Couleurs de l'évolution urbaine — intensité inversée + lotissements en noir

Vous nous avez demandé d'inverser l'intensité des couleurs de l'évolution urbaine (rouge clair pour 2017, rouge intermédiaire pour 2020, rouge foncé pour 2024) et d'afficher les lotissements planifiés en noir.

C'est fait, sur toutes les pages concernées (`/carte/`, Diagnostic → Urbanisation, et les 3 communes) : Empreinte 2017 en rouge clair, Empreinte 2020 en rouge intermédiaire, Empreinte 2024 en rouge foncé, Lotissements planifiés en noir. L'ordre d'affichage des couches (2017 au premier plan, 2020 au milieu, 2024 en arrière-plan) que vous aviez demandé précédemment a été conservé à l'identique — seule l'intensité des couleurs a changé, pas l'empilement des couches.

**Aucune nouvelle donnée n'est nécessaire de votre part pour ce point.**

### O. Cartes officielles ajoutées à la rubrique Risques naturels

Vous avez signalé que la rubrique Risques naturels ne montrait pas de carte, contrairement aux autres rubriques du diagnostic. Les deux cartes officielles que vous avez transmises (dossier « Cartographie inondation et vulnérabilité ») sont maintenant affichées dans cette rubrique, en plus des couches interactives déjà en place :
- **Carte du risque d'inondation** (carte des aléas naturels — hauteur de submersion pour crue centennale, avec les zones d'érosion côtière également représentées sur le même document) ;
- **Carte de vulnérabilité**.

Chaque carte est affichable en grand, téléchargeable au format PDF d'origine, et reliée à la carte interactive correspondante.

**RECEIVED / INTEGRATED — aucune nouvelle donnée n'est nécessaire de votre part pour ce point.**

### P. Peuplement — quartiers de Saint-Louis et bâtiments (données client)

Conformément à votre demande, la rubrique Peuplement a été mise à jour avec les données que vous avez transmises :
- **Quartiers — Saint-Louis** : remplacés par votre nouvelle couche `quartier_saint_louis`, affichée en implantation ponctuelle (un point par quartier), au même format que Gandon et Ndiébène Gandiol ;
- **Bâtiments** : la couche « Localités / villages (sans nom) » a été retirée et remplacée par votre couche `bati.shp` (15 481 empreintes bâties pour Saint-Louis).

**RECEIVED / INTEGRATED — aucune nouvelle donnée n'est nécessaire de votre part pour ce point.**

Par conséquent, notre demande précédente concernant les noms des 372 localités/villages est retirée : cette couche n'est plus utilisée dans la rubrique Peuplement (remplacée par les bâtiments ci-dessus) et ne bloque donc plus rien sur le site actuellement. Si vous souhaitez malgré tout que nous l'intégrions ailleurs à l'avenir, les noms resteront utiles le cas échéant.

### Q. Nom affiché dans le bandeau du site

Vous avez demandé de remplacer « SIG Saint-Louis », affiché en haut à gauche du site, par un intitulé reflétant mieux la portée intercommunale du projet. Le bandeau (et le pied de page) affichent désormais **« SIG WEB Interactif »**, sur toutes les pages. Le grand titre de la page d'accueil (déjà validé avec vous précédemment) n'a pas été modifié — seul ce petit intitulé d'en-tête a changé.

**RECEIVED / INTEGRATED — aucune nouvelle donnée n'est nécessaire de votre part pour ce point.**

---

## 3. Compléments simples attendus pour le site (textes/visuels)

Le titre de la page d'accueil, son texte d'introduction et le nouveau libellé remplaçant « Thèmes du diagnostic » (désormais « Thèmes des plans intercommunaux ») nous ont déjà été communiqués et sont intégrés sur le site — inutile de nous les retransmettre. Les deux nouvelles rubriques demandées (« Développement économique & énergie » et « Gouvernance et intercommunalité ») ont également été intégrées à la page d'accueil et au diagnostic.

Les logos Sénégal, ADM, COMETE et RINA sont désormais tous intégrés et réordonnés dans le pied de page.

Il reste à ce jour à confirmer :
- Symbole exact à retirer de la carte des équipements ;
- La phrase « Ajouter aussi à la rubrique urbanisation » : son sens précis ne nous permet pas encore d'identifier ce qui doit être ajouté à cette rubrique. Merci de préciser ce qui devrait y être ajouté (donnée, carte, texte ou lien).

Par ailleurs, la palette de couleurs (bleu, 3 niveaux de contraste, sans transparence) a déjà été appliquée aux couches d'évolution urbaine à titre de proposition. Merci de nous confirmer si cette proposition vous convient ou si une autre teinte est souhaitée.

---

## 4. Fonctionnalités SIG avancées

Vous avez mentionné le souhait de disposer de fonctionnalités proches de celles d'ArcGIS/QGIS. Avant de développer quoi que ce soit dans ce sens, merci de bien vouloir indiquer, pour chacune des fonctions suivantes, si elle est :

**Nécessaire** / **Optionnelle** / **Non requise**

| Fonctionnalité | Nécessaire | Optionnelle | Non requise |
|---|---|---|---|
| Recherche d'un quartier / d'une zone | | | |
| Consultation des attributs d'une couche | | | |
| Sélection/activation de couches | | | |
| Zone tampon (buffer) | | | |
| Analyse de zones de servitude | | | |
| Intersection spatiale entre couches | | | |
| Export de données sélectionnées | | | |
| Téléchargement des couches SIG | | | |
| Outils de dessin / édition | | | |

À titre indicatif, les fonctions de recherche, de consultation et de sélection de couches reposent sur une technologie simple déjà utilisée sur le site. Les fonctions d'analyse spatiale avancée (buffer, intersection, servitudes) impliquent en revanche des choix techniques plus lourds, qu'il est préférable de cadrer précisément avec vous avant de les entreprendre.

---

## 5. Priorisation

Afin d'organiser la suite des travaux, merci de classer les chantiers suivants par ordre de priorité :

1. Finalisation du contenu PCU/PCUI
2. Complément des couches SIG manquantes
3. Fonctionnalités SIG avancées
4. Bilinguisme français/wolof
5. Optimisation mobile / application web progressive (PWA)
6. Tableau de bord statistique

---

## 6. Tableau récapitulatif

| Élément | Statut actuel | Donnée demandée | Priorité |
|---|---|---|---|
| Diagnostic par commune | Intégré | — | — |
| SVD (vision, axes, programmes) | Intégré | — | — |
| Occupation du sol 2020, MNT, topographie | Intégré | — | — |
| Peuplement (quartiers, bâtiments) | Intégré (partiel pour Ndiébène Gandiol) | Population de 7 quartiers de Ndiébène Gandiol | À confirmer |
| Carte interactive — remarques (palette rouge, rubriques, filtres) | Intégré | Jeu de données équipements pour Gandon | — |
| Carte Topographie — affichage corrigé, libellé « nouvelle donnée » retiré | Intégré | Confirmation souhaitée : conserver les 2 couches de courbes de niveau (même pas de 5 m) ou n'en garder qu'une | Optionnelle |
| Occupation du sol 2020 — 17 classes sélectionnables séparément, libellé « nouvelle donnée » retiré | Intégré | — | — |
| Évolution urbaine — intensité des couleurs inversée (2017 clair → 2024 foncé), lotissements planifiés en noir | Intégré | — | — |
| Cartes officielles Inondation + Vulnérabilité — ajoutées à la rubrique Risques naturels | Intégré | — | — |
| Quartiers Saint-Louis (points) + Bâtiments — données client intégrées, ancienne couche Localités retirée | Intégré | — | — |
| Bandeau du site — « SIG Saint-Louis » remplacé par « SIG WEB Interactif » | Intégré | — | — |
| Énergie / activités économiques | Partiel (Gandon et Ndiébène Gandiol uniquement) | Données pour Saint-Louis ; couverture énergétique élargie | À confirmer |
| Rapport de présentation PCU/PCUI | En attente | Document officiel (3 communes) | À confirmer |
| Zonage PCU/PCUI | Partiel (Gandon uniquement, non approuvé) | Zonage officiel validé + confirmation du statut de la couche Gandon | À confirmer |
| PIP | Partiel (issu des tableaux SVD) | Tableau PIP officiel | À confirmer |
| Règlement d'urbanisme | En attente | Document officiel | À confirmer |
| EES | En attente | Rapport officiel | À confirmer |
| Atlas cartographique | En attente | Document officiel ou confirmation d'une alternative | À confirmer |
| Servitudes / contraintes | En attente | Couches SIG officielles | À confirmer |
| ZAC / ZAD | En attente | Documents/couches officiels si applicable | À confirmer |
| Bassins versants | En attente | Couche officielle ou accord pour dérivation du MNT | À confirmer |
| Textes du site (titre, introduction, libellé, nouvelles rubriques) | Reçus, intégrés | — | — |
| Logos partenaires (Sénégal, ADM, COMETE, RINA) | Reçus, intégrés | — | — |
| Visuel du site (symbole équipements) | En attente | Précision du symbole à retirer | À confirmer |
| Rubrique urbanisation (« Ajouter aussi à la rubrique urbanisation ») | Sens à préciser | Préciser ce qui doit être ajouté | À confirmer |
| Fonctionnalités SIG avancées | Non commencé | Confirmation du périmètre requis | À confirmer |

---

## Prochaine étape proposée

Dès réception des éléments ci-dessus :
1. Le contenu du PCU/PCUI sera complété pour les trois communes.
2. Les couches SIG restantes seront intégrées.
3. Les fonctionnalités avancées demandées seront développées selon le périmètre que vous aurez confirmé.
4. Une dernière phase de validation et de livraison sera réalisée avec vous.

Nous restons à votre disposition pour toute précision.

---

`CLIENT DATA REQUEST READY FOR REVIEW`
