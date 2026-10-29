def levenshtein(a, b):
    n, m = len(a), len(b)
    # tabla (n+1) x (m+1) llena de ceros
    D = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            costo = 0 if a[i-1] == b[j-1] else 1
            D[i][j] = min(
                D[i-1][j] + 1,        # borrar
                D[i][j-1] + 1,        # insertar
                D[i-1][j-1] + costo)   # sustituir
            
    return D[n][m]


def similitud_levenshtein(a, b):
    if max(len(a), len(b)) == 0:
        return 1.0
    return 1 - levenshtein(a, b) / max(len(a), len(b))


if __name__ == "__main__":
    import json, time
    from preprocesamiento import preprocesar

    with open("corpus.json", encoding="utf-8") as f:
        corpus = json.load(f)
    tokens = [preprocesar(a["abstract"]) for a in corpus]

    print("Distancia(1, 2) =", levenshtein(tokens[0], tokens[1]))
    print("Similitud(1, 2) =", round(similitud_levenshtein(tokens[0], tokens[1]), 4))

    inicio = time.perf_counter()
    pares = []
    for i in range(len(tokens)):
        for j in range(i + 1, len(tokens)):
            pares.append((similitud_levenshtein(tokens[i], tokens[j]), i + 1, j + 1))
    fin = time.perf_counter()
    pares.sort(reverse=True)

    print(f"190 pares en {fin - inicio:.2f} s")
    print("Top 5 pares más parecidos:")
    for sim, i, j in pares[:5]:
        print(f"  {i}-{j}: {sim:.4f}")