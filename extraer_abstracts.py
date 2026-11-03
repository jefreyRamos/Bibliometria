import os
import json
import unicodedata
from pypdf import PdfReader

MARCAS_FIN = ["\nkeywords", "\nkey words", "introduction", "corresponding author"]

CORTES_MANUALES = {
    "9.": "development efforts.",
}


def extraer_abstract(ruta_pdf):
    lector = PdfReader(ruta_pdf)
    texto = ""
    for pagina in lector.pages[:2]:
        texto += pagina.extract_text() + "\n"
    texto = texto.replace("A B S T R A C T", "ABSTRACT") # Normalizar el texto del pdf 7
    minus = texto.lower()

    inicio = minus.find("abstract")
    if inicio == -1:
        return None
    inicio += len("abstract")

    fin = -1
    for marca in MARCAS_FIN:
        pos = minus.find(marca, inicio + 300) # Buscar la marca de fin a partir de 300 caracteres después del inicio del abstract
        if pos != -1 and (fin == -1 or pos < fin): # Actualizar la posición de fin si se encuentra una marca más cercana
            fin = pos
    if fin == -1:
        return None

    abstract = texto[inicio:fin].replace("-\n", "")
    lineas = abstract.strip().split("\n")
    if lineas[0].lower().startswith("keywords"): # Eliminar la línea de keywords si está al inicio del abstract
        while lineas and len(lineas[0]) < 60:
            lineas.pop(0)
    abstract = " ".join(lineas).strip()

    nombre = os.path.basename(ruta_pdf)
    for prefijo, frase_final in CORTES_MANUALES.items(): # Recortar el abstract si el nombre del archivo coincide con un prefijo y contiene la frase final
        if nombre.startswith(prefijo):
            pos = abstract.find(frase_final)
            if pos != -1: # Recortar el abstract hasta la frase final si se encuentra
                abstract = abstract[:pos + len(frase_final)]

    if abstract.endswith("1."):
        abstract = abstract[:-2].strip() # Eliminar el "1." al final del abstract si está presente
    abstract = abstract.lstrip(":.- —").strip()
    return unicodedata.normalize("NFKC", abstract)


corpus = []
archivos = [n for n in os.listdir("pdfs") if n.lower().endswith(".pdf")]
archivos = sorted(archivos, key=lambda n: int(n.split(".")[0])) # Ordenar los archivos por el número al inicio del nombre del archivo
for nombre in archivos:
    if not nombre.lower().endswith(".pdf"):
        continue
    resultado = extraer_abstract(os.path.join("pdfs", nombre))
    numero = int(nombre.split(".")[0])
    corpus.append({"id": numero, "archivo": nombre, "abstract": resultado}) # Agregar el resultado al corpus como un diccionario con el id, nombre del archivo y abstract
    print(f"{numero}: {len(resultado or '')} caracteres")

with open("corpus.json", "w", encoding="utf-8") as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2) # Guardar el corpus en un archivo JSON con codificación UTF-8 y formato legible
print("Guardado corpus.json con", len(corpus), "artículos")