"""Main FastAPI application entry point."""
from fastapi import FastAPI
import uvicorn

from api.controllers.url_controller import router as url_router

app = FastAPI(title="URL Shortener", version="0.1.0")

# Include routers
app.include_router(url_router)


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "URL Shortener API"}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}


def run():
    """Run the FastAPI application using uvicorn."""
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    run()