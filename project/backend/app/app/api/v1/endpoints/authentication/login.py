from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.api.v1.dependencies.security import JWTAuthenticationMarker
from app.api.v1.dependencies.utils import ConfigMailMarker
from app.services.security.jwt import JWTAuthenticationService
from app.services.worker.tasks import task_send_mail_user_login

router = APIRouter()


@router.post("/login/access-token")
async def login_access_token(
        auth: JWTAuthenticationService = Depends(JWTAuthenticationMarker),
        form_data: OAuth2PasswordRequestForm = Depends(),
        mail_config: dict = Depends(ConfigMailMarker)
) -> Any:
    try:
        access_token = await auth.authenticate_user(form_data)
        task_send_mail_user_login.delay(mail_config, form_data.username)
        return {"access_token": access_token, "token_type": "bearer"}
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect login or password',
            headers={"WWW-Authenticate": "Bearer"},
        )
