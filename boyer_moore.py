def tabla_mal_caracter(patron):
    ultima = {}
    for k in range(len(patron)):
        ultima[patron[k]] = k          # última posición de cada carácter
    return ultima


def boyer_moore(texto, patron):
    n, m = len(texto), len(patron)
    ultima = tabla_mal_caracter(patron)
    posiciones = []
    comparaciones = 0
    s = 0                               # desplazamiento del patrón sobre el texto
    while s <= n - m:
        j = m - 1                       # empezamos por el final del patrón
        while j >= 0:
            comparaciones += 1
            if patron[j] != texto[s + j]:
                break
            j -= 1
        if j < 0:                       # coincidió completo
            posiciones.append(s)
            if s + m < n:
                s += m - ultima.get(texto[s + m], -1)
            else:
                s += 1
        else:
            s += max(1, j - ultima.get(texto[s + j], -1))
    return posiciones, comparaciones


if __name__ == "__main__":
    print(tabla_mal_caracter("ABABCABAB"))
    print(boyer_moore("ABABDABACDABABCABAB", "ABABCABAB"))
    print(boyer_moore("AAAAA", "AA"))