"""
test_coherence.py — Non-régression des agrégats publiés.

Objectif : si une modification du parser, des règles ou des arbitrages déplace un
chiffre, il faut que ça se VOIE, au lieu d'être publié sans que personne ne s'en
aperçoive.

Les valeurs attendues ci-dessous ont été validées avec l'équipe ESM. Tout écart fait
échouer le test (code 1). Si l'écart est légitime (nouveau bilan, correctif de lecture,
arbitrage revu), mettre à jour ATTENDU **dans le même commit que la modification**, en
expliquant pourquoi dans le message de commit.

Usage : python3 test_coherence.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

# --- Référence validée (23 bénéficiaires, lot de septembre 2026) ------------
ATTENDU = {
    'n_beneficiaires': 23,
    'fesi': {'paires_completes': 23, 'ameliorations': 7, 'stables': 9, 'degradations': 7},
    'ressentis': {           # paires complètes par dimension
        'aise': 19, 'satisfaction': 20, 'confiance': 20, 'serenite': 21,
    },
    'at': {'mise_en_place': 10, 'essayee': 10, 'preconisee': 6},
    'services': {'effective': 10, 'engagee': 9, 'presentee': 22},
    'objectifs': {'atteint': 38, 'partiel': 16, 'non': 9},
    'deplacements': {'grilles_apres_exploitables': 23},
}


def main():
    path = os.path.join(HERE, 'dataset.json')
    if not os.path.isfile(path):
        print("⛔  dataset.json introuvable : lancer ./maj.sh d'abord.")
        sys.exit(2)
    d = json.load(open(path, encoding='utf-8'))

    ecarts = []

    def cmp(libelle, attendu, obtenu):
        if attendu != obtenu:
            ecarts.append(f"{libelle} : attendu {attendu}, obtenu {obtenu}")

    cmp('nombre de bénéficiaires', ATTENDU['n_beneficiaires'], len(d))

    # FES-I : rappel, un delta NÉGATIF est une amélioration (moins de peur)
    deltas = [r['fesi_delta'] for r in d
              if r['fesi_avant'] is not None and r['fesi_apres'] is not None]
    cmp('FES-I paires complètes', ATTENDU['fesi']['paires_completes'], len(deltas))
    cmp('FES-I améliorations', ATTENDU['fesi']['ameliorations'], sum(1 for x in deltas if x < 0))
    cmp('FES-I stables', ATTENDU['fesi']['stables'], sum(1 for x in deltas if x == 0))
    cmp('FES-I dégradations', ATTENDU['fesi']['degradations'], sum(1 for x in deltas if x > 0))

    for dim, n in ATTENDU['ressentis'].items():
        obtenu = sum(1 for r in d if r['ressentis'][dim]['avant'] is not None
                     and r['ressentis'][dim]['apres'] is not None)
        cmp(f'ressenti {dim} — paires complètes', n, obtenu)

    for statut, n in ATTENDU['at'].items():
        cmp(f'aides techniques « {statut} »', n,
            sum(1 for r in d for a in (r.get('at') or []) if a['statut'] == statut))

    for statut, n in ATTENDU['services'].items():
        cmp(f'services « {statut} »', n,
            sum(1 for r in d for s in (r.get('services') or []) if s['statut'] == statut))

    for k, n in ATTENDU['objectifs'].items():
        cmp(f'objectifs {k}', n, sum(r['objectifs'][k] for r in d))

    exploitables = sum(1 for r in d if sum(r['deplacements']['apres']['modes'].values()) > 0)
    cmp('grilles de déplacements « après » exploitables',
        ATTENDU['deplacements']['grilles_apres_exploitables'], exploitables)

    # Contrôle structurel : aucun statut inattendu ne doit apparaître
    statuts_at = {a['statut'] for r in d for a in (r.get('at') or [])}
    statuts_sv = {s['statut'] for r in d for s in (r.get('services') or [])}
    inconnus = (statuts_at - set(ATTENDU['at'])) | (statuts_sv - set(ATTENDU['services']))
    if inconnus:
        ecarts.append(f"statut(s) inconnu(s) dans le dataset : {sorted(inconnus)}")

    if ecarts:
        print(f"⛔  {len(ecarts)} écart(s) par rapport à la référence validée :\n")
        for e in ecarts:
            print('   ', e)
        print("\nSi l'écart est légitime (nouveau bilan, correctif, arbitrage revu),")
        print("mettre à jour ATTENDU dans test_coherence.py au même commit, en expliquant")
        print("pourquoi dans le message de commit. Sinon : ne pas publier.")
        sys.exit(1)

    print(f"✅  Agrégats conformes à la référence validée ({len(d)} bénéficiaires).")
    print("   FES-I, ressentis, aides techniques, services, objectifs, déplacements.")


if __name__ == '__main__':
    main()
