import os

from dotenv import load_dotenv

from dotenv import load_dotenv, find_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from MongoDBAccess.Recipe.AccessObject.DAO import DAO
from MongoDBAccess.Recipe.AccessObject.Interface import DAOInterface
from MongoDBAccess.Recipe.Services.Service import Service
from MongoDBAccess.Recipe.Services.Interface import ServiceInterface

load_dotenv(find_dotenv())

PASSWORD = os.environ.get("MONGODB_PASSWORD")
CONNECTION_STRING = (
    f"mongodb+srv://Jonathan:{PASSWORD}@cluster0.c03kgdq.mongodb.net/test"
)
DB_NAME = "Recipes_db"
COLLECTION_NAME = "recipes"
async_client = AsyncIOMotorClient(CONNECTION_STRING)
recipe_db: DAOInterface = DAO(async_client, DB_NAME, COLLECTION_NAME)
recipe_service_db: ServiceInterface = Service(recipe_db)
