from redis import asyncio as redis

from app.settings.config import settings

redis_client_auth = redis.from_url(settings.regis_config.REDIS_URL_AUTH)
