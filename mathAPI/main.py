# main.py
#
# Entry point for the Math Microservice.
# Sets up FastAPI with JWT auth, static frontend, Swagger docs, and Prometheus monitoring.

import threading
import time
import webbrowser
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

from prometheus_fastapi_instrumentator import Instrumentator

from app.api.auth import router as auth_router
from app.controllers.math_controller import router as math_router
from app.models.database import Base, engine

# Directory with frontend files
FRONTEND_DIR = "frontend"

# Create DB tables from SQLAlchemy models
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="Math Microservice (JWT Protected)",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# 🔍 Enable Prometheus monitoring
Instrumentator().instrument(app).expose(app)

# Enable CORS for all origins (ok for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static HTML files from frontend/
app.mount(
    path="/static",
    app=StaticFiles(directory=FRONTEND_DIR, html=True),
    name="static",
)

# Redirect root → login.html
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/static/login.html")

# Register routers
app.include_router(auth_router)     # /login
app.include_router(math_router)     # /api/v1/pow etc.

# On startup: open login page in browser
@app.on_event("startup")
def open_login_page():
    def _open():
        time.sleep(1)
        webbrowser.open("http://127.0.0.1:8000/")
    threading.Thread(target=_open, daemon=True).start()

# Add JWT auth support in Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="Microservice for mathematical operations with JWT protection.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Run with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
