# preprocess_pdf.py
import fitz  # PyMuPDF
import os
import json

# Pfade zu den PDF-Dateien
pdf_files = {
    "modulhandbuch": "data/modulhandbuch.pdf",
    "pruefungsordnung": "data/pruefungsordnung.pdf"
}

# Funktion zum Extrahieren des Textes
def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text() + "\n"  # Zeilenumbruch ergänzen
    return text

# Alle Texte extrahieren und speichern
for name, path in pdf_files.items():
    if os.path.exists(path):
        try:
            print(f"📄 Extrahiere: {path}")
            text = extract_text_from_pdf(path)
            output_path = f"data/{name}.json"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Sicherstellen, dass data/ existiert
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump({"text": text}, f, ensure_ascii=False, indent=2)
            print(f"✅ Gespeichert unter: {output_path}")
        except Exception as e:
            print(f"❌ Fehler beim Verarbeiten von {path}: {e}")
    else:
        print(f"⚠️ Datei nicht gefunden: {path}")
