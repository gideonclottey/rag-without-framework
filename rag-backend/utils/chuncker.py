def chunk_text(text, chunk_size: int=500, overlap: int=50)-> list:
    """Chunk text into smaller pieces with specified size and overlap."""

    if not text:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        start += chunk_size - overlap  # Move start forward with overlap

    return chunks


def chunk_documents(docs: list, chunk_size: int=500, overlap:int =50) -> list:
    """Chunk a list of documents into smaller pieces."""
    all_chunks = []
    for doc in docs:
        text = doc['text']
        chunks = chunk_text(text, chunk_size, overlap)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                'chunk_id': f"{doc['file_name']}_chunk_{i+1}",
                'text': chunk
            })

    return all_chunks