from fastapi import FastAPI, Request, HTTPException
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from recipes.FastApiProject.Routes.recipe_routes import configure_routes
from recipes.MongoDBAccess.setup import recipe_service_db

app = FastAPI(title="recipe_app")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])


async def error_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"error": f"Internal Server Error: {e}"}, status_code=500)


app.middleware("http")(error_middleware)

configure_routes(app, recipe_service_db)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
