import json
from sentence_transformers import SentenceTransformer
from embeddings_word2vec import coseno_denso

if __name__ == "__main__":
    with open("corpus.json", encoding="utf-8") as f:
        corpus = json.load(f)
    textos = [a["abstract"] for a in corpus]

    modelo = SentenceTransformer("all-MiniLM-L6-v2")
    vectores = [list(v) for v in modelo.encode(textos)]
    print("Dimensión del vector:", len(vectores[0]))

    print("Coseno(1, 2) =", round(coseno_denso(vectores[0], vectores[1]), 4))
    pares = []
    for i in range(len(vectores)):
        for j in range(i + 1, len(vectores)):
            pares.append((coseno_denso(vectores[i], vectores[j]), i + 1, j + 1))
    pares.sort(reverse=True)
    print("Top 5:")
    for sim, i, j in pares[:5]:
        print(f"  {i}-{j}: {sim:.4f}")