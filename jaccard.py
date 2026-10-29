def jaccard_similarity(tokens_a, tokens_b):
    """
    Calcula la similitud de Jaccard entre dos conjuntos.
    
    Args:
        tokens_a (set): Primer conjunto de tokens.
        tokens_b (set): Segundo conjunto de tokens.
        
    Returns:
        float: Similitud de Jaccard entre los dos conjuntos.
    """
    conjuntos_a = set(tokens_a)
    conjuntos_b = set(tokens_b)

    intersection = 0
    for token in conjuntos_a:
        if token in conjuntos_b: # Si el token está en ambos conjuntos, incrementamos la intersección
            intersection += 1
    union = len(conjuntos_a) + len(conjuntos_b) - intersection  # Tamaño de la unión
    if union == 0:
        return 0.0  # Evitar división por cero si ambos conjuntos están vacíos
    return intersection / union
if __name__ == "__main__":
        import json
        from preprocesamiento import preprocesar

        with open("corpus.json", encoding="utf-8") as f:
            corpus = json.load(f)

        tokens = [preprocesar(articulo["abstract"]) for articulo in corpus]

        print("Jaccard entre el abstract del 1er y el 2do artículo:",round (jaccard_similarity(tokens[0], tokens[1]), 4))

        mejor = (0, 0, 0.0)  # (índice del artículo A, índice del artículo B, similitud máxima)
        for i in range(len(tokens)):
            for j in range(i + 1, len(tokens)):
                similitud = jaccard_similarity(tokens[i], tokens[j])
                if similitud > mejor[2]:
                    mejor = (i + 1, j + 1, similitud)
        print(f"Los artículos con mayor similitud de Jaccard son el {mejor[0]} y el {mejor[1]} con una similitud de {mejor[2]: .4f}")