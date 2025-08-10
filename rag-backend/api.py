import os
import shutil
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, File ,UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from typing import Optional as optional, List
#internal imports
from utils.file_loader import load_document_from_folder
from utils.chuncker import chunk_documents
from utils.embedder import embed_chunks
from utils.retriever import store_chunks_in_chroma, retrieve_relevant_chunks
from utils.generator import ask_gemini

app = FastAPI(title="RAG Backend API", version="1.0.0")

# CORS configuration for UI access

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ingestRequest(BaseModel):
    folder: str = "data"
    chunck_size: int = 500
    overlap: int = 50
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
@app.post("/upload")
async def upload_file(
    files: optional[list[UploadFile]] = File(None),
    file: optional[List[UploadFile]] = File(None),
    ):
   
   incoming = files or file or []
   if not incoming:
       return {"saved": [], "folder": str(DATA_DIR), "message": "No files uploaded."}
   
   saved: List[str] = []
   for f in incoming:
       dest = DATA_DIR / f.filename
       with dest.open("wb") as out:
           shutil.copyfileobj(f.file, out)
       saved.append(f.filename  )
       return {"Saved": saved, "folder": str(DATA_DIR)}
   


   
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
def ingest(request: ingestRequest):
    try:
        docs = load_document_from_folder(request.folder)
        chunks = chunk_documents(docs, chunk_size=request.chunck_size, overlap=request.overlap)     
        texts = [chunk["text"] for chunk in chunks]
        embs = embed_chunks(texts)
        store_chunks_in_chroma(chunks, embs)
        return {"message": f"Successfully ingested {len(docs)} documents and {len(chunks)} chunks."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/query")
def query(request: QueryRequest):
    try:
        chunks = retrieve_relevant_chunks(request.query, top_k=request.top_k)
        answer = ask_gemini(request.query, chunks)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))