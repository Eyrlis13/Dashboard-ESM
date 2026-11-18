"""
journal_audit.py — Produit la piste d'audit des décisions qualitatives.

Les deux arbitrages qualitatifs du projet (aides techniques, services de mobilité)
sont faits par LECTURE des bilans, puis validés par l'équipe. Ils vivent dans
`at_curated.csv` et `services_curated.csv`, qui ne sont pas versionnés parce qu'ils
sont indexés par nom de dossier.

Ce script en tire `audit_arbitrages.csv`, VERSIONNÉ et anonymisé : une ligne par
décision, rattachée à l'ID anonyme du dashboard, avec la phrase du bilan qui la
justifie. Un contrôleur externe peut donc remonter chaque chiffre du dashboard
jusqu'à la phrase d'origine, sans accéder aux fichiers nominatifs.

Il VÉRIFIE au passage que les décisions du dataset publié correspondent exactement
aux fichiers d'arbitrage : toute divergence fait échouer le script (code 1).

Usage : python3 journal_audit.py
"""
import csv, json, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
AT_CSV   = os.path.join(HERE, 'at_curated.csv')
SV_CSV   = os.path.join(HERE, 'services_curated.csv')
DATASET  = os.path.join(HERE, 'dataset.json')
OUT      = os.path.join(HERE, 'audit_arbitrages.csv')


def lire(path, col_libelle):
    """Lignes d'un fichier d'arbitrage. Les lignes de statut « aucune » sont des
    marqueurs de relecture (dossier lu, rien à déclarer) : conservées pour la
    traçabilité, mais signalées comme telles."""
    if not os.path.isfile(path):
        print(f"⛔  Fichier d'arbitrage absent : {os.path.basename(path)}")
        print("    Il n'est pas versionné. Le restaurer depuis la sauvegarde")
        print("    conservée avec le dossier bilans/ (voir AUDIT.md).")
        sys.exit(2)
    out = []
    with open(path, encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            cle = (row.get('cle') or '').strip().upper()
            if not cle:
                continue
            out.append({
                'cle': cle,
                'libelle': (row.get(col_libelle) or '').strip(),
                'statut': (row.get('statut') or '').strip(),
                'source': ' '.join((row.get('source') or '').split()),
            })
    return out


def main():
    at = lire(AT_CSV, 'type')
    sv = lire(SV_CSV, 'service')

    # L'ID anonyme est attribué par ordre alphabétique des dossiers présents :
    # on le reconstitue de la même façon, puis on le VÉRIFIE contre le dataset.
    cles = sorted({r['cle'] for r in at} | {r['cle'] for r in sv})
    id_de = {c: str(i) for i, c in enumerate(cles, 1)}

    if not os.path.isfile(DATASET):
        print(f"⛔  dataset.json introuvable : lancer d'abord ./maj.sh")
        sys.exit(2)
    data = json.load(open(DATASET, encoding='utf-8'))

    if len(data) != len(cles):
        print(f"⛔  {len(data)} bénéficiaires dans dataset.json mais {len(cles)} dossiers arbitrés.")
        print("    Un bilan a été ajouté ou retiré sans régénérer, ou un arbitrage manque.")
        print("    -> compléter avec « python3 etat_traitement.py », puis relancer ./maj.sh")
        sys.exit(1)

    # --- Contrôle de cohérence : dataset publié == fichiers d'arbitrage ---
    cle_de = {v: k for k, v in id_de.items()}
    divergences = []
    for rec in data:
        cle = cle_de.get(rec['id'])
        attendu_at = {(r['libelle'], r['statut']) for r in at
                      if r['cle'] == cle and r['statut'] != 'aucune'}
        obtenu_at = {(a['type'], a['statut']) for a in (rec.get('at') or [])}
        attendu_sv = {(r['libelle'], r['statut']) for r in sv
                      if r['cle'] == cle and r['statut'] != 'aucune'}
        obtenu_sv = {(x['service'], x['statut']) for x in (rec.get('services') or [])}
        if attendu_at != obtenu_at:
            divergences.append(f"N°{rec['id']} — aides techniques : {attendu_at ^ obtenu_at}")
        if attendu_sv != obtenu_sv:
            divergences.append(f"N°{rec['id']} — services : {attendu_sv ^ obtenu_sv}")
    if divergences:
        print(f"⛔  {len(divergences)} divergence(s) entre dataset.json et les arbitrages :")
        for d in divergences:
            print('   ', d)
        print("    -> régénérer (./maj.sh) pour réaligner, puis relancer ce script.")
        sys.exit(1)

    # --- Écriture du journal ---
    lignes = []
    for dom, src in (('Aide technique', at), ('Service', sv)):
        for r in src:
            lignes.append({
                'id_anonyme': id_de[r['cle']],
                'domaine': dom,
                'libelle': r['libelle'],
                'statut': r['statut'],
                'phrase_source': r['source'],
            })
    lignes.sort(key=lambda r: (r['domaine'], r['libelle'], int(r['id_anonyme'])))

    with open(OUT, 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.writer(fh)
        w.writerow(['id_anonyme', 'domaine', 'libelle', 'statut', 'phrase_source'])
        for r in lignes:
            w.writerow([r['id_anonyme'], r['domaine'], r['libelle'], r['statut'], r['phrase_source']])

    reels = [r for r in lignes if r['statut'] != 'aucune']
    print(f"✅  dataset.json et les arbitrages concordent sur les {len(data)} dossiers.")
    print(f"-> {OUT}")
    print(f"   {len(reels)} décisions + {len(lignes)-len(reels)} marqueurs « relu, rien à déclarer »")
    print(f"   généré le {datetime.date.today().isoformat()}")
    sans_source = [r for r in reels if not r['phrase_source']]
    if sans_source:
        print(f"\n⚠  {len(sans_source)} décision(s) sans phrase source — à compléter pour l'audit :")
        for r in sans_source[:10]:
            print(f"     N°{r['id_anonyme']} {r['domaine']} / {r['libelle']} ({r['statut']})")


if __name__ == '__main__':
    main()
