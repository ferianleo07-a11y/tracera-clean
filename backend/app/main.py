# FastAPI Application Entry Point &amp; Lifespan Hooks

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.database import connect_to_database, close_database_connection
from backend.app.routes import analytics, profiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Event Startup: Buat connection pool database
    await connect_to_database()
    yield
    # Event Shutdown: Tutup koneksi database
    await close_database_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version= settings.VERSION,
    description="REST API Skills Intelligence OJT 2026 UGM Science Techno Park",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Konfigurasi Cross-Origin Resource Sharing (CORS) untuk akses Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrasi Router Endpoints
app.include_router(analytics.router, prefix=settings.API_V1_STR)
app.include_router(profiles.router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint health check sistem."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

@app.get("/", tags =["Root"])
async def root():
    return {
        "message": "Skills Intelligence API is running.",
        "documentation": "/docs"
    }