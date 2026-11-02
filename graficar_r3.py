import csv
import matplotlib.pyplot as plt

filas = list(csv.DictReader(open("resultados_r3.csv", encoding="utf-8")))
m_max = max(int(f["m"]) for f in filas)
for alg in ["KMP", "Boyer-Moore", "Rabin-Karp"]:
    pts = sorted((int(f["n"]), float(f["tiempo_ms"])) for f in filas
                if f["algoritmo"] == alg and int(f["m"]) == m_max)
    plt.plot([p[0] for p in pts], [p[1] for p in pts], marker="o", label=alg)
plt.xlabel("Tamaño del texto n (caracteres)")
plt.ylabel("Tiempo (ms)")
plt.title(f"Tiempo vs n (m = {m_max}): los tres crecen lineal, O(n+m)")
plt.legend(); plt.grid(alpha=0.3)
plt.savefig("tiempos_r3.png", dpi=150, bbox_inches="tight")
print("Listo: tiempos_r3.png")