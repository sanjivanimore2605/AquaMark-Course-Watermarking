import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AquaMark — Secure Digital Watermarking & Document Integrity Platform"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./aquamark.db"
    
    # Security & Cryptography
    SECRET_KEY: str = "aquamark-dev-super-secure-secret-key-32-bytes-min-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    
    # Argon2id Parameters
    ARGON2_TIME_COST: int = 2
    ARGON2_MEMORY_COST: int = 65536
    ARGON2_PARALLELISM: int = 2
    
    # Storage Paths
    BASE_STORAGE_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../storage"))
    UPLOAD_DIR: str = os.path.join(BASE_STORAGE_PATH, "uploads")
    PROTECTED_DIR: str = os.path.join(BASE_STORAGE_PATH, "protected")
    KEYS_DIR: str = os.path.join(BASE_STORAGE_PATH, "keys")
    EXPERIMENTS_DIR: str = os.path.join(BASE_STORAGE_PATH, "experiments")
    
    # Upload limits
    MAX_UPLOAD_SIZE_BYTES: int = 25 * 1024 * 1024  # 25 MB
    MAX_PAGE_COUNT: int = 100
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure directories exist
for path in [settings.UPLOAD_DIR, settings.PROTECTED_DIR, settings.KEYS_DIR, settings.EXPERIMENTS_DIR]:
    os.makedirs(path, exist_ok=True)
