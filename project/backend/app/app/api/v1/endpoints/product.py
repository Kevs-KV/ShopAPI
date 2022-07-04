from fastapi import APIRouter, Depends
from fastapi.responses import Response

from services.database.repositories.product_repository import ProductRepository
from services.database.schemas.product import ProductDTO, ProductBodySpec

router = APIRouter()


@router.post('/product/create/')
async def product_create(product: ProductDTO = ProductBodySpec.item, product_crud=Depends(ProductRepository)):
    await product_crud.add_product(**product.dict(exclude_unset=True, exclude_none=True))
    return Response(status_code=201)
