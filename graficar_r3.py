import csv
import matplotlib.pyplot as plt
from datos_proyecto import huella
import json

filas = list(csv.DictReader(open('resultados_r3.csv', encoding='utf8')))
corpus = json.load(open('corpus.json', encoding='utf8'))
if any(f['corpus_sha256'] != huella(corpus) for f in filas):
    raise ValueError('Regenerar experimento_r3.py para el corpus actual')
m_max = max(int(f['m']) for f in filas)
fig, ejes = plt.subplots(1, 2, figsize=(12, 4))
for eje, campo, titulo in zip(ejes, ['preparacion_ms','busqueda_ms'], ['Preparación del patrón','Búsqueda en el texto']):
    for alg in ['KMP','Boyer-Moore','Rabin-Karp']:
        pts = sorted((int(f['n']),float(f[campo])) for f in filas if f['algoritmo']==alg and int(f['m'])==m_max)
        eje.plot([p[0] for p in pts],[p[1] for p in pts],marker='o',label=alg)
    eje.set_xlabel('n (caracteres)')
    eje.set_ylabel('Mediana observada (ms)')
    eje.set_title(f'{titulo}, m={m_max}')
    eje.legend(); eje.grid(alpha=0.3)
fig.suptitle('Mediciones en este equipo; no son una demostración de Big O')
fig.tight_layout()
fig.savefig('tiempos_r3.png', dpi=150)
