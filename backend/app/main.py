from fastapi import FastAPI
from app.routers import chat

app = FastAPI(title="Nirman Setu Core")

app.include_router(chat.router)

@app.get("/")
def root():
    return {"status": "running"}