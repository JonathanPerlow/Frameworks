from sanic import Sanic
from sanic.response import json

from recipes.MongoDBAccess.Recipe.Services.Interface import ServiceInterface
from recipes.MongoDBAccess.Recipe.Models.Recipe import RecipeModel
from recipes.MongoDBAccess.Recipe.CustomErrorClass import DatabaseError
from sanic_openapi import openapi


def configure_routes(_app: Sanic, db_service: ServiceInterface):
    @_app.post("/create_recipe/<name:str>/<ingredients:str>", name="create_recipe")
    @openapi.response(201, {"application/json": RecipeModel}, description="Recipe created successfully.")
    @openapi.body(RecipeModel, description="Recipe data")
    async def create_recipe(request):
        try:
            name = request.json.get("name")
            ingredients = request.json.get("ingredients")
            recipe = await db_service.create_recipe(name, ingredients)
            if recipe:
                return json(recipe, status=201)
            return json({"error": f"The {recipe} could not be found"}, status=404)
        except DatabaseError as e:
            # Log it, will figure it out later
            print(f"Database error: {e}")
            return json({"error": "Internal Server Error"}, status=500)

    @_app.get("/get_recipe_by_id/<_id:str>", name="get_recipe_by_id")
    @openapi.response(201, {"application/json": RecipeModel}, description="Fetching a recipe was successfully")
    @openapi.body(RecipeModel, description="recipe data")
    async def get_one(request, _id: str):
        try:
            recipe = await db_service.get_one_recipe(_id)
            if recipe:
                return json(recipe, status=200)
            return json({"error": f"The {_id} could not be found"}, status=404)
        except DatabaseError as e:
            # Log it, will figure it out late
            print(f"Database error: {e}")

            return json({"error": "Internal Server Error"}, status=500)

    @_app.get("/get_recipes", name="get_recipes")
    @openapi.response(201, {"application/json": RecipeModel}, description="Fetching the recipes went good")
    @openapi.body(RecipeModel, description="recipe data")
    async def get_all(request):
        try:
            recipe = await db_service.get_all_recipes()
            if recipe:
                return json(recipe, status=200)
            return json({"error": f"The films could not be found"}, status=404)
        except DatabaseError as e:
            # Log it, will figure it out late
            print(f"Database error: {e}")

            return json({"error": "Internal Server Error"}, status=500)
