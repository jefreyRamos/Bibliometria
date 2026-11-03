# Casos reproducibles para la sustentación

Generar: `python demos.py`. Huella del corpus: fb78daaca64f8412cbd5730f60a7253324dfa02826200fe3504e848c93a6566a 

## R1: artículos 1 y 2 completos

### Artículo 1: Artificial intelligence literacy in higher and adult education: A scoping literature review

Matthias Carl Laupichler, Alexandra Aster, Jana Schirch, Tobias Raupach 

 Since artificial intelligence (AI) is finding its way into more and more areas of everyday life, improving the AI skills of non-experts is important and will become even more relevant in the future. While it is necessary that children learn about the possibilities of AI at an early age, adults in higher education and beyond should also have at least a basic understanding of AI (i.e., AI literacy) to be able to interact effectively with the technology. To evaluate the current state of the literature on AI literacy in higher and adult education, a scoping literature review was conducted with the objective of identifying thematic foci and recent research trends. Ten research databases were searched and out of 902 initial records, 30 studies were identified using predefined eligibility criteria, whereof the content was evaluated in the review. The results indicated that research in this area is still in its infancy and needs refinement in terms of how to define AI literacy in adult education as well as what content should be taught to non-experts. Lastly, several recommendations for research and practice are derived from the results. 

### Artículo 2: Systematic literature review on opportunities, challenges, and future research recommendations of artificial intelligence in education

Thomas K.F. Chiu, Qi Xia, Xinyan Zhou, Ching Sing Chai, Miaoting Cheng 

 Applications of artificial intelligence in education (AIEd) are emerging and are new to researchers and practitioners alike. Reviews of the relevant literature have not examined how AI technologies have been integrated into each of the four key educational domains of learning, teaching, assessment, and administration. The relationships between the technologies and learning outcomes for students and teachers have also been neglected. This systematic review study aims to understand the opportunities and challenges of AIEd by examining the literature from the last 10 years (2012–2021) using matrix coding and content analysis approaches. The results present the current focus of AIEd research by identifying 13 roles of AI technologies in the key educational domains, 7 learning outcomes of AIEd, and 10 major challenges. The review also provides suggestions for future directions of AIEd research. 

Resultados sobre todos los tokens (SBERT recibe el abstract original):

| Método | Similitud |
|---|---:|
| jaccard | 0.1 |
| tfidf | 0.03464423714898264 |
| levenshtein | 0.058252427184465994 |
| needleman | 0.07547169811320754 |
| word2vec | 0.8262544527923138 |
| sbert | 0.5897856449207447 |

Jaccard: tamaños 82, 61; intersección 13; unión 130. J=13/130.

## Ejemplo pequeño de programación dinámica

Son los primeros tres tokens de cada abstract; NO sustituyen los resultados completos.

A = ['since', 'artificial', 'intelligence'] ; B = ['applications', 'artificial', 'intelligence'] 

### Levenshtein 

| prefijo | vacío | applications | artificial | intelligence |
|---|---|---|---|---|
| vacío | 0 | 1 | 2 | 3 |
| since | 1 | 1 | 2 | 3 |
| artificial | 2 | 2 | 1 | 2 |
| intelligence | 3 | 3 | 2 | 1 |

Cada celda interior, en orden de filas:
```text
D[1,1] = min(1+1, 1+1, 0+1) = 1
D[1,2] = min(2+1, 1+1, 1+1) = 2
D[1,3] = min(3+1, 2+1, 2+1) = 3
D[2,1] = min(1+1, 2+1, 1+1) = 2
D[2,2] = min(2+1, 2+1, 1+0) = 1
D[2,3] = min(3+1, 1+1, 2+1) = 2
D[3,1] = min(2+1, 3+1, 2+1) = 3
D[3,2] = min(1+1, 3+1, 2+1) = 2
D[3,3] = min(2+1, 2+1, 1+0) = 1
```

### Needleman-Wunsch 

| prefijo | vacío | applications | artificial | intelligence |
|---|---|---|---|---|
| vacío | 0 | -1 | -2 | -3 |
| since | -1 | -1 | -2 | -3 |
| artificial | -2 | -2 | 0 | -1 |
| intelligence | -3 | -3 | -1 | 1 |

Cada celda interior, en orden de filas:
```text
F[1,1] = max(0+(-1), -1-1, -1-1) = -1
F[1,2] = max(-1+(-1), -2-1, -1-1) = -2
F[1,3] = max(-2+(-1), -3-1, -2-1) = -3
F[2,1] = max(-1+(-1), -1-1, -2-1) = -2
F[2,2] = max(-1+(1), -2-1, -2-1) = 0
F[2,3] = max(-2+(-1), -3-1, 0-1) = -1
F[3,1] = max(-2+(-1), -2-1, -3-1) = -3
F[3,2] = max(-2+(-1), 0-1, -3-1) = -1
F[3,3] = max(0+(1), -1-1, -1-1) = 1
```

Alineamiento pequeño: (['since', 'artificial', 'intelligence'], ['applications', 'artificial', 'intelligence']) 

