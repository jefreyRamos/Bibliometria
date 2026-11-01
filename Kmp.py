def tabla_lps(patron):
    m = len(patron)
    lps = [0] * m
    largo = 0      # largo del prefijo-sufijo actual
    i = 1
    while i < m:
        if patron[i] == patron[largo]:
            largo += 1
            lps[i] = largo
            i += 1
        elif largo != 0:
            largo = lps[largo -1]
            pass
        else:
            lps[i] = 0
            i += 1
            pass
    return lps


def kmp(texto, patron):
    n, m = len(texto), len(patron)
    lps = tabla_lps(patron)
    posiciones = []
    comparaciones = 0
    i = j = 0          # i recorre el texto, j el patrón
    while i < n:
        comparaciones += 1
        if texto[i] == patron[j]:
            i += 1
            j += 1
            if j == m:                       # ¡encontrado!
                posiciones.append(i - m)
                j = lps[j - 1]
        elif j != 0:
            j = lps[j - 1]
            pass
        else:
            i += 1
            pass
    return posiciones, comparaciones


if __name__ == "__main__":
    print(tabla_lps("ABABCABAB"))
    print(kmp("ABABDABACDABABCABAB", "ABABCABAB"))
    print(kmp("AAAAA", "AA"))