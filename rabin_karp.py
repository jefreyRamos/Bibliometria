BASE, Q = 256, 101          # base (tamaño del alfabeto) y un número primo

def rabin_karp(texto, patron, traza=False):
    n, m = len(texto), len(patron)
    h = 1
    for _ in range(m - 1):
        h = (h * BASE) % Q                  # BASE^(m-1) mod Q
    hp = ht = 0
    for k in range(m):
        hp = (BASE * hp + ord(patron[k])) % Q
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
            ht = (BASE * (ht - ord(texto[s]) * h) + ord(texto[s + m])) % Q
    return posiciones, comparaciones, colisiones


if __name__ == "__main__":
    print(rabin_karp("ABABDABACDABABCABAB", "ABABCABAB"))
    print(rabin_karp("AAAAA", "AA"))
    print("\n--- TRAZA RABIN-KARP ---")
    rabin_karp("ABABDABACDABABCABAB", "ABABCABAB", traza=True)
