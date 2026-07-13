# Règles d'arbitrage — Ressentis mobilité (à appliquer à l'identique)

Ce document **fige** la façon dont on traite les 4 échelles de ressenti des bilans
ESM. Toute nouvelle donnée doit suivre exactement ces règles, pour rester comparable.

## Les 4 dimensions (toutes réorientées « plus haut = mieux »)

| Dimension affichée | Question source | Sens |
|---|---|---|
| **Aisance** | « à l'aise dans mes déplacements / ma mobilité » | 10 = tout à fait à l'aise |
| **Satisfaction** | « satisfait de mes déplacements » | 10 = extrêmement satisfait |
| **Confiance face à la chute** | « crainte de chuter / je crains de tomber » | 10 = ne craint **jamais** de chuter |
| **Sérénité** | « serein concernant mes déplacements » | 10 = extrêmement serein |

> ⚠️ **Arbitrage clé — la crainte est INVERSÉE.** La question mesure la *peur*
> (haut = mauvais). On l'affiche en **« Confiance face à la chute »** = son opposé,
> pour que les 4 axes se lisent dans le même sens (haut = mieux). « Craint jamais »
> → confiance 10 ; « craint constamment » → confiance 0.

## Échelle commune : score de 0 à 10 (« positivité »)

L'ancre **négative** vaut 0, l'ancre **positive** vaut 10. On lit toujours
l'orientation sur **le texte des ancres**, jamais sur le chiffre brut.

## Conversions selon le format de saisie rencontré

| Format dans l'Excel | Règle de conversion |
|---|---|
| **Échelle 1→10, case en gras** | position `v` → `(v−1)/9 × 10` (gauche = pire = 0) |
| **Nombre isolé 0→10** (ancres qualitatives) | tel quel pour aisance/satisfaction/sérénité ; **confiance = 10 − nombre** (le nombre code la peur) |
| **4 niveaux qualitatifs, case surlignée** | niveau `L` (1 = pire … 4 = meilleur) → `(L−1)/3 × 10` soit 0 / 3,3 / 6,7 / 10 |
| **Fourchette** (« 7-8 ») | milieu de la fourchette |
| **Adjectif seul** | lexique fixe : pas du tout = 0 · peu = 3,3 · assez = 6,7 · tout à fait = 10 |
| **Vide / illisible / non marqué** | `null` (« non renseigné ») — **jamais inventé** |

Lexique des niveaux qualitatifs (surlignés) :
- Aisance / Satisfaction / Sérénité : `pas du tout` = 1 · `peu` = 2 · `assez` = 3 · `à l'aise / satisfait / très serein` = 4
- Crainte : `constamment` = 1 · `souvent` = 2 · `quelques fois` = 3 · `jamais` = 4 (→ confiance croissante)

## Comparaison avant / après

- On ne calcule un **progrès** que pour les bénéficiaires ayant un score **avant ET après**
  pour la dimension considérée (paires complètes uniquement), comme pour le FES-I.
- Un Δ **positif** (score plus haut après) = **amélioration**.

## Extraction & saisie

- L'extraction automatique (`parse_esm.py → get_ressentis`) est **best-effort** :
  elle gère les 3 formats ci-dessus mais tous les fichiers ne sont pas lisibles
  (cases non marquées, onglets vides).
- Les valeurs non lisibles sont complétées à la main via `ressentis_manuel.csv`
  (non versionné — voir `.gitignore`), fusionné par le parser. Le manuel **prime**
  sur l'automatique.

_Dernière mise à jour : juillet 2026._
