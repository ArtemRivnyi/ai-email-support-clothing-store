import os
from dotenv import load_dotenv
from utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

class SecretsManager:
    """
    Unified interface for accessing secrets.
    Currently uses environment variables (local .env), but can be extended
    to support AWS Secrets Manager, Google Secret Manager, or HashiCorp Vault.
    """
    
    @staticmethod
    def get_secret(key: str, default: str = None) -> str:
        """
        Retrieve a secret by key.
        """
        # In the future, logic can be added here to check a provider:
        # if os.getenv("SECRET_PROVIDER") == "AWS":
        #     return get_aws_secret(key)
        
        value = os.getenv(key, default)
        if value is None:
            logger.warning(f"Secret '{key}' not found and no default provided.")
        return value

# Global instance
secrets = SecretsManager()
