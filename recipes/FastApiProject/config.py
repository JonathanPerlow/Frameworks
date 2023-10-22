import os
from dotenv import load_dotenv
current_directory = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_directory, '..', 'MongoDBAccess', '.env')
load_dotenv(env_file_path)
PASSWORD = os.getenv("MONGODB_PASSWORD")
CONNECTION_STRING = (
    f"mongodb+srv://Jonathan:{PASSWORD}@cluster0.c03kgdq.mongodb.net/test"
)
DB_NAME = "Recipes_db"
COLLECTION_NAME = "recipes"
