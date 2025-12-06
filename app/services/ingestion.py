import os
from pypdf import PdfReader
from langchain_huggingface import HuggingFaceEmbeddings  # <-- Updated import
from sqlalchemy.orm import Session
from app.models import Document, DocumentChunk

# Initialize Local Hugging Face Model
# This runs locally on CPU (or GPU if available)
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def process_pdf(file_path: str, filename: str, db: Session):
    # 1. Read PDF
    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    # 2. Create Document Record
    new_doc = Document(filename=filename)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # 3. Chunking 
    chunk_size = 500  # Smaller chunks often work better with smaller models
    overlap = 50
    chunks = []
    
    text_len = len(full_text)
    start = 0
    while start < text_len:
        end = start + chunk_size
        chunk_text = full_text[start:end]
        chunks.append(chunk_text)
        start += (chunk_size - overlap)

    # 4. Generate Embeddings & Save
    # We batch process for speed
    vectors = embedding_model.embed_documents(chunks)
    
    for idx, (text_content, vector) in enumerate(zip(chunks, vectors)):
        db_chunk = DocumentChunk(
            document_id=new_doc.id,
            chunk_index=idx,
            chunk_text=text_content,
            embedding=vector
        )
        db.add(db_chunk)
    
    db.commit()
    return new_doc.id