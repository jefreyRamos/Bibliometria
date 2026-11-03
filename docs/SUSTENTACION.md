# Guía breve de sustentación

1. Abrir el corpus: mostrar que solo el campo abstract entra al análisis. Enseñar los límites de 7 y 9 y sus autores completos. Explicar normalización y por qué no se borran palabras para arreglar extracción.
2. Seleccionar artículos 1 y 2. Mostrar los seis resultados de los abstracts completos en CASOS_REALES.md. Explicar qué información conserva o pierde cada representación.
3. Usar el ejemplo pequeño señalado: tres tokens reales de cada abstract. Dibujar inicialización y llenar cada celda con min para Levenshtein y max para NW. Mostrar el traceback y la diferencia entre puntaje y porcentaje de identidad.
4. Elegir una fila de la tabla TF-IDF: contar ocurrencias, dividir por longitud, contar documentos con el término, aplicar ln(20/df), multiplicar pesos. Después sumar productos y dividir por normas. No confundir el ejemplo de un término con el coseno del documento completo.
5. Explicar que las librerías generan embeddings; nuestros ciclos promedian Word2Vec y calculan coseno de los vectores densos. Mostrar producto y normas completos, no calcular similitud solo con cinco componentes. Aclarar escasez de datos Word2Vec y truncamiento SBERT.
6. Dibujar las cuatro hojas 1,2,7,9 del ejemplo y seguir los candidatos de cada fusión. Single=min, complete=max, average=promedio de pares. Calcular a, b, s de un documento y luego el promedio. Comparar los 20 con igual matriz y k; mencionar empates y ausencia de etiquetas humanas.
7. Mostrar el fragmento real y el patrón intelligence. Recorrer LPS, última aparición, un fallo y desplazamiento BM, hash inicial y actualización modular RK. Mostrar resultados del abstract completo y solapamiento con AAAAA/AA como prueba adicional sintética.
8. Abrir el CSV: identificar preparación y búsqueda separadas. Contrastar mediciones con cotas teóricas sin inferir complejidad de una sola ejecución. Explicar qué cuenta comparaciones y qué no.
9. Presentar pruebas y estado real del despliegue. Leer y adaptar la declaración de IA. Cada integrante debe poder seguir una celda, una fusión y un desplazamiento sin depender de la herramienta.
