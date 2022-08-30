import typing

from app.services.database.models.product import Product
from app.services.database.models.product.category import Category
from app.services.database.repositories.base import Base, Model
from app.services.database.schemas.product.category import CategoryDTO


class CategoryRepository(Base):
    model = Category

    async def add_category(self,
                           obj_in: CategoryDTO,
                           ) -> Model:
        payload = obj_in.__dict__
        return await self._insert(**payload)

    async def get_categories(self) -> typing.List[Model]:
        return await self._select_all()

    async def delete_category(self, category_id: int) -> Model:
        return await self._delete(self.model.id, category_id)

    async def get_category_products(self, category_id: int, page: int, limit: int) -> Model:
        return await self._pagination_child(page=page, limit=limit, key=category_id, filter_model=Product,
                                               order=self.model.id,
                                               filter_order=Product.category_id)

    async def update_category(self, category_id: int, new_name: str) -> None:
        return await self._update(self.model.id == category_id, name=new_name)
