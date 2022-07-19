import typing

from services.database.models.product.category import Category
from services.database.repositories.base import Base, Model
from services.database.schemas.product.category import CategoryDTO


class CategoryRepository(Base):
    model = Category

    async def add_category(self,
                           obj_in: CategoryDTO,
                           ) -> Model:
        payload = obj_in.__dict__
        return await self._insert(**payload)

    async def get_categories(self) -> typing.List[Model]:
        return await self._select_all()

    async def category_delete(self, category_id: int) -> Model:
        return await self._delete(self.model.id, category_id)
