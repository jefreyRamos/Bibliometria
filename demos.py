"""Genera el documento de casos con datos reales y resultados completos."""
import json
import math
from pathlib import Path
from datos_proyecto import cargar_resultados, huella
from preprocesamiento import preprocesar
from tfidf_coseno import calcular_idf, vector_tfidf, coseno
from levenshtein import tabla_levenshtein
from needleman_wusch import needleman_wunsch, traceback
from embeddings_word2vec import coseno_denso
from clustering import clustering_jerarquico, distancia_clusters
from silhouette import cortar, silhouette
from Kmp import kmp, tabla_lps
from boyer_moore import boyer_moore, tabla_mal_caracter
from rabin_karp import rabin_karp, BASE, Q, preparar
from contextlib import redirect_stdout

def tabla(filas):
    for fila in filas:
        print('| ' + ' | '.join((str(x) for x in fila)) + ' |')

def mostrar_similitudes(corpus, matrices, tokens):
    print('## R1: artículos 1 y 2 completos\n')
    for d in corpus[:2]:
        print(f"### Artículo {d['id']}: {d['titulo']}\n")
        print(', '.join(d['autores']), '\n\n', d['abstract'], '\n')
    print('Resultados sobre todos los tokens (SBERT recibe el abstract original):\n')
    print('| Método | Similitud |\n|---|---:|')
    tabla([[k, v[0][1]] for k, v in matrices.items()])
    a, b = tokens[:2]
    sa, sb = (set(a), set(b))
    print(f'\nJaccard: tamaños {len(sa)}, {len(sb)}; intersección {len(sa & sb)}; unión {len(sa | sb)}. J={len(sa & sb)}/{len(sa | sb)}.\n')

def mostrar_matrices_pequenas(tokens):
    a, b = tokens[:2]
    print('## Ejemplo pequeño de programación dinámica\n')
    aa, bb = (a[:3], b[:3])
    print('Son los primeros tres tokens de cada abstract; NO sustituyen los resultados completos.\n')
    print('A =', aa, '; B =', bb, '\n')
    for nombre, F in [('Levenshtein', tabla_levenshtein(aa, bb)), ('Needleman-Wunsch', needleman_wunsch(aa, bb))]:
        print('###', nombre, '\n')
        print('| prefijo | vacío | ' + ' | '.join(bb) + ' |')
        print('|---|' + '---|' * (len(bb) + 1))
        tabla([['vacío' if i == 0 else aa[i - 1]] + fila for i, fila in enumerate(F)])
        print('\nCada celda interior, en orden de filas:\n```text')
        for i in range(1, len(aa) + 1):
            for j in range(1, len(bb) + 1):
                if nombre == 'Levenshtein':
                    costo = int(aa[i - 1] != bb[j - 1])
                    print(f'D[{i},{j}] = min({F[i - 1][j]}+1, {F[i][j - 1]}+1, {F[i - 1][j - 1]}+{costo}) = {F[i][j]}')
                else:
                    puntos = 1 if aa[i - 1] == bb[j - 1] else -1
                    print(f'F[{i},{j}] = max({F[i - 1][j - 1]}+({puntos}), {F[i - 1][j]}-1, {F[i][j - 1]}-1) = {F[i][j]}')
        print('```\n')
    F = needleman_wunsch(aa, bb)
    print('Alineamiento pequeño:', traceback(aa, bb, F), '\n')

def mostrar_tfidf(tokens, idf):
    a, b = tokens[:2]
    sa, sb = (set(a), set(b))
    print('## TF-IDF: conteos y operaciones del caso completo\n')
    va, vb = (vector_tfidf(a, idf), vector_tfidf(b, idf))
    print('N=20; TF=cantidad/longitud; IDF=ln(N/df). Vocabulario en orden alfabético, sin ranking.\n')
    print('| término | cA | cB | df | IDF | peso A | peso B | producto |\n|---|---:|---:|---:|---:|---:|---:|---:|')
    for t in sorted(sa | sb):
        df = sum((t in doc for doc in tokens))
        tabla([[t, a.count(t), b.count(t), df, round(idf[t], 6), round(va.get(t, 0), 8), round(vb.get(t, 0), 8), round(va.get(t, 0) * vb.get(t, 0), 10)]])
    producto = sum((va[t] * vb.get(t, 0) for t in va))
    na = math.sqrt(sum((x * x for x in va.values())))
    nb = math.sqrt(sum((x * x for x in vb.values())))
    print(f'\nLongitudes: {len(a)}, {len(b)}. Producto={producto}; normas={na}, {nb}. Coseno={producto}/({na}*{nb})={coseno(va, vb)}. Ángulo={math.degrees(math.acos(max(-1, min(1, coseno(va, vb)))))} grados.\n')

