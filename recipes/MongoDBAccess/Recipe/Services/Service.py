from bson import ObjectId
from recipes.MongoDBAccess.Recipe.CustomErrorClass import DatabaseError
from recipes.MongoDBAccess.Recipe.Models.Recipe import RecipeModel
from ..AccessObject.Interface import DAOInterface
from .Interface import ServiceInterface


class Service(ServiceInterface):
    def __init__(self, recipe_dao: DAOInterface):
        self.recipe_dao = recipe_dao

    async def create_recipe(self, name: str, ingredients: str) -> dict:
        try:
            _id = ObjectId()
            recipe_document: dict = RecipeModel(
              id=_id, name=name, ingredients=ingredients
            ).model_dump()
            await self.recipe_dao.save_recipe(recipe_document)
            return recipe_document
        except DatabaseError as db_error:
            raise db_error

    async def get_one_recipe(self, _id) -> dict:
        try:
            query: dict = {"_id": ObjectId(_id)}
            recipe_document = await self.recipe_dao.get_one_recipe(query)
            recipe = {}
            if recipe_document:
                _id = str(recipe_document.get("_id"))
                recipe_data = {
                    key: value for key, value in recipe_document.items() if key != "_id"
                }
                recipe_model = RecipeModel(id=_id, **recipe_data)
                recipe_json = recipe_model.model_dump()
                return recipe_json
            return recipe
        except DatabaseError as db_error:
            raise db_error

    async def get_all_recipes(self) -> list:

        try:
            recipes = []
            recipe_documents = await self.recipe_dao.get_all_recipe()
            if recipe_documents:
                for recipe_document in recipe_documents:
                    _id = str(recipe_document.get("_id"))
                    recipe_data = {
                        key: value for key, value in recipe_document.items() if key != "_id"
                    }
                    recipe_model = RecipeModel(id=_id, **recipe_data)
                    recipes_json = recipe_model.model_dump()
                    recipes.append(recipes_json)
            return recipes
        except DatabaseError as db_error:
            raise db_error

    async def update_one_recipe(self, _id, name, ingredients) -> str:
        try:
            id_query = {"_id": ObjectId(_id)}
            recipe_document = await self.recipe_dao.get_one_recipe(id_query)

            if recipe_document:
                recipe_id = str(_id)
                update = RecipeModel(id=recipe_id, name=name, ingredients=ingredients)
                updated_count = self.recipe_dao.update_one_recipe(
                    recipe_document, update
                )
                if updated_count == 1:
                    return f"Successful update of {_id}"
                if recipe_document == 0:
                    return f"Unsuccessful update of {_id}"
            return "The recipe doesn't exist"

        except DatabaseError as db_error:
            raise db_error

    async def delete_one_recipe(self, _id) -> str:
        try:
            query: dict = {"_id": _id}
            recipe_document = await self.recipe_dao.delete_one(query)
            if recipe_document == 1:
                return f"Successful delete of {_id}"
            if recipe_document == 0:
                return f"The id:{_id} didn't exist in the database "
        except DatabaseError as db_error:
            raise db_error
