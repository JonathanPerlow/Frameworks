from abc import ABC, abstractmethod

from ..Models.Recipe import RecipeModel


class DAOInterface(ABC):
    @abstractmethod
    async def save_recipe(self, recipe: dict) -> object:
        pass

    @abstractmethod
    async def get_all_recipe(self) -> list:
        pass

    @abstractmethod
    async def get_one_recipe(self, query: dict) -> dict:
        pass

    @abstractmethod
    async def update_one_recipe(
        self, recipe_document: dict, update: RecipeModel
    ) -> int:
        pass

    @abstractmethod
    async def delete_one(self, query: dict) -> int:
        pass
