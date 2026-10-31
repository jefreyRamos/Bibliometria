import json
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from clustering import clustering_jerarquico

with open("matrices.json", encoding="utf-8") as f:
    matrices = json.load(f)
S = matrices["sbert"]
N = len(S)
D = [[1 - S[i][j] for j in range(N)] for i in range(N)]
etiquetas = [str(i + 1) for i in range(N)]

fig, ejes = plt.subplots(1, 3, figsize=(18, 5))
for eje, criterio in zip(ejes, ["single", "complete", "average"]):
    fusiones = clustering_jerarquico(D, criterio)
    dendrogram(fusiones, labels=etiquetas, ax=eje)
    eje.set_title(f"{criterio} (SBERT)")
    eje.set_ylabel("distancia = 1 - similitud")
plt.tight_layout()
plt.savefig("dendrogramas_sbert.png", dpi=150)
print("Guardado dendrogramas_sbert.png")