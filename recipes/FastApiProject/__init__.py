import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from recipes.FastApiProject import config
from recipes.MongoDBAccess import DAO, DAOInterface, Service, ServiceInterface
from recipes.MongoDBAccess.Recipe.CustomErrorClass import DatabaseError
from recipes.MongoDBAccess.Recipe.Models.Recipe import RecipeModel

async_client = AsyncIOMotorClient(config.CONNECTION_STRING)
recipe_db: DAOInterface = DAO(async_client, config.DB_NAME, config.COLLECTION_NAME)
db_service: ServiceInterface = Service(recipe_db)

app = FastAPI(title="recipe_app")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def error_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(
            content={"error": f"Internal Server Error: {e}"}, status_code=500
        )


@app.post(
    "/create_recipe/{name}/{ingredients}",
    response_model=RecipeModel,
    status_code=201,
)
async def create_recipe(name: str, ingredients: str):
    try:
        recipe = await db_service.create_recipe(name, ingredients)
        if recipe:
            return recipe
        raise HTTPException(
            status_code=404,
            detail=f"The recipe with name {name} could not be created",
        )
    except DatabaseError as e:
        # Log it, will figure it out later
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/get_recipe_by_id/{recipe_id}", response_model=RecipeModel)
async def get_recipe_by_id(recipe_id: str):
    try:
        recipe = await db_service.get_one_recipe(recipe_id)
        if recipe:
            return recipe
        raise HTTPException(
            status_code=404,
            detail=f"The recipe with ID: {recipe_id} could not be found",
        )
    except DatabaseError as e:
        # Log it, will figure it out later
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/get_recipes", response_model=list[RecipeModel])
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


app.middleware("http")(error_middleware)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
