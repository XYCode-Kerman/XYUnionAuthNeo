import os

import dotenv

dotenv.load_dotenv()

SECRET = os.environ['SECRET']

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = int(os.environ['REDIS_PORT'])
REDIS_USERNAME = os.environ.get('REDIS_USERNAME', None)
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
