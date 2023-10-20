from fastapi import FastAPI, HTTPException

from MongoDBAccess.Recipe.Services.Interface import ServiceInterface
from MongoDBAccess.Recipe.Models.Recipe import RecipeModel
from MongoDBAccess.Recipe.CustomErrorClass import DatabaseError


def configure_routes(_app: FastAPI, db_service: ServiceInterface):
    @_app.post("/create_recipe/{name}/{ingredients}", response_model=RecipeModel, status_code=201)
    async def create_recipe(name: str, ingredients: str):
        try:
            recipe = await db_service.create_recipe(name, ingredients)
            if recipe:
                return recipe
            raise HTTPException(status_code=404, detail=f"The recipe with name {name} could not be created")
        except DatabaseError as e:
            # Log it, will figure it out later
            print(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @_app.get("/get_recipe_by_id/{recipe_id}", response_model=RecipeModel)
    async def get_recipe_by_id(recipe_id: str):
        try:
            recipe = await db_service.get_one_recipe(recipe_id)
            if recipe:
                return recipe
            raise HTTPException(status_code=404, detail=f"The recipe with ID: {recipe_id} could not be found")
        except DatabaseError as e:
            # Log it, will figure it out later
            print(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @_app.get("/get_recipes", response_model=list[RecipeModel])
    async def get_recipes():
        try:
            recipes = await db_service.get_all_recipes()
            if recipes:
                return recipes
            raise HTTPException(status_code=404, detail="No recipes found")
        except DatabaseError as e:
            # Log it, will figure it out later
            print(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
