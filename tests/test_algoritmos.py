import itertools
import json
from pathlib import Path
import unittest
from Kmp import kmp, tabla_lps
from boyer_moore import boyer_moore
from rabin_karp import rabin_karp
from medicion import PREPARADORES, BUSCADORES
from clustering import clustering_jerarquico
from silhouette import silhouette, cortar
from levenshtein import levenshtein
from needleman_wusch import needleman_wunsch, traceback, similitud_nw
from tfidf_coseno import calcular_idf, vector_tfidf, coseno
from jaccard import jaccard_similarity


class Algoritmos(unittest.TestCase):
    def test_busqueda_exhaustiva(self):
        cadenas = [''.join(p) for n in range(7) for p in itertools.product('ab', repeat=n)]
        patrones = [''.join(p) for n in range(5) for p in itertools.product('ab', repeat=n)]
        for texto in cadenas + ['á😊á😊á']:
            for patron in patrones + ['á😊', '😊á', 'demasiado largo']:
                esperado = [] if not patron else [i for i in range(len(texto)-len(patron)+1) if texto[i:i+len(patron)] == patron]
                for nombre, f in [('KMP', kmp), ('Boyer-Moore', boyer_moore), ('Rabin-Karp', rabin_karp)]:
                    self.assertEqual(f(texto, patron)[0], esperado, (nombre, texto, patron))
                    self.assertEqual(BUSCADORES[nombre](texto, patron, PREPARADORES[nombre](patron))[0], esperado)

    def test_similitud(self):
        self.assertEqual(levenshtein('kitten','sitting'), 3)
        self.assertEqual(levenshtein([],['a']), 1)
        self.assertEqual(needleman_wunsch('GATTACA','GCATGCU')[-1][-1], 0)
        self.assertEqual(similitud_nw([],[]), 1)
        idf = calcular_idf([['a','a'],['b']])
        self.assertAlmostEqual(vector_tfidf(['a','a'], idf)['a'], idf['a'])
        self.assertEqual(coseno({},{}), 0)
        self.assertEqual(jaccard_similarity(['a'],['a']), 1)

    def test_clustering(self):
        D = [[0,1,5,6],[1,0,4,5],[5,4,0,1],[6,5,1,0]]
        for criterio, altura in [('single',4),('complete',6),('average',5)]:
            Z = clustering_jerarquico(D,criterio)
            self.assertEqual(Z[-1][2], altura)
            self.assertAlmostEqual(silhouette(D,cortar(Z,4,2)), (1-1/5.5+1-1/4.5)/2)
        self.assertEqual(silhouette([[0,0,0],[0,0,0],[0,0,0]],[0,0,1]),0)

    def test_corpus(self):
        from extraer_abstracts import extraer_abstract
        c=json.loads(Path('corpus.json').read_text(encoding='utf8'))
        limites=json.loads(Path('datos/limites_pdf.json').read_text(encoding='utf8'))
        self.assertEqual([d['id'] for d in c], list(range(1,21)))
        for d,l in zip(c,limites):
            self.assertEqual(d['abstract'],extraer_abstract(Path('pdfs')/d['archivo'],l))
            self.assertTrue(d['titulo'] and d['autores'])
            self.assertNotIn('Keywords:',d['abstract'])
            self.assertNotIn('1. Introduction',d['abstract'])
        self.assertTrue(c[6]['abstract'].startswith('The rapid expansion'))
        self.assertTrue(c[8]['abstract'].endswith('development efforts.'))
        self.assertEqual(len(c[19]['autores']),4)


if __name__ == '__main__':
    unittest.main()
