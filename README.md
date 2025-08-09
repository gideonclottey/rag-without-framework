# rag-without-framework
 Retrieval-Augmented Generation (RAG) system without using LangChain or similar frameworks

 # RAG Without Frameworks (FastAPI + Chroma + Gemini)

## Setup
python -m venv venv
# Windows PowerShell
./venv/Scripts/Activate.ps1
pip install -r requirements.txt

# env
copy env.example .env
# then edit .env and set GEMINI_API_KEY

## Run API
uvicorn api:app --reload --port 8000

## Endpoints
- POST /ingest { folder, chunk_size, overlap }
- POST /query { query, top_k }
- POST /upload (multipart/form-data)

## Dev URLs
- /docs
- /health

