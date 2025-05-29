from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

INDEX_NAME = "test-index"

try:
    if es.indices.exists(index=INDEX_NAME):
        print("✅ Index existiert.")
    else:
        print("❌ Index existiert nicht.")
except Exception as e:
    print("❗ FEHLER beim Check:", e)
