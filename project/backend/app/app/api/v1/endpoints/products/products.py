from fastapi import APIRouter, Depends, Security
from fastapi.responses import Response

from api.v1.dependencies.database_marker import ProductRepositoryDependencyMarker
from services.database.repositories.product.product_repository import ProductRepository
from services.database.schemas.product.product import ProductDTO, ProductBodySpec
from services.security.jwt import JWTSecurityHead

router = APIRouter()


@router.post('/create/', dependencies=[Security(JWTSecurityHead(), scopes=['admin'])])
async def product_create(
        product_crud: ProductRepository = Depends(ProductRepositoryDependencyMarker),
        product: ProductDTO = ProductBodySpec.item):
    await product_crud.add_product(**product.dict(exclude_unset=True, exclude_none=True))
    return Response(status_code=201)


@router.get('/all/')
async def product_all(product_crud: ProductRepository = Depends(ProductRepositoryDependencyMarker)):
    return await product_crud.all_product()


@router.get('/search/')
async def product_search(value: str, product_crud: ProductRepository = Depends(ProductRepositoryDependencyMarker)):
    return await product_crud.search_product_by_name(value)


@router.delete('/delete/')
async def product_delete(product_id: int, product_crud: ProductRepository = Depends(ProductRepositoryDependencyMarker)):
    return await product_crud.delete_product(product_id)
