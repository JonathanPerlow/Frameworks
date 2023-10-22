from motor.motor_asyncio import AsyncIOMotorClient
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, json, text
from sanic_cors import CORS
from sanic_openapi import openapi, openapi2_blueprint

from recipes.MongoDBAccess import DAO, DAOInterface, Service, ServiceInterface
from recipes.MongoDBAccess.Recipe.CustomErrorClass import DatabaseError
from recipes.MongoDBAccess.Recipe.Models.Recipe import RecipeModel
from recipes.SanicAPI import config

async_client = AsyncIOMotorClient(config.CONNECTION_STRING)
recipe_db: DAOInterface = DAO(async_client, config.DB_NAME, config.COLLECTION_NAME)
db_service: ServiceInterface = Service(recipe_db)

app = Sanic("recipe_apps")
# Cors configurations
CORS(app, automatic_options=True)

app.blueprint(openapi2_blueprint)


@app.post("/create_recipe/<name:str>/<ingredients:str>", name="create_recipe")
@openapi.response(
    201,
    {"application/json": RecipeModel},
    description="Recipe created successfully.",
)
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


@app.get("/get_recipe_by_id/<_id:str>", name="get_recipe_by_id")
@openapi.response(
    201,
    {"application/json": RecipeModel},
    description="Fetching a recipe was successfully",
)
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


@app.get("/get_recipes", name="get_recipes")
@openapi.response(
    201,
    {"application/json": RecipeModel},
    description="Fetching the recipes went good",
)
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


async def error_middleware(request: Request, response: HTTPResponse):
    try:
        return response
    except Exception as e:
        return text(f"Internal Server Error: {str(e)}", status=500)


app.register_middleware(error_middleware, attach_to="response")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
