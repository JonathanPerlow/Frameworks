from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, text
from sanic_openapi import openapi2_blueprint
from SanicAPI.Routes.recipe_routes import configure_routes
from MongoDBAccess.setup import recipe_service_db
from sanic_cors import CORS

app = Sanic("recipe_app")

# Cors configurations
CORS(app, automatic_options=True)

app.blueprint(openapi2_blueprint)


async def error_middleware(request: Request, response: HTTPResponse):
    try:
        return response
    except Exception as e:
        return text(f"Internal Server Error: {str(e)}", status=500)


app.register_middleware(error_middleware, attach_to='response')
configure_routes(app, recipe_service_db)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)