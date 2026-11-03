import json
from pathlib import Path
import unittest
from unittest.mock import patch
from datos_proyecto import cargar_resultados, huella_codigo
from preprocesamiento import preprocesar
from tfidf_coseno import calcular_idf, vector_tfidf, coseno
from jaccard import jaccard_similarity
from levenshtein import similitud_levenshtein
from needleman_wusch import similitud_nw


class Resultados(unittest.TestCase):
    def test_matrices_del_corpus_actual(self):
        corpus, M = cargar_resultados()
        self.assertEqual(set(M), {'jaccard','tfidf','levenshtein','needleman','word2vec','sbert'})
        for matriz in M.values():
            self.assertEqual(len(matriz),20)
            for i in range(20):
                self.assertEqual(len(matriz[i]),20)
                self.assertEqual(matriz[i][i],1)
                for j in range(20):
                    self.assertEqual(matriz[i][j],matriz[j][i])
                    self.assertTrue(-1 <= matriz[i][j] <= 1)
        t=[preprocesar(d['abstract']) for d in corpus]
        idf=calcular_idf(t)
        a,b=t[6],t[8]
        self.assertAlmostEqual(M['tfidf'][6][8],coseno(vector_tfidf(a,idf),vector_tfidf(b,idf)))
        self.assertAlmostEqual(M['jaccard'][6][8],jaccard_similarity(a,b))
        self.assertAlmostEqual(M['levenshtein'][6][8],similitud_levenshtein(a,b))
        self.assertAlmostEqual(M['needleman'][6][8],similitud_nw(a,b))
        with patch('datos_proyecto.huella',return_value='corpus alterado'):
            with self.assertRaises(ValueError): cargar_resultados()

    def test_vectores_y_enlaces(self):
        import math
        from scipy.cluster.hierarchy import linkage
        from scipy.spatial.distance import squareform
        from sklearn.metrics import silhouette_score
        from clustering import clustering_jerarquico
        from silhouette import silhouette, cortar
        corpus,M=cargar_resultados()
        V=json.loads(Path('resultados/vectores.json').read_text(encoding='utf8'))
        for nombre,dim in [('word2vec',100),('sbert',384)]:
            self.assertEqual(len(V[nombre]),20)
            self.assertTrue(all(len(v)==dim for v in V[nombre]))
            u,v=V[nombre][:2]
            esperado=sum(x*y for x,y in zip(u,v))/(math.sqrt(sum(x*x for x in u))*math.sqrt(sum(y*y for y in v)))
            self.assertAlmostEqual(M[nombre][0][1],esperado)
        # Librerías solo como referencia de prueba, nunca para calcular los resultados de la app.
        D=[[0 if i==j else 1-M['tfidf'][i][j] for j in range(20)] for i in range(20)]
        for criterio in ['single','complete','average']:
            Z=clustering_jerarquico(D,criterio)
            referencia=linkage(squareform(D),method=criterio)
            for fila,ref in zip(Z,referencia): self.assertAlmostEqual(fila[2],ref[2])
            etiquetas=cortar(Z,20,3)
            self.assertAlmostEqual(silhouette(D,etiquetas),silhouette_score(D,etiquetas,metric='precomputed'))


if __name__=='__main__': unittest.main()
