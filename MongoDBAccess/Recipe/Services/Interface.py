from abc import ABC, abstractmethod


class ServiceInterface(ABC):

    @abstractmethod
    async def create_recipe(self, name, ingredients) -> str:
        pass

    @abstractmethod
    async def get_one_recipe(self, _id) -> dict:
        pass

    @abstractmethod
    async def get_all_recipes(self) -> list:
        pass

    @abstractmethod
    async def update_one_recipe(self, _id, name, ingredients) -> str:
        pass

    @abstractmethod
    async def delete_one_recipe(self, _id) -> str:
        pass
