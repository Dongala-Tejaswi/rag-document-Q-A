import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

def get_cache(key):
    return r.get(key)

def set_cache(key, value):
    r.set(key, value)