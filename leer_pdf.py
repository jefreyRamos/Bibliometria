from pypdf import PdfReader

lector = PdfReader("pdfs/1. Artificial intelligence literacy in higher and adult education A scoping literature review.pdf")

print("Número de páginas:", len(lector.pages))

texto = lector.pages[0].extract_text()
print(texto)