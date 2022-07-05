from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from config.settings import settings
from services.database.repositories.user_repository import UserRepository
from services.database.schemas.token import Token
from services.security.jwt import create_access_token

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
async def login_access_token(
        user_crud=Depends(UserRepository), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = await user_crud.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
