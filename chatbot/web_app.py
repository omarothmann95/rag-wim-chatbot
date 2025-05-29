# chatbot/web_app.py
import os
import streamlit as st
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_elasticsearch import ElasticsearchStore
from langchain.chains import RetrievalQA

# 🔐 .env laden
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ⚙️ Elasticsearch-Client
es = Elasticsearch("http://localhost:9200", request_timeout=30)
INDEX_NAME = "studiengang-index"

# 🧠 Embedding-Modell
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=OPENAI_API_KEY
)

# 🔎 Vektorsuche mit ElasticsearchStore
vectorstore = ElasticsearchStore(
    index_name=INDEX_NAME,
    embedding=embedding_model,
    es_connection=es, 
)

# 💬 GPT-Modell
llm = ChatOpenAI(
    model="gpt-4-turbo",
    temperature=0.2,
    openai_api_key=OPENAI_API_KEY
)

# 🔁 QA-Kette mit Quellenanzeige
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 10}),
    return_source_documents=True
)

# 🌐 Streamlit UI
st.set_page_config(page_title="WIM Studiengangs-Chatbot", page_icon="🎓")
st.title("🎓 Studiengang Wirtschaftsinformatik – GPT-Chatbot")
st.markdown("Stelle Fragen zum Studiengang, z. B. Inhalte, Prüfungen, Bewerbungen...")

frage = st.text_input("🧠 Deine Frage:")

if frage:
    with st.spinner("💭 GPT denkt nach..."):
        result = qa_chain.invoke({"query": frage})
        st.markdown("## 💬 GPT-Antwort")
        st.write(result["result"])

        
