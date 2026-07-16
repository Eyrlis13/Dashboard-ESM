# Règles d'arbitrage — Aides techniques (AT) (à appliquer à l'identique)

Ce document **fige** la façon de classer les aides techniques (AT) à la mobilité
travaillées pendant l'accompagnement ESM. Ces arbitrages sont **qualitatifs** :
ils se lisent dans le texte libre du **Plan d'accompagnement** (séances, résumés)
et du **Bilan de fin de suivi** (objectifs, atteinte, commentaires, synthèse).

> Ils ne sont **pas** automatisables de façon fiable : la nuance vit dans les
> formulations. La classification est donc faite par **lecture**, puis **validée**
> par l'équipe. Elle est stockée dans `at_curated.csv` (non versionné).

## Principe : un entonnoir, un seul statut par AT

Chaque AT est comptée **une seule fois**, à son **stade le plus avancé atteint** :

```
Préconisée  →  Essayée  →  Mise en place
(proposée)     (testée)     (acquise)
```

Une AT mise en place a forcément été essayée : on la compte alors en **« mise en
place »**, pas en « essayée ». De même une AT essayée a été préconisée : on la
compte en **« essayée »**.

## Les 3 statuts et leurs déclencheurs

| Statut | Définition | Indices dans le texte |
|---|---|---|
| **Mise en place** | Acquise / adoptée dans le quotidien | « acquisition », « acquis », « a acheté », « va le prendre », « laissé en prêt » (et gardé), « adopté », apparaît dans les AT utilisées **après** et pas avant |
| **Essayée** | Testée pendant le suivi, **mais non acquise** | « essai », « essayé », « testé », « mise en situation », « essai concluant » **sans** acquisition ; « envisage d'en acquérir » (= pas encore fait) → reste *essayée* |
| **Préconisée** | Proposée **mais même pas essayée** | « refus essai », « essais non souhaités », objectif « essayer… » → **Non atteint**, « découverte » / « a vu une vidéo » sans essai réel |

## Cas limites (trancher ainsi, sauf info plus récente)

- **« Essai concluant, envisage d'acheter »** → *essayée* (l'achat n'est pas encore
  réalisé au moment du bilan). Ex. le scooter électrique de plusieurs bénéficiaires.
- **« Laissé en prêt »** → *mise en place* (l'AT est en usage), même si l'adhésion
  reste fragile — à réévaluer au suivi 6 mois.
- **AT déjà utilisée avant l'ESM** (canne, déambulateur pré-existants) → **ne pas**
  la compter comme « mise en place par l'ESM » ; seule une AT **nouvelle** compte.
- **Refus par l'entourage** (« décision des enfants ») → *préconisée* (non aboutie).

## Champs produits (dans `dataset.json`, par bénéficiaire)

`at` : liste de `{ "type": "...", "statut": "mise_en_place|essayee|preconisee" }`.

Types normalisés rencontrés : Déambulateur / rollator · Canne · Canne-siège / chariot
· Scooter électrique · Vélo tricycle · Bâtons de marche · Compteur de pas ·
Aide aux transferts (coussin / poignée). Ajouter au besoin, en restant cohérent.

## Procédure à chaque nouveau lot de bilans

1. Lire le Plan d'accompagnement + le Bilan de fin des **nouveaux** bilans.
2. Proposer la classification (AT + statut) **avec la phrase source** à l'appui.
3. Faire **valider** par l'équipe (l'ergo qui a rédigé le bilan est la référence).
4. Ajouter les lignes validées à `at_curated.csv`, régénérer, vérifier, publier.

> À terme, un **formulaire de saisie** (statut choisi dans un menu par l'ergo)
> supprimerait cet arbitrage a posteriori : la donnée serait propre à la source.

_Dernière mise à jour : juillet 2026._
