"""Preparación del patrón independiente de cada búsqueda."""
from statistics import median
from time import perf_counter
from Kmp import tabla_lps, buscar_preparado as buscar_kmp
from boyer_moore import tabla_mal_caracter, buscar_preparado as buscar_bm
from rabin_karp import preparar, buscar_preparado as buscar_rk
PREPARADORES = {'KMP': tabla_lps, 'Boyer-Moore': tabla_mal_caracter, 'Rabin-Karp': preparar}
BUSCADORES = {'KMP': buscar_kmp, 'Boyer-Moore': buscar_bm, 'Rabin-Karp': buscar_rk}


def medir(nombre, texto, patron, repeticiones=7):
    tiempos_preparacion, tiempos_busqueda = [], []
    for _ in range(repeticiones):
        inicio = perf_counter()
        preparado = PREPARADORES[nombre](patron)
        tiempos_preparacion.append((perf_counter() - inicio) * 1000)
        inicio = perf_counter()
        resultado = BUSCADORES[nombre](texto, patron, preparado)
        tiempos_busqueda.append((perf_counter() - inicio) * 1000)
    return resultado, median(tiempos_preparacion), median(tiempos_busqueda)
