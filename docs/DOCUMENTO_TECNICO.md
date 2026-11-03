# Bibliometría: documento técnico y arquitectura

## Alcance y correspondencia con el enunciado

Se leyó completo el documento del profesor (3 páginas). R1 exige selección de dos o más artículos, cuatro métodos clásicos explícitos y dos enfoques de embeddings; R2 exige tres enlaces, dendrogramas y evaluación interna; R3 exige KMP, Boyer–Moore y Rabin–Karp, trazas y contraste entre preparación, búsqueda y Big O; R4 exige despliegue y documentación. El enunciado no fija fórmulas concretas de normalización ni exige algoritmos de ordenamiento o rankings de palabras.

La aplicación selecciona artículos y consulta las seis matrices calculadas sobre el corpus fijo. Esto evita entrenar modelos cada vez que se selecciona un par. TF-IDF y Word2Vec se ajustan sobre los 20 abstracts, no solo sobre el subconjunto seleccionado. No cambia su resultado al seleccionar otros artículos.

## Organización sin capas adicionales

- Raíz: `app.py` presenta los datos; los módulos de similitud, clustering y búsqueda contienen los algoritmos explícitos. Se conserva su organización y los métodos correctos del proyecto original.
- `pdfs/`: los 20 originales. `datos/limites_pdf.json`: títulos, autores y límites auditables. `corpus.json`: exclusivamente abstracts como texto de análisis, más metadatos separados.
- `matrices.py`: calcula seis matrices; `datos_proyecto.py`: verifica huellas de corpus y código. `resultados/`: procedencia y vectores completos.
- `demos.py`: genera `docs/CASOS_REALES.md`; `demo_r1.py` y `demo_r3.py`: demostraciones complementarias. `experimento_r3.py`: mediciones reproducibles.
- `tests/`: pruebas. `docs/`: documentación y sustentación. `scripts/`: utilidades de mantenimiento, no necesarias para ejecutar la aplicación.

Flujo: PDF → extracción y normalización → corpus → preprocesamiento/vectorización → seis matrices → distancias → agrupamiento y evaluación → aplicación. La búsqueda opera directamente sobre el abstract, sin eliminar stopwords.

## Extracción y metadatos

El corpus es estático: se usan límites inicial y final por artículo, en su página 1. Si falta uno, la extracción falla explícitamente antes de guardar el corpus. No es un extractor general de cualquier PDF. Los límites y listas completas de autores se cotejaron con el texto de la primera página; los metadatos PDF omitían coautores en varios casos. Se conservan los nombres tal como se publican, incluidas iniciales: no se inventan expansiones de iniciales.

Artículo 7: se inicia en «The rapid expansion», después de las palabras clave intercaladas; termina en «future human-centred LA/AIED systems.». Artículo 9: termina en «development efforts.», antes del párrafo «Since Alan Turing»; no hay encabezado Introduction inmediato. El corte genérico por Introduction incluiría texto ajeno al abstract.

Se unen palabras divididas por guion al final de línea y se normalizan ligaduras Unicode y espacios. No se elimina `fig` ni ninguna otra palabra para disimular contaminación. Estas transformaciones pueden afectar la representación literal del PDF; el corpus es la versión normalizada que ve la aplicación. Los metadatos no participan en las similitudes.

## R1: fórmulas elegidas y correspondencia con el código

Son convenciones habituales elegidas para este proyecto; el PDF no afirma que el profesor haya enseñado estas fórmulas.

`preprocesar` convierte a minúsculas, conserva caracteres alfanuméricos y excluye stopwords y tokens de longitud 1. Jaccard, TF-IDF, Levenshtein, NW y Word2Vec reciben esos tokens; SBERT recibe el abstract normalizado sin quitar stopwords. La búsqueda exacta recibe los caracteres del abstract.

**Jaccard.** J(A,B)=|A∩B|/|A∪B|, donde A y B son conjuntos de tokens. Los ciclos cuentan intersección y unión. Dos conjuntos vacíos tienen similitud 0 por convención, conservando el método original; no hay evidencia léxica para comparar. No considera frecuencia ni orden.

