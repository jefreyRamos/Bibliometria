"""Extracción para los 20 PDF estáticos: límites explícitos auditables en datos/."""
import json
import re
import unicodedata
from pathlib import Path
from pypdf import PdfReader

RAIZ = Path(__file__).resolve().parent


def normalizar(texto):
    # Espacio espurio antes de ligadura y palabras partidas al final de línea.
    texto = re.sub(r'(\w) +([ﬁﬂ])', r'\1\2', texto)
    texto = re.sub(r'(\w) *-\s*\n\s*(\w)', r'\1\2', texto)
    return ' '.join(unicodedata.normalize('NFKC', texto).split())


def extraer_abstract(ruta_pdf, limite):
    texto = normalizar(PdfReader(ruta_pdf).pages[limite['pagina'] - 1].extract_text())
    inicio = texto.find(limite['inicio'])
    fin = texto.find(limite['fin'], inicio)
    if inicio < 0 or fin < inicio:
        raise ValueError(f"No se verificaron los límites de {ruta_pdf}; revisar el PDF")
    return texto[inicio:fin + len(limite['fin'])]


def main():
    limites = json.loads((RAIZ / 'datos/limites_pdf.json').read_text(encoding='utf8'))
    archivos = set(p.name for p in (RAIZ / 'pdfs').glob('*.pdf'))
    if len(limites) != 20 or archivos != set(d['archivo'] for d in limites):
        raise ValueError('Se requieren exactamente los 20 PDF del manifiesto')
    corpus = []
    for limite in limites:
        doc = {k: limite[k] for k in ('id', 'archivo', 'titulo', 'autores')}
        doc['abstract'] = extraer_abstract(RAIZ / 'pdfs' / doc['archivo'], limite)
        corpus.append(doc)
        print(doc['id'], len(doc['abstract']), 'caracteres')
    (RAIZ / 'corpus.json').write_text(json.dumps(corpus, ensure_ascii=False, indent=2), encoding='utf8')


if __name__ == '__main__':
    main()
