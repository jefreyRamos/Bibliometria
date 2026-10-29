import os
import unicodedata
from pypdf import PdfReader

def extraer_abstract(ruta_pdf):
    lector = PdfReader(ruta_pdf)
    texto = ""
    for pagina in lector.pages[:2]: # Leer solo las primeras 2 páginas
        texto += pagina.extract_text() + "\n"
    minus = texto.lower()
    inicio = minus.find("abstract")
    if inicio == -1:
        return None  # No se encontró la palabra "abstract"
    inicio += len("abstract")
    fin = minus.find("introduction", inicio)
    if fin == -1:
        return None  # No se encontró la palabra "introduction"
    abstract = texto[inicio:fin].strip()
    if abstract.endswith("1."):
        abstract = abstract[:-2].strip()
    abstract = abstract.replace("\n", " ")
    abstract = abstract.lstrip(":.- —").strip()
    abstract = unicodedata.normalize("NFKC", abstract)
    return abstract

archivos = sorted(os.listdir("pdfs"))
for nombre in archivos:
    if not nombre.lower().endswith(".pdf"):
        continue
    resultado = extraer_abstract(os.path.join("pdfs", nombre))
    if resultado is None:
        print(f"No se encontró el abstract en {nombre}")
    else:
        print(f"Abstract de {nombre}: {len(resultado)} caracteres:", resultado[:100])