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

La **case cochée** peut être marquée de plusieurs façons (**gras**, **couleur de police**
rouge, ou **surlignage** jaune) et se trouver sur la ligne de la question, **juste au-dessus
ou juste en dessous**. La bonne ligne de réponse est identifiée par son vocabulaire propre
(« serein », « satisfait », « constamment/jamais »…) pour éviter toute confusion entre items.

| Format dans l'Excel | Règle de conversion |
|---|---|
| **Échelle 1→10** (case cochée) | position `v` → `(v−1)/9 × 10` (gauche = pire = 0) |
| **4 niveaux qualitatifs** (case cochée) | **position** de la case cochée, `i` de 0 (pire, à gauche) à `n−1` (meilleur) → `i/(n−1) × 10`. Pour 4 niveaux : 0 / 3,3 / 6,7 / 10. *Méthode positionnelle : indépendante du libellé exact (« Assez à l'aise », « Peu serein »…).* |
| **Nombre isolé 0→10** | tel quel pour aisance/satisfaction/sérénité ; **confiance = 10 − nombre** (le nombre code la peur) |
| **Fourchette** (« 7-8 ») | milieu de la fourchette |
| **Adjectif seul** (texte libre) | ramené à la position équivalente sur l'échelle des niveaux |
| **Vide / illisible / non marqué** | `null` (« non renseigné ») — **jamais inventé** |

> Pour la **crainte / confiance**, les 4 niveaux vont de « Constamment » (gauche = 0 = peur
> maximale) à « Jamais » (droite = 10 = pleine confiance) : la méthode positionnelle donne
> donc directement la **confiance** (plus haut = mieux), sans inversion supplémentaire.

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
