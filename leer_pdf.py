from pypdf import PdfReader

lector = PdfReader("pdfs/1. Artificial intelligence literacy in higher and adult education A scoping literature review.pdf")
texto = lector.pages[0].extract_text()
minus = texto.lower()

inicio = minus.find("abstract")
inicio = inicio + len("abstract")

fin = minus.find("introduction", inicio)

abstract = texto[inicio:fin].strip()

if abstract.endswith("1."):
    abstract = abstract[:-2].strip()

abstract = abstract.replace("\n", " ")

print(abstract)