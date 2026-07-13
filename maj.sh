#!/usr/bin/env bash
#
# maj.sh — Met à jour le dashboard ESM en une seule commande.
#
#   1. Régénère les données anonymisées depuis les bilans Excel (bilans/).
#   2. Contrôle « zéro fuite de nom ».
#   3. Ne remplace dataset.json QUE si le contrôle passe.
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
echo "▶ 1/2  Régénération des données depuis : $BILANS_DIR"
python3 parse_esm.py "$BILANS_DIR" "$TMP"

echo ""
echo "▶ 2/2  Contrôle anonymisation (zéro fuite de nom)"
if python3 verify_anon.py "$TMP" "$BILANS_DIR"; then
    mv "$TMP" dataset.json
    trap - EXIT
    echo ""
    echo "✅  dataset.json mis à jour ET vérifié."
    echo ""
    echo "    Prochaine étape pour publier :"
    echo "      git add dataset.json"
    echo "      git commit -m \"Mise à jour des données ESM\""
    echo "      git push"
else
    echo ""
    echo "⛔  Fuite détectée : dataset.json N'A PAS été modifié. Rien n'est publié."
    exit 1
fi
