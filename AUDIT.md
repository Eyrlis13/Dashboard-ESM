# AUDIT.md — remonter n'importe quel chiffre jusqu'à sa source

Ce document répond à une question : **si quelqu'un conteste un chiffre du dashboard,
comment prouve-t-on d'où il vient ?**

## Les trois niveaux de preuve

| Niveau | Fichier | Versionné ? | Ce qu'il prouve |
|---|---|---|---|
| 1. Résultat publié | `dataset.json`, `resultats_anonymises.csv` | ✅ oui | Le chiffre affiché |
| 2. Décision qualitative | `audit_arbitrages.csv` | ✅ oui | Pourquoi chaque AT / service est classé ainsi, **avec la phrase du bilan** |
| 3. Donnée source | `bilans/*.xlsx`, `at_curated.csv`, `services_curated.csv` | ❌ non (nominatif) | La donnée brute, consultable sur place uniquement |

Les niveaux 1 et 2 sont publics et suffisent à vérifier **la méthode et la cohérence**.
Le niveau 3 est nécessaire pour vérifier **les valeurs elles-mêmes**, et ne sort pas du
poste de travail : c'est une donnée de santé nominative.

## Remonter un chiffre, cas par cas

### « D'où vient ce score FES-I ? »
`resultats_anonymises.csv` → colonnes `fesi_avant`, `fesi_apres`, `fesi_delta` pour le
bénéficiaire N°x. La règle de calcul est dans `REGLES_ARBITRAGE` (ligne « FES-I /
Score ») : somme des 7 items de la Short FES-I, chacun coté 1 à 4, score 7-28.
Sur place : onglets « FES-I avant » / « FES-I après » du bilan.

**Attention au sens :** un Δ **négatif** est une amélioration (moins de peur).

### « D'où vient cette moyenne de ressenti ? »
`resultats_anonymises.csv` → colonnes `ressenti_<dimension>_avant` / `_apres`.
Les moyennes d'évolution ne portent que sur les **paires complètes** (score avant ET
après pour cette dimension) : les dénominateurs ne sont donc pas 23. Les conversions
depuis le format Excel (échelle, niveaux qualitatifs, fourchette, adjectif) sont dans
`REGLES_RESSENTIS.md`.

**Attention au sens :** ici un Δ **positif** est une amélioration. La crainte de chuter
est affichée inversée, sous le nom « confiance face à la chute ».

### « Pourquoi cette aide technique est-elle comptée comme mise en place ? »
`audit_arbitrages.csv` → ligne (`id_anonyme`, `domaine`, `libelle`) : elle porte le
`statut` et la `phrase_source`, c'est-à-dire la phrase du bilan qui a justifié la
décision. La grille de décision est dans `REGLES_AIDES_TECHNIQUES.md`.

### « Pourquoi cette orientation est-elle comptée comme effective ? »
Même chose, domaine `Service`, grille dans `REGLES_SERVICES.md`.

### « D'où vient le résultat central, 15 bénéficiaires sur 23 ? »
`resultats_anonymises.csv` → colonne `solution_mise_en_place` (oui/non). Définition :
**au moins une aide technique acquise OU au moins un service effectif**. Décomposition
recalculable depuis les colonnes `at_mises_en_place` et `services_effectifs` :
9 avec une AT acquise + 8 avec un service effectif − 2 ayant les deux = **15**.
Le détail nominatif de chaque décision est dans `audit_arbitrages.csv`.

### « D'où vient l'évolution sur les sorties sociales ? »
`resultats_anonymises.csv` → colonnes `fesi_sortir_avant`, `fesi_sortir_apres`,
`fesi_sortir_delta`. C'est l'item « Sortir (service religieux, réunion de famille…) »
de la Short FES-I, coté 1 (pas du tout inquiet) à 4 (très inquiet).
**Δ négatif = amélioration.** 23 paires complètes.

### « D'où vient le report modal ? »
`resultats_anonymises.csv` → colonnes `mode_<catégorie>_avant` / `_apres`, plus
`trajets_avant` / `trajets_apres` pour refaire les pourcentages, et
`deplacements_apres_reporte` qui signale les 4 grilles « après » non re-saisies
(reportées depuis l'avant car notées inchangées par l'ergothérapeute).
Les évolutions s'expriment en **points de pourcentage**, pas en nombre de trajets :
le total de trajets renseignés n'est pas le même avant et après.

