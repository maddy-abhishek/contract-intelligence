from fastapi import FastAPI

app = FastAPI(title="Contract Intelligence API")

@app.get("/healthz")
def health_check():
    return {"status": "ok", "message": "Service is running"}