## TF-IDF: conteos y operaciones del caso completo

N=20; TF=cantidad/longitud; IDF=ln(N/df). Vocabulario en orden alfabético, sin ranking.

| término | cA | cB | df | IDF | peso A | peso B | producto |
|---|---:|---:|---:|---:|---:|---:|---:|
| 10 | 0 | 2 | 1 | 2.995732 | 0 | 0.07584132 | 0.0 |
| 13 | 0 | 1 | 1 | 2.995732 | 0 | 0.03792066 | 0.0 |
| 2012 | 0 | 1 | 1 | 2.995732 | 0 | 0.03792066 | 0.0 |
| 2021 | 0 | 1 | 1 | 2.995732 | 0 | 0.03792066 | 0.0 |
| 30 | 1 | 0 | 2 | 2.302585 | 0.0223552 | 0 | 0.0 |
| 902 | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| able | 1 | 0 | 2 | 2.302585 | 0.0223552 | 0 | 0.0 |
| administration | 0 | 1 | 1 | 2.995732 | 0 | 0.03792066 | 0.0 |
| adult | 2 | 0 | 1 | 2.995732 | 0.05816956 | 0 | 0.0 |
| adults | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| age | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| ai | 7 | 2 | 18 | 0.105361 | 0.00716042 | 0.00266735 | 1.90994e-05 |
| aied | 0 | 5 | 7 | 1.049822 | 0 | 0.06644444 | 0.0 |
| aims | 0 | 1 | 4 | 1.609438 | 0 | 0.02037263 | 0.0 |
| alike | 0 | 1 | 1 | 2.995732 | 0 | 0.03792066 | 0.0 |
| analysis | 0 | 1 | 7 | 1.049822 | 0 | 0.01328889 | 0.0 |
| applications | 0 | 1 | 8 | 0.916291 | 0 | 0.01159862 | 0.0 |
| approaches | 0 | 1 | 5 | 1.386294 | 0 | 0.01754803 | 0.0 |
| area | 1 | 0 | 2 | 2.302585 | 0.0223552 | 0 | 0.0 |
| areas | 1 | 0 | 3 | 1.89712 | 0.01841864 | 0 | 0.0 |
| artificial | 1 | 1 | 20 | 0.0 | 0.0 | 0.0 | 0.0 |
| assessment | 0 | 1 | 10 | 0.693147 | 0 | 0.00877401 | 0.0 |
| basic | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| become | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| beyond | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| challenges | 0 | 2 | 6 | 1.203973 | 0 | 0.03048032 | 0.0 |
| children | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| coding | 0 | 1 | 3 | 1.89712 | 0 | 0.02401418 | 0.0 |
| conducted | 1 | 0 | 8 | 0.916291 | 0.00889603 | 0 | 0.0 |
| content | 2 | 1 | 6 | 1.203973 | 0.02337811 | 0.01524016 | 0.0003562862 |
| criteria | 1 | 0 | 6 | 1.203973 | 0.01168906 | 0 | 0.0 |
| current | 1 | 1 | 8 | 0.916291 | 0.00889603 | 0.01159862 | 0.0001031816 |
| databases | 1 | 0 | 2 | 2.302585 | 0.0223552 | 0 | 0.0 |
| define | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| derived | 1 | 0 | 2 | 2.302585 | 0.0223552 | 0 | 0.0 |
| directions | 0 | 1 | 3 | 1.89712 | 0 | 0.02401418 | 0.0 |
| domains | 0 | 2 | 5 | 1.386294 | 0 | 0.03509606 | 0.0 |
| early | 1 | 0 | 2 | 2.302585 | 0.0223552 | 0 | 0.0 |
| education | 3 | 1 | 18 | 0.105361 | 0.00306875 | 0.00133368 | 4.0927e-06 |
| educational | 0 | 2 | 14 | 0.356675 | 0 | 0.00902975 | 0.0 |
| effectively | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| eligibility | 1 | 0 | 2 | 2.302585 | 0.0223552 | 0 | 0.0 |
| emerging | 0 | 1 | 4 | 1.609438 | 0 | 0.02037263 | 0.0 |
| evaluate | 1 | 0 | 2 | 2.302585 | 0.0223552 | 0 | 0.0 |
| evaluated | 1 | 0 | 2 | 2.302585 | 0.0223552 | 0 | 0.0 |
| even | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| everyday | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| examined | 0 | 1 | 3 | 1.89712 | 0 | 0.02401418 | 0.0 |
| examining | 0 | 1 | 2 | 2.302585 | 0 | 0.02914665 | 0.0 |
| experts | 2 | 0 | 2 | 2.302585 | 0.04471039 | 0 | 0.0 |
| finding | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| foci | 1 | 0 | 3 | 1.89712 | 0.01841864 | 0 | 0.0 |
| focus | 0 | 1 | 4 | 1.609438 | 0 | 0.02037263 | 0.0 |
| four | 0 | 1 | 3 | 1.89712 | 0 | 0.02401418 | 0.0 |
| future | 1 | 1 | 11 | 0.597837 | 0.00580424 | 0.00756756 | 4.39239e-05 |
| higher | 2 | 0 | 6 | 1.203973 | 0.02337811 | 0 | 0.0 |
| identified | 1 | 0 | 6 | 1.203973 | 0.01168906 | 0 | 0.0 |
| identifying | 1 | 1 | 2 | 2.302585 | 0.0223552 | 0.02914665 | 0.000651579 |
| important | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| improving | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| indicated | 1 | 0 | 3 | 1.89712 | 0.01841864 | 0 | 0.0 |
| infancy | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| initial | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| integrated | 0 | 1 | 1 | 2.995732 | 0 | 0.03792066 | 0.0 |
| intelligence | 1 | 1 | 20 | 0.0 | 0.0 | 0.0 | 0.0 |
| interact | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| key | 0 | 2 | 4 | 1.609438 | 0 | 0.04074526 | 0.0 |
| last | 0 | 1 | 2 | 2.302585 | 0 | 0.02914665 | 0.0 |
| lastly | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| learn | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| learning | 0 | 3 | 11 | 0.597837 | 0 | 0.02270267 | 0.0 |
| least | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| life | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| literacy | 3 | 0 | 2 | 2.302585 | 0.06706559 | 0 | 0.0 |
| literature | 2 | 2 | 11 | 0.597837 | 0.01160849 | 0.01513511 | 0.0001756958 |
| major | 0 | 1 | 2 | 2.302585 | 0 | 0.02914665 | 0.0 |
| matrix | 0 | 1 | 1 | 2.995732 | 0 | 0.03792066 | 0.0 |
| necessary | 1 | 0 | 2 | 2.302585 | 0.0223552 | 0 | 0.0 |
| needs | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| neglected | 0 | 1 | 1 | 2.995732 | 0 | 0.03792066 | 0.0 |
| new | 0 | 1 | 3 | 1.89712 | 0 | 0.02401418 | 0.0 |
| non | 2 | 0 | 1 | 2.995732 | 0.05816956 | 0 | 0.0 |
| objective | 1 | 0 | 2 | 2.302585 | 0.0223552 | 0 | 0.0 |
| opportunities | 0 | 1 | 4 | 1.609438 | 0 | 0.02037263 | 0.0 |
| out | 1 | 0 | 2 | 2.302585 | 0.0223552 | 0 | 0.0 |
| outcomes | 0 | 2 | 3 | 1.89712 | 0 | 0.04802835 | 0.0 |
| possibilities | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| practice | 1 | 0 | 5 | 1.386294 | 0.01345917 | 0 | 0.0 |
| practitioners | 0 | 1 | 1 | 2.995732 | 0 | 0.03792066 | 0.0 |
| predefined | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| present | 0 | 1 | 2 | 2.302585 | 0 | 0.02914665 | 0.0 |
| provides | 0 | 1 | 4 | 1.609438 | 0 | 0.02037263 | 0.0 |
| recent | 1 | 0 | 6 | 1.203973 | 0.01168906 | 0 | 0.0 |
| recommendations | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| records | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| refinement | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| relationships | 0 | 1 | 3 | 1.89712 | 0 | 0.02401418 | 0.0 |
| relevant | 1 | 1 | 7 | 1.049822 | 0.01019245 | 0.01328889 | 0.0001354463 |
| research | 4 | 2 | 16 | 0.223144 | 0.00866577 | 0.0056492 | 4.89547e-05 |
| researchers | 0 | 1 | 5 | 1.386294 | 0 | 0.01754803 | 0.0 |
| results | 2 | 1 | 8 | 0.916291 | 0.01779205 | 0.01159862 | 0.0002063632 |
| review | 2 | 2 | 18 | 0.105361 | 0.00204584 | 0.00266735 | 5.457e-06 |
| reviews | 0 | 1 | 6 | 1.203973 | 0 | 0.01524016 | 0.0 |
| roles | 0 | 1 | 1 | 2.995732 | 0 | 0.03792066 | 0.0 |
| scoping | 1 | 0 | 3 | 1.89712 | 0.01841864 | 0 | 0.0 |
| searched | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| several | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| since | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| skills | 1 | 0 | 3 | 1.89712 | 0.01841864 | 0 | 0.0 |
| state | 1 | 0 | 5 | 1.386294 | 0.01345917 | 0 | 0.0 |
| still | 1 | 0 | 5 | 1.386294 | 0.01345917 | 0 | 0.0 |
| students | 0 | 1 | 8 | 0.916291 | 0 | 0.01159862 | 0.0 |
| studies | 1 | 0 | 13 | 0.430783 | 0.00418236 | 0 | 0.0 |
| study | 0 | 1 | 9 | 0.798508 | 0 | 0.01010769 | 0.0 |
| suggestions | 0 | 1 | 4 | 1.609438 | 0 | 0.02037263 | 0.0 |
| systematic | 0 | 1 | 10 | 0.693147 | 0 | 0.00877401 | 0.0 |
| taught | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| teachers | 0 | 1 | 5 | 1.386294 | 0 | 0.01754803 | 0.0 |
| teaching | 0 | 1 | 6 | 1.203973 | 0 | 0.01524016 | 0.0 |
| technologies | 0 | 3 | 6 | 1.203973 | 0 | 0.04572049 | 0.0 |
| technology | 1 | 0 | 6 | 1.203973 | 0.01168906 | 0 | 0.0 |
| ten | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| terms | 1 | 0 | 4 | 1.609438 | 0.01562561 | 0 | 0.0 |
| thematic | 1 | 0 | 5 | 1.386294 | 0.01345917 | 0 | 0.0 |
| trends | 1 | 0 | 5 | 1.386294 | 0.01345917 | 0 | 0.0 |
| understand | 0 | 1 | 5 | 1.386294 | 0 | 0.01754803 | 0.0 |
| understanding | 1 | 0 | 7 | 1.049822 | 0.01019245 | 0 | 0.0 |
| way | 1 | 0 | 2 | 2.302585 | 0.0223552 | 0 | 0.0 |
| whereof | 1 | 0 | 1 | 2.995732 | 0.02908478 | 0 | 0.0 |
| years | 0 | 1 | 3 | 1.89712 | 0 | 0.02401418 | 0.0 |

