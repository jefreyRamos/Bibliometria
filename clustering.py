def distancia_clusters(A, B, D, criterio):
    distancias = []
    for i in A:
        for j in B:
            distancias.append(D[i][j])
    if criterio == "single":
        return min(distancias)
    elif criterio == "complete":
        return max(distancias)
    elif criterio == "average":
        return sum(distancias) / len(distancias)

def clustering_jerarquico(D, criterio):
    N = len(D)
    clusters = {i: [i] for i in range(N)}   # id del grupo -> documentos
    siguiente_id = N
    fusiones = []
    while len(clusters) > 1:
        mejor = None                         # (distancia, id_a, id_b)
        ids = list(clusters.keys())
        for x in range(len(ids)):
            for y in range(x + 1, len(ids)):
                d = distancia_clusters(clusters[ids[x]], clusters[ids[y]], D, criterio)
                if mejor is None or d < mejor[0]:
                    mejor = (d, ids[x], ids[y])
        d, a, b = mejor
        nuevo = clusters[a] + clusters[b]
        del clusters[a]
        del clusters[b]
        clusters[siguiente_id] = nuevo
        fusiones.append([a, b, d, len(nuevo)])
        siguiente_id += 1
    return fusiones

if __name__ == "__main__":
    # 4 puntos en una recta: 0, 1, 5, 6
    D = [[0, 1, 5, 6],
         [1, 0, 4, 5],
         [5, 4, 0, 1],
         [6, 5, 1, 0]]
    for criterio in ["single", "complete", "average"]:
        print(criterio, clustering_jerarquico(D, criterio))