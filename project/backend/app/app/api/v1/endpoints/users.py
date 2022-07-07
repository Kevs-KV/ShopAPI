from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from api.v1.dependencies.database_marker import UserRepositoryDependencyMarker
from services.database.repositories.user_repository import UserRepository
from services.database.schemas.user import UserCreate, User

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


@router.get("/{email}")
async def get_user(email: str, user_crud: UserRepository = Depends(UserRepositoryDependencyMarker)):
    user = await user_crud.get_by_email(email)
    return user
