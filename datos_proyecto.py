"""Huella de los datos y del código que produce las matrices."""
import hashlib
import json
from pathlib import Path
RAIZ = Path(__file__).resolve().parent
FUENTES = ['preprocesamiento.py', 'jaccard.py', 'tfidf_coseno.py', 'levenshtein.py',
           'needleman_wusch.py', 'embeddings_word2vec.py', 'matrices.py']


def huella(corpus):
    datos = json.dumps(corpus, ensure_ascii=False, sort_keys=True).encode('utf8')
    return hashlib.sha256(datos).hexdigest()


def huella_codigo():
    contenido = b''.join((RAIZ / nombre).read_text(encoding='utf-8-sig').replace('\r\n', '\n').encode('utf8') for nombre in FUENTES)
    return hashlib.sha256(contenido).hexdigest()


def cargar_resultados():
    corpus = json.loads((RAIZ / 'corpus.json').read_text(encoding='utf8'))
    matrices = json.loads((RAIZ / 'matrices.json').read_text(encoding='utf8'))
    meta = json.loads((RAIZ / 'resultados/procedencia.json').read_text(encoding='utf8'))
    if meta['corpus_sha256'] != huella(corpus) or meta['codigo_sha256'] != huella_codigo():
        raise ValueError('Resultados desactualizados. Ejecuta python matrices.py y las demostraciones.')
    return corpus, matrices