Longitudes: 103, 79. Producto=0.0017500797718316724; normas=0.23166903104312314, 0.2180513902765118. Coseno=0.0017500797718316724/(0.23166903104312314*0.2180513902765118)=0.03464423714898264. Ángulo=88.01463414475853 grados.

## Embeddings: operación numérica completa

Word2Vec: gensim entrena vectores de palabras de 100 componentes, ventana 5, skip-gram, 100 épocas, semilla 42 y un trabajador. El vector documental promedia los vectores de sus tokens. SBERT usa all-MiniLM-L6-v2 y genera 384 componentes. Ver limitaciones de truncamiento y entrenamiento en DOCUMENTO_TECNICO.md.

word2vec: 100 componentes. Primeras cinco (solo ilustración): [0.17624205350875854, 0.15069171786308289, -0.03147421032190323, -0.10183090716600418, -0.10219793766736984] y [0.20990101993083954, 0.24336399137973785, -0.2671113908290863, -0.08561287075281143, -0.20016644895076752]. Con TODAS: producto=3.3638752608437477; normas=1.964862280996875,2.0720200533986914; coseno=0.8262544527923138. Vectores completos en resultados/vectores.json.

sbert: 384 componentes. Primeras cinco (solo ilustración): [0.043269187211990356, 0.0039865439757704735, 0.025171935558319092, 0.007264425978064537, -0.015537458471953869] y [-0.029961252585053444, 0.019604258239269257, -0.08233336359262466, 0.03847184777259827, -0.0014488622546195984]. Con TODAS: producto=0.5897856693642306; normas=0.9999999510191067,1.0000000904255923; coseno=0.5897856449207447. Vectores completos en resultados/vectores.json.

