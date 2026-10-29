import json

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "of", "in", "on", "at", "to", "for",
    "with", "by", "from", "as", "is", "are", "was", "were", "be", "been", "being",
    "this", "that", "these", "those", "it", "its", "we", "our", "they", "their",
    "has", "have", "had", "do", "does", "did", "not", "no", "can", "could",
    "will", "would", "may", "might", "should", "also", "such", "than", "then",
    "there", "which", "who", "what", "how", "while", "into", "about", "between",
    "both", "each", "more", "most", "other", "some", "all", "any", "only",
    "well", "however", "based", "using", "used", "use", "through", "within",
    "among", "s", "e", "g", "i", "et", "al",
}

ARREGLOS = {"arti ficial": "artificial", "signi ficant": "significant"}


def preprocesar(texto):
    texto = texto.lower()
    for malo, bueno in ARREGLOS.items():
        texto = texto.replace(malo, bueno)

    limpio = ""
    for c in texto:
        if c.isalnum(): # Mantener solo caracteres alfanuméricos
            limpio += c
        else:
            limpio += " "

    tokens = limpio.split() # Dividir el texto en tokens usando espacios como separadores
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1] # Eliminar tokens que son stopwords o tienen longitud menor o igual a 1


if __name__ == "__main__": # hace que el código dentro de este bloque solo se ejecute si el archivo se ejecuta directamente, no si se importa como módulo
    with open("corpus.json", encoding="utf-8") as f:
        corpus = json.load(f)

    primero = corpus[0]["abstract"]
    tokens = preprocesar(primero)
    print("Palabras antes:", len(primero.split()))
    print("Tokens después:", len(tokens))
    print(tokens[:30])