from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ContractExtraction
from app.services.extraction import extract_contract_fields
from pydantic import BaseModel
from typing import List, Optional
from app.services.rag import ask_question

router = APIRouter()

@router.post("/extract/{document_id}", response_model=ContractExtraction)
async def extract_data(document_id: int, db: Session = Depends(get_db)):
    """
    Extracts structured fields (parties, dates, liability) from a specific document.
    """
    try:
        # Call the service
        data = extract_contract_fields(document_id, db)
        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Log the error here in production
        raise HTTPException(status_code=500, detail=str(e))

# Schema for the Request
class QuestionRequest(BaseModel):
    question: str

# Schema for the Response
class Citation(BaseModel):
    document_id: int
    text: str

class AnswerResponse(BaseModel):
    answer: str
    citations: List[Citation]

@router.post("/ask", response_model=AnswerResponse)
async def ask_document_question(request: QuestionRequest, db: Session = Depends(get_db)):
    """
    RAG Endpoint: Answers questions based on uploaded documents.
    """
    try:
        response = ask_question(request.question, db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))