from ishemalink import settings
import json

def get_redis_client():
    return settings.redis_client

def cache_get(key):
    data = get_redis_client().get(key)
    if data:
        return json.loads(data)
    return None

def cache_set(key, value, ex=60*60*24):
    return get_redis_client().set(key, json.dumps(value), ex=ex)

def cache_delete(key):
    return get_redis_client().delete(key)