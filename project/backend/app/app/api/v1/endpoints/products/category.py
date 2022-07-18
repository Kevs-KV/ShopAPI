from fastapi import APIRouter, Depends, Security
from fastapi.responses import Response

from api.v1.dependencies.database_marker import ProductRepositoryDependencyMarker, CategoryRepositoryDependencyMarker
from services.database.repositories.product.category_repository import CategoryRepository
from services.database.schemas.product.category import CategoryDTO, CategoryBodySpec
from services.security.jwt import JWTSecurityHead

router = APIRouter()


@router.post('/create/', dependencies=[])
async def category_create(category: CategoryDTO = CategoryBodySpec.item,
                          category_crud: CategoryRepository = Depends(CategoryRepositoryDependencyMarker)):
    await category_crud.add_category(category)
    return Response(status_code=201)
