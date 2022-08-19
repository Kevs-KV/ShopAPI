from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.dependencies.database_marker import UserRepositoryDependencyMarker
from app.api.v1.dependencies.security import JWTAuthenticationMarker, JWTSecurityMarker
from app.api.v1.dependencies.utils import ConfigMailMarker
from app.services.database.repositories.user.user_repository import UserRepository
from app.services.database.schemas.user.user import UserCreate, User
from app.services.security.jwt import JWTAuthenticationService, JWTSecurityService
from app.services.worker.tasks import task_send_mail_register, check_user_activate, task_send_mail_reset_password

router = APIRouter()


@router.post("/register/", response_model=User)
async def register_user(user_in: UserCreate,
                      user_crud: UserRepository = Depends(UserRepositoryDependencyMarker),
                      auth: JWTAuthenticationService = Depends(JWTAuthenticationMarker),
                      mail_config: dict = Depends(ConfigMailMarker),
                      ) -> Any:
    user = await user_crud.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await user_crud.create_user(obj_in=user_in)
    token = await auth.identification_user_token(username=user.full_name, email=user.email)
    task_send_mail_register.delay(mail_config, user.email, token)
    check_user_activate.apply_async(args=[user.email], countdown=360)
    return user


@router.get('/register/{token}')
async def activate_user(token: str, user_crud: UserRepository = Depends(UserRepositoryDependencyMarker),
                        jwt_service: JWTSecurityService = Depends(JWTSecurityMarker)):
    token_payload = await jwt_service.decode_identification_user_token(token)
    user = await user_crud.get_by_email(token_payload['email'])
    if user and user.full_name == token_payload['username']:
        await user_crud.activate_user(user.email)
        return {"success": True, 'detail': f'User {user.full_name} has registered by email: {user.email} '}
    return {'detail': 'Registration time expired'}


@router.get('/password/reset/')
async def password_reset(email: str, user_crud: UserRepository = Depends(UserRepositoryDependencyMarker),
                         auth: JWTAuthenticationService = Depends(JWTAuthenticationMarker),
                         mail_config: dict = Depends(ConfigMailMarker),
                         ):
    user = await user_crud.get_by_email(email)
    if user:
        token = await auth.identification_user_token(username=user.full_name, email=user.email)
        task_send_mail_reset_password.delay(mail_config, user.email, token)
        return {"success": True, 'detail': f'Password reset sent to {user.email}'}
    raise HTTPException(
        status_code=400,
        detail="No such user exists",
    )


@router.post('/password/reset/{token}')
async def password_change(token: str, new_password: str,
                          user_crud: UserRepository = Depends(UserRepositoryDependencyMarker),
                          jwt_service: JWTSecurityService = Depends(JWTSecurityMarker)):
    token_payload = await jwt_service.decode_identification_user_token(token)
    user = await user_crud.get_by_email(token_payload['email'])
    if user and user.full_name == token_payload['username']:
        await user_crud.password_change_user(user.email, new_password)
        return {"success": True}
    raise HTTPException(
        status_code=400,
        detail="Link is not valid",
    )
