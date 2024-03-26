from redis import asyncio as redis

from app.settings.config import settings

REDIS_USER = settings.redis_config.REDIS_USER
REDIS_PASS = settings.redis_config.REDIS_PASS
REDIS_HOST = settings.redis_config.REDIS_HOST
REDIS_PORT = settings.redis_config.REDIS_PORT

redis_client_auth = redis.from_url(f"redis://{REDIS_USER}:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}")
