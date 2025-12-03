from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    # API Configuration
    api_title: str = "LưuGọn API"
    api_version: str = "1.0.0"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # CORS Configuration
    cors_origins: str = "http://localhost:3000"
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    
    # Supabase Configuration
    supabase_url: str
    supabase_key: str
    
    # File Upload Configuration
    max_file_size_mb: int = 10
    allowed_image_types: list = ["image/jpeg", "image/png", "image/webp", "image/gif"]
    allowed_image_extensions: list = [".jpg", ".jpeg", ".png", ".webp", ".gif"]
    
    # Text Configuration
    max_text_length: int = 1000000
    
    # URL Configuration
    base_url: str = "http://localhost:3000"
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_period_seconds: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self) -> list:
        """Convert CORS_ORIGINS string to list"""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins

settings = Settings()
