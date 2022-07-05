from fastapi import APIRouter, Depends
from fastapi.responses import Response

from services.database.repositories.product_repository import ProductRepository
from services.database.schemas.product import ProductDTO, ProductBodySpec

router = APIRouter()


@router.post('/create/')
async def product_create(product: ProductDTO = ProductBodySpec.item, product_crud=Depends(ProductRepository)):
    await product_crud.add_product(**product.dict(exclude_unset=True, exclude_none=True))
    return Response(status_code=201)


@router.get('/all/')
async def product_all(product_crud=Depends(ProductRepository)):
    return await product_crud.all_product()


@router.get('/search/')
async def product_search(value: str, product_crud=Depends(ProductRepository)):
    return await product_crud.search_product(value)
