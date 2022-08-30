from app.services.database.models.product import Product
from app.services.database.models.product.brand import Brand
from app.services.database.repositories.base import Base, Model
from app.services.database.schemas.product.brand import BrandDTO


class BrandRepository(Base):
    model = Brand

    async def add_brand(self,
                        obj_in: BrandDTO,
                        ) -> Model:
        payload = obj_in.__dict__
        return await self._insert(**payload)

    async def get_brands(self):
        return await self._select_all()

    async def delete_brand(self, brand_id):
        return await self._delete(self.model.id, brand_id)

    async def update_brand(self, brand_id: int, new_name: str) -> None:
        return await self._update(self.model.id == brand_id, name=new_name)

    async def get_brand_products(self, category_id: int, page: int, limit: int) -> Model:
        return await self._pagination_child(page=page, limit=limit, key=category_id, order=self.model.id,
                                               filter_model=Product,
                                               filter_order=Product.category_id)
