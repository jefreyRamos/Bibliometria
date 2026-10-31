import json, time
from gensim.models import Word2Vec
from sentence_transformers import SentenceTransformer
from preprocesamiento import preprocesar
from jaccard import jaccard_similarity
from tfidf_coseno import calcular_idf, vector_tfidf, coseno
from levenshtein import similitud_levenshtein
from needleman_wusch import similitud_nw
from embeddings_word2vec import vector_promedio, coseno_denso

def matriz(n, f):
    M = [[1.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            M[i][j] = M[j][i] = round(float(f(i, j)), 4)
    return M

with open("corpus.json", encoding="utf-8") as f:
    corpus = json.load(f)
textos = [a["abstract"] for a in corpus]
tokens = [preprocesar(t) for t in textos]
N = len(tokens)

idf = calcular_idf(tokens)
v_tfidf = [vector_tfidf(t, idf) for t in tokens]
w2v = Word2Vec(sentences=tokens, vector_size=100, window=5,
               min_count=1, sg=1, epochs=100, seed=42, workers=1)
v_w2v = [vector_promedio(t, w2v) for t in tokens]
v_sbert = [list(map(float, v)) for v in SentenceTransformer("all-MiniLM-L6-v2").encode(textos)]

metodos = {
    "jaccard":     lambda i, j: jaccard_similarity(tokens[i], tokens[j]),
    "tfidf":       lambda i, j: coseno(v_tfidf[i], v_tfidf[j]),
    "levenshtein": lambda i, j: similitud_levenshtein(tokens[i], tokens[j]),
    "needleman":   lambda i, j: similitud_nw(tokens[i], tokens[j]),
    "word2vec":    lambda i, j: coseno_denso(v_w2v[i], v_w2v[j]),
    "sbert":       lambda i, j: coseno_denso(v_sbert[i], v_sbert[j]),
}

resultado = {}
for nombre, f in metodos.items():
    inicio = time.perf_counter()
    resultado[nombre] = matriz(N, f)
    print(f"{nombre:12s} {time.perf_counter() - inicio:.3f} s")

with open("matrices.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=1)
print("Guardado matrices.json")