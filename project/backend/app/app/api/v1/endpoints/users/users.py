from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Security

from app.api.v1.dependencies.database_marker import UserRepositoryDependencyMarker
from app.services.database.repositories.user.user_repository import UserRepository
from app.services.database.schemas.user.user import UserCreate, User
from app.services.security.jwt import JWTSecurityHead

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


@router.get("/{email}/", response_model=User)
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
