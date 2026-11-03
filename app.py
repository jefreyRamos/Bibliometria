import json, time
import streamlit as st
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from clustering import clustering_jerarquico
from silhouette import cortar, silhouette
from Kmp import kmp
from boyer_moore import boyer_moore
from rabin_karp import rabin_karp

st.set_page_config(page_title="Bibliometría - Análisis de Algoritmos", layout="wide")

def cargar():
    from datos_proyecto import cargar_resultados
    return cargar_resultados()

try:
    corpus, matrices = cargar()
except (ValueError, FileNotFoundError) as error:
    st.error(str(error))
    st.stop()
N = len(corpus)
nombres = [f'{d["id"]}. {d["titulo"][:80]}' for d in corpus]
METODOS = {"Jaccard": "jaccard", "Coseno TF-IDF": "tfidf", "Levenshtein": "levenshtein",
        "Needleman-Wunsch": "needleman", "Word2Vec": "word2vec", "Sentence-BERT": "sbert"}
BUSQUEDA = {"KMP": kmp, "Boyer-Moore": boyer_moore, "Rabin-Karp": rabin_karp}

st.sidebar.title("Bibliometría")
st.sidebar.caption("Análisis de Algoritmos 2026-2 · Universidad del Quindío")
pagina = st.sidebar.radio("Sección", ["Corpus", "R1 · Similitud", "R2 · Clustering", "R3 · Búsqueda de patrones"])

if pagina == "Corpus":
    st.header("Corpus: 20 artículos sobre IA en educación")
    st.dataframe([{"#": d["id"], "Título": d["titulo"], "Autores": ", ".join(d["autores"])}
                for d in corpus], width="stretch", hide_index=True)
    i = st.selectbox("Ver el abstract de:", range(N), format_func=lambda k: nombres[k])
    st.write(corpus[i]["abstract"])

elif pagina == "R1 · Similitud":
    st.header("R1 · Similitud textual entre abstracts")
    elegidos = st.multiselect("Elige dos o más artículos", range(N), default=[0, 1],
                              format_func=lambda k: nombres[k])
    if len(elegidos) < 2:
        st.warning("Elige al menos dos artículos.")
    else:
        st.subheader("Similitud por pares según los 6 métodos")
        pares = [{"Par": f"{a + 1} - {b + 1}",
                  **{nombre: round(matrices[clave][a][b], 4) for nombre, clave in METODOS.items()}}
                 for x, a in enumerate(elegidos) for b in elegidos[x + 1:]]
        st.dataframe(pares, width="stretch", hide_index=True)
    st.caption("Las escalas miden aspectos distintos. Un valor mayor no prueba que el método sea mejor.")
    st.subheader("Matriz de similitud 20×20")
    metodo = st.selectbox("Método", list(METODOS), index=5)
    fig, ax = plt.subplots(figsize=(7, 6))
    M = [[None if i == j else matrices[METODOS[metodo]][i][j] for j in range(N)] for i in range(N)]
    im = ax.imshow([[float("nan") if v is None else v for v in fila] for fila in M], cmap="viridis")
    ax.set_xticks(range(N), [str(k + 1) for k in range(N)])
    ax.set_yticks(range(N), [str(k + 1) for k in range(N)])
    fig.colorbar(im)
    st.pyplot(fig)

elif pagina == "R2 · Clustering":
    st.header("R2 · Clustering jerárquico aglomerativo")
    c1, c2, c3 = st.columns(3)
    metodo = c1.selectbox("Matriz de similitud", list(METODOS), index=5)
    criterio = c2.radio("Criterio de enlace", ["single", "complete", "average"], horizontal=True)
    k = c3.slider("Número de grupos (k)", 2, 6, 2)
    S = matrices[METODOS[metodo]]
    D = [[1 - S[i][j] for j in range(N)] for i in range(N)]
    fusiones = clustering_jerarquico(D, criterio)
    fig, ax = plt.subplots(figsize=(12, 5))
    dendrogram(fusiones, labels=[str(i + 1) for i in range(N)], ax=ax)
    ax.set_ylabel("distancia = 1 - similitud")
    ax.set_title(f"{criterio} · {metodo}")
    st.pyplot(fig)
    comparacion = []
    for enlace in ['single', 'complete', 'average']:
        arbol = clustering_jerarquico(D, enlace)
        comparacion.append({'Enlace': enlace, 'k': k, 'Silhouette': silhouette(D, cortar(arbol, N, k))})
    st.dataframe(comparacion, hide_index=True)
    st.caption('Mayor silhouette indica separación según esta distancia y este k; no demuestra calidad temática. Puede haber empates.')
    etiquetas = cortar(fusiones, N, k)
    st.metric("Coeficiente silhouette", f"{silhouette(D, etiquetas):.4f}")
    for g in sorted(set(etiquetas)):
        docs = [i + 1 for i in range(N) if etiquetas[i] == g]
        st.write(f"**Grupo {g + 1}** ({len(docs)} artículos): {docs}")

else:
    st.header("R3 · Búsqueda de patrones en los abstracts")
    patron = st.text_input("Patrón a buscar", "generative")
    ignorar = st.checkbox('Ignorar mayúsculas', value=False)
    if ignorar:
        patron = patron.lower()
    st.caption('Posiciones desde cero en el abstract mostrado (o convertido a minúsculas si se activa la opción). Patrón vacío: ninguna coincidencia.')
    if patron:
        filas, resumen = [], []
        for nombre, f in BUSQUEDA.items():
            comparaciones, encontradas = 0, 0
            from medicion import PREPARADORES, BUSCADORES
            t0 = time.perf_counter()
            preparado = PREPARADORES[nombre](patron)
            preparacion_ms = (time.perf_counter() - t0) * 1000
            t = 0.0
            for d in corpus:
                texto = d['abstract'].lower() if ignorar else d['abstract']
                inicio = time.perf_counter()
                r = BUSCADORES[nombre](texto, patron, preparado)
                t += (time.perf_counter() - inicio) * 1000
                comparaciones += r[1]
                encontradas += len(r[0])
                if nombre == "KMP" and r[0]:
                    filas.append({"#": d["id"], "Título": d["titulo"],
                                "Autores": ", ".join(d["autores"]), "Apariciones": len(r[0]), "Posiciones": str(r[0])})
            resumen.append({"Algoritmo": nombre, "Apariciones": encontradas,
                            "Comparaciones de caracteres": comparaciones, "Preparación (ms)": preparacion_ms, "Búsqueda (ms)": t})
        st.subheader("Comparación de los 3 algoritmos")
        st.dataframe(resumen, width="stretch", hide_index=True)
        st.subheader(f"Artículos donde aparece «{patron}»")
        st.dataframe(filas, width="stretch", hide_index=True)