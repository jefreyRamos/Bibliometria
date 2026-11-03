"""Demostración paso a paso de R3 con un patrón real sobre un fragmento de un abstract.
Ejecutar:  python -X utf8 demo_r3.py > demo_r3.txt
"""
import json
from Kmp import kmp, tabla_lps
from boyer_moore import boyer_moore, tabla_mal_caracter
from rabin_karp import rabin_karp

PATRON = "generative"

with open("corpus.json", encoding="utf-8") as f:
    corpus = json.load(f)

# Primer abstract que contiene el patrón y un fragmento corto alrededor de la primera aparición.
# (el "in" y el find de aquí solo eligen el fragmento de la demo; la búsqueda la hacen los 3 algoritmos)
doc = next(d for d in corpus if PATRON in d["abstract"].lower())
abstract = doc["abstract"].lower()
inicio = max(0, abstract.find(PATRON) - 40)
texto = abstract[inicio:inicio + 100]

print(f"Artículo {doc['id']}: {doc['titulo']}")
print(f"Patrón: '{PATRON}'  (m = {len(PATRON)})")
print(f"Fragmento del abstract (n = {len(texto)}):")
print(f"'{texto}'\n")

print("=" * 70)
print("KMP")
print("Tabla LPS:", tabla_lps(PATRON))
pos, comp = kmp(texto, PATRON, traza=True)
print(f"Resultado KMP: posiciones={pos}, comparaciones={comp}\n")

print("=" * 70)
print("BOYER-MOORE (regla del carácter malo)")
print("Tabla de carácter malo:", tabla_mal_caracter(PATRON))
pos, comp = boyer_moore(texto, PATRON, traza=True)
print(f"Resultado BM: posiciones={pos}, comparaciones={comp}\n")

print("=" * 70)
print("RABIN-KARP")
pos, comp, col = rabin_karp(texto, PATRON, traza=True)
print(f"Resultado RK: posiciones={pos}, comparaciones={comp}, colisiones={col}\n")

print("=" * 70)
print(f"Comprobación: texto[{pos[0]}:{pos[0] + len(PATRON)}] = '{texto[pos[0]:pos[0] + len(PATRON)]}'" if pos else "No se encontró")
