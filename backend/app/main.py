from fastapi import FastAPI

from app.routers.eligibility import router as eligibility_router

app = FastAPI(
    title="Nirman Setu Core API",
    description="AI-powered government scheme eligibility platform",
    version="1.0.0"
)

app.include_router(eligibility_router)


@app.get("/")
def root():
    return {
        "message": "Nirman Setu Core API is running"
    }