import os
from dotenv import load_dotenv
import redis

load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST') or 'localhost'
REDIS_PORT = int(os.getenv('REDIS_PORT') or '6379')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True,
    protocol=2
)

