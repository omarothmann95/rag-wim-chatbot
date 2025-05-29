# scrape_web.py
import requests as rq    # Http anfragen
from bs4 import BeautifulSoup # HTML parsen
import json

# Ziel-URL
url = "https://www.inf.reutlingen-university.de/studium/master/wirtschaftsinformatik-wim"


# Funktion zum Scrapen
def textauslesen(url):
    antwort = rq.get(url)
    soup = BeautifulSoup(antwort.text, "html.parser")

    # Entferne Menü, Footer, Skripte, Styles
    for tag in soup(["script", "style", "header", "footer", "nav"]):
        tag.decompose()

    # Extrahiere sauberen Text
    text = soup.get_text(separator=" ", strip=True)
    return text

# Text holen und als Chunks speichern
text = textauslesen(url)
chunks = [text[i:i+800] for i in range(0, len(text), 700)]

with open("data/website_chunks.json", "w", encoding="utf-8") as f: # Speichern der Chunks
    json.dump(chunks, f, ensure_ascii=False, indent=2) # JSON formatieren

print(f"✅ {len(chunks)} Chunks gespeichert in: data/website_chunks.json")
