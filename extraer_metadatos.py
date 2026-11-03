"""Actualiza metadatos desde la transcripción revisada, sin perder coautores."""
import json
from pathlib import Path


def main():
    corpus = json.loads(Path('corpus.json').read_text(encoding='utf8'))
    limites = json.loads(Path('datos/limites_pdf.json').read_text(encoding='utf8'))
    por_id = {d['id']: d for d in limites}
    for doc in corpus:
        fuente = por_id[doc['id']]
        doc['titulo'] = fuente['titulo']
        doc['autores'] = fuente['autores']
    Path('corpus.json').write_text(json.dumps(corpus, ensure_ascii=False, indent=2), encoding='utf8')


if __name__ == '__main__':
    main()
