import redis
import pickle
import os
import functools
import hashlib
from utils.logger import get_logger

logger = get_logger(__name__)

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

class CacheManager:
    def __init__(self):
        try:
            self.redis = redis.from_url(REDIS_URL)
            self.redis.ping()
            self.enabled = True
        except Exception as e:
            logger.error("cache_init_failed", error=str(e))
            self.enabled = False

    def get(self, key):
        if not self.enabled: return None
        try:
            data = self.redis.get(key)
            if data:
                return pickle.loads(data) # nosec B301
        except Exception as e:
            logger.error("cache_get_error", key=key, error=str(e))
        return None

    def set(self, key, value, ttl=300):
        if not self.enabled: return
        try:
            self.redis.setex(key, ttl, pickle.dumps(value))
        except Exception as e:
            logger.error("cache_set_error", key=key, error=str(e))

    def cached(self, prefix, ttl=300):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self.enabled:
                    return func(*args, **kwargs)
                
                # Create a cache key based on args
                key_data = f"{prefix}:{func.__name__}:{args}:{kwargs}"
                key_hash = hashlib.sha256(key_data.encode()).hexdigest()
                cache_key = f"{prefix}:{key_hash}"
                
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    logger.info("cache_hit", key=cache_key)
                    return cached_result
                
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result
            return wrapper
        return decorator

cache = CacheManager()
