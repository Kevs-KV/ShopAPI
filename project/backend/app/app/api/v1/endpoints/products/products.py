from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.responses import Response

from api.v1.dependencies.database_marker import ProductRepositoryDependencyMarker, CommentRepositoryDependencyMarker
from services.database.repositories.product.comment_repositiry import CommentRepository
from services.database.repositories.product.product_repository import ProductRepository
from services.database.schemas.product.comment import CommentDTO, CommentBodySpec
from services.database.schemas.product.product import ProductDTO, ProductBodySpec
from services.security.jwt import JWTSecurityHead

router = APIRouter()


@router.post('/create/', dependencies=[Security(JWTSecurityHead(), scopes=['admin'])])
async def product_create(
        product_crud: ProductRepository = Depends(ProductRepositoryDependencyMarker),
        product: ProductDTO = ProductBodySpec.item):
    await product_crud.add_product(**product.dict(exclude_unset=True, exclude_none=True))
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
