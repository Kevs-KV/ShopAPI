from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from api.v1.dependencies.security import JWTAuthenticationMarker
from services.security.jwt import JWTAuthenticationService

router = APIRouter()


@router.post("/login/access-token")
async def login_access_token(
        auth: JWTAuthenticationService = Depends(JWTAuthenticationMarker),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    try:
        access_token = await auth.authenticate_user(form_data)
        return {"access_token": access_token, "token_type": "bearer"}
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='no auth',
            headers={"WWW-Authenticate": "Bearer"},
        )
