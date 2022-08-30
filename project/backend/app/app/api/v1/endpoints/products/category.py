from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import Response
from sqlalchemy.exc import IntegrityError, DBAPIError

from app.api.v1.dependencies.database_marker import CategoryRepositoryDependencyMarker
from app.services.database.repositories.product.category_repository import CategoryRepository
from app.services.database.schemas.product.category import CategoryDTO, CategoryBodySpec
from app.services.security.jwt import JWTSecurityHead

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
async def category_delete(category_id: int,
                          category_crud: CategoryRepository = Depends(CategoryRepositoryDependencyMarker)):
    try:
        return await category_crud.delete_category(category_id)
    except TypeError:
        raise HTTPException(
            status_code=404, detail=f"There isn't entry with id={category_id}"
        )


@router.get('/id={category_id}/page={page}/limit={limit}/')
async def get_category_products(category_id: int,
                                page: int, limit: int,
                                category_crud: CategoryRepository = Depends(CategoryRepositoryDependencyMarker)):
    try:
        return await category_crud.get_category_products(category_id, page, limit)
    except DBAPIError:
        raise HTTPException(
            status_code=404, detail=f"There isn't entry with id={category_id}"
        )


@router.put('/{category_id}/update/')
async def category_update(category_id: int,
                          new_name: str,
                          category_crud: CategoryRepository = Depends(CategoryRepositoryDependencyMarker)):
    try:
        await category_crud.update_category(category_id, new_name)
        return {"success": True, 'detail': f'category id={category_id} updated'}
    except IntegrityError:
        raise HTTPException(
            status_code=404, detail=f"invalid data to update record id={category_id}"
        )
