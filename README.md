# Dashboard ESM — Impact des Équipes Spécialisées Mobilité

Tableau de bord web qui transforme les bilans ergo (Excel) de l'expérimentation
**ESM 2025-2026** en une visualisation claire et **entièrement anonymisée**,
différenciée par département.

> 🔒 Aucune donnée nominative n'est publiée. Les `.xlsx` bruts ne quittent
> jamais la machine ; seul `dataset.json` (anonymisé et vérifié) est mis en ligne.

## À quoi ça ressemble

Le dashboard (`index.html`) présente : les indicateurs clés (cohorte, âge moyen,
évolution du FES-I, atteinte des objectifs), les trajectoires individuelles de
peur de chuter (avant/après), le report modal des déplacements, et les verbatims
(bénéficiaires + synthèses ergo). Un filtre par département est disponible.

## Le pipeline en 3 fichiers

| Fichier | Rôle |
|---|---|
| `parse_esm.py`   | Lit les `bilans/*.xlsx`, extrait et **anonymise** → `dataset.json` |
| `verify_anon.py` | Contrôle « zéro fuite de nom » — **bloque** si un nom passe |
| `index.html`     | Le dashboard, qui charge `dataset.json` |
| `etat_traitement.py` | Dit quels dossiers restent à arbitrer à la main (AT / services) |

## Redonner tout le dossier à chaque fois : aucun problème

Tout le calcul automatique (âge, GIR, FES-I, ressentis, déplacements, objectifs) est
**recalculé de zéro** à chaque régénération. On peut donc redéposer l'intégralité des
bilans à chaque lot : le résultat est identique, il n'y a rien à « ne pas refaire ».

Seuls les deux arbitrages **qualitatifs** demandent une lecture humaine, et ils sont
mémorisés par dossier dans `at_curated.csv` et `services_curated.csv` (non versionnés).
`etat_traitement.py` compare les bilans présents à ces deux fichiers et liste ce qui
reste à faire. Un dossier relu sans aide technique ni service est noté avec le statut
**`aucune`** : c'est ce qui distingue « relu, rien à déclarer » de « jamais relu ».

## Mettre à jour avec de nouveaux bilans

1. Déposer les nouveaux bilans terminés dans le dossier `bilans/`
   (fichiers `Bilan_ESM_Ergo_*.xlsx`).
2. Lancer, depuis la racine du projet :
   ```bash
   ./maj.sh
   ```
   Le script régénère `dataset.json`, vérifie l'absence de fuite, et **ne publie
   rien** si un nom a échappé à l'anonymisation.
3. Publier :
   ```bash
   git add dataset.json && git commit -m "Mise à jour des données ESM" && git push
   ```

## Prévisualiser en local

Le dashboard charge ses données via `fetch`, donc un double-clic sur le fichier
ne suffit pas. Lancer un petit serveur :

```bash
python3 -m http.server
# puis ouvrir http://localhost:8000
```

## Mise en ligne (GitHub Pages)

Le déploiement est automatique via GitHub Actions à chaque mise à jour de la
branche `main`. Activation (une seule fois) :
**Settings → Pages → Build and deployment → Source : « GitHub Actions »**.

## Sécurité — règles non négociables

- `bilans/` et tous les `*.xlsx` sont exclus par `.gitignore`.
- Le contrôle d'anonymisation tourne à chaque régénération et bloque la
  publication en cas de fuite (nom, « Mme/Dr X », email, téléphone).