SBERT: límite 256 tokens del tokenizador; artículos truncados: [3, 4, 5, 7, 8, 10, 12, 13, 15, 17, 18, 19, 20] 

En este par Word2Vec=0.8263 y TF-IDF=0.0346: comparten tema, pero los términos comunes pierden peso IDF y los vectores aprendidos con pocos documentos pueden ser poco discriminativos. Esto explica diferencias de escala, no valida un ganador.

Los seis valores no son calificaciones de calidad. Jaccard no usa frecuencia ni orden; TF-IDF distingue términos infrecuentes; edición y alineamiento penalizan cambios de orden; Word2Vec aprende de un corpus muy pequeño; SBERT incorpora entrenamiento externo y límites de longitud. No hay etiquetas humanas para concluir cuál comprende mejor estos artículos.

## R2: ejemplo pequeño, artículos 1, 2, 7 y 9

Distancia TF-IDF = 1 - coseno. Índices locales 0,1,2,3 corresponden a artículos 1,2,7,9.
```text
[0.0, 0.9653557628510173, 0.9898498784568449, 0.964032433131245]
[0.9653557628510173, 0.0, 0.932845276618849, 0.8671046689403099]
[0.9898498784568449, 0.932845276618849, 0.0, 0.9408030307084313]
[0.964032433131245, 0.8671046689403099, 0.9408030307084313, 0.0]
```

