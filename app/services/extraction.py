import os
from sqlalchemy.orm import Session
from app.models import Document, DocumentChunk
from app.schemas import ContractExtraction
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.prompts import ChatPromptTemplate

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def extract_contract_fields(document_id: int, db: Session) -> ContractExtraction:
    # 1. Fetch text 
    chunks = db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document_id
    ).order_by(DocumentChunk.chunk_index).limit(15).all()
    
    if not chunks:
        raise ValueError("Document has no text chunks processed.")

    full_text = "\n".join([chunk.chunk_text for chunk in chunks])

    # 2. Define Prompt 
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert legal AI. Extract structured data from the following contract text."),
        ("human", "{text}")
    ])

    # 3. Structured Output
    structured_llm = llm.with_structured_output(ContractExtraction)
    
    # 4. Run Chain
    chain = prompt | structured_llm
    result = chain.invoke({"text": full_text})
    
    return result