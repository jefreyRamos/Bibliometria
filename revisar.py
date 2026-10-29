from pypdf import PdfReader

for n in ["7", "9", "17"]:
    import os
    nombre = [f for f in os.listdir("pdfs") if f.startswith(n + ".")][0]
    texto = PdfReader("pdfs/" + nombre).pages[0].extract_text()
    print("=====", nombre)
    print(texto[:1500])