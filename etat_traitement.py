"""
etat_traitement.py — « Qu'est-ce qui reste à traiter ? »

Le calcul automatique (âge, GIR, FES-I, ressentis, déplacements, objectifs) est
recalculé de zéro à chaque régénération : redonner tout le dossier `bilans/` ne
pose aucun problème, le résultat est identique.

Ce qui NE se recalcule pas tout seul, ce sont les deux arbitrages qualitatifs,
qui demandent une lecture humaine du texte libre :
  - les aides techniques   -> at_curated.csv
  - les services/orientations -> services_curated.csv

Ce script compare les bilans présents aux dossiers déjà arbitrés et dit, pour
chacun, ce qu'il reste à faire. Il ne modifie rien.

Usage : python3 etat_traitement.py [dossier_bilans]
"""
import csv, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def cle_dossier(path):
    """Même normalisation que parse_esm.build_dataset : le nom de fichier EST la clé."""
    b = os.path.basename(path).replace('Bilan_ESM_Ergo_', '').replace('.xlsx', '')
    b = b.replace('VF_', '').replace('bis_V3_', '').replace('Mme_', '').replace('_1', '')
    b = re.sub(r'_?termin[eé]?_?$', '', b, flags=re.IGNORECASE)
    return b.strip().upper().replace(' ', '').strip('_')


def cles_arbitrees(fichier, colonne):
    """Clés présentes dans un CSV curé, y compris les lignes « aucune »
    (= relu, rien à déclarer). Renvoie {clé: nb_lignes_réelles} ou None si absent."""
    path = os.path.join(HERE, fichier)
    if not os.path.isfile(path):
        return None
    vus = {}
    with open(path, encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            cle = (row.get('cle') or '').strip().upper()
            if not cle:
                continue
            reel = (row.get('statut') or '').strip().lower() != 'aucune'
            vus[cle] = vus.get(cle, 0) + (1 if reel else 0)
    return vus


def main():
    bilans_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'bilans')
    fichiers = sorted(glob.glob(os.path.join(bilans_dir, 'Bilan_ESM_Ergo_*.xlsx')))
    if not fichiers:
        print(f"⚠  Aucun bilan trouvé dans : {bilans_dir}")
        sys.exit(2)

    cles = {cle_dossier(f): f for f in fichiers}
    at = cles_arbitrees('at_curated.csv', 'type')
    sv = cles_arbitrees('services_curated.csv', 'service')

    manquants = []
    for fichier, vus in (('at_curated.csv', at), ('services_curated.csv', sv)):
        if vus is None:
            manquants.append(fichier)
    if manquants:
        print("⚠  Fichier(s) d'arbitrage absent(s) : " + ', '.join(manquants))
        print("   Ils ne sont pas versionnés (données de travail). Sans eux, TOUS les")
        print("   dossiers sont à ré-arbitrer — et rien ne garantit des choix identiques.")
        print("   → les conserver avec les bilans, hors du dépôt Git.\n")

    largeur = max(len(c) for c in cles)
    print(f"{'dossier'.ljust(largeur)}  {'aides techn.':>13}  {'services':>13}")
    print('─' * (largeur + 32))

    a_faire = []
    for cle in sorted(cles):
        def etat(vus):
            if vus is None:
                return '?'
            if cle not in vus:
                return 'À TRAITER'
            return f"{vus[cle]} ligne(s)" if vus[cle] else 'aucune'
        e_at, e_sv = etat(at), etat(sv)
        if 'À TRAITER' in (e_at, e_sv):
            a_faire.append(cle)
        print(f"{cle.ljust(largeur)}  {e_at:>13}  {e_sv:>13}")

    print()
    if a_faire:
        print(f"▶  {len(a_faire)} dossier(s) à arbitrer : {', '.join(a_faire)}")
        print("   Lire le Plan d'accompagnement + le Bilan de fin de suivi, appliquer")
        print("   REGLES_AIDES_TECHNIQUES.md et REGLES_SERVICES.md, puis compléter les CSV.")
        print("   Un dossier relu SANS aide technique / SANS service se note quand même,")
        print("   avec le statut « aucune » : c'est ce qui distingue « relu, rien » de")
        print("   « jamais relu ».")
    else:
        print("✅  Tous les dossiers présents ont été arbitrés (AT et services).")

    print(f"\n   {len(cles)} bilan(s) dans {bilans_dir}")


if __name__ == '__main__':
    main()
