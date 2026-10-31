def levenshtein(a, b):
    n, m = len(a), len(b)
    # tabla (n+1) x (m+1) llena de ceros
    D = [[0] * (m + 1) for _ in range(n + 1)] # se crea una matriz de tamaño (n+1) x (m+1) para almacenar las distancias de Levenshtein entre los prefijos de las cadenas a y b. Cada celda D[i][j] representa la distancia de Levenshtein entre los primeros i caracteres de a y los primeros j caracteres de b.

    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j

    for i in range(1, n + 1): # recorrer cada caracter de a
        for j in range(1, m + 1):
            costo = 0 if a[i-1] == b[j-1] else 1 # se compara el caracter i-1 de a con el caracter j-1 de b
            D[i][j] = min(
                D[i-1][j] + 1,        # borrar
                D[i][j-1] + 1,        # insertar
                D[i-1][j-1] + costo)   # sustituir
            
    return D[n][m]


def similitud_levenshtein(a, b):
    if max(len(a), len(b)) == 0:
        return 1.0
    return 1 - levenshtein(a, b) / max(len(a), len(b)) # La función `similitud_levenshtein` calcula la similitud entre dos cadenas `a` y `b` utilizando la distancia de Levenshtein. La similitud se define como 1 menos la distancia de Levenshtein normalizada por la longitud máxima de las dos cadenas. Si ambas cadenas están vacías, la similitud se considera 1.0.


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
            pares.append((similitud_levenshtein(tokens[i], tokens[j]), i + 1, j + 1)) # La función `similitud_levenshtein` se llama para cada par de tokens (abstracts preprocesados) y se almacena la similitud junto con los índices de los abstracts en la lista `pares`. Los índices se incrementan en 1 para que sean más legibles (ya que las listas en Python son 0-indexadas). Esto permite comparar todos los abstracts entre sí y obtener una lista de similitudes para su posterior análisis.
    fin = time.perf_counter()
    pares.sort(reverse=True)

    print(f"190 pares en {fin - inicio:.2f} s")
    print("Top 5 pares más parecidos:")
    for sim, i, j in pares[:5]: # Se imprimen los 5 pares de abstracts más similares, mostrando la similitud y los índices de los abstracts correspondientes. La lista `pares` se ha ordenado previamente en orden descendente de similitud, por lo que los primeros 5 elementos representan los pares más similares.
        print(f"  {i}-{j}: {sim:.4f}")