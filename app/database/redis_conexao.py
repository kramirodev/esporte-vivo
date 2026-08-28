import os
from dotenv import load_dotenv
import redis

load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=None,
    decode_responses= True,
    protocol=2
)

