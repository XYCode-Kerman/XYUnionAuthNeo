from redis.asyncio import Redis

from configs import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_USERNAME

db = Redis(host=REDIS_HOST, port=REDIS_PORT,
           password=REDIS_PASSWORD, username=REDIS_USERNAME)