**TF-IDF.** Para término t y documento d: TF(t,d)=c(t,d)/L(d), donde c es su conteo y L el número de tokens. DF(t) cuenta documentos que contienen t; IDF(t)=ln(N/DF(t)), N=20. El diccionario de pesos guarda TF·IDF. Se conserva esta versión sin suavizado: los términos presentes en todos los documentos pesan cero. Coseno(u,v)=Σuᵢvᵢ/(√Σuᵢ² √Σvᵢ²). El ciclo suma productos y calcula las dos normas; vector nulo da 0. Ángulo=arccos(coseno), mostrado en grados en el caso de estudio.

**Levenshtein por tokens.** D[i,0]=i, D[0,j]=j. D[i,j]=min(D[i−1,j]+1, D[i,j−1]+1, D[i−1,j−1]+c), c=0 si los tokens coinciden y 1 en otro caso. Son borrar, insertar y sustituir. Similitud=1−D[n,m]/max(n,m); ambos vacíos dan 1. `tabla_levenshtein` expone la tabla que usa `levenshtein`.

**Needleman–Wunsch por tokens.** Coincidencia +1, sustitución −1, hueco −1. F[i,0]=−i, F[0,j]=−j. F[i,j]=max(F[i−1,j−1]+p, F[i−1,j]−1, F[i,j−1]−1), donde p depende de igualdad. Traceback prioriza diagonal, arriba, izquierda en empates. Se conserva la identidad del alineamiento: coincidencias/longitud del alineamiento, no el puntaje bruto normalizado. Dos vacíos dan 1. La identidad depende de la regla de desempate; un puntaje óptimo puede tener varios alineamientos.

**Word2Vec.** Gensim genera vectores de palabras mediante entrenamiento skip-gram sobre estos 20 abstracts; el vector documental es v(d)=Σv(token)/L(d), contando repeticiones. Configuración: 100 dimensiones, ventana 5, min_count=1, 100 épocas, seed=42, workers=1. `vector_promedio` suma cada componente con ciclos. `coseno_denso` calcula la fórmula anterior explícitamente. Corpus pequeño: no equivale a un modelo semántico ampliamente entrenado; puede producir cosenos altos poco discriminativos. La semilla y un trabajador ayudan a repetir, pero también influyen versiones y hashing de Python; ejecutar con PYTHONHASHSEED=0.

**Sentence-BERT.** SentenceTransformer all-MiniLM-L6-v2 genera embeddings densos de 384 dimensiones; el coseno se calcula con el mismo ciclo explícito. El modelo puede truncar abstracts largos según su límite de tokens del tokenizador, diferente del conteo de palabras; esto debe considerarse al interpretar la comparación de abstracts completos. No se agregan otros algoritmos de segmentación. Las primeras componentes son ilustrativas: el resultado usa todas las dimensiones. Se guardan vectores completos para revisar producto y normas.

Los valores de los seis métodos no comparten una escala de calidad. No hay verdad de referencia anotada por humanos. Un coseno mayor no prueba superioridad frente a una similitud de edición menor.

## R2: enlaces y evaluación

D(i,j)=1−S(i,j); diagonal cero. Coseno negativo puede producir distancia mayor que 1: es válido. Los pares de grupos se recorren explícitamente; single toma el mínimo, complete el máximo y average el promedio de TODAS las distancias entre miembros (no promedio sin ponderar de grupos). Se fusiona el par de menor distancia; en empates se conserva el primero del recorrido. SciPy solo dibuja los dendrogramas: no calcula los enlaces.

Para cada artículo i: a(i) es el promedio de distancias a los demás miembros de su grupo; b(i) es el menor promedio de distancias hacia otro grupo. s(i)=(b−a)/max(a,b); singleton o denominador cero da 0. La evaluación global es Σs(i)/N, entre −1 y 1. Se comparan los tres enlaces usando la MISMA matriz y el MISMO k. Un valor mayor indica separación interna según esa representación; no demuestra coherencia temática ni superioridad universal. `CASOS_REALES.md` muestra candidatos, fusiones y cada término de silhouette para cuatro artículos; después presenta la comparación de los 20. Puede haber empates.

