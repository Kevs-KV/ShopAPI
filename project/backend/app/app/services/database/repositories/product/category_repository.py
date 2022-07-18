from services.database.models.product.category import Category
from services.database.repositories.base import Base, Model
from services.database.schemas.product.category import CategoryDTO
from utils.database_utils import filter_payload


class CategoryRepository(Base):
    model = Category

    async def add_category(self,
                           obj_in: CategoryDTO,
                           ) -> Model:
        payload = obj_in.__dict__
        return await self._insert(**payload)
