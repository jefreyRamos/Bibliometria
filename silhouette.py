import json
from clustering import clustering_jerarquico

def cortar(fusiones, N, k):
    """Repite las primeras N-k fusiones y devuelve el grupo de cada documento."""
    grupos = {i: [i] for i in range(N)}
    siguiente = N
    for a, b, d, t in fusiones[:N - k]:
        grupos[siguiente] = grupos[a] + grupos[b]
        del grupos[a]
        del grupos[b]
        siguiente += 1
    etiquetas = [0] * N
    for num, docs in enumerate(grupos.values()):
        for doc in docs:
            etiquetas[doc] = num
    return etiquetas


def silhouette(D, etiquetas):
    N = len(D)
    total = 0.0
    for i in range(N):
        mismo = [D[i][j] for j in range(N) if j != i and etiquetas[j] == etiquetas[i]]
        if len(mismo) == 0:          # grupo de un solo documento: s(i) = 0
            continue
        a = sum(mismo) / len(mismo)
        b = None
        for g in set(etiquetas):
            if g == etiquetas[i]:
                continue
            otro = [D[i][j] for j in range(N) if etiquetas[j] == g]
            if len(otro) == 0:
                continue
            b = min(b, sum(otro) / len(otro)) if b is not None else sum(otro) / len(otro) # si todavía no tengo b, tomo este promedio; si ya tengo, me quedo con el menor
        if b is None:                # no hay otro grupo: s(i) = 0
            continue
        total += (b - a) / max(a, b)
    if N == 0:
        return 0.0
    return total / N


if __name__ == "__main__":
    D4 = [[0, 1, 5, 6], [1, 0, 4, 5], [5, 4, 0, 1], [6, 5, 1, 0]]
    print("Prueba:", round(silhouette(D4, [0, 0, 1, 1]), 3))   # debe dar 0.798

    with open("matrices.json", encoding="utf-8") as f:
        S = json.load(f)["sbert"]
    N = len(S)
    D = [[1 - S[i][j] for j in range(N)] for i in range(N)]

    for criterio in ["single", "complete", "average"]:
        fusiones = clustering_jerarquico(D, criterio)
        for k in range(2, 7):
            s = silhouette(D, cortar(fusiones, N, k))
            print(f"{criterio:9s} k={k}  silhouette={s:.4f}")