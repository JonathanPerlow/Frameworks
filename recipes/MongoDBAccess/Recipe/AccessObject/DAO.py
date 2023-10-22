from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

from recipes.MongoDBAccess.Recipe.CustomErrorClass import DatabaseError

from ..Models.Recipe import RecipeModel

# from Interface import DAOInterface
from .Interface import DAOInterface


class DAO(DAOInterface):
    def __init__(
        self, client: AsyncIOMotorClient, database_name: str, collection_name: str
    ):
        self.client = client
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    async def save_recipe(self, recipe: RecipeModel):
        try:
            await self.collection.insert_one(recipe)
        except PyMongoError as e:
            raise DatabaseError(f"An error occurred when saving recipe: {e}")

    async def get_all_recipe(self) -> list:
        try:
            recipe_cursor = self.collection.find({})
            recipes = [recipe for recipe in await recipe_cursor.to_list(length=100)]
            return recipes
        except PyMongoError as e:
            raise DatabaseError(f"An error occurred when fetching all the recipes: {e}")

    async def get_one_recipe(self, query: dict) -> dict:
        try:
            recipe_document: dict = await self.collection.find_one(query)
            return recipe_document
        except PyMongoError as e:
            raise DatabaseError(f"An error occurred when fetching the recipe: {e}")

    # Update recipe method
    async def update_one_recipe(
        self, recipe_document: dict, update: RecipeModel
    ) -> int:
        try:
            recipe = await self.collection.update_one(recipe_document, {"$set": update})
            return recipe.modified_count
        except PyMongoError as e:
            raise DatabaseError(f"An error occurred when updating the recipe: {e}")

    # remove recipe method
    async def delete_one(self, query: dict) -> int:
        try:
            result = await self.collection.delete_one(query)
            return result.deleted_count
        except PyMongoError as e:
            raise DatabaseError(f"An error occurred when deleting the recipe: {e}")
