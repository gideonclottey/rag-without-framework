
from pathlib import Path
import fitz  # PyMuPDF
import docx


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_text(file_path: str) -> str:
    """Extract text from a plain text file."""  
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text(file_path: str) -> str:       
    """Extract text from various file types."""
    suffix= Path(file_path).suffix.lower()
    if suffix == '.pdf':
        return extract_text_from_pdf(str(file_path))
    elif suffix == '.docx':
        return extract_text_from_docx(str(file_path))  
    elif suffix == '.txt':
        return extract_text_from_text(str(file_path))
    else:
        raise ValueError(f"Unsupported file type: {suffix}")    
    

def load_document_from_folder(folder_path: str):
    """Load a document from a specified folder and extract its text."""

    folder = Path(folder_path)
    docs = []
    for file in folder.glob('*'):
        if file.is_file():
            try:
                text = extract_text(str(file))
                docs.append({
                    'file_name': file.name,
                    'text': text
                })
            except Exception as e:
                print(f"Error processing {file}: {e}")
    return docs