import os

PASSWORD = os.environ.get("MONGODB_PASSWORD")
CONNECTION_STRING = (
    f"mongodb+srv://Jonathan:{PASSWORD}@cluster0.c03kgdq.mongodb.net/test"
)
DB_NAME = "Recipes_db"
COLLECTION_NAME = "recipes"
