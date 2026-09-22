# Règles d'arbitrage — Services & orientations de mobilité (à appliquer à l'identique)

Ce document **fige** la façon de classer les **redirections vers un service** de mobilité
travaillées pendant l'accompagnement ESM. Il est le pendant de `REGLES_AIDES_TECHNIQUES.md` :
l'un compte le **matériel**, l'autre compte les **solutions humaines et organisationnelles**.

> Pourquoi les séparer : une AT acquise et une orientation qui aboutit ne se travaillent pas
> pareil et ne coûtent pas pareil. Les mélanger rendrait les deux compteurs illisibles.
> Un bénéficiaire peut très bien repartir sans aucune AT mais avec un accompagnement
> bénévole hebdomadaire — c'est un résultat de l'ESM à part entière.

## Principe : un entonnoir, un seul statut par service

Chaque service est compté **une seule fois**, à son **stade le plus avancé atteint** :

```
Présentée   →   Engagée        →   Effective
(info)          (démarche)         (en place et utilisé)
```

Ce vocabulaire reprend celui des bilans eux-mêmes, qui cotent les solutions en
**Découverte → En cours → Acquis** dans l'onglet « Bilan fin de suivi ».

## Les 3 statuts et leurs déclencheurs

| Statut | Définition | Indices dans le texte |
|---|---|---|
| **Effective** | Le service est en place et utilisé | « Acquis », « validé », « mis en place », objectif correspondant **Atteint**, usage constaté (« utilise de nouveau seule les transports en commun »), verbatim de réussite |
| **Engagée** | Démarche entamée, usage **pas encore installé** | « dossier créé / déposé », « inscription », « s'est inscrite mais pas encore essayé », « En cours », « Essai » du dispositif, contact pris avec le prestataire |
| **Présentée** | Information donnée, **sans démarche derrière** | « Découverte », « présentation des solutions », « a vu une vidéo », « connaît le dispositif mais ne se sent pas apte », refus avant toute démarche, non-éligibilité |

## Types normalisés

Regrouper au niveau du **type de solution**, pas de la marque locale — sinon chaque
territoire crée ses propres catégories et les chiffres ne s'additionnent plus.

| Type retenu | Ce qu'il regroupe |
|---|---|
| **Sortir Plus** | forfait Sortir Plus / Sortir + (dispositif national, souvent cité seul) |
| **Transport à la demande** | TAD d'agglo (Azalys, REMI, Résa'bus), AIMV, conciergerie communale |
| **Transports en commun (réassurance)** | bus, tram, train — accompagnement et mise en situation |
| **Application d'aide au déplacement** | Mon Guide Fil Bleu / Fil Blanc, City Mapper, Accès Plus, SNCF Connect, géolocalisation |
| **Accompagnement par un tiers / bénévole** | assos (Valentin Haüy, P'Roche de vous), Unis-Cité / service civique, SAD, service résidence |
| **Covoiturage** | BlaBlaCar, covoiturage famille / voisins |
| **Taxi / VTC** | taxi, VSL hors prescription |

Ajouter un type au besoin, en restant à ce niveau de granularité.

## Cas limites (trancher ainsi, sauf info plus récente)

- **Dossier déposé mais service jamais utilisé** → *engagée*, jamais *effective*.
  C'est précisément l'écart qu'on veut pouvoir mesurer.
- **Échec de l'essai puis refus de poursuivre** → reste *engagée* (la démarche a bien eu
  lieu) ; le refus se lit dans le commentaire, pas dans le statut.
- **Non-éligibilité** (ex. Sortir Plus refusé faute d'avoir 75 ans) → *présentée*.
  L'orientation a été travaillée mais n'a pas pu s'engager.
- **Service acté avec l'aidant** plutôt qu'avec le bénéficiaire (troubles cognitifs) →
  *effective* si l'objectif correspondant est coté **Atteint**.
- **Décidé, démarrage prévu après le bilan** (ex. intervenants attendus le mois suivant)
  → *effective* si le bilan écrit « a été mis en place » — à reconfirmer au suivi 6 mois.
- **Un « refus » dans une phrase à rallonge** : vérifier **à quoi il se rattache** avant
  de dégrader un statut. Les commentaires de bilan enchaînent les solutions sans
  ponctuation (« Service transport à la demande validé covoiturage refus essai tricycle
  et parking relais ») : ici le refus porte sur le **tricycle**, pas sur le covoiturage.
  Recouper avec le Plan d'accompagnement, qui écrit la même chose en clair.
- **Croiser avec la grille « Modes de déplacements après »** : c'est la preuve d'usage la
  plus fiable. Un mode qui apparaît **après et pas avant**, sur une ligne de trajet
  précise, vaut *effective* même si le texte libre reste flou.
- **Solution évoquée « pour plus tard »** (« envisage le taxi dans le futur ») → *présentée*.
- **Démarches de droits** (dossier APA, MDPH) → **ne pas compter** : ce sont des
  financements, pas des solutions de mobilité.
- **Une AT n'est jamais un service** et inversement. Le disque pivotant va dans
  `at_curated.csv`, Sortir Plus dans `services_curated.csv`.

## Champs produits (dans `dataset.json`, par bénéficiaire)

`services` : liste de `{ "service": "...", "statut": "effective|engagee|presentee" }`.

Dans `resultats_anonymises.csv` : `services_effectifs`, `services_engages`,
`services_presentes`, `services_detail`.

## Procédure à chaque nouveau lot de bilans

1. Lire le **Plan d'accompagnement** (comptes rendus de séance) + le **Bilan de fin de
   suivi** (objectifs + cotation, lignes « Solution N » et leur niveau d'acquisition).
2. Proposer la classification **avec la phrase source** à l'appui.
3. Faire **valider** par l'équipe (l'ergo qui a rédigé le bilan est la référence).
4. Ajouter les lignes validées à `services_curated.csv`, régénérer, vérifier, publier.

### Format de `services_curated.csv` (non versionné)

```
cle,service,statut,source
STOLL,Sortir Plus,effective,« Solution 1 : Sortir Plus » = Acquis
```

La colonne **`source`** garde la phrase du bilan qui justifie l'arbitrage. Elle sert
uniquement à la relecture humaine : **elle n'est pas exportée dans `dataset.json`**,
donc elle ne sort jamais du poste de travail.

_Dernière mise à jour : septembre 2026._
