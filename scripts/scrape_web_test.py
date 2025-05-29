# scrape_web.py
import requests as rq
from bs4 import BeautifulSoup
import json

# Alle Zielseiten
urls = {
    "website": "https://www.inf.reutlingen-university.de/studium/master/wirtschaftsinformatik-wim",
    "ranking": "https://www.inf.reutlingen-university.de/fakultaet/ranking-akkreditierung",
    "aktuelles": "https://www.inf.reutlingen-university.de/fakultaet/aktuelles"
}

# Text aus HTML extrahieren
def textauslesen(url):
    antwort = rq.get(url)
    soup = BeautifulSoup(antwort.text, "html.parser")
    for tag in soup(["script", "style", "header", "footer", "nav"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)

# Alle Seiten durchgehen
for name, url in urls.items():
    print(f"🔎 Lade: {url}")
    text = textauslesen(url)
    chunks = [text[i:i+800] for i in range(0, len(text), 700)]
    with open(f"data/{name}_chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(chunks)} Chunks gespeichert in: data/{name}_chunks.json")
