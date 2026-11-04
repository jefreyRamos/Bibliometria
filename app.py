import json, time, html
import streamlit as st
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from clustering import clustering_jerarquico
from silhouette import cortar, silhouette
from Kmp import kmp
from boyer_moore import boyer_moore
from rabin_karp import rabin_karp

st.set_page_config(page_title="Bibliometría - Análisis de Algoritmos", layout="wide")

@st.cache_data
def cargar():
    with open("corpus.json", encoding="utf-8") as f:
        corpus = json.load(f)
    with open("matrices.json", encoding="utf-8") as f:
        matrices = json.load(f)
    return corpus, matrices

corpus, matrices = cargar()
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
    st.subheader("Matriz de similitud 20×20")
    metodo = st.selectbox("Método", list(METODOS), index=5)
    fig, ax = plt.subplots(figsize=(11, 9.5))
    M = [[None if i == j else matrices[METODOS[metodo]][i][j] for j in range(N)] for i in range(N)]
    im = ax.imshow([[float("nan") if v is None else v for v in fila] for fila in M], cmap="viridis")
    ax.set_xticks(range(N), [str(k + 1) for k in range(N)])
    ax.set_yticks(range(N), [str(k + 1) for k in range(N)])
    S = matrices[METODOS[metodo]]
    valores = [S[i][j] for i in range(N) for j in range(N) if i != j]
    medio = (min(valores) + max(valores)) / 2
    for i in range(N):
        for j in range(N):
            if i != j:
                ax.text(j, i, f"{S[i][j]:.2f}", ha="center", va="center", fontsize=6,
                        color="black" if S[i][j] > medio else "white")
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
    corte = (fusiones[N - k - 1][2] + fusiones[N - k][2]) / 2
    dendrogram(fusiones, labels=[str(i + 1) for i in range(N)], ax=ax,
            color_threshold=corte, above_threshold_color="gray")
    ax.axhline(corte, color="red", linestyle="--", linewidth=1, label=f"corte en k = {k}")
    ax.legend()
    ax.set_ylabel("distancia = 1 - similitud")
    ax.set_title(f"{criterio} · {metodo}")
    st.pyplot(fig)
    etiquetas = cortar(fusiones, N, k)
    st.metric("Coeficiente silhouette", f"{silhouette(D, etiquetas):.4f}")
    st.subheader("¿Qué criterio y qué k agrupan mejor?")
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    valores_k = range(2, 7)
    for c in ["single", "complete", "average"]:
        arbol = clustering_jerarquico(D, c)
        ax2.plot(valores_k, [silhouette(D, cortar(arbol, N, kk)) for kk in valores_k],
                marker="o", label=c)
    ax2.set_xlabel("número de grupos k")
    ax2.set_ylabel("silueta promedio")
    ax2.legend()
    ax2.grid(alpha=0.3)
    st.pyplot(fig2)
    for g in sorted(set(etiquetas)):
        docs = [i + 1 for i in range(N) if etiquetas[i] == g]
        st.write(f"**Grupo {g + 1}** ({len(docs)} artículos): {docs}")

else:
    st.header("R3 · Búsqueda de patrones en los abstracts")
    patron = st.text_input("Patrón a buscar", "generative").lower()
    if patron:
        filas, resumen = [], []
        for nombre, f in BUSQUEDA.items():
            comparaciones, encontradas = 0, 0
            t0 = time.perf_counter()
            for d in corpus:
                r = f(d["abstract"].lower(), patron)
                comparaciones += r[1]
                encontradas += len(r[0])
                if nombre == "KMP" and r[0]:
                    filas.append({"#": d["id"], "Título": d["titulo"],
                                "Apariciones": len(r[0]), "Posiciones": str(r[0][:10])})
            t = (time.perf_counter() - t0) * 1000
            resumen.append({"Algoritmo": nombre, "Apariciones": encontradas,
                            "Comparaciones": comparaciones, "Tiempo (ms)": round(t, 3)})
        st.subheader("Comparación de los 3 algoritmos")
        st.dataframe(resumen, width="stretch", hide_index=True)
        st.subheader(f"Artículos donde aparece «{patron}»")
        st.dataframe(filas, width="stretch", hide_index=True)
        st.subheader("Comparaciones vs. tiempo")
        nombres_alg = [r["Algoritmo"] for r in resumen]
        fig3, (ax_c, ax_t) = plt.subplots(1, 2, figsize=(10, 3.5))
        ax_c.bar(nombres_alg, [r["Comparaciones"] for r in resumen], color=["tab:blue", "tab:orange", "tab:green"])
        ax_c.set_title("Comparaciones de caracteres")
        ax_t.bar(nombres_alg, [r["Tiempo (ms)"] for r in resumen], color=["tab:blue", "tab:orange", "tab:green"])
        ax_t.set_title("Tiempo (ms)")
        for i, r in enumerate(resumen):
            ax_c.text(i, r["Comparaciones"], f'{r["Comparaciones"]}', ha="center", va="bottom")
            ax_t.text(i, r["Tiempo (ms)"], f'{r["Tiempo (ms)"]:.2f}', ha="center", va="bottom")
        st.pyplot(fig3)
        st.caption("Rabin-Karp compara pocas letras (solo cuando los hashes coinciden), "
                "pero calcula un hash en cada ventana del texto; por eso puede tardar más.")

        # --- B: texto con el patrón resaltado ---
        if filas:
            st.subheader("Patrón resaltado en el abstract")
            elegido = st.selectbox("Artículo", [fila["#"] for fila in filas],
                                format_func=lambda i: nombres[i - 1])
            texto = corpus[elegido - 1]["abstract"]
            posiciones = kmp(texto.lower(), patron)[0]
            partes, ultimo = [], 0
            for p in posiciones:
                partes.append(html.escape(texto[ultimo:p]))
                partes.append(f"<mark>{html.escape(texto[p:p + len(patron)])}</mark><sub>{p}</sub>")
                ultimo = p + len(patron)
            partes.append(html.escape(texto[ultimo:]))
            st.markdown("".join(partes), unsafe_allow_html=True)
            st.caption("El número pequeño es la posición que devuelve el algoritmo (desde 0).")