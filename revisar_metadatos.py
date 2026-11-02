import os
from pypdf import PdfReader

archivos = sorted([a for a in os.listdir("pdfs") if a.lower().endswith(".pdf")],
                key=lambda a: int(a.split(".")[0]))
for a in archivos:
    meta = PdfReader(os.path.join("pdfs", a)).metadata
    titulo = meta.title if meta and meta.title else "-"
    autor = meta.author if meta and meta.author else "-"
    print(f"{a[:6]:6s} | {titulo[:70]:70s} | {autor[:50]}")