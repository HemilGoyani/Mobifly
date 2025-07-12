import redis.asyncio as redis

redis_client = redis.Redis(
    host="localhost",  # or "redis" in docker
    port=6379,
    db=0,
    decode_responses=True
)
