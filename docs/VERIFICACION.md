# Verificación del 3 de noviembre de 2026

Trabajo directo en el checkout original; `git status --short` estaba limpio al comenzar. No se creó otra copia ni se modificaron los PDF originales. Se usó la habilidad PDF para leer el enunciado completo y comprobar visualmente sus tres páginas y las primeras páginas de los artículos 7 y 9.

## Estado por requisito

| Requisito | Implementación y evidencia | Estado |
|---|---|---|
| Corpus | 20 abstracts, límites explícitos, listas completas de autores publicadas; pruebas de reextracción y revisión especial de 7 y 9 | Comprobado con pypdf 6.21.4 |
| R1 | Cuatro algoritmos explícitos, Word2Vec y Sentence-BERT; selección múltiple; seis matrices 20×20 | Regenerado y probado |
| R1 matemático | Dos abstracts completos, tabla de seis resultados, matrices pequeñas y cada celda, conteos y pesos TF-IDF, productos y normas densos | docs/CASOS_REALES.md |
| R2 | Tres enlaces propios; dendrogramas; comparación silhouette con igual matriz y k; caso de cuatro artículos y evaluación completa | Probado y regenerado |
| R3 | Preparadores separados y tres buscadores explícitos; solapamientos, vacíos y patrón largo; trazas con patrón real intelligence | Probado |
| R3 rendimiento | 36 filas, mediana de 7 repeticiones, preparación y búsqueda separadas, contraste teórico y limitaciones | Regenerado |
| R4 documentación | Arquitectura, fórmulas, variables, ejecución, instrucciones de despliegue y guía de sustentación | Preparado |
| R4 despliegue público | Falta destino/URL pública comprobable | Pendiente |
| Declaración IA | Borrador explícito, incluye modificación directa del código | Revisión estudiantil pendiente; falta documento adicional del profesor |

## Pruebas ejecutadas

`python -m unittest discover -s tests -v`: **6 pruebas, todas OK**. La prueba exhaustiva compara 128 textos (incluido uno Unicode) con 34 patrones, usando tres envoltorios y tres búsquedas con patrón preparado: 26 112 verificaciones de resultados frente a un recorrido de referencia. Incluye textos vacíos, patrones vacíos, patrones largos y solapamientos. También se verificaron distancias conocidas, puntaje NW, TF-IDF, casos nulos, extracción de los 20 archivos y metadatos.

Las matrices se verificaron como seis matrices simétricas 20×20, con diagonal 1 y valores válidos. Se recalcularon las cuatro similitudes clásicas para el par 7–9; los cosenos densos se verificaron contra los vectores guardados. Se comprobó que una huella distinta del corpus rechaza los resultados. Las alturas de los tres enlaces se compararon con SciPy y silhouette con scikit-learn para la matriz TF-IDF de los 20 artículos. Esas implementaciones de referencia se usan solo en pruebas, nunca para producir los resultados de la aplicación.

`python tests/comprobar_app.py`: **OK** mediante Streamlit AppTest. Se probaron Corpus (7 y 9), selección de tres artículos en R1, advertencia al elegir solo uno, tres enlaces en R2, k=6, búsqueda vacía, patrón ausente más largo que cualquier abstract, generative y sensibilidad a mayúsculas. Los tres algoritmos reportaron el mismo total de ocurrencias.

Se regeneraron `corpus.json`, `matrices.json`, `resultados/vectores.json`, `resultados/procedencia.json`, `docs/CASOS_REALES.md`, ambas demostraciones .txt, `resultados_r3.csv` y las dos gráficas. Se inspeccionaron visualmente los tres dendrogramas y la gráfica de tiempos. No se hizo inspección visual de la interfaz en un navegador ni verificación HTTP pública; AppTest comprueba la ejecución y elementos de la aplicación, no su aspecto en todos los tamaños de pantalla.

## Particularidades del entorno y límites

El alias `python` de Windows no ejecutaba un intérprete y `py` no detectó una instalación. Se utilizó Python 3.12 del runtime de Codex y se instalaron las dependencias en `.deps/` dentro del proyecto, excluida de Git. Para esos comandos se configuró PYTHONPATH con `.deps` (y la raíz al ejecutar AppTest). Las instrucciones normales del README usan un entorno virtual propio. La instalación de dependencias y descarga del modelo necesitaron acceso de red autorizado. El aislamiento bloqueó sockets internos de asyncio; AppTest se completó correctamente fuera del aislamiento con autorización. Los intentos bloqueados se detuvieron.

Una primera comparación de reextracción detectó diferencias de espacios con la versión del lector del runtime. Se regeneró el corpus con la versión fijada en requirements.txt y después se regeneró todo el conjunto de resultados; no se reutilizaron matrices antiguas.

Sentence-BERT tiene límite de **256 tokens de su tokenizador**. En esta ejecución truncó los artículos **3, 4, 5, 7, 8, 10, 12, 13, 15, 17, 18, 19 y 20**. Los artículos 1 y 2 del caso principal no fueron truncados. Las longitudes están en procedencia.json; no se disimula esta limitación cambiando los textos ni añadiendo otro algoritmo. Los resultados «completos» se refieren a la ejecución sobre cada entrada de abstract, sujeta a ese límite del modelo.

No se afirma que exista despliegue público. Para cerrar R4, seguir README, abrir la URL desde otro equipo y registrar URL, fecha y comprobaciones. El equipo estudiantil debe validar la comprensión del diseño y revisar la declaración IA antes de entregar.

## Ejemplo de tiempos observados

Patrón de 36 caracteres; medianas de 7 ejecuciones. El tamaño mayor es repetición sintética del corpus.

| n | Algoritmo | Preparación ms | Búsqueda ms |
|---:|---|---:|---:|
| 28268 | KMP | 0.003800 | 3.166200 |
| 28268 | Boyer-Moore | 0.002500 | 0.737400 |
| 28268 | Rabin-Karp | 0.008800 | 6.850500 |
| 226144 | KMP | 0.010600 | 26.292800 |
| 226144 | Boyer-Moore | 0.004400 | 6.030600 |
| 226144 | Rabin-Karp | 0.013700 | 56.432600 |

En esta muestra Boyer–Moore por carácter malo tardó menos en buscar este patrón; esto no cambia su peor caso O(nm). La preparación no depende de n: sus fluctuaciones son ruido de medición. RK hace actualizaciones modulares y verificaciones por colisiones; menos comparaciones de caracteres no implica menor tiempo.

## Corrección del arranque local

Se añadió `.streamlit/config.toml` con `global.developmentMode=false`: la instalación en `.deps` hacía que Streamlit activara modo de desarrollo y esperara la interfaz en el puerto 3000. Tras reiniciar el servidor se verificó HTTP 200 en `/` con el HTML de Streamlit y HTTP 200 `ok` en `/_stcore/health` del puerto 8501. Esta verificación es local; el despliegue público continúa pendiente.
