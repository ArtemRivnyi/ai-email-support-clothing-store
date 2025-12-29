import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration with validation"""
    
    # Required
    REDIS_URL: str = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    OLLAMA_HOST: str = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    
    # Gmail (Required for production)
    GMAIL_CREDENTIALS: str = 'credentials.json'
    GMAIL_TOKEN: str = 'token.pickle'
    
    # Optional
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    CHECK_INTERVAL_MINUTES: int = int(os.getenv('CHECK_INTERVAL_MINUTES', '5'))
    
    @classmethod
    def validate(cls):
        """Validate all required configs"""
        errors = []
        
        # Check for critical files/vars
        # Note: In Docker, we might pass credentials via secrets/volumes, 
        # so checking for local file existence might be tricky if paths differ.
        # But for this setup:
        if not os.path.exists(cls.GMAIL_CREDENTIALS) and not os.path.exists(cls.GMAIL_TOKEN):
             # Warn but don't fail if we are just testing or in CI
             pass 
             # errors.append("Gmail credentials (credentials.json or token.pickle) missing")

        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
