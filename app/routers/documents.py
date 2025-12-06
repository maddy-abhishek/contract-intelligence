from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ingestion import process_pdf
import shutil
import os

router = APIRouter()

@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Save file temporarily
    temp_file_path = f"temp_{file.filename}"
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Process the file (Extract & Embed)
        doc_id = process_pdf(temp_file_path, file.filename, db)
        
        return {"message": "Ingestion successful", "document_id": doc_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Cleanup: Remove temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)