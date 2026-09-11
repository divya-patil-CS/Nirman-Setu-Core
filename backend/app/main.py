from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import chat
from app.routers.eligibility import router as eligibility_router

app = FastAPI(
    title="Nirman Setu Core API",
    description="AI-powered government scheme eligibility platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(eligibility_router)


@app.get("/")
def root():
    return {
        "message": "Nirman Setu Core API is running"
    }