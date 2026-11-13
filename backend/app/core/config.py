# Pydantic BaseSettings Configuration

import os
import json
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
class Settings(BaseSettings):
    PROJECT_NAME: str = "Skills Intelligence API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # MongoDB Configuration
    MONGO_URI: str
    DB_NAME: str = "tracera"
    COLLECTION_NAME: str = "raw_linkedin"
    PROCESSED_COLLECTION_NAME: str = "profiles_db"

    # Security Configuration
    INTERNAL_API_KEY: str = "tracera-skills-intelligence-secret-key-2026"

    # CORS Origins (Bisa berupa list string atau JSON string)
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:8501", "http://127.0.0.1:8501"]
    
    # Server Execution Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    ENVIRONMENT: str = "development"
    @field_validator("CORS_ORIGINS", mode="before")
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )
settings = Settings()

