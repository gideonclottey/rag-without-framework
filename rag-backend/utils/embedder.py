from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(chunk_texts:list) -> list:
    """Embed a list of text chunks using a pre-trained SentenceTransformer model."""
    embeddings = embedding_model.encode(chunk_texts, convert_to_numpy=True).tolist()
    return embeddings