Esta implementación sencilla examina los pares de miembros para cada candidato en cada fusión: tiempo O(N³) y almacenamiento O(N²) con N documentos. La evaluación directa cuesta O(N²) para un k fijo. Se prioriza transparencia para N=20.

## R3: búsqueda y medición

Convención: patrón vacío devuelve ninguna coincidencia; patrón más largo también. Se devuelven todas las posiciones, desde cero, incluidas coincidencias solapadas. Búsqueda sensible a mayúsculas por defecto; la aplicación permite buscar en minúsculas explícitamente. No usa find ni index para resolver las ocurrencias. El extractor puede usar find para delimitar la sección del PDF, tarea distinta de R3.

- KMP: LPS[j] es la longitud del prefijo propio que también es sufijo de patron[:j+1]. Ante fallo j vuelve a LPS[j−1]; tras coincidencia también, conservando solapamientos. Preparación O(m), búsqueda O(n+m), memoria auxiliar O(m).
- Boyer–Moore: se conserva la variante permitida de carácter malo. El diccionario guarda la última posición de cada carácter; ante fallo en j desplaza max(1,j−ultima[carácter]); tras coincidencia usa el siguiente carácter del texto cuando existe. Preparación O(m), peor búsqueda O(nm), memoria O(m). No se atribuyen las garantías de variantes con sufijo bueno a esta implementación.
- Rabin–Karp: BASE=256 es base polinómica, no una restricción a ASCII; se usa ord para Unicode. Q=101 es primo pequeño para facilitar operaciones y mostrar colisiones. H=Σord(cᵢ)·BASE^(m−1−i) mod Q; h=BASE^(m−1) mod Q; nueva ventana=(BASE·(H−ord(saliente)·h)+ord(entrante)) mod Q. Hash igual obliga a verificar caracteres. Preparación O(m); búsqueda esperada O(n+m) bajo pocas colisiones; peor O(nm). Espacio auxiliar O(1), aparte de resultados. El primo pequeño puede aumentar verificaciones.

n=caracteres del texto, m=caracteres del patrón. Las cotas excluyen almacenar las posiciones encontradas. `medicion.py` prepara fuera del intervalo de búsqueda; RK incluye el hash de la primera ventana del texto en la búsqueda. El experimento usa mediana de 7 repeticiones, factores 1,2,4,8 y tres patrones reales; repetir texto es un ensayo sintético, no documentos nuevos. Los tiempos observados dependen del equipo y ruido; no demuestran Big O. Los conteos solo miden comparaciones de caracteres durante búsqueda; no equivalen al total de operaciones ni hacen directamente comparables los costos del hash y LPS. La aplicación mide una ejecución sobre los 20 abstracts, con una sola preparación compartida por algoritmo.

## Validación y entrega

Ejecutar las instrucciones del README. `docs/VERIFICACION.md` registra lo realmente comprobado. Las huellas impiden usar matrices del corpus anterior: al modificar corpus o los módulos declarados, regenerar matrices, casos, dendrogramas y mediciones como conjunto. La huella no sustituye una revisión humana del contenido de los PDF.

R4 requiere una URL pública comprobada. Preparar instrucciones no equivale a desplegar. El documento adicional con criterios de uso de IA mencionado por el profesor no fue suministrado: revisar la declaración de apoyo con ese material antes de entregar.

## Costos de R1

Con n y m tokens de los documentos, Levenshtein y NW llenan (n+1)(m+1) celdas: tiempo y espacio O(nm); traceback de NW O(n+m). Jaccard construye conjuntos y los recorre: O(n+m) esperado con tablas hash, espacio O(n+m). TF-IDF sobre T tokens del corpus construye DF y conteos en O(T) esperado; el coseno disperso recorre las entradas de los dos vectores en O(|u|+|v|), con espacio proporcional al vocabulario almacenado. El promedio Word2Vec cuesta O(L·d) para L tokens y d componentes, y coseno denso O(d). Estas cotas no incluyen entrenamiento Word2Vec ni inferencia SBERT: son trabajos de las librerías, dependientes de configuración y modelo; no se presentan como costo de un simple coseno. Se evalúan 20·19/2=190 pares por método. Los segundos impresos por matrices.py corresponden a comparaciones una vez preparados los vectores.
