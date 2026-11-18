# CLAUDE.md — à lire AVANT toute intervention sur ce dépôt

Ce projet produit un dashboard d'impact **anonymisé** à partir de bilans ergothérapie
nominatifs (expérimentation ESM 2025-2026, Merci Julie). Il doit rester **reproductible**
et **auditable** : les mêmes bilans doivent toujours donner les mêmes chiffres, et chaque
chiffre doit pouvoir être remonté jusqu'à sa source.

## Règles absolues

1. **Ne jamais versionner de donnée nominative.** Les `.xlsx`, `at_curated.csv`,
   `services_curated.csv` et `ressentis_manuel.csv` sont indexés par nom de dossier :
   ils restent hors dépôt (`.gitignore`). Seuls `dataset.json`,
   `resultats_anonymises.csv` et `audit_arbitrages.csv` sont publiables.
2. **Ne jamais publier sans le contrôle d'anonymisation.** `./maj.sh` le fait et bloque
   en cas de fuite. Ne pas contourner.
3. **Ne jamais inventer une valeur.** Une donnée absente, illisible ou non marquée vaut
   `null` (« non renseigné »). Pas d'imputation, pas de moyenne de remplacement.
4. **Ne jamais changer une règle d'arbitrage sans le dire.** Les règles sont figées dans
   les trois documents ci-dessous. Si un cas nouveau les oblige à bouger, il faut
   l'écrire dans le document concerné ET dans le journal des décisions, puis signaler
   l'impact chiffré sur les résultats déjà publiés.

## Lire ceci avant de toucher aux données

| Document | Ce qu'il fige |
|---|---|
| `REGLES_RESSENTIS.md` | Les 4 échelles de ressenti : orientation, inversion de la crainte, conversions |
| `REGLES_AIDES_TECHNIQUES.md` | Entonnoir *préconisée → essayée → mise en place*, cas limites |
| `REGLES_SERVICES.md` | Entonnoir *présentée → engagée → effective*, cas limites |
| `README_POUR_CLAUDE_CODE.md` | Journal des décisions méthodologiques et leur motif |
| `AUDIT.md` | Comment un contrôleur externe remonte un chiffre jusqu'à sa source |

## Deux pièges à connaître

**Le sens des deltas n'est pas le même partout.**
- **FES-I** : score clinique non retourné → Δ **négatif** = amélioration (moins de peur).
- **Ressentis** : les 4 axes sont réorientés « plus haut = mieux » → Δ **positif** =
  amélioration. La crainte de chuter est affichée inversée, en « confiance ».

Ne jamais commenter une évolution sans vérifier de quel indicateur il s'agit.

**Les bilans Excel sont hétérogènes.** La valeur cochée peut être marquée en gras, en
couleur de police, ou surlignée ; elle peut être une ligne au-dessus ou en dessous de la
question ; les objectifs sont cotés tantôt « Atteint/Partiellement/Non atteint », tantôt
« Oui/Non » ; certains onglets changent de nom. Le parser gère ces cas : les corrections
sont commentées à l'endroit où elles s'appliquent dans `parse_esm.py`. **Ne pas
« simplifier » ces branches** sans comprendre quel fichier les a rendues nécessaires.

## Procédure pour un nouveau lot de bilans

Tout le calcul automatique est **refait de zéro** à chaque régénération : on redépose
donc TOUS les bilans, rien n'est « sauté ». Un correctif de lecture profite
rétroactivement à tous les anciens dossiers.

```bash
# 0. déposer tous les .xlsx dans bilans/  (+ restaurer at_curated.csv et
#    services_curated.csv depuis la sauvegarde — voir AUDIT.md)

python3 etat_traitement.py     # 1. quels dossiers restent à arbitrer ?
#   -> lire le Plan d'accompagnement + le Bilan de fin de suivi des nouveaux dossiers
#   -> proposer la classification AVEC LA PHRASE SOURCE, la faire valider par l'équipe
#   -> compléter at_curated.csv / services_curated.csv (colonne `source` obligatoire)
#   -> un dossier relu sans rien à déclarer : statut « aucune »

./maj.sh                       # 2. régénère + contrôle anonymisation (bloquant)
python3 journal_audit.py       # 3. piste d'audit + contrôle de cohérence
python3 test_coherence.py      # 4. non-régression des agrégats
```

Puis commit et push. **Si une étape échoue, ne pas publier.**

## Ce qui demande une validation humaine

Les classements d'aides techniques et de services sont **qualitatifs** : ils se lisent
dans le texte libre, et la nuance vit dans les formulations. Ne jamais les décider seul :
proposer, citer la phrase, faire valider. L'ergothérapeute qui a rédigé le bilan est la
référence. Signaler explicitement les cas limites plutôt que de trancher en silence.

## Ton

L'interlocutrice est experte de son métier et non technique. Expliquer les arbitrages
en français clair, dire ce qui est incertain, et ne jamais présenter une estimation
comme une mesure.
