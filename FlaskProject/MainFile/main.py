from flask import Flask, request, jsonify
from FlaskProject.Routes.recipe_routes import configure_routes
from MongoDBAccess.setup import recipe_service_db
import uvicorn
from flasgger import Swagger

app = Flask("recipe_app",)
swagger = Swagger(app)

# CORS configuration (if needed)
# from flask_cors import CORS
# CORS(app)

configure_routes(app, recipe_service_db)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)