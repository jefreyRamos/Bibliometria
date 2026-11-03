"""Genera todas las matrices del mismo corpus; ejecutar desde la raíz."""
import json
import time
import os
import importlib.metadata
from pathlib import Path
from gensim.models import Word2Vec
from sentence_transformers import SentenceTransformer
from datos_proyecto import huella, huella_codigo
from preprocesamiento import preprocesar
from jaccard import jaccard_similarity
from tfidf_coseno import calcular_idf, vector_tfidf, coseno
from levenshtein import similitud_levenshtein
from needleman_wusch import similitud_nw
from embeddings_word2vec import vector_promedio, coseno_denso


def matriz(n, comparar):
    resultado = [[1.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            valor = max(-1.0, min(1.0, float(comparar(i, j))))
            resultado[i][j] = resultado[j][i] = valor
    return resultado


def guardar(ruta, contenido):
    temporal = Path(str(ruta) + '.tmp')
    temporal.write_text(json.dumps(contenido, ensure_ascii=False, indent=2), encoding='utf8')
    temporal.replace(ruta)


def main():
    corpus = json.loads(Path('corpus.json').read_text(encoding='utf8'))
    textos = [d['abstract'] for d in corpus]
    tokens = [preprocesar(t) for t in textos]
    idf = calcular_idf(tokens)
    v_tfidf = [vector_tfidf(t, idf) for t in tokens]
    w2v = Word2Vec(sentences=tokens, vector_size=100, window=5,
                   min_count=1, sg=1, epochs=100, seed=42, workers=1)
    v_w2v = [[float(x) for x in vector_promedio(t, w2v)] for t in tokens]
    modelo = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    v_sbert = [[float(x) for x in v] for v in modelo.encode(textos)]
    longitudes = [len(modelo.tokenizer(t)['input_ids']) for t in textos]
    metodos = {
        'jaccard': lambda i,j: jaccard_similarity(tokens[i],tokens[j]),
        'tfidf': lambda i,j: coseno(v_tfidf[i],v_tfidf[j]),
        'levenshtein': lambda i,j: similitud_levenshtein(tokens[i],tokens[j]),
        'needleman': lambda i,j: similitud_nw(tokens[i],tokens[j]),
        'word2vec': lambda i,j: coseno_denso(v_w2v[i],v_w2v[j]),
        'sbert': lambda i,j: coseno_denso(v_sbert[i],v_sbert[j]),
    }
    resultado = {}
    for nombre, comparar in metodos.items():
        inicio = time.perf_counter()
        resultado[nombre] = matriz(len(corpus), comparar)
        print(nombre, round(time.perf_counter()-inicio,3), 'segundos (comparación de vectores/textos; excluye entrenamiento)')
    Path('resultados').mkdir(exist_ok=True)
    guardar('resultados/vectores.json', {'word2vec':v_w2v,'sbert':v_sbert})
    guardar('matrices.json', resultado)
    # Se escribe al final: una ejecución fallida no certifica matrices antiguas.
    guardar('resultados/procedencia.json', {
        'corpus_sha256':huella(corpus), 'codigo_sha256':huella_codigo(),
        'sbert_modelo':'sentence-transformers/all-MiniLM-L6-v2',
        'sbert_revision':getattr(modelo[0].auto_model.config, '_commit_hash', None),
        'sbert_max_seq_length':modelo.max_seq_length,
        'sbert_longitudes_tokenizador':longitudes,
        'sbert_articulos_truncados':[d['id'] for d,n in zip(corpus,longitudes) if n>modelo.max_seq_length],
        'word2vec':{'dimensiones':100,'window':5,'epochs':100,'seed':42,'workers':1,'sg':1,'min_count':1},
        'pythonhashseed':os.environ.get('PYTHONHASHSEED','no fijado'),
        'versiones':{p:importlib.metadata.version(p) for p in ['gensim','sentence-transformers','torch','numpy']}
    })


if __name__ == '__main__':
    main()
