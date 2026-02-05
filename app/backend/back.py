from fastapi import FastAPI
from backend.api.v1.router import router as v1_router

app = FastAPI(title="Diagram Recognition API", version="0.1")

app.include_router(v1_router)

@app.get("/")
def root():
    return {"message": "Diagram Recognition API is running"}