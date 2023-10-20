import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
from motor.motor_asyncio import AsyncIOMotorClient

from recipes.MongoDBAccess.Recipe.AccessObject.DAO import DAO
from recipes.MongoDBAccess.Recipe.AccessObject.Interface import DAOInterface
from recipes.MongoDBAccess.Recipe.Services.Interface import ServiceInterface
from recipes.MongoDBAccess.Recipe.Services.Service import Service


def get_recipes_db(
    connection_string: str, db_name: str, collection_name: str
) -> ServiceInterface:
    async_client: AsyncIOMotorClient = AsyncIOMotorClient(connection_string)
    recipe_db: DAOInterface = DAO(async_client, db_name, collection_name)
    recipe_service_db: ServiceInterface = Service(recipe_db)
    return recipe_service_db
