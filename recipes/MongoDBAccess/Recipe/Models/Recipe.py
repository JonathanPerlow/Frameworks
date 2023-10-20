from typing import Optional

from bson import ObjectId
from pydantic import BaseModel


class RecipeModel(BaseModel):
    _id: Optional[ObjectId] = None
    name: str
    ingredients: str
