from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Agentic RAG for Software Engineering Question Answering",
)


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "environment": settings.app_env,
        "version": "1.0.0",
    }


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": f"Welcome to {settings.app_name}"
    }
    