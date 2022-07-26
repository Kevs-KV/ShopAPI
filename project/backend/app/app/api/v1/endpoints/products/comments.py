from fastapi import APIRouter, Depends, Security

from api.v1.dependencies.database_marker import CommentRepositoryDependencyMarker
from services.database.repositories.product.comment_repositiry import CommentRepository
from services.security.jwt import JWTSecurityHead

router = APIRouter()


@router.delete('/{comment_id}/delete/', dependencies=[Security(JWTSecurityHead(), scopes=['admin'])])
async def product_add_comment(comment_id: int,
                              comment_crud: CommentRepository = Depends(CommentRepositoryDependencyMarker)):
    return await comment_crud.delete_comment(comment_id)
