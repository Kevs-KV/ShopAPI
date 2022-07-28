from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import Response

from api.v1.dependencies.database_marker import CategoryRepositoryDependencyMarker, BrandRepositoryDependencyMarker
from services.database.repositories.product.brand_repository import BrandRepository
from services.database.repositories.product.category_repository import CategoryRepository
from services.database.schemas.product.brand import BrandDTO
from services.database.schemas.product.category import CategoryDTO, CategoryBodySpec
from services.security.jwt import JWTSecurityHead

router = APIRouter()


@router.post('/create/', dependencies=[Security(JWTSecurityHead(), scopes=['admin'])])
async def brand_create(brand: BrandDTO = CategoryBodySpec.item,
                          brand_crud: BrandRepository = Depends(BrandRepositoryDependencyMarker)):
    await brand_crud.add_brand(brand)
    return Response(status_code=201)


@router.get('/categories/')
async def brand_get_all(brand_crud: BrandRepository = Depends(BrandRepositoryDependencyMarker)):
    return await brand_crud.get_brands()


@router.delete('/delete/', dependencies=[Security(JWTSecurityHead(), scopes=['admin'])])
async def brand_delete(brand_id: int, brand_crud: BrandRepository = Depends(BrandRepositoryDependencyMarker)):
    try:
        return await brand_crud.delete_brand(brand_id)
    except TypeError:
        raise HTTPException(
            status_code=404, detail=f"There isn't entry with id={brand_id}"
        )
