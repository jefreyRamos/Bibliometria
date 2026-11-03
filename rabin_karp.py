BASE, Q = 256, 101          # base (tamaño del alfabeto) y un número primo

def rabin_karp(texto, patron, traza=False):
    n, m = len(texto), len(patron)
    return buscar_preparado(texto, patron, preparar(patron), traza)


def preparar(patron):
    h = 1
    for _ in range(max(0, len(patron) - 1)):
        h = h * BASE % Q
    hp = 0
    for letra in patron:
        hp = (BASE * hp + ord(letra)) % Q
    return h, hp


def buscar_preparado(texto, patron, preparado, traza=False):
    n, m = len(texto), len(patron)
    if m == 0 or m > n:
        return [], 0, 0
    h, hp = preparado
    ht = 0
    for k in range(m):
        ht = (BASE * ht + ord(texto[k])) % Q
    posiciones, comparaciones, colisiones = [], 0, 0
    for s in range(n - m + 1):
        if traza:
            print(f"s={s:2d} ventana='{texto[s:s + m]}' hp={hp:3d} ht={ht:3d}"
                f"{'  ← hashes iguales' if hp == ht else ''}")
        if hp == ht:                        # posible coincidencia: verificar letra a letra
            k = 0
            while k < m:
                comparaciones += 1
                if texto[s + k] != patron[k]:
                    break
                k += 1
            if k == m:
                posiciones.append(s)
            else:
                colisiones += 1
        if s < n - m:
            nuevo = (BASE * (ht - ord(texto[s]) * h) + ord(texto[s + m])) % Q
            if traza:
                print(f"hash siguiente = ({BASE} * ({ht} - {ord(texto[s])} * {h}) + {ord(texto[s+m])}) mod {Q} = {nuevo}")
            ht = nuevo
    return posiciones, comparaciones, colisiones


if __name__ == "__main__":
    print(rabin_karp("ABABDABACDABABCABAB", "ABABCABAB"))
    print(rabin_karp("AAAAA", "AA"))
    print("\n--- TRAZA RABIN-KARP ---")
    rabin_karp("ABABDABACDABABCABAB", "ABABCABAB", traza=True)
