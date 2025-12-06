from fastapi import FastAPI
from app.database import engine, Base
from app.routers import documents, analysis  # <-- Import the new router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contract Intelligence API")

app.include_router(documents.router)
app.include_router(analysis.router)          # <-- Register the new router

@app.get("/healthz")
def health_check():
    return {"status": "ok"}