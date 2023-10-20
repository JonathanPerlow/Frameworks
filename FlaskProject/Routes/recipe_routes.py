import asyncio

from flask import Flask, jsonify, request

from MongoDBAccess.Recipe.Services.Interface import ServiceInterface
from MongoDBAccess.Recipe.Models.Recipe import RecipeModel
from MongoDBAccess.Recipe.CustomErrorClass import DatabaseError


def configure_routes(_app: Flask, db_service: ServiceInterface):
    @_app.route("/create_recipe/<string:name>/<string:ingredients>", methods=["POST"])
    def create_recipe(name: str, ingredients: str):
        """
           Create a new recipe.
           ---
           parameters:
             - name: name
               in: path
               type: string
               required: true
               description: Name of the recipe
             - name: ingredients
               in: path
               type: string
               required: true
               description: Ingredients of the recipe
           responses:
             201:
               description: Recipe created successfully
             400:
               description: Invalid input data
             500:
               description: Internal Server Error
           """
        try:
            data = request.get_json()
            name = data.get("name")
            ingredients = data.get("ingredients")
            if not name or not ingredients:
                return jsonify({"error": "Invalid input data"}), 400
            recipe = asyncio.run(db_service.create_recipe(name, ingredients))
            if recipe:
                return jsonify(recipe), 201
        except DatabaseError as e:
            # Log it, will figure it out later
            print(f"Database error: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    @_app.route("/get_recipe_by_id/<string:recipe_id>", methods=["GET"])
    def get_recipe_by_id(recipe_id: str):
        """
            Get details of a recipe by ID.
            ---
            parameters:
              - name: recipe_id
                in: path
                type: string
                required: true
                description: ID of the recipe to retrieve
            responses:
              200:
                description: Recipe details retrieved successfully
              404:
                description: Recipe not found
              500:
                description: Internal Server Error
            """
        try:
            data = request.get_json()
            _id = data.get("recipe_id")
            recipe = asyncio.run(db_service.get_one_recipe(_id))
            if recipe:
                return jsonify(recipe), 200
            return jsonify(f"The recipe with ID: {recipe_id} could not be found"), 404
        except DatabaseError as e:
            # Log it, will figure it out later
            print(f"Database error: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    @_app.route("/get_recipes", methods=["GET"])
    def get_recipes():
        """
            Get a list of all recipes.
            ---
            responses:
              200:
                description: Recipes retrieved successfully
              404:
                description: Recipes not found
              500:
                description: Internal Server Error
            """
        try:
            recipes = asyncio.run(db_service.get_all_recipes())
            if recipes:
                return jsonify(recipes), 200
            return jsonify(f"The recipes could not be found"), 404
        except DatabaseError as e:
            # Log it, will figure it out later
            print(f"Database error: {e}")
            return jsonify({"error": "Internal Server Error"}), 500
