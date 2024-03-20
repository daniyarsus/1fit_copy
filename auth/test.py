import redis

from app.settings.config import settings


def read_users_in_redis():
    try:
        client = redis.from_url(settings.regis_config.REDIS_URL_JWT)
        keys = client.keys('*')
        data = {}
        for key in keys:
            value = client.get(key)
            if value is not None:
                data[key.decode('utf-8')] = value.decode('utf-8')
        return data
    except Exception as e:
        return {"error": f"Failed to connect to Redis: {e}"}


print(read_users_in_redis())
