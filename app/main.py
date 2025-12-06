from fastapi import FastAPI
from app.database import engine, Base
from app.routers import documents

# Create database tables automatically on startup
# This runs the SQL to create "documents" and "document_chunks" tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contract Intelligence API")

# Register the router
app.include_router(documents.router)

@app.get("/healthz")
def health_check():
    return {"status": "ok", "message": "Service is running"}