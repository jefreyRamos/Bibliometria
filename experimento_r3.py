import csv
import json
from medicion import medir, BUSCADORES
from datos_proyecto import huella


def main():
    corpus = json.load(open('corpus.json', encoding='utf8'))
    base = ' '.join(d['abstract'].lower() for d in corpus)
    filas = []
    for factor in [1, 2, 4, 8]:
        texto = (base + '\n') * factor
        for patron in ['generative', 'large language models', 'artificial intelligence in education']:
            for nombre in BUSCADORES:
                r, preparacion, busqueda = medir(nombre, texto, patron)
                filas.append([len(texto), len(patron), patron, nombre, len(r[0]), r[1], preparacion, busqueda, huella(corpus)])
    with open('resultados_r3.csv', 'w', newline='', encoding='utf8') as f:
        w = csv.writer(f)
        w.writerow(['n','m','patron','algoritmo','encontradas','comparaciones','preparacion_ms','busqueda_ms','corpus_sha256'])
        w.writerows(filas)
    print('36 mediciones; mediana de 7 repeticiones; preparación y búsqueda separadas.')


if __name__ == '__main__':
    main()
