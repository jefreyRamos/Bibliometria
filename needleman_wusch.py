MATCH, MISMATCH, GAP = 1, -1, -1

def needleman_wunsch(a, b):
    n, m = len(a), len(b)
    F = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        F[i][0] = i * GAP
    for j in range(1, m + 1):
        F[0][j] = j * GAP
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            puntos = MATCH if a[i-1] == b[j-1] else MISMATCH
            F[i][j] = max(F[i-1][j-1] + puntos,   # alinear
                          F[i-1][j] + GAP,        # hueco en b
                          F[i][j-1] + GAP)        # hueco en a
    return F


def traceback(a, b, F):
    i, j = len(a), len(b)
    alin_a, alin_b = [], []
    while i > 0 or j > 0:
        puntos = MATCH if i > 0 and j > 0 and a[i-1] == b[j-1] else MISMATCH
        if i > 0 and j > 0 and F[i][j] == F[i-1][j-1] + puntos:   # diagonal
            alin_a.append(a[i-1]); alin_b.append(b[j-1])
            i -= 1; j -= 1
        elif i > 0 and F[i][j] == F[i-1][j] + GAP:                 # arriba
            alin_a.append(a[i-1]); alin_b.append("-")
            i -= 1
        else:                                                      # izquierda
            alin_a.append("-"); alin_b.append(b[j-1])
            j -= 1
    alin_a.reverse()
    alin_b.reverse()
    return alin_a, alin_b


def similitud_nw(a, b):
    F = needleman_wunsch(a, b)
    alin_a, alin_b = traceback(a, b, F)
    if len(alin_a) == 0:
        return 1.0
    coincidencias = 0
    for k in range(len(alin_a)):
        if alin_a[k] == alin_b[k]:
            coincidencias += 1
    return coincidencias / len(alin_a)


if __name__ == "__main__":
    import json, time
    from preprocesamiento import preprocesar

    F = needleman_wunsch("GATTACA", "GCATGCU")
    A, B = traceback("GATTACA", "GCATGCU", F)
    print("Puntaje:", F[-1][-1])          # 0
    print("".join(A))                     # G-ATTACA
    print("".join(B))                     # GCA-TGCU
    print(similitud_nw("GATTACA", "GCATGCU"))  # 0.5

    with open("corpus.json", encoding="utf-8") as f:
        corpus = json.load(f)
    tokens = [preprocesar(a["abstract"]) for a in corpus]

    F = needleman_wunsch(tokens[0], tokens[1])
    print("Puntaje(1, 2) =", F[-1][-1])
    print("Similitud(1, 2) =", round(similitud_nw(tokens[0], tokens[1]), 4))

    inicio = time.perf_counter()
    pares = []
    for i in range(len(tokens)):
        for j in range(i + 1, len(tokens)):
            pares.append((similitud_nw(tokens[i], tokens[j]), i + 1, j + 1))
    fin = time.perf_counter()
    pares.sort(reverse=True)

    print(f"190 pares en {fin - inicio:.2f} s")
    print("Top 5 pares más parecidos:")
    for sim, i, j in pares[:5]:
        print(f"  {i}-{j}: {sim:.4f}")