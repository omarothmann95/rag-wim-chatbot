# split_text.py
import json
import os
import textwrap

# Welche Dateien splitten?
input_files = {
    "module": "data/modulhandbuch.json",
    "pruefung": "data/pruefungsordnung.json"
}

# Länge der Chunks (Zeichen)
chunk_size = 800
overlap = 100

def split_text(text, size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += size - overlap
    return chunks

for key, file_path in input_files.items():
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            text = data["text"]
            chunks = split_text(text, chunk_size, overlap)
            
            output_path = f"data/{key}_chunks.json"
            with open(output_path, "w", encoding="utf-8") as out_f:
                json.dump(chunks, out_f, ensure_ascii=False, indent=2)
            print(f"✅ {len(chunks)} Chunks gespeichert unter: {output_path}")
    else:
        print(f"⚠️ Datei nicht gefunden: {file_path}")
