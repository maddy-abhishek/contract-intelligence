from fastapi import FastAPI
from app.database import engine, Base
from app.routers import documents, analysis  
from prometheus_fastapi_instrumentator import Instrumentator

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contract Intelligence API")

app.include_router(documents.router)
app.include_router(analysis.router)         
Instrumentator().instrument(app).expose(app)

@app.get("/healthz")
def health_check():
    return {"status": "ok"}