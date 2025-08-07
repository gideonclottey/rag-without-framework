from pathlib import Path

#document handling 
import fitz # PyMuPDF
import docx

# text processing
import re
from typing import List, Dict, Any

# embedding import
from sentence_transformers import SentenceTransformer

# vector store import
import chromadb
from chromadb.config import Settings

#LLM import
#import google.generative as genai

# FastAPI import
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# internal imports
print("Step 1: Import started")
from utils.file_loader import load_document_from_folder
from utils.chuncker import chunk_documents
from utils.embedder import embed_chunks
from utils.retriever import store_chunks_in_chroma
from utils.retriever import retrieve_relevant_chunks
from utils.generator import ask_gemini

print("✅ All modules imported")

docs = load_document_from_folder("data")
print(f"✅ Loaded {len(docs)} docs")

chunks = chunk_documents(docs)
print(f"✅ Chunked into {len(chunks)} chunks")

chunk_texts = [chunk["text"] for chunk in chunks]
embeddings = embed_chunks(chunk_texts)
print(f"✅ Embedded {len(embeddings)} chunks")

store_chunks_in_chroma(chunks, embeddings)
print("✅ Stored in ChromaDB")

query = input("❓ Ask a question: ")
top_chunks = retrieve_relevant_chunks(query, top_k=5)
print("✅ Retrieved top chunks")

answer = ask_gemini(query, top_chunks)
print("✅ Gemini answered")

print("Answer:\n", answer)