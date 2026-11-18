#!/usr/bin/env bash
#
# maj.sh — Met à jour le dashboard ESM en une seule commande.
#
#   0. Signale les dossiers pas encore arbitrés (aides techniques / services).
#   1. Régénère les données anonymisées depuis les bilans Excel (bilans/).
#   2. Contrôle « zéro fuite de nom ».
#   3. Ne remplace dataset.json QUE si le contrôle passe.
#   4. Produit la piste d'audit et vérifie la non-régression des agrégats.
#      → aucune donnée nominative n'est jamais publiée, même transitoirement.
#
# Usage : ./maj.sh [dossier_bilans]   (par défaut : bilans/)

set -euo pipefail
cd "$(dirname "$0")"

BILANS_DIR="${1:-bilans}"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

echo "──────────────────────────────────────────────"
echo "  Mise à jour du dashboard ESM"
echo "──────────────────────────────────────────────"

echo ""
echo "▶ 0/4  Dossiers restant à arbitrer"
# on ne garde que les lignes actionnables (le détail complet :
#   python3 etat_traitement.py)
python3 etat_traitement.py "$BILANS_DIR" \
  | grep -E "À TRAITER|^▶|^✅|^⚠|^   " || true

echo ""
echo "▶ 1/4  Régénération des données depuis : $BILANS_DIR"
python3 parse_esm.py "$BILANS_DIR" "$TMP"

echo ""
echo "▶ 2/4  Contrôle anonymisation (zéro fuite de nom)"
if python3 verify_anon.py "$TMP" "$BILANS_DIR"; then
    mv "$TMP" dataset.json
    trap - EXIT
    echo ""
    echo "✅  dataset.json mis à jour ET vérifié."
    echo ""
    echo "▶ 3/4  Piste d'audit (journal des arbitrages + cohérence)"
    python3 journal_audit.py

    echo ""
    echo "▶ 4/4  Non-régression des agrégats"
    python3 test_coherence.py

    echo ""
    echo "    Prochaine étape pour publier :"
    echo "      git add dataset.json resultats_anonymises.csv audit_arbitrages.csv"
    echo "      git commit -m \"Mise à jour des données ESM\""
    echo "      git push"
else
    echo ""
    echo "⛔  Fuite détectée : dataset.json N'A PAS été modifié. Rien n'est publié."
    exit 1
fi
