import os
from sqlalchemy.orm import Session
from app.models import DocumentChunk
from app.schemas import AuditReport
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0, 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def audit_contract(document_id: int, db: Session) -> AuditReport:
    # 1. Fetch text (First 15 chunks is usually enough for key terms)
    chunks = db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document_id
    ).order_by(DocumentChunk.chunk_index).limit(15).all()
    
    if not chunks:
        raise ValueError("Document has no text chunks processed.")

    full_text = "\n".join([chunk.chunk_text for chunk in chunks])

    # 2. Define the Risk Rules in the Prompt
    # This is the "Brain" of the auditor
    system_prompt = """
    You are a strict AI Contract Auditor. Review the contract text for the following specific risks:
    
    1. **Unlimited Liability**: If liability is not capped or is uncapped for indirect damages. (Severity: High)
    2. **Auto-Renewal**: If the contract renews automatically with less than 30 days notice. (Severity: Medium)
    3. **Broad Indemnity**: If the client must indemnify the provider for "any and all claims" without standard exceptions. (Severity: High)
    4. **Termination**: If the provider can terminate for convenience (without cause) immediately. (Severity: High)
    
    Return a JSON object with a summary and a list of identified risks. 
    If a risk is NOT found, do not include it in the list.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{text}")
    ])

    # 3. Force Structured Output
    structured_llm = llm.with_structured_output(AuditReport)
    
    # 4. Run Analysis
    chain = prompt | structured_llm
    report = chain.invoke({"text": full_text})
    
    return report