import os

from pymongo import AsyncMongoClient, MongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.database import Database

MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(MONGODB_URI)
async_client = AsyncMongoClient(MONGODB_URI)


# -------------------------------------------------------------------------
# MongoDB Connection
# -------------------------------------------------------------------------
def get_database(db_name: str) -> Database:
    return client[db_name]


# -------------------------------------------------------------------------
# MongoDB Connection (ASYNC)
# -------------------------------------------------------------------------
def get_database_async(db_name: str) -> AsyncDatabase:
    return async_client[db_name]
