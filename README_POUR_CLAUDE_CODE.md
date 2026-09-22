# Projet Dashboard ESM — Contexte pour Claude Code

## But
Pipeline reproductible qui transforme des bilans ergo Excel (Équipe Spécialisée
Mobilité) en un dashboard web anonymisé, différencié par département.

## Fichiers de ce dossier
- `index.html` — le dashboard (architecture à onglets, charge `dataset.json` via `fetch`).
- `vendor/chart.umd.js` — Chart.js embarqué localement (pas de dépendance CDN).
- `dataset.json` — données anonymisées (le SEUL fichier de données publiable).
- `parse_esm.py` — moteur d'extraction + anonymisation (voir plus bas).
- `verify_anon.py` — contrôle « zéro fuite de nom » (bloque la publication si fuite).
- `maj.sh` — régénération + contrôle en une seule commande.
- `bilans/` — dépôt des `.xlsx` bruts (NON versionné, cf. `.gitignore`).
- `.github/workflows/pages.yml` — déploiement automatique sur GitHub Pages.
- `README.md` — mode d'emploi rapide.
- `README_POUR_CLAUDE_CODE.md` — ce fichier (contexte détaillé).

## Workflow cible
1. Les ergos remplissent leurs bilans Excel comme d'habitude (aucun changement).
2. On dépose les nouveaux bilans dans un dossier `bilans/` (NON versionné).
3. On lance la régénération → `dataset.json` anonymisé mis à jour.
4. Le dashboard lit `dataset.json` et affiche les résultats.
5. À terme : hébergement GitHub Pages (comme le dashboard ergothèque existant).

## Ce que fait parse_esm.py
- Lit tous les `Bilan_ESM_Ergo_*.xlsx` d'un dossier.
- Dédoublonne : si versions multiples (base + `_terminé`), garde `_terminé`.
- Extrait par participant : âge, GIR, zone, permis, FES-I avant/après (+ delta),
  conduite en solo avant/après, modes alternatifs avant/après, objectifs
  (atteints/partiels/non), verbatims bénéficiaire + synthèse ergo.
- ANONYMISE entièrement :
  - ID = `département-numéro` (ex. `41-03`), jamais de nom.
  - Département déduit du code postal de l'adresse, sinon d'une ville citée.
  - Le texte libre (verbatims/synthèses) est nettoyé : noms, "Mme X",
    emails, téléphones remplacés par […].
- Sort `dataset.json` (le SEUL fichier publiable).

## Règles de sécurité NON négociables
- Les `.xlsx` nominatifs ne partent JAMAIS sur GitHub.
  `.gitignore` doit contenir : `bilans/` et `*.xlsx`.
- Une vérification "zéro fuite de nom" doit tourner à chaque régénération
  et BLOQUER la publication si un nom passe au travers.

## Dettes techniques connues (à améliorer)
- Comptage du report modal encore approximatif (libellés ambigus).
- 1 participant sans département identifiable → "non renseigné", à compléter à la main.

## Décisions déjà prises
- **FES-I : on ne retient que les 7 items de la version COURTE** (Short FES-I, Kempen 2008)
  pour TOUS les bénéficiaires — certains bilans utilisent la version 16 items, d'autres la
  courte. Les 7 items communs (habillage, douche/bain, chaise, escaliers, atteindre,
  pente, sortir) donnent un score 7-28 comparable pour tout le monde.
  Paliers cliniques : faible 7-8 · modérée 9-13 · élevée 14-28.
- L'item « Sortir » est isolé (`fesi_sortir`) et mis en avant : c'est celui qui colle le
  mieux à la mission ESM.
- Le suivi 6 mois vit dans l'onglet « Suivi » de chaque bilan : **non exploité** pour l'instant
  (le parser ne lit jamais cet onglet).
- Les bilans nommés « REFUS » sont exclus de la cohorte.
- Anonymisation : les noms sont masqués **à l'échelle de tout le corpus** (un nom connu dans
  un bilan est masqué dans tous), ce qui couvre aussi les professionnels cités.
- GUERAULT : réintégré (juillet 2026). Son FES-I après n'a pas été mesuré → considéré
  identique à l'avant (stable, Δ0), sur décision métier. Un garde-fou rejette désormais
  tout FES-I ≤ 0 (non rempli).
- Les 4 échelles de ressentis (aise/satisfaction/crainte/sérénité) NE sont pas
  exploitables automatiquement dans les fichiers actuels → volontairement mises
  de côté pour l'instant. Ne pas tenter de les inventer.

## Améliorations réalisées (juillet 2026)
- [x] Dashboard découplé de ses données : `index.html` charge `dataset.json`
      via `fetch` (message d'aide clair si ouvert en local sans serveur).
- [x] Script unique `maj.sh` : régénération + contrôle anonymisation.
- [x] Contrôle « zéro fuite » (`verify_anon.py`) qui BLOQUE la publication.
- [x] `parse_esm.py` rendu portable (plus aucun chemin en dur ; lit `bilans/`,
      écrit `dataset.json`). Ajout du masquage des noms de soignants (Dr/Pr).
- [x] Déploiement GitHub Pages via GitHub Actions.

## Restes / pistes ultérieures
- Comptage du report modal encore approximatif (libellés ambigus dans les Excel).
- 1 participant sans département identifiable → "non renseigné", à compléter à la main.
- Créer un jeu de test `.xlsx` synthétique pour valider le parser en CI.
