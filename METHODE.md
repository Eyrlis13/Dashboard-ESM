# METHODE.md — informations de méthode à joindre à toute présentation des résultats

Ce document rassemble les éléments de cadrage qu'un lecteur extérieur demandera avant
d'accepter les chiffres. **Il est volontairement incomplet** : les points marqués
« À COMPLÉTER » ne sont pas dans les fichiers actuels et ne doivent pas être devinés.

## Ce qui est établi

### Taille et composition de la cohorte
**23 parcours.** Un bilan = un bénéficiaire. Deux dossiers nommés « REFUS » ont été
exclus : la personne n'est pas entrée dans l'accompagnement. Aucune autre exclusion.

### Qui apprécie l'atteinte des objectifs
**L'ergothérapeute qui a conduit l'accompagnement**, dans la colonne « ATTEINTE DES
OBJECTIFS » de l'onglet « Bilan fin de suivi » de son propre bilan.

> ⚠️ C'est une **auto-évaluation par le professionnel intervenant**, pas une évaluation
> indépendante. C'est la limite méthodologique la plus importante du dispositif et elle
> doit être énoncée telle quelle : l'atteinte des objectifs n'est pas un critère mesuré,
> c'est un jugement professionnel. Les scores FES-I, eux, sont des mesures
> instrumentées (échelle validée, Kempen 2008).

Les classements d'aides techniques et de services sont, eux, des **relectures a
posteriori** du texte libre des bilans, faites selon des règles écrites
(`REGLES_AIDES_TECHNIQUES.md`, `REGLES_SERVICES.md`) et validées par l'équipe. Chaque
décision est tracée avec sa phrase source dans `audit_arbitrages.csv`.

### Ce qui est mesuré vs jugé

| Indicateur | Nature |
|---|---|
| Score FES-I (7 items, 7-28) | **Mesure** — échelle validée |
| Item FES-I « Sortir » | **Mesure** — item de la même échelle |
| Modes de déplacement | **Relevé** — grille de trajets renseignée par l'ergothérapeute |
| Ressentis (4 échelles 0-10) | **Déclaratif** du bénéficiaire, converti selon des règles fixes |
| Atteinte des objectifs | **Jugement** de l'ergothérapeute intervenante |
| AT / services et leur statut | **Relecture** a posteriori du texte libre, selon règles écrites |

## À COMPLÉTER — extractible des bilans au prochain lot

Ces informations existent dans les fichiers sources mais ne sont pas encore remontées
dans le dataset. Elles seront ajoutées au prochain passage sur le dossier `bilans/`.

- **Période couverte** : date du premier entretien et date du bilan de fin, par dossier.
  Les bilans portent ces dates (« J'ai rencontré le 02/05/2025… », dates des lignes
  « Solution »). À agréger en date de début / date de fin de cohorte.
- **Durée de chaque parcours** : écart entre le premier entretien et le bilan de fin.
- **Nombre de séances réalisées** : l'onglet « Plan d'accompagnement » comporte un bloc
  « PROGRAMME » avec les séances et leur intervenant.

## À COMPLÉTER — seule l'équipe ESM peut répondre

- **Exhaustivité.** Les 23 parcours sont-ils **tous** les accompagnements ESM terminés
  sur la période, ou une sélection ? Cette réponse n'est pas dans les fichiers. Elle est
  décisive : une sélection, même involontaire, change la portée de tous les résultats.
  Si l'ensemble est exhaustif, il faut pouvoir le dire ; sinon il faut dire sur quel
  critère les dossiers ont été retenus, et combien d'accompagnements existaient au total.
- **Dénominateur réel de l'expérimentation** : combien de personnes ont été orientées
  vers l'ESM, combien ont refusé, combien sont encore en cours ? Les 23 sont des parcours
  **terminés** : ils ne disent rien du taux d'adhésion ni des abandons.
- **Comparaison** : il n'y a **pas de groupe témoin**. Les évolutions observées ne peuvent
  pas être attribuées causalement à l'ESM — elles décrivent ce qui s'est passé pendant
  l'accompagnement, pas ce qui se serait passé sans lui. À énoncer explicitement.

## Formulation prudente du résultat central

> Sur les 23 parcours ESM terminés, **15 personnes (65 %) repartent avec au moins une
> solution de mobilité effectivement en place** : 9 avec une aide technique acquise,
> 8 avec une orientation vers un service aboutie, 2 avec les deux.

Ce qu'il ne faut PAS en dire : que l'ESM en est la cause (pas de groupe témoin), ni que
les 8 autres n'ont rien retiré de l'accompagnement — plusieurs ont essayé du matériel ou
engagé des démarches sans aboutir, ce que les statuts « essayée » et « engagée » comptent
séparément.
