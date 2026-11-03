import json, time, csv
from Kmp import kmp
from boyer_moore import boyer_moore
from rabin_karp import rabin_karp

def medir(f, texto, patron, repeticiones=5):
    mejor = None
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        r = f(texto, patron)
        t = time.perf_counter() - t0
        if mejor is None or t < mejor:
            mejor = t
    return r, mejor

with open("corpus.json", encoding="utf-8") as f:
    corpus = json.load(f)
base = " ".join(a["abstract"].lower() for a in corpus)
print("Caracteres del texto base:", len(base))

patrones = ["generative", "large language models", "artificial intelligence in education"]
algoritmos = [("KMP", kmp), ("Boyer-Moore", boyer_moore), ("Rabin-Karp", rabin_karp)]
filas = []
for factor in [1, 2, 4, 8]:
    texto = base * factor
    for patron in patrones:
        for nombre, f in algoritmos:
            r, t = medir(f, texto, patron)
            filas.append([len(texto), len(patron), nombre, len(r[0]), r[1], round(t * 1000, 3)])
            print(f"n={len(texto):7d} m={len(patron):2d} {nombre:12s} "
                  f"encontradas={len(r[0]):4d} comparaciones={r[1]:7d} tiempo={t*1000:8.2f} ms")

with open("resultados_r3.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["n", "m", "algoritmo", "encontradas", "comparaciones", "tiempo_ms"])
    w.writerows(filas)
print("Guardado resultados_r3.csv")