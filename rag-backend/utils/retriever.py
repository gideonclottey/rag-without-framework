import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./db")


collection = client.get_or_create_collection('rag_chunks')

def store_chunks_in_chroma(chunks, embeddings, batch_size=10):
    ids = [chunk["chunk_id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]

    # ✅ Break into batches
    for i in range(0, len(ids), batch_size):
        collection.add(
            ids=ids[i:i+batch_size],
            documents=documents[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size],
        )

    print(f"✅ Stored {len(ids)} chunks in ChromaDB.")

def reset_collection():
    global collection
    try:
        client.delete_collection('rag_chunks')
        print("✅ Collection 'rag_chunks' deleted.")
    except Exception:
        pass
    collection = client.get_or_create_collection('rag_chunks')

def retrieve_relevant_chunks(query: str, top_k: int=5) -> list:
    """Retrieve the most relevant text chunks for a given query."""
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = embedding_model.encode([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results['documents'][0] if 'documents' in results and results['documents'] else []