### single 
```text
Candidatos 0,1: distancias [0.9653557628510173]; single=0.9653557628510173
Candidatos 0,2: distancias [0.9898498784568449]; single=0.9898498784568449
Candidatos 0,3: distancias [0.964032433131245]; single=0.964032433131245
Candidatos 1,2: distancias [0.932845276618849]; single=0.932845276618849
Candidatos 1,3: distancias [0.8671046689403099]; single=0.8671046689403099
Candidatos 2,3: distancias [0.9408030307084313]; single=0.9408030307084313
Fusión 1,3 a distancia 0.8671046689403099; nuevo grupo 4
Candidatos 0,2: distancias [0.9898498784568449]; single=0.9898498784568449
Candidatos 0,4: distancias [0.9653557628510173, 0.964032433131245]; single=0.964032433131245
Candidatos 2,4: distancias [0.932845276618849, 0.9408030307084313]; single=0.932845276618849
Fusión 2,4 a distancia 0.932845276618849; nuevo grupo 5
Candidatos 0,5: distancias [0.9898498784568449, 0.9653557628510173, 0.964032433131245]; single=0.964032433131245
Fusión 0,5 a distancia 0.964032433131245; nuevo grupo 6
i=0: a=0; b=0.9730793581463691; s=0 (singleton => 0)
i=1: a=0.8999749727795794; b=0.9653557628510173; s=0.06772714535659545 (singleton => 0)
i=2: a=0.9368241536636401; b=0.9898498784568449; s=0.053569461336774385 (singleton => 0)
i=3: a=0.9039538498243707; b=0.964032433131245; s=0.06232008513627998 (singleton => 0)
Promedio silhouette: 0.045904172957412455 
```

### complete 
```text
Candidatos 0,1: distancias [0.9653557628510173]; complete=0.9653557628510173
Candidatos 0,2: distancias [0.9898498784568449]; complete=0.9898498784568449
Candidatos 0,3: distancias [0.964032433131245]; complete=0.964032433131245
Candidatos 1,2: distancias [0.932845276618849]; complete=0.932845276618849
Candidatos 1,3: distancias [0.8671046689403099]; complete=0.8671046689403099
Candidatos 2,3: distancias [0.9408030307084313]; complete=0.9408030307084313
Fusión 1,3 a distancia 0.8671046689403099; nuevo grupo 4
Candidatos 0,2: distancias [0.9898498784568449]; complete=0.9898498784568449
Candidatos 0,4: distancias [0.9653557628510173, 0.964032433131245]; complete=0.9653557628510173
Candidatos 2,4: distancias [0.932845276618849, 0.9408030307084313]; complete=0.9408030307084313
Fusión 2,4 a distancia 0.9408030307084313; nuevo grupo 5
Candidatos 0,5: distancias [0.9898498784568449, 0.9653557628510173, 0.964032433131245]; complete=0.9898498784568449
Fusión 0,5 a distancia 0.9898498784568449; nuevo grupo 6
i=0: a=0; b=0.9730793581463691; s=0 (singleton => 0)
i=1: a=0.8999749727795794; b=0.9653557628510173; s=0.06772714535659545 (singleton => 0)
i=2: a=0.9368241536636401; b=0.9898498784568449; s=0.053569461336774385 (singleton => 0)
i=3: a=0.9039538498243707; b=0.964032433131245; s=0.06232008513627998 (singleton => 0)
Promedio silhouette: 0.045904172957412455 
```

### average 
```text
Candidatos 0,1: distancias [0.9653557628510173]; average=0.9653557628510173
Candidatos 0,2: distancias [0.9898498784568449]; average=0.9898498784568449
Candidatos 0,3: distancias [0.964032433131245]; average=0.964032433131245
Candidatos 1,2: distancias [0.932845276618849]; average=0.932845276618849
Candidatos 1,3: distancias [0.8671046689403099]; average=0.8671046689403099
Candidatos 2,3: distancias [0.9408030307084313]; average=0.9408030307084313
Fusión 1,3 a distancia 0.8671046689403099; nuevo grupo 4
Candidatos 0,2: distancias [0.9898498784568449]; average=0.9898498784568449
Candidatos 0,4: distancias [0.9653557628510173, 0.964032433131245]; average=0.9646940979911311
Candidatos 2,4: distancias [0.932845276618849, 0.9408030307084313]; average=0.9368241536636401
Fusión 2,4 a distancia 0.9368241536636401; nuevo grupo 5
Candidatos 0,5: distancias [0.9898498784568449, 0.9653557628510173, 0.964032433131245]; average=0.9730793581463691
Fusión 0,5 a distancia 0.9730793581463691; nuevo grupo 6
i=0: a=0; b=0.9730793581463691; s=0 (singleton => 0)
i=1: a=0.8999749727795794; b=0.9653557628510173; s=0.06772714535659545 (singleton => 0)
i=2: a=0.9368241536636401; b=0.9898498784568449; s=0.053569461336774385 (singleton => 0)
i=3: a=0.9039538498243707; b=0.964032433131245; s=0.06232008513627998 (singleton => 0)
Promedio silhouette: 0.045904172957412455 
```

### Resultado sobre los 20 abstracts completos

Se conserva k=2 para comparar los tres criterios en cada representación.

| Método | Enlace | k | Silhouette |
|---|---|---:|---:|
| jaccard | single | 2 | 0.03742016344066916 |
| jaccard | complete | 2 | 0.032874547827252035 |
| jaccard | average | 2 | 0.032874547827252035 |

Mayor separación para jaccard con k=2: ['single'] . No demuestra coherencia temática.

