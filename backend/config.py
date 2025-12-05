"""Application configuration"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Silent Signal"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis (optional - disabled if Docker not available)
    REDIS_URL: str = ""
    REDIS_CACHE_TTL: int = 3600
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    CORS_CREDENTIALS: bool = True
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    # WorkOS
    WORKOS_API_KEY: str = ""
    WORKOS_CLIENT_ID: str = ""
    WORKOS_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    WORKOS_COOKIE_PASSWORD: str = ""
    
    # Cerebras
    CEREBRAS_API_KEY: str = ""
    CEREBRAS_API_URL: str = "https://api.cerebras.ai/v1"
    CEREBRAS_MODEL: str = "llama3.1-8b"
    
    # ElevenLabs
    ELEVENLABS_API_KEY: str = ""
    ELEVENLABS_VOICE_ID: str = "21m00Tcm4TlvDq8ikWAM"
    ELEVENLABS_MODEL: str = "eleven_monolingual_v1"
    
    # Raindrop
    RAINDROP_API_KEY: str = ""
    RAINDROP_API_URL: str = "https://api.raindrop.ai/v1"
    RAINDROP_SMARTFLOW_ID: str = ""
    
    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_ID_FREE: str = ""
    STRIPE_PRICE_ID_PREMIUM: str = ""
    
    # Searchable
    SEARCHABLE_API_KEY: str = ""
    SEARCHABLE_INDEX_NAME: str = "silentsignal_gestures"
    SEARCHABLE_API_URL: str = "https://api.searchable.ai/v1"
    
    # Vultr
    VULTR_API_KEY: str = ""
    VULTR_INSTANCE_ID: str = ""
    VULTR_OBJECT_STORAGE_URL: str = ""
    
    # Cloudflare
    CLOUDFLARE_API_TOKEN: str = ""
    CLOUDFLARE_ZONE_ID: str = ""
    CLOUDFLARE_ACCOUNT_ID: str = ""
    
    # Netlify
    NETLIFY_AUTH_TOKEN: str = ""
    NETLIFY_SITE_ID: str = ""
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
