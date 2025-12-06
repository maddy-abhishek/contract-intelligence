import os
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import DocumentChunk
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Setup Models
# Must match the model used in ingestion!
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Use Gemini for the answer generation
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3, # Slight creativity allowed, but mostly factual
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def retrieve_documents(query: str, db: Session, limit: int = 5):
    """
    1. Embed the query.
    2. Perform vector search in Postgres.
    3. Return the most relevant chunks.
    """
    # Generate vector for the question
    query_vector = embedding_model.embed_query(query)
    
    # Perform Similarity Search using pgvector's cosine distance operator (<=>)
    # We order by distance (lower is better)
    stmt = select(DocumentChunk).order_by(
        DocumentChunk.embedding.cosine_distance(query_vector)
    ).limit(limit)
    
    results = db.execute(stmt).scalars().all()
    return results

def ask_question(query: str, db: Session):
    # 1. Retrieve Context
    retrieved_chunks = retrieve_documents(query, db)
    
    if not retrieved_chunks:
        return {
            "answer": "I couldn't find any relevant information in the documents.",
            "citations": []
        }

    # 2. Format Context for the LLM
    # We create a string that looks like:
    # [Source ID: 1, Page: 2] Text...
    context_text = ""
    citations = []
    
    for chunk in retrieved_chunks:
        citation_str = f"[Doc ID: {chunk.document_id}, Page: {chunk.chunk_index}]" # using index as proxy for page if simple
        context_text += f"{citation_str}\n{chunk.chunk_text}\n\n"
        
        citations.append({
            "document_id": chunk.document_id,
            "text": chunk.chunk_text[:100] + "...", # Preview
            "score": "High Relevance" # In a real app, you'd calculate the score
        })

    # 3. Construct Prompt
    prompt = ChatPromptTemplate.from_template("""
    You are an expert contract assistant. Answer the user question based ONLY on the following context. 
    If the answer is not in the context, say "I don't know".
    
    Context:
    {context}
    
    Question: 
    {question}
    
    Answer:
    """)

    # 4. Generate Answer
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context_text, "question": query})
    
    return {
        "answer": answer,
        "citations": citations
    }