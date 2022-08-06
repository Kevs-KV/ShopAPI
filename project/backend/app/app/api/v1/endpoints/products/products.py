from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import Response
from sqlalchemy.exc import IntegrityError

from app.api.v1.dependencies.database_marker import ProductRepositoryDependencyMarker, CommentRepositoryDependencyMarker
from app.services.database.repositories.product.comment_repositiry import CommentRepository
from app.services.database.repositories.product.product_repository import ProductRepository
from app.services.database.schemas.product.comment import CommentDTO, CommentBodySpec
from app.services.database.schemas.product.product import ProductDTO, ProductBodySpec, ProductUpdate
from app.services.security.jwt import JWTSecurityHead

router = APIRouter()


@router.post('/create/', dependencies=[Security(JWTSecurityHead(), scopes=['admin'])])
async def product_create(
        product_crud: ProductRepository = Depends(ProductRepositoryDependencyMarker),
        product: ProductDTO = ProductBodySpec.item):
    try:
        await product_crud.add_product(**product.dict(exclude_unset=True, exclude_none=True))
    except IntegrityError:
        raise HTTPException(
            status_code=404, detail=f"Wrong entry data"
        )
    return Response(status_code=201)


@router.post('/{product_id}/create/comment')
async def product_add_comment(comment: CommentDTO = CommentBodySpec.item,
                              user=Security(JWTSecurityHead(), scopes=['admin', 'user']),
                              comment_crud: CommentRepository = Depends(CommentRepositoryDependencyMarker)):
    return await comment_crud.add_comment(comment, user.id)


@router.get('/all/')
async def product_all(product_crud: ProductRepository = Depends(ProductRepositoryDependencyMarker)):
    return await product_crud.all_product()


@router.get('/{product_id}/')
async def product_get(product_id: int, product_crud: ProductRepository = Depends(ProductRepositoryDependencyMarker)):
    return await product_crud.detail_product(product_id)


@router.get('/search/')
async def product_search(value: str, product_crud: ProductRepository = Depends(ProductRepositoryDependencyMarker)):
    return await product_crud.search_product_by_name(value)


@router.delete('/delete/', dependencies=[Security(JWTSecurityHead(), scopes=['admin'])])
async def product_delete(product_id: int, product_crud: ProductRepository = Depends(ProductRepositoryDependencyMarker)):
    try:
        return await product_crud.delete_product(product_id)
    except TypeError:
        raise HTTPException(
            status_code=404, detail=f"There isn't entry with id={product_id}"
        )


@router.put('/{product_id}/update/')
async def product_update(product_id: int, product: ProductUpdate = ProductBodySpec.item,
                         product_crud: ProductRepository = Depends(ProductRepositoryDependencyMarker)):
    try:
        await product_crud.update_product(product_id, product)
        return {"success": True, 'detail': f'product id={product_id} updated'}
    except IntegrityError:
        raise HTTPException(
            status_code=404, detail=f"invalid data to update record id={product_id}"
        )
