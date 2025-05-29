import os
import json
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from langchain_openai import OpenAIEmbeddings

# API-Key laden
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Elasticsearch-Client
es = Elasticsearch(
    "http://localhost:9200",
    request_timeout=30
)


# Index-Name
INDEX_NAME = "studiengang-index"

# OpenAI Embedding-Modell
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)

# Quelle: Chunks aus JSON
sources = {
    "module": "data/module_chunks.json",
    "pruefung": "data/pruefung_chunks.json",
    "website": "data/website_chunks.json",
    "ranking": "data/ranking_chunks.json",
    "aktuelles": "data/aktuelles_chunks.json"
}

# Versuche alten Index zu löschen (wenn er existiert)
try:
    es.indices.delete(index=INDEX_NAME)
    print(f"🗑️ Alter Index gelöscht: {INDEX_NAME}")
except Exception as e:
    print(f"ℹ️ Kein vorhandener Index zu löschen: {e}")


# Neuen Index mit richtigem Mapping anlegen
es.indices.create(
    index=INDEX_NAME,
    mappings={
        "properties": {
            "text": {"type": "text"},
            "source": {"type": "keyword"},
            "vector": {
                "type": "dense_vector",
                "dims": 1536,
                "index": True,
                "similarity": "cosine"
            }
        }
    }
)
print(f"📦 Neuer Index erstellt: {INDEX_NAME}")

# Embeddings erstellen und einfügen
for source_name, path in sources.items():
    with open(path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    for i, chunk in enumerate(chunks):
        vector = embedding_model.embed_query(chunk)
        doc = {
            "text": chunk,
            "source": source_name,
            "vector": vector
        }
        es.index(index=INDEX_NAME, document=doc)

    print(f"✅ {len(chunks)} Chunks von {source_name} gespeichert.")