def mostrar_embeddings(vectores, matrices):
    print('## Embeddings: operación numérica completa\n')
    print('Word2Vec: gensim entrena vectores de palabras de 100 componentes, ventana 5, skip-gram, 100 épocas, semilla 42 y un trabajador. El vector documental promedia los vectores de sus tokens. SBERT usa all-MiniLM-L6-v2 y genera 384 componentes. Ver limitaciones de truncamiento y entrenamiento en DOCUMENTO_TECNICO.md.\n')
    for metodo in ['word2vec', 'sbert']:
        u, v = vectores[metodo][:2]
        p = sum((x * y for x, y in zip(u, v)))
        nu = math.sqrt(sum((x * x for x in u)))
        nv = math.sqrt(sum((x * x for x in v)))
        print(f'{metodo}: {len(u)} componentes. Primeras cinco (solo ilustración): {u[:5]} y {v[:5]}. Con TODAS: producto={p}; normas={nu},{nv}; coseno={coseno_denso(u, v)}. Vectores completos en resultados/vectores.json.\n')
    meta = json.loads(Path('resultados/procedencia.json').read_text(encoding='utf8'))
    print('SBERT: límite', meta['sbert_max_seq_length'], 'tokens del tokenizador; artículos truncados:', meta['sbert_articulos_truncados'], '\n')
    print(f"En este par Word2Vec={matrices['word2vec'][0][1]:.4f} y TF-IDF={matrices['tfidf'][0][1]:.4f}: comparten tema, pero los términos comunes pierden peso IDF y los vectores aprendidos con pocos documentos pueden ser poco discriminativos. Esto explica diferencias de escala, no valida un ganador.\n")
    print('Los seis valores no son calificaciones de calidad. Jaccard no usa frecuencia ni orden; TF-IDF distingue términos infrecuentes; edición y alineamiento penalizan cambios de orden; Word2Vec aprende de un corpus muy pequeño; SBERT incorpora entrenamiento externo y límites de longitud. No hay etiquetas humanas para concluir cuál comprende mejor estos artículos.\n')

def mostrar_fusiones(matrices):
    print('## R2: ejemplo pequeño, artículos 1, 2, 7 y 9\n')
    ids = [0, 1, 6, 8]
    S = matrices['tfidf']
    D = [[0.0 if i == j else max(0, 1 - S[i][j]) for j in ids] for i in ids]
    print('Distancia TF-IDF = 1 - coseno. Índices locales 0,1,2,3 corresponden a artículos 1,2,7,9.\n```text')
    for fila in D:
        print(fila)
    print('```\n')
    for criterio in ['single', 'complete', 'average']:
        Z = clustering_jerarquico(D, criterio)
        grupos = {i: [i] for i in range(4)}
        print('###', criterio, '\n```text')
        for paso, (x, y, d, n) in enumerate(Z):
            for ia in list(grupos):
                for ib in list(grupos):
                    if ia < ib:
                        dist = [D[i][j] for i in grupos[ia] for j in grupos[ib]]
                        print(f'Candidatos {ia},{ib}: distancias {dist}; {criterio}={distancia_clusters(grupos[ia], grupos[ib], D, criterio)}')
            print(f'Fusión {x},{y} a distancia {d}; nuevo grupo {4 + paso}')
            grupos[4 + paso] = grupos.pop(x) + grupos.pop(y)
        labels = cortar(Z, 4, 2)
        for i in range(4):
            mismo = [D[i][j] for j in range(4) if i != j and labels[i] == labels[j]]
            otros = [sum((D[i][j] for j in range(4) if labels[j] == g)) / labels.count(g) for g in set(labels) if g != labels[i]]
            ai = sum(mismo) / len(mismo) if mismo else 0
            bi = min(otros)
            si = (bi - ai) / max(ai, bi) if mismo and max(ai, bi) > 0 else 0
            print(f'i={i}: a={ai}; b={bi}; s={si} (singleton => 0)')
        print('Promedio silhouette:', silhouette(D, labels), '\n```\n')

