import json, math
from gensim.models import Word2Vec
from preprocesamiento import preprocesar

def vector_promedio(tokens, modelo):
    suma = [0.0] * modelo.vector_size
    cuenta = 0
    for palabra in tokens:
        if palabra in modelo.wv:
            v = modelo.wv[palabra]
            for k in range(len(suma)):
                suma[k] += v[k]
            cuenta += 1
    if cuenta == 0:
        return suma
    return [x / cuenta for x in suma]

def coseno_denso(u, v):
    producto = 0.0
    for k in range(len(u)):
        producto += u[k] * v[k]
    norma_u = math.sqrt(sum(x * x for x in u))
    norma_v = math.sqrt(sum(x * x for x in v))
    if norma_u == 0 or norma_v == 0:
        return 0.0
    return producto / (norma_u * norma_v)

if __name__ == "__main__":
    with open("corpus.json", encoding="utf-8") as f:
        corpus = json.load(f)
    tokens = [preprocesar(a["abstract"]) for a in corpus]

    modelo = Word2Vec(sentences=tokens, vector_size=100, window=5,
                      min_count=1, sg=1, epochs=100, seed=42, workers=1)
    vectores = [vector_promedio(t, modelo) for t in tokens]

    print("Coseno(1, 2) =", round(coseno_denso(vectores[0], vectores[1]), 4))
    pares = []
    for i in range(len(vectores)):
        for j in range(i + 1, len(vectores)):
            pares.append((coseno_denso(vectores[i], vectores[j]), i + 1, j + 1))
    pares.sort(reverse=True)
    print("Top 5:")
    for sim, i, j in pares[:5]:
        print(f"  {i}-{j}: {sim:.4f}")