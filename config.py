"""
Configuration settings for the Portfolio API
Minimal version for Vercel deployment
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Settings
    APP_NAME: str = "Anshul Parate AI Portfolio Assistant"
    APP_VERSION: str = "3.0.0-minimal"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # CORS Settings
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:5174",
        "*"  # Allow all origins for development
    ]
    
    # Google Gemini Settings
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.5-pro"  # Fastest model
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_OUTPUT_TOKENS: int = 2048  # Reduced for faster responses
    
    # Memory Settings
    MAX_CONVERSATION_HISTORY: int = 10  # Keep only last 10 messages
    
    # Session Settings
    DEFAULT_SESSION_ID: str = "default"
    SESSION_TIMEOUT_MINUTES: int = 30
    
    def validate(self):
        """Validate required settings - returns True if valid, raises ValueError if not"""
        if not self.GOOGLE_API_KEY:
            raise ValueError(
                "❌ GOOGLE_API_KEY is not set in environment variables. "
                "Please add it in Vercel Dashboard: Settings > Environment Variables. "
                "Get your key from: https://makersuite.google.com/app/apikey"
            )
        return True
    
    def is_configured(self) -> bool:
        """Check if API key is configured without raising exception"""
        return bool(self.GOOGLE_API_KEY)

# Create settings instance
settings = Settings()
