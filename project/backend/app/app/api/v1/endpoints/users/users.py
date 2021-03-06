from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Security

from api.v1.dependencies.database_marker import UserRepositoryDependencyMarker
from services.database.repositories.user.user_repository import UserRepository
from services.database.schemas.user.user import UserCreate, User
from services.security.jwt import JWTSecurityHead

router = APIRouter()


@router.post("/", response_model=User)
async def create_user(user_in: UserCreate,
                      user_crud: UserRepository = Depends(UserRepositoryDependencyMarker),
                      ) -> Any:
    user = await user_crud.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await user_crud.create_user(obj_in=user_in)
    return user


@router.get("/{email}/")
async def get_user(email: str, user_crud: UserRepository = Depends(UserRepositoryDependencyMarker)):
    user = await user_crud.get_by_email(email)
    return user


@router.delete('/delete/', dependencies=[Security(JWTSecurityHead(), scopes=['admin'])])
async def delete_user(email: str, user_crud: UserRepository = Depends(UserRepositoryDependencyMarker)):
    try:
        return await user_crud.delete_user(email)
    except TypeError:
        raise HTTPException(
            status_code=404, detail=f"There isn't entry with email={email}"
        )