def mostrar_evaluacion_completa(matrices):
    print('### Resultado sobre los 20 abstracts completos\n')
    print('Se conserva k=2 para comparar los tres criterios en cada representación.\n')
    for metodo, S in matrices.items():
        print('| Método | Enlace | k | Silhouette |\n|---|---|---:|---:|')
        D = [[0 if i == j else max(0, 1 - S[i][j]) for j in range(20)] for i in range(20)]
        puntuaciones = []
        for criterio in ['single', 'complete', 'average']:
            Z = clustering_jerarquico(D, criterio)
            valor = silhouette(D, cortar(Z, 20, 2))
            puntuaciones.append((criterio, valor))
            tabla([[metodo, criterio, 2, valor]])
        mayor = max((v for _, v in puntuaciones))
        print('\nMayor separación para', metodo, 'con k=2:', [c for c, v in puntuaciones if abs(v - mayor) < 1e-12], '. No demuestra coherencia temática.\n')

def mostrar_busqueda(corpus):
    print('## R3: fragmento real y resultado del abstract completo\n')
    patron = 'intelligence'
    doc = next((d for d in corpus if kmp(d['abstract'].lower(), patron)[0]))
    texto = doc['abstract'].lower()
    primera = kmp(texto, patron)[0][0]
    inicio = max(0, primera - 15)
    fragmento = texto[inicio:primera + len(patron) + 20]
    print(f"Artículo {doc['id']}, minúsculas; inicio del fragmento en abstract={inicio}. Patrón={patron}.\n\n`{fragmento}`\n")
    print('Preparación LPS: valor para cada prefijo del patrón (longitud de prefijo propio que también es sufijo):\n```text')
    for j in range(1, len(patron) + 1):
        print(patron[:j], tabla_lps(patron[:j])[-1])
    print('Tabla carácter malo: cada asignación reemplaza la última posición conocida:')
    ultima = {}
    for j, c in enumerate(patron):
        ultima[c] = j
        print(j, c, dict(ultima))
    h, hp = preparar(patron)
    acumulado = 0
    print(f'RK: h={BASE}^({len(patron)}-1) mod {Q}={h}')
    for c in patron:
        nuevo = (BASE * acumulado + ord(c)) % Q
        print(f'({BASE}*{acumulado}+{ord(c)}) mod {Q}={nuevo} (carácter {c})')
        acumulado = nuevo
    for nombre, fn in [('KMP', kmp), ('Boyer-Moore', boyer_moore), ('Rabin-Karp', rabin_karp)]:
        print('\n', nombre, 'traza del fragmento:')
        print('Resultado:', fn(fragmento, patron, traza=True))
        print('Resultado del abstract completo (posiciones desde cero):', fn(texto, patron))
    print('```\nLas comparaciones cuentan caracteres en búsqueda; RK también hace hashes no contados como comparaciones. Ver resultados_r3.csv para tiempos medidos por separado.')

def main():
    corpus, matrices = cargar_resultados()
    vectores = json.loads(Path('resultados/vectores.json').read_text(encoding='utf8'))
    tokens = [preprocesar(d['abstract']) for d in corpus]
    idf = calcular_idf(tokens)
    with open('docs/CASOS_REALES.md', 'w', encoding='utf8') as archivo:
        with redirect_stdout(archivo):
            print('# Casos reproducibles para la sustentación\n')
            print('Generar: `python demos.py`. Huella del corpus:', huella(corpus), '\n')
            mostrar_similitudes(corpus, matrices, tokens)
            mostrar_matrices_pequenas(tokens)
            mostrar_tfidf(tokens, idf)
            mostrar_embeddings(vectores, matrices)
            mostrar_fusiones(matrices)
            mostrar_evaluacion_completa(matrices)
            mostrar_busqueda(corpus)
    print('Generado docs/CASOS_REALES.md')
if __name__ == '__main__':
    main()
