from fastapi import APIRouter, Depends, Security
from fastapi.responses import Response

from api.v1.dependencies.database_marker import CategoryRepositoryDependencyMarker
from services.database.repositories.product.category_repository import CategoryRepository
from services.database.schemas.product.category import CategoryDTO, CategoryBodySpec
from services.security.jwt import JWTSecurityHead

router = APIRouter()


@router.post('/create/', dependencies=[Security(JWTSecurityHead(), scopes=['admin'])])
async def category_create(category: CategoryDTO = CategoryBodySpec.item,
                          category_crud: CategoryRepository = Depends(CategoryRepositoryDependencyMarker)):
    await category_crud.add_category(category)
    return Response(status_code=201)


@router.get('/categories/')
async def categoty_get_all(category_crud: CategoryRepository = Depends(CategoryRepositoryDependencyMarker)):
    return await category_crud.get_categories()


@router.delete('/delete/', dependencies=[Security(JWTSecurityHead(), scopes=['admin'])])
async def category_delete(category_id: int, category_crud: CategoryRepository = Depends(CategoryRepositoryDependencyMarker)):
    return await category_crud.category_delete(category_id)