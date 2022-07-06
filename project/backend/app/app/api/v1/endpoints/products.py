from fastapi import APIRouter, Depends
from fastapi.responses import Response

from services.database.models.user import User
from services.database.repositories.product_repository import ProductRepository
from services.database.schemas.product import ProductDTO, ProductBodySpec
from services.security.oauth import get_current_active_superuser

router = APIRouter()


@router.post('/create/')
async def product_create(product: ProductDTO = ProductBodySpec.item, product_crud=Depends(ProductRepository),
                         current_user: User = Depends(get_current_active_superuser)):
    if current_user.is_active:
        await product_crud.add_product(**product.dict(exclude_unset=True, exclude_none=True))
        return Response(status_code=201)


@router.get('/all/')
async def product_all(product_crud=Depends(ProductRepository)):
    return await product_crud.all_product()


@router.get('/search/')
async def product_search(value: str, product_crud=Depends(ProductRepository)):
    return await product_crud.search_product(value)


@router.delete('/delete/')
async def product_search(product_id: int, product_crud=Depends(ProductRepository)):
    return await product_crud.delete_product(product_id)
