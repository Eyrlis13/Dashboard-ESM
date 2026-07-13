"""
verify_anon.py — Contrôle « zéro fuite de nom » sur dataset.json.

Objectif : BLOQUER la publication si une donnée nominative a échappé à
l'anonymisation. Sort en code 1 dès qu'une fuite est détectée, 0 si tout est propre.

Deux niveaux de contrôle :
  1. Heuristiques (sans besoin des sources) : emails, téléphones,
     « Mme/M./Dr + Nom » resté en clair.
  2. Recoupement avec les sources (si les .xlsx sont présents dans bilans/) :
     on ré-extrait les vrais noms et on vérifie qu'aucun n'apparaît dans dataset.json.

Usage : python3 verify_anon.py [dataset.json] [dossier_bilans]
"""
import json, re, os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))

# Réutilise les helpers du parser (mêmes règles d'extraction de noms).
try:
    import openpyxl
    from parse_esm import get_names_from_file, BILANS_DIR, OUTPUT_JSON
    HAVE_SOURCES = True
except Exception:
    HAVE_SOURCES = False
    BILANS_DIR = os.path.join(HERE, 'bilans')
    OUTPUT_JSON = os.path.join(HERE, 'dataset.json')

# --- Motifs de fuite bloquants (aucune source requise) ----------------------
PATTERNS = [
    ('email',    re.compile(r'\b[\w.+-]+@[\w-]+\.[\w.-]+\b')),
    ('téléphone',re.compile(r'\b0\d(?:[ .]?\d{2}){4}\b')),
    # civilité/titre suivi d'un mot Capitalisé d'au moins 2 minuscules
    # (évite les simples initiales type « Mme L » et les placeholders « […] »)
    ('nom en clair après civilité',
        re.compile(r'\b(?:Mme|M\.|Mr|Monsieur|Madame|Dr|Docteur|Pr|Professeur)\.?\s+'
                   r'[A-ZÉÈÀ][a-zéèàêâîôûç]{2,}')),
]


def iter_strings(obj, path=''):
    """Parcourt récursivement le JSON et rend (chemin, texte) pour chaque chaîne."""
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_strings(v, f'{path}.{k}' if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_strings(v, f'{path}[{i}]')


def load_source_names(bilans_dir):
    """Ré-extrait les vrais noms depuis les .xlsx pour recoupement. Jamais stockés."""
    names = set()
    files = glob.glob(os.path.join(bilans_dir, 'Bilan_ESM_Ergo_*.xlsx'))
    for f in files:
        # nom de famille déduit du nom de fichier (comme dans le parser)
        b = os.path.basename(f).replace('Bilan_ESM_Ergo_', '').replace('.xlsx', '')
        b = re.sub(r'(_terminé|VF_|bis_V3_|Mme_|_1)', '', b).strip()
        for tok in re.split(r'[ _]+', b):
            if len(tok) >= 3:
                names.add(tok)
        try:
            wb = openpyxl.load_workbook(f, data_only=True)
            names |= get_names_from_file(wb)
        except Exception as e:
            print(f"   (avertissement : lecture de {os.path.basename(f)} impossible — {e})")
    # tokens trop courts ou trop génériques écartés
    return {n for n in names if len(n) >= 3}


def check(dataset_path, bilans_dir):
    with open(dataset_path, encoding='utf-8') as fh:
        data = json.load(fh)

    findings = []  # (gravité, où, extrait)

    # 1) Heuristiques
    for path, txt in iter_strings(data):
        for label, rx in PATTERNS:
            for m in rx.finditer(txt):
                findings.append((label, path, m.group(0)))

    # 2) Recoupement avec les sources (si disponibles)
    source_names = set()
    if HAVE_SOURCES and os.path.isdir(bilans_dir):
        source_names = load_source_names(bilans_dir)
    if source_names:
        rx_names = re.compile(
            r'\b(' + '|'.join(re.escape(n) for n in sorted(source_names, key=len, reverse=True)) + r')\b',
            re.IGNORECASE)
        for path, txt in iter_strings(data):
            for m in rx_names.finditer(txt):
                findings.append(('nom source présent', path, m.group(0)))

    return findings, source_names


def main():
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else OUTPUT_JSON
    bilans_dir   = sys.argv[2] if len(sys.argv) > 2 else BILANS_DIR

    if not os.path.isfile(dataset_path):
        print(f"⚠  dataset introuvable : {dataset_path}")
        sys.exit(2)

    findings, source_names = check(dataset_path, bilans_dir)

    print(f"Contrôle anonymisation — {os.path.basename(dataset_path)}")
    if source_names:
        print(f"  Recoupement actif : {len(source_names)} noms sources vérifiés.")
    else:
        print("  (Sources .xlsx absentes : contrôle heuristique seul — emails, téléphones, « Mme/Dr + Nom ».)")

    if not findings:
        print("\n✅  Aucune fuite détectée. Publication autorisée.")
        sys.exit(0)

    print(f"\n⛔  {len(findings)} fuite(s) potentielle(s) — PUBLICATION BLOQUÉE :\n")
    for label, path, extrait in findings:
        print(f"   [{label}] {path}\n       → « {extrait} »")
    print("\nCorrige l'anonymisation (parse_esm.py → scrub_text) puis relance la régénération.")
    sys.exit(1)


if __name__ == '__main__':
    main()
