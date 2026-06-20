# Chat with your PDF

A simple full-stack app to upload a PDF and ask questions about it. Built as a learning project for LangChain (RAG pipeline).

## Stack

- **Backend:** FastAPI, LangChain, FAISS, HuggingFace embeddings, Groq (LLaMA 3.1)
- **Frontend:** React + TypeScript, Vite

## How it works

1. Upload a PDF → backend loads it, splits it into chunks, embeds each chunk, and stores them in a FAISS vector index
2. Ask a question → backend finds the most relevant chunks (semantic search), builds a prompt with that context + recent chat history, and sends it to Groq's LLM for an answer

## Run it

**Backend**

```
cd backend
pip install -r requirements.txt
# add GROQ_API_KEY to a .env file
uvicorn main:app --reload
```

Runs on `http://localhost:8000`

**Frontend**

```
cd frontend
npm install
npm run dev
```

Runs on `http://localhost:5173`
