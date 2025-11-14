import redis
from config import REDIS_HOST, REDIS_PORT

def get_redis_client():
    return redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0,
        decode_responses=True
    )
