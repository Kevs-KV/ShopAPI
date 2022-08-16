from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Security

from app.api.v1.dependencies.database_marker import UserRepositoryDependencyMarker
from app.api.v1.dependencies.security import JWTAuthenticationMarker, JWTSecurityMarker
from app.api.v1.dependencies.utils import ConfigMailMarker
from app.services.database.repositories.user.user_repository import UserRepository
from app.services.database.schemas.user.user import UserCreate, User
from app.services.security.jwt import JWTSecurityHead, JWTAuthenticationService, JWTSecurityService
from app.services.worker.tasks import task_send_mail_register

router = APIRouter()


@router.post("/", response_model=User)
async def create_user(user_in: UserCreate,
                      user_crud: UserRepository = Depends(UserRepositoryDependencyMarker),
                      auth: JWTAuthenticationService = Depends(JWTAuthenticationMarker),
                      mail_config: dict = Depends(ConfigMailMarker)
                      ) -> Any:
    user = await user_crud.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await user_crud.create_user(obj_in=user_in)
    token = await auth.registration_user_token(username=user.full_name, email=user.email)
    task_send_mail_register.delay(mail_config, user.email, token)
    return user


@router.get('/register/{token}')
async def activate_user(token: str, user_crud: UserRepository = Depends(UserRepositoryDependencyMarker),
                        jwt_service: JWTSecurityService = Depends(JWTSecurityMarker)):
    token_payload = await jwt_service.decode_register_token(token)
    user = await user_crud.get_by_email(token_payload['email'])
    if user and user.full_name == token_payload['username']:
        await user_crud.activate_user(user.email)
        return {"success": True, 'detail': f'User {user.full_name} has registered by email: {user.email} '}
    else:
        return {'detail': 'Registration time expired'}


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
