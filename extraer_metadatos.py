import os, json
from pypdf import PdfReader

CORRECCIONES = {
    "13": {"titulo": "Artificial intelligence for education and its emphasis on assessment and adversity quotient: a review",
        "autores": ["Jyoti Mudkanna Gavhane", "Reena Pagare"]},
    "14": {"autores": ["Tamar Mikeladze", "Paulien C. Meijer", "Roald P. Verhoeff"]},
}

def separar_autores(texto):
    texto = texto.replace(" and ", ",")
    return [a.strip() for a in texto.split(",") if a.strip()]

with open("corpus.json", encoding="utf-8") as f:
    corpus = json.load(f)

for doc in corpus:
    meta = PdfReader(os.path.join("pdfs", doc["archivo"])).metadata
    doc["titulo"] = (meta.title or "").strip() if meta else ""
    doc["autores"] = separar_autores(meta.author) if meta and meta.author else []
    num = doc["archivo"].split(".")[0]
    if num in CORRECCIONES:
        doc.update(CORRECCIONES[num])
    print(f'{doc["id"]:2} | {doc["titulo"][:60]:60s} | {", ".join(doc["autores"])[:40]}')

with open("corpus.json", "w", encoding="utf-8") as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)
print("corpus.json actualizado con titulo y autores")