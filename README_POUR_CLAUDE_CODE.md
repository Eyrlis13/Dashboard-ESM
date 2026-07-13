# Projet Dashboard ESM — Contexte pour Claude Code

## But
Pipeline reproductible qui transforme des bilans ergo Excel (Équipe Spécialisée
Mobilité) en un dashboard web anonymisé, différencié par département.

## Fichiers de ce dossier
- `parse_esm.py` — moteur d'extraction + anonymisation (voir plus bas).
- `dashboard_esm.html` — interface validée (prototype fonctionnel).
- `README_POUR_CLAUDE_CODE.md` — ce fichier.

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
- GUERAULT exclu (pas de FES-I après).
- Les 4 échelles de ressentis (aise/satisfaction/crainte/sérénité) NE sont pas
  exploitables automatiquement dans les fichiers actuels → volontairement mises
  de côté pour l'instant. Ne pas tenter de les inventer.

## Améliorations à faire sur Claude Code
- Découpler le dashboard de ses données : charger `dataset.json` via fetch
  au lieu de l'embarquer en dur dans le HTML.
- Créer un script unique `maj.sh` : régénération + contrôle anonymisation
  en une seule commande.