| Método | Enlace | k | Silhouette |
|---|---|---:|---:|
| tfidf | single | 2 | 0.020108555870753823 |
| tfidf | complete | 2 | 0.013674852954570544 |
| tfidf | average | 2 | 0.015859791401037736 |

Mayor separación para tfidf con k=2: ['single'] . No demuestra coherencia temática.

| Método | Enlace | k | Silhouette |
|---|---|---:|---:|
| levenshtein | single | 2 | 0.013328278871249582 |
| levenshtein | complete | 2 | 0.0059712555298640155 |
| levenshtein | average | 2 | 0.013328278871249582 |

Mayor separación para levenshtein con k=2: ['single', 'average'] . No demuestra coherencia temática.

| Método | Enlace | k | Silhouette |
|---|---|---:|---:|
| needleman | single | 2 | 0.018201632608602164 |
| needleman | complete | 2 | 0.012277409562299096 |
| needleman | average | 2 | 0.018201632608602164 |

Mayor separación para needleman con k=2: ['single', 'average'] . No demuestra coherencia temática.

| Método | Enlace | k | Silhouette |
|---|---|---:|---:|
| word2vec | single | 2 | 0.2780154856294288 |
| word2vec | complete | 2 | 0.19988216225390276 |
| word2vec | average | 2 | 0.27097655377792035 |

Mayor separación para word2vec con k=2: ['single'] . No demuestra coherencia temática.

| Método | Enlace | k | Silhouette |
|---|---|---:|---:|
| sbert | single | 2 | 0.09519565724207625 |
| sbert | complete | 2 | 0.18582881412521499 |
| sbert | average | 2 | 0.1562912700754851 |

Mayor separación para sbert con k=2: ['complete'] . No demuestra coherencia temática.

## R3: fragmento real y resultado del abstract completo

Artículo 1, minúsculas; inicio del fragmento en abstract=2. Patrón=intelligence.

`nce artificial intelligence (ai) is finding its`

