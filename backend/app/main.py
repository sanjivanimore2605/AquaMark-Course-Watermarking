import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.api.v1 import auth, documents, watermarks, verify, experiments, dashboard

# Initialize tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Secure Digital Watermarking and Document Integrity Platform for Educational Course Content.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(watermarks.router, prefix=settings.API_V1_STR)
app.include_router(verify.router, prefix=settings.API_V1_STR)
app.include_router(experiments.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "HEALTHY", "system": "AquaMark", "version": "1.0.0"}
