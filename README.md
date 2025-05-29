# RAG-Chatbot: Studiengang Wirtschaftsinformatik

Dieses Projekt ist ein intelligenter Chatbot, der Fragen zum Studiengang Wirtschaftsinformatik an der Hochschule Reutlingen beantwortet – basierend auf echten Inhalten aus dem Modulhandbuch, der Prüfungsordnung und der Studiengangswebseite.

# Technologien

- GPT (OpenAI via `langchain_openai`)
- Elasticsearch für Vektor-Suche
- LangChain für RAG-Verwaltung
- Streamlit als Weboberfläche
- PDF- und Webscraping für Datenbasis

#Projektstruktur

```bash
rag-wim-chatbot/
├── data/               # PDF-Inhalte + Chunks
├── scripts/            # Scraper + Preprocessing + Embedding
├── chatbot/            # RAG-Interface + Web-UI
├── .env                # OpenAI API Key (nicht hochladen!)
├── .gitignore
├── requirements.txt
└── README.md

# Startanleitung
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# .env-Datei anlegen
echo "OPENAI_API_KEY=dein_api_key" > .env

# Start
streamlit run chatbot/web_app.py