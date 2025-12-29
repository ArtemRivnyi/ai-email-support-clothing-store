from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config.secrets import secrets
import os

REDIS_URL = secrets.get_secret('REDIS_URL', 'redis://localhost:6379/0')

# Initialize Limiter
# We use get_remote_address to identify users by IP
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=REDIS_URL,
    default_limits=["200 per day", "50 per hour"],
    strategy="fixed-window",
    swallow_errors=True
)

def init_rate_limiter(app):
    limiter.init_app(app)
    return limiter
