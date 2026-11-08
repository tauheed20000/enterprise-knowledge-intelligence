from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Enterprise Knowledge Intelligence",
    description="AI-powered Enterprise Knowledge Assistant",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Welcome to Enterprise Knowledge Intelligence",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Enterprise Knowledge Intelligence"
    }