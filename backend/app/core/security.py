# API Key Authentication Middleware & Dependency

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from backend.app.core.config import settings

# Header kunci otorisasi: X-API-KEY
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Validasi header X-API-KEY.
    Jika request datang dari lingkungan development lokal tanpa API key,
    bisa diizinkan secara bersyarat, atau tolak dengan HTTP 403 Forbidden.
    """
    if not api_key:
        if settings.ENVIRONMENT == "development":
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Header 'X-API-KEY' tidak ditemukan pada request!"
        )
    if api_key != settings.INTERNAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kredensial API Key tidak valid atau telah kedaluwarsa!"
        )
    return True
    