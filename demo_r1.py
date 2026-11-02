import json, math
from preprocesamiento import preprocesar
from jaccard import jaccard_similarity
from tfidf_coseno import calcular_idf, vector_tfidf, coseno
from levenshtein import levenshtein, similitud_levenshtein
from needleman_wusch import needleman_wunsch, traceback, similitud_nw

with open("corpus.json", encoding="utf-8") as f:
    corpus = json.load(f)
A, B = corpus[0], corpus[1]
ta, tb = preprocesar(A["abstract"]), preprocesar(B["abstract"])
todos = [preprocesar(d["abstract"]) for d in corpus]

print("=== PASO 0: PREPROCESAMIENTO ===")
print(f"A: {len(A['abstract'].split())} palabras -> {len(ta)} tokens. Primeros 12: {ta[:12]}")
print(f"B: {len(B['abstract'].split())} palabras -> {len(tb)} tokens. Primeros 12: {tb[:12]}")

print("\n=== 1. JACCARD ===")
sa, sb = set(ta), set(tb)
comunes = [p for p in sa if p in sb]
inter = len(comunes)
union = len(sa) + len(sb) - inter
print(f"|A| = {len(sa)}  |B| = {len(sb)}  |A∩B| = {inter}  |A∪B| = {len(sa)} + {len(sb)} - {inter} = {union}")
print("Palabras en común:", sorted(comunes))
print(f"J = {inter} / {union} = {jaccard_similarity(ta, tb):.4f}")

print("\n=== 2. TF-IDF + COSENO ===")
idf = calcular_idf(todos)
va, vb = vector_tfidf(ta, idf), vector_tfidf(tb, idf)
aportes = sorted([(va[p] * vb[p], p) for p in va if p in vb], reverse=True)
print("Palabras que más aportan al producto punto:")
for ap, p in aportes[:5]:
    print(f"  {p:15s} idf={idf[p]:.3f}  A={va[p]:.4f}  B={vb[p]:.4f}  aporte={ap:.6f}")
prod = sum(ap for ap, _ in aportes)
na = math.sqrt(sum(v * v for v in va.values()))
nb = math.sqrt(sum(v * v for v in vb.values()))
print(f"A·B = {prod:.6f}  ||A|| = {na:.4f}  ||B|| = {nb:.4f}")
print(f"cos = {prod:.6f} / ({na:.4f} x {nb:.4f}) = {coseno(va, vb):.4f}")

print("\n=== 3. LEVENSHTEIN (por tokens) ===")
d = levenshtein(ta, tb)
print(f"Tabla de {len(ta) + 1} x {len(tb) + 1} = {(len(ta) + 1) * (len(tb) + 1)} celdas")
print(f"Distancia = {d}  ->  similitud = 1 - {d}/{max(len(ta), len(tb))} = {similitud_levenshtein(ta, tb):.4f}")

print("\n=== 4. NEEDLEMAN-WUNSCH ===")
F = needleman_wunsch(ta, tb)
al_a, al_b = traceback(ta, tb, F)
coinc = [al_a[k] for k in range(len(al_a)) if al_a[k] == al_b[k]]
print(f"Puntaje = {F[-1][-1]}  longitud del alineamiento = {len(al_a)}")
print("Primeras 12 posiciones del alineamiento:")
for k in range(12):
    print(f"  {al_a[k]:15s} | {al_b[k]:15s} {'<- coinciden' if al_a[k] == al_b[k] else ''}")
print("Tokens que quedaron alineados:", coinc)
print(f"Identidad = {len(coinc)} / {len(al_a)} = {similitud_nw(ta, tb):.4f}")

print("\n=== 5 y 6. EMBEDDINGS (de matrices.json) ===")
with open("matrices.json", encoding="utf-8") as f:
    M = json.load(f)
print(f"Word2Vec (promedio de vectores de 100 dim) = {M['word2vec'][0][1]:.4f}")
print(f"Sentence-BERT (vector de 384 dim)          = {M['sbert'][0][1]:.4f}")