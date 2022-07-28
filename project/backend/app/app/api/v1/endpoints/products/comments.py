from fastapi import APIRouter, Depends, Security, HTTPException

from api.v1.dependencies.database_marker import CommentRepositoryDependencyMarker
from services.database.repositories.product.comment_repositiry import CommentRepository
from services.security.jwt import JWTSecurityHead

router = APIRouter()


@router.delete('/{comment_id}/delete/', dependencies=[Security(JWTSecurityHead(), scopes=['admin'])])
async def comment_delete(comment_id: int,
                              comment_crud: CommentRepository = Depends(CommentRepositoryDependencyMarker)):
    try:
        return await comment_crud.delete_comment(comment_id)
    except TypeError:
        raise HTTPException(
            status_code=404, detail=f"There isn't entry with id={comment_id}"
        )
