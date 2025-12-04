"""
Configuration settings for the Insight Weaver API
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Settings
    APP_NAME: str = "Anshul Parate AI Portfolio Assistant"
    APP_VERSION: str = "2.0.0"
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
    GEMINI_MODEL: str = "gemini-2.5-pro"  # Faster model for quick responses
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_OUTPUT_TOKENS: int = 100000024  # Reduced for faster responses
    
    # Memory Settings
    MAX_CONVERSATION_HISTORY: int = 10  # Keep only last 10 messages
    MEMORY_WINDOW_SIZE: int = 10  # Rolling window of conversations
    
    # LangChain Settings
    LANGCHAIN_VERBOSE: bool = False  # Disabled for production speed
    
    # Session Settings
    DEFAULT_SESSION_ID: str = "default"
    SESSION_TIMEOUT_MINUTES: int = 30
    
    # Performance Settings
    ENABLE_CACHING: bool = True
    CACHE_TTL_SECONDS: int = 300  # 5 minutes
    
    def validate(self):
        """Validate required settings"""
        if not self.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY is not set. "
                "Please add it to your .env file. "
                "Get your key from: https://makersuite.google.com/app/apikey"
            )
        return True

# Create settings instance
settings = Settings()