### « Qui est le bénéficiaire N°7 ? »
Impossible depuis les fichiers publiés : c'est volontaire. Le rapprochement se fait sur
place, à partir de `at_curated.csv` / `services_curated.csv`, qui sont indexés par nom
de dossier. L'ID anonyme est attribué par ordre alphabétique des dossiers présents.

> ⚠️ **L'ID anonyme n'est pas stable dans le temps.** Il se décale quand un bilan entre
> ou sort de la cohorte. Un audit doit donc travailler sur **une génération datée** :
> noter le commit du dépôt, ou la date de génération du journal.

## Les contrôles automatiques

| Commande | Ce qu'elle garantit | Bloquante ? |
|---|---|---|
| `python3 verify_anon.py` | Aucun nom, mail ou téléphone dans les fichiers publiés. Recoupe avec les vrais noms extraits des bilans | ✅ oui (`maj.sh` ne publie rien si elle échoue) |
| `python3 journal_audit.py` | Les décisions du dataset publié correspondent **exactement** aux fichiers d'arbitrage | ✅ oui (code 1 en cas de divergence) |
| `python3 test_coherence.py` | Les agrégats n'ont pas bougé sans raison depuis la dernière validation | ✅ oui |
| `python3 etat_traitement.py` | Aucun dossier n'a été oublié à l'arbitrage | informatif |
| garde-fou dans `parse_esm.py` | Refuse de produire un dataset si les fichiers d'arbitrage manquent, au lieu d'afficher silencieusement « zéro aide technique » | ✅ oui (code 3) |

## Limites connues, à déclarer d'emblée

Un audit honnête commence par ses propres trous. À la date de ce document :

1. **13 décisions d'aide technique sans phrase source.** Elles ont été arbitrées lors
   d'un premier lot, avant la mise en place de la colonne `source`. Les décisions sont
   validées, mais leur justification n'est pas tracée par écrit.
   `journal_audit.py` les liste à chaque exécution. **À compléter au prochain passage
   sur les bilans.**
2. **Ressentis incomplets.** Selon la dimension, 19 à 21 paires complètes sur 23 : les
   cases non marquées dans les Excel ne sont pas interprétées.
3. **Un FES-I après non mesuré** (1 dossier), considéré identique à l'avant sur décision
   métier — tracé dans le journal des décisions.
4. **Quatre grilles de déplacements « après » non re-saisies**, reportées depuis l'avant
   parce que l'ergothérapeute a noté que rien n'avait changé. Le dossier compte comme
   stable, et le champ `reporte_car_inchange` le signale dans `dataset.json`.
5. **Deux arbitrages limites validés par l'équipe** : un essai de déambulateur réalisé au
   domicile mais refusé à l'extérieur, compté *essayée* ; une aide technique voiture
   essayée avec intention d'achat non confirmée, comptée *essayée*.
6. **Un cas à reconfirmer** : une canne laissée en prêt et utilisée en intérieur a été
   comptée *essayée*, alors que la règle « laissé en prêt (et gardé) » pointe vers
   *mise en place*. La canne n'ayant pas été acquise et l'usage restant partiel, le
   classement *essayée* a été retenu — à valider par l'ergothérapeute rédactrice.
7. **Suivi à 6 mois non exploité.** Il existe dans un onglet « Suivi » de chaque bilan,
   jamais lu par le parser.
8. **Informations de méthode incomplètes.** Période couverte, durée des parcours et
   nombre de séances ne sont pas encore remontés dans le dataset (extractibles des
   bilans). L'exhaustivité de la cohorte et l'absence de groupe témoin ne peuvent être
   renseignées que par l'équipe ESM. Voir **`METHODE.md`**.
9. **L'atteinte des objectifs est une auto-évaluation** par l'ergothérapeute
   intervenante, pas une évaluation indépendante. Les scores FES-I, eux, sont des
   mesures instrumentées. Voir `METHODE.md`.

## Sauvegarde des fichiers non versionnés

`at_curated.csv`, `services_curated.csv` et `ressentis_manuel.csv` ne sont pas dans le
dépôt mais **sont nécessaires pour reproduire les chiffres**. Ils ont déjà été perdus
deux fois lors de réinitialisations de l'environnement de travail.

**Ils doivent être conservés avec le dossier `bilans/`**, sur le poste de travail, et
redéposés en même temps que les bilans à chaque nouveau lot. Sans eux, les arbitrages
qualitatifs sont à refaire intégralement, et rien ne garantit des décisions identiques
sur les cas limites.
