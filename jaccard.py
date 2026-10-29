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
        if token in conjuntos_b:
            intersection += 1
    union = len(conjuntos_a) + len(conjuntos_b) - intersection  # Tamaño de la unión
    if union == 0:
        return 0.0  # Evitar división por cero si ambos conjuntos están vacíos
    return intersection / union
if __name__ == "__main__":
        print(jaccard_similarity({"modelo", "genera", "texto"}, {"modelo", "genera", "imagen"}))