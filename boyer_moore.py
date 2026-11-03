def tabla_mal_caracter(patron):
    ultima = {}
    for k in range(len(patron)):
        ultima[patron[k]] = k          # última posición de cada carácter
    return ultima


def boyer_moore(texto, patron, traza=False):
    return buscar_preparado(texto, patron, tabla_mal_caracter(patron), traza)


def buscar_preparado(texto, patron, ultima, traza=False):
    n, m = len(texto), len(patron)
    if m == 0 or m > n:
        return [], 0
    posiciones = []
    comparaciones = 0
    s = 0                               # desplazamiento del patrón sobre el texto
    while s <= n - m:
        if traza:
            print(texto)
            print(' ' * s + patron + f'  (s={s})')
        j = m - 1                       # empezamos por el final del patrón
        while j >= 0:
            comparaciones += 1
            if patron[j] != texto[s + j]:
                break
            j -= 1
        if j < 0:                       # coincidió completo
            if traza:
                print(f"s={s:2d} coincidencia completa")
            posiciones.append(s)
            if s + m < n:
                s += m - ultima.get(texto[s + m], -1)
            else:
                s += 1
        else:
            salto = max(1, j - ultima.get(texto[s + j], -1))
            if traza:
                print(f"s={s:2d} falla en j={j}: texto='{texto[s + j]}' patron='{patron[j]}'  → salto {salto}")
            s += salto
    return posiciones, comparaciones


if __name__ == "__main__":
    print(tabla_mal_caracter("ABABCABAB"))
    print(boyer_moore("ABABDABACDABABCABAB", "ABABCABAB"))
    print(boyer_moore("AAAAA", "AA"))
    print("\n--- TRAZA BOYER-MOORE ---")
    boyer_moore("ABABDABACDABABCABAB", "ABABCABAB", traza=True)