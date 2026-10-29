import math


def calcular_idf(documentos):
    """documentos: lista de listas de tokens. Devuelve {palabra: idf}."""
    N = len(documentos)
    df = {}
    for doc in documentos:
        for palabra in set(doc):
            df[palabra] = df.get(palabra, 0) + 1 # cuenta cuántas veces aparece cada palabra
    idf = {}
    for palabra in df:
        idf[palabra] = math.log(N / df[palabra]) # calcula el idf de cada palabra
    return idf


def vector_tfidf(tokens, idf):
    """Devuelve {palabra: peso tf-idf} para un documento."""
    conteo = {}
    for palabra in tokens: # cuenta cuántas veces aparece cada palabra
        conteo[palabra] = conteo.get(palabra, 0) + 1
    vector = {}
    for palabra in conteo: # calcula el tf-idf de cada palabra
        tf = conteo[palabra] / len(tokens)
        vector[palabra] = tf * idf.get(palabra, 0)
        pass
    return vector


def coseno(v1, v2):
    """Similitud del coseno entre dos vectores-diccionario."""
    producto = 0.0
    for palabra in v1: # suma el producto de los pesos tf-idf de las palabras que aparecen en ambos vectores
        if palabra in v2:
            producto += v1[palabra] * v2[palabra] # producto escalar
    norma1 = math.sqrt(sum(p * p for p in v1.values()))
    norma2 = math.sqrt(sum(p * p for p in v2.values()))
    if norma1 == 0 or norma2 == 0:
        return 0.0
    return producto / (norma1 * norma2)

if __name__ == "__main__":
    import json
    from preprocesamiento import preprocesar

    with open("corpus.json", encoding="utf-8") as f:
        corpus = json.load(f)

    tokens = [preprocesar(a["abstract"]) for a in corpus]
    idf = calcular_idf(tokens)
    vectores = [vector_tfidf(t, idf) for t in tokens]

    print("Coseno(1, 2) =", round(coseno(vectores[0], vectores[1]), 4))

    pares = []
    for i in range(len(vectores)):
        for j in range(i + 1, len(vectores)):
            pares.append((coseno(vectores[i], vectores[j]), i + 1, j + 1))
    pares.sort(reverse=True)

    print("Top 5 pares más parecidos:")
    for sim, i, j in pares[:5]:
        print(f"  {i}-{j}: {sim:.4f}")