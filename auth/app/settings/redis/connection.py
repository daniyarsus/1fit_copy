from redis import asyncio as redis

from app.settings.config import settings


redis_client_jwt = redis.from_url(settings.regis_config.REDIS_URL_JWT)
redis_client_register = redis.from_url(settings.regis_config.REDIS_URL_REGISTER)
redis_client_password = redis.from_url(settings.regis_config.REDIS_URL_PASSWORD)
