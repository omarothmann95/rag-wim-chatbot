# chatbot_query.py
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_elasticsearch import ElasticsearchStore
from langchain.chains import RetrievalQA

# .env laden
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Elasticsearch Client
es = Elasticsearch("http://localhost:9200", request_timeout=30)
INDEX_NAME = "studiengang-index"

# Embedding Modell
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)

# Neuer Vectorstore mit ElasticsearchStore
vectorstore = ElasticsearchStore(
    es_connection=es,
    index_name=INDEX_NAME,
    embedding=embedding_model,
)

# GPT-Modell (ChatOpenAI)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, openai_api_key=OPENAI_API_KEY)

# Retrieval-basiertes QA-System
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True
)

# Eingabe starten
print("🎓 Frag mich etwas zum Studiengang Wirtschaftsinformatik (Tippe 'exit' zum Beenden)")

while True:
    frage = input("\n🧠 Deine Frage: ")
    if frage.lower() == "exit":
        break

    antwort = qa_chain.invoke({"query": frage})
    print("\n💬 GPT-Antwort:\n", antwort["result"])
    print("-" * 60)
