# Dossier `bilans/` — fichiers Excel bruts (NON versionnés)

C'est ici qu'on dépose les bilans ergo terminés :
`Bilan_ESM_Ergo_*.xlsx`

## ⚠️ Règle de sécurité
Le contenu de ce dossier **ne part JAMAIS sur GitHub**. Il contient des données
nominatives. Le `.gitignore` du projet ignore automatiquement tous les `.xlsx`
d'ici — seul ce `README.md` est versionné, pour que le dossier existe.

## Comment ça marche
1. Déposer les nouveaux `Bilan_ESM_Ergo_*.xlsx` dans ce dossier.
2. Lancer, depuis la racine du projet : `./maj.sh`
3. Le script régénère `dataset.json` (anonymisé) et **bloque** si un nom fuit.
4. Le dashboard (`index.html`) lit `dataset.json` mis à jour.