Preparación LPS: valor para cada prefijo del patrón (longitud de prefijo propio que también es sufijo):
```text
i 0
in 0
int 0
inte 0
intel 0
intell 0
intelli 1
intellig 0
intellige 0
intelligen 0
intelligenc 0
intelligence 0
Tabla carácter malo: cada asignación reemplaza la última posición conocida:
0 i {'i': 0}
1 n {'i': 0, 'n': 1}
2 t {'i': 0, 'n': 1, 't': 2}
3 e {'i': 0, 'n': 1, 't': 2, 'e': 3}
4 l {'i': 0, 'n': 1, 't': 2, 'e': 3, 'l': 4}
5 l {'i': 0, 'n': 1, 't': 2, 'e': 3, 'l': 5}
6 i {'i': 6, 'n': 1, 't': 2, 'e': 3, 'l': 5}
7 g {'i': 6, 'n': 1, 't': 2, 'e': 3, 'l': 5, 'g': 7}
8 e {'i': 6, 'n': 1, 't': 2, 'e': 8, 'l': 5, 'g': 7}
9 n {'i': 6, 'n': 9, 't': 2, 'e': 8, 'l': 5, 'g': 7}
10 c {'i': 6, 'n': 9, 't': 2, 'e': 8, 'l': 5, 'g': 7, 'c': 10}
11 e {'i': 6, 'n': 9, 't': 2, 'e': 11, 'l': 5, 'g': 7, 'c': 10}
RK: h=256^(12-1) mod 101=92
(256*0+105) mod 101=4 (carácter i)
(256*4+110) mod 101=23 (carácter n)
(256*23+116) mod 101=45 (carácter t)
(256*45+101) mod 101=6 (carácter e)
(256*6+108) mod 101=28 (carácter l)
(256*28+108) mod 101=4 (carácter l)
(256*4+105) mod 101=18 (carácter i)
(256*18+103) mod 101=65 (carácter g)
(256*65+101) mod 101=76 (carácter e)
(256*76+110) mod 101=73 (carácter n)
(256*73+99) mod 101=1 (carácter c)
(256*1+101) mod 101=54 (carácter e)

 KMP traza del fragmento:
i= 0 j= 0  texto[i]=n  patron[j]=i  FALLO
i= 1 j= 0  texto[i]=c  patron[j]=i  FALLO
i= 2 j= 0  texto[i]=e  patron[j]=i  FALLO
i= 3 j= 0  texto[i]=   patron[j]=i  FALLO
i= 4 j= 0  texto[i]=a  patron[j]=i  FALLO
i= 5 j= 0  texto[i]=r  patron[j]=i  FALLO
i= 6 j= 0  texto[i]=t  patron[j]=i  FALLO
i= 7 j= 0  texto[i]=i  patron[j]=i  coinciden
i= 8 j= 1  texto[i]=f  patron[j]=n  FALLO
i= 8 j= 0  texto[i]=f  patron[j]=i  FALLO
i= 9 j= 0  texto[i]=i  patron[j]=i  coinciden
i=10 j= 1  texto[i]=c  patron[j]=n  FALLO
i=10 j= 0  texto[i]=c  patron[j]=i  FALLO
i=11 j= 0  texto[i]=i  patron[j]=i  coinciden
i=12 j= 1  texto[i]=a  patron[j]=n  FALLO
i=12 j= 0  texto[i]=a  patron[j]=i  FALLO
i=13 j= 0  texto[i]=l  patron[j]=i  FALLO
i=14 j= 0  texto[i]=   patron[j]=i  FALLO
i=15 j= 0  texto[i]=i  patron[j]=i  coinciden
i=16 j= 1  texto[i]=n  patron[j]=n  coinciden
i=17 j= 2  texto[i]=t  patron[j]=t  coinciden
i=18 j= 3  texto[i]=e  patron[j]=e  coinciden
i=19 j= 4  texto[i]=l  patron[j]=l  coinciden
i=20 j= 5  texto[i]=l  patron[j]=l  coinciden
i=21 j= 6  texto[i]=i  patron[j]=i  coinciden
i=22 j= 7  texto[i]=g  patron[j]=g  coinciden
i=23 j= 8  texto[i]=e  patron[j]=e  coinciden
i=24 j= 9  texto[i]=n  patron[j]=n  coinciden
i=25 j=10  texto[i]=c  patron[j]=c  coinciden
i=26 j=11  texto[i]=e  patron[j]=e  coinciden
i=27 j= 0  texto[i]=   patron[j]=i  FALLO
i=28 j= 0  texto[i]=(  patron[j]=i  FALLO
i=29 j= 0  texto[i]=a  patron[j]=i  FALLO
i=30 j= 0  texto[i]=i  patron[j]=i  coinciden
i=31 j= 1  texto[i]=)  patron[j]=n  FALLO
i=31 j= 0  texto[i]=)  patron[j]=i  FALLO
i=32 j= 0  texto[i]=   patron[j]=i  FALLO
i=33 j= 0  texto[i]=i  patron[j]=i  coinciden
i=34 j= 1  texto[i]=s  patron[j]=n  FALLO
i=34 j= 0  texto[i]=s  patron[j]=i  FALLO
i=35 j= 0  texto[i]=   patron[j]=i  FALLO
i=36 j= 0  texto[i]=f  patron[j]=i  FALLO
i=37 j= 0  texto[i]=i  patron[j]=i  coinciden
i=38 j= 1  texto[i]=n  patron[j]=n  coinciden
i=39 j= 2  texto[i]=d  patron[j]=t  FALLO
i=39 j= 0  texto[i]=d  patron[j]=i  FALLO
i=40 j= 0  texto[i]=i  patron[j]=i  coinciden
i=41 j= 1  texto[i]=n  patron[j]=n  coinciden
i=42 j= 2  texto[i]=g  patron[j]=t  FALLO
i=42 j= 0  texto[i]=g  patron[j]=i  FALLO
i=43 j= 0  texto[i]=   patron[j]=i  FALLO
i=44 j= 0  texto[i]=i  patron[j]=i  coinciden
i=45 j= 1  texto[i]=t  patron[j]=n  FALLO
i=45 j= 0  texto[i]=t  patron[j]=i  FALLO
i=46 j= 0  texto[i]=s  patron[j]=i  FALLO
Resultado: ([15], 55)
Resultado del abstract completo (posiciones desde cero): ([17], 1239)

 Boyer-Moore traza del fragmento:
nce artificial intelligence (ai) is finding its
intelligence  (s=0)
s= 0 falla en j=11: texto='i' patron='e'  → salto 5
nce artificial intelligence (ai) is finding its
     intelligence  (s=5)
s= 5 falla en j=11: texto='n' patron='e'  → salto 2
nce artificial intelligence (ai) is finding its
       intelligence  (s=7)
s= 7 falla en j=10: texto='t' patron='c'  → salto 8
nce artificial intelligence (ai) is finding its
               intelligence  (s=15)
s=15 coincidencia completa
nce artificial intelligence (ai) is finding its
                            intelligence  (s=28)
s=28 falla en j=11: texto='d' patron='e'  → salto 12
Resultado: ([15], 17)
Resultado del abstract completo (posiciones desde cero): ([17], 142)

 Rabin-Karp traza del fragmento:
s= 0 ventana='nce artifici' hp= 54 ht= 87
hash siguiente = (256 * (87 - 110 * 92) + 97) mod 101 = 79
s= 1 ventana='ce artificia' hp= 54 ht= 79
hash siguiente = (256 * (79 - 99 * 92) + 108) mod 101 = 69
s= 2 ventana='e artificial' hp= 54 ht= 69
hash siguiente = (256 * (69 - 101 * 92) + 32) mod 101 = 21
s= 3 ventana=' artificial ' hp= 54 ht= 21
hash siguiente = (256 * (21 - 32 * 92) + 105) mod 101 = 25
s= 4 ventana='artificial i' hp= 54 ht= 25
hash siguiente = (256 * (25 - 97 * 92) + 110) mod 101 = 21
s= 5 ventana='rtificial in' hp= 54 ht= 21
hash siguiente = (256 * (21 - 114 * 92) + 116) mod 101 = 94
s= 6 ventana='tificial int' hp= 54 ht= 94
hash siguiente = (256 * (94 - 116 * 92) + 101) mod 101 = 44
s= 7 ventana='ificial inte' hp= 54 ht= 44
hash siguiente = (256 * (44 - 105 * 92) + 108) mod 101 = 85
s= 8 ventana='ficial intel' hp= 54 ht= 85
hash siguiente = (256 * (85 - 102 * 92) + 108) mod 101 = 33
s= 9 ventana='icial intell' hp= 54 ht= 33
hash siguiente = (256 * (33 - 105 * 92) + 105) mod 101 = 94
s=10 ventana='cial intelli' hp= 54 ht= 94
hash siguiente = (256 * (94 - 99 * 92) + 103) mod 101 = 66
s=11 ventana='ial intellig' hp= 54 ht= 66
hash siguiente = (256 * (66 - 105 * 92) + 101) mod 101 = 54
s=12 ventana='al intellige' hp= 54 ht= 54  ← hashes iguales
hash siguiente = (256 * (54 - 97 * 92) + 110) mod 101 = 72
s=13 ventana='l intelligen' hp= 54 ht= 72
hash siguiente = (256 * (72 - 108 * 92) + 99) mod 101 = 16
s=14 ventana=' intelligenc' hp= 54 ht= 16
hash siguiente = (256 * (16 - 32 * 92) + 101) mod 101 = 54
s=15 ventana='intelligence' hp= 54 ht= 54  ← hashes iguales
hash siguiente = (256 * (54 - 105 * 92) + 32) mod 101 = 44
s=16 ventana='ntelligence ' hp= 54 ht= 44
hash siguiente = (256 * (44 - 110 * 92) + 40) mod 101 = 23
s=17 ventana='telligence (' hp= 54 ht= 23
hash siguiente = (256 * (23 - 116 * 92) + 97) mod 101 = 44
s=18 ventana='elligence (a' hp= 54 ht= 44
hash siguiente = (256 * (44 - 101 * 92) + 105) mod 101 = 57
s=19 ventana='lligence (ai' hp= 54 ht= 57
hash siguiente = (256 * (57 - 108 * 92) + 41) mod 101 = 57
s=20 ventana='ligence (ai)' hp= 54 ht= 57
hash siguiente = (256 * (57 - 108 * 92) + 32) mod 101 = 48
s=21 ventana='igence (ai) ' hp= 54 ht= 48
hash siguiente = (256 * (48 - 105 * 92) + 105) mod 101 = 96
s=22 ventana='gence (ai) i' hp= 54 ht= 96
hash siguiente = (256 * (96 - 103 * 92) + 115) mod 101 = 9
s=23 ventana='ence (ai) is' hp= 54 ht=  9
hash siguiente = (256 * (9 - 101 * 92) + 32) mod 101 = 13
s=24 ventana='nce (ai) is ' hp= 54 ht= 13
hash siguiente = (256 * (13 - 110 * 92) + 102) mod 101 = 27
s=25 ventana='ce (ai) is f' hp= 54 ht= 27
hash siguiente = (256 * (27 - 99 * 92) + 105) mod 101 = 86
s=26 ventana='e (ai) is fi' hp= 54 ht= 86
hash siguiente = (256 * (86 - 101 * 92) + 110) mod 101 = 7
s=27 ventana=' (ai) is fin' hp= 54 ht=  7
hash siguiente = (256 * (7 - 32 * 92) + 100) mod 101 = 72
s=28 ventana='(ai) is find' hp= 54 ht= 72
hash siguiente = (256 * (72 - 40 * 92) + 105) mod 101 = 1
s=29 ventana='ai) is findi' hp= 54 ht=  1
hash siguiente = (256 * (1 - 97 * 92) + 110) mod 101 = 38
s=30 ventana='i) is findin' hp= 54 ht= 38
hash siguiente = (256 * (38 - 105 * 92) + 103) mod 101 = 59
s=31 ventana=') is finding' hp= 54 ht= 59
hash siguiente = (256 * (59 - 41 * 92) + 32) mod 101 = 15
s=32 ventana=' is finding ' hp= 54 ht= 15
hash siguiente = (256 * (15 - 32 * 92) + 105) mod 101 = 4
s=33 ventana='is finding i' hp= 54 ht=  4
hash siguiente = (256 * (4 - 105 * 92) + 116) mod 101 = 54
s=34 ventana='s finding it' hp= 54 ht= 54  ← hashes iguales
hash siguiente = (256 * (54 - 115 * 92) + 115) mod 101 = 38
s=35 ventana=' finding its' hp= 54 ht= 38
Resultado: ([15], 14, 2)
Resultado del abstract completo (posiciones desde cero): ([17], 28, 15)
```
Las comparaciones cuentan caracteres en búsqueda; RK también hace hashes no contados como comparaciones. Ver resultados_r3.csv para tiempos medidos por separado.
