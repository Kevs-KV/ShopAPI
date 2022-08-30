from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import Response
from sqlalchemy.exc import IntegrityError, DBAPIError

from app.api.v1.dependencies.database_marker import BrandRepositoryDependencyMarker
from app.services.database.repositories.product.brand_repository import BrandRepository
from app.services.database.schemas.product.brand import BrandDTO
from app.services.database.schemas.product.category import CategoryBodySpec
from app.services.security.jwt import JWTSecurityHead

router = APIRouter()


@router.post('/create/', dependencies=[Security(JWTSecurityHead(), scopes=['admin'])])
async def brand_create(brand: BrandDTO = CategoryBodySpec.item,
                       brand_crud: BrandRepository = Depends(BrandRepositoryDependencyMarker)):
    await brand_crud.add_brand(brand)
    return Response(status_code=201)


@router.get('/all/')
async def brand_get_all(brand_crud: BrandRepository = Depends(BrandRepositoryDependencyMarker)):
    return await brand_crud.get_brands()


@router.get('/id={brand_id}/page={page}/limit={limit}/')
async def get_brand_products(brand_id: int,
                             page: int, limit: int,
                             brand_crud: BrandRepository = Depends(BrandRepositoryDependencyMarker)):
    try:
        return await brand_crud.get_brand_products(brand_id, page, limit)
    except DBAPIError:
        raise HTTPException(
            status_code=404, detail=f"There isn't entry with id={brand_id}"
        )


@router.delete('/delete/', dependencies=[Security(JWTSecurityHead(), scopes=['admin'])])
async def brand_delete(brand_id: int, brand_crud: BrandRepository = Depends(BrandRepositoryDependencyMarker)):
    try:
        return await brand_crud.delete_brand(brand_id)
    except TypeError:
        raise HTTPException(
            status_code=404, detail=f"There isn't entry with id={brand_id}"
        )


@router.put('/{brand_id}/update/')
async def brand_update(brand_id: int,
                       new_name: str,
                       brand_crud: BrandRepository = Depends(BrandRepositoryDependencyMarker)):
    try:
        await brand_crud.update_brand(brand_id, new_name)
        return {"success": True, 'detail': f'brand id={brand_id} updated'}
    except IntegrityError:
        raise HTTPException(
            status_code=404, detail=f"invalid data to update record id={brand_id}"
        )
