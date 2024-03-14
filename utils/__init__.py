import casbin
from motor.motor_asyncio import AsyncIOMotorClient

from config import DATABASE_NAME, DATABASE_URL
from utils.enforcer import enforcer

db = AsyncIOMotorClient(DATABASE_URL)[DATABASE_NAME]
