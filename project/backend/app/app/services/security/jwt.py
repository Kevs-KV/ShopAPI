from datetime import datetime, timedelta
from typing import NewType, Any

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import SecurityScopes
from jose import jwt
from pydantic import ValidationError
from starlette import status

from app.api.v1.dependencies.security import JWTSecurityMarker
from app.services.database.models.user.user import User
from app.services.database.repositories.user.user_repository import UserRepository
from app.services.database.schemas.security.token import TokenPayload
from app.services.security.oauth import reusable_oauth2
from app.utils.password_hashing import PasswordHasher

JWTToken = NewType("JWTToken", str)


class JWTAuthenticationService:

    def __init__(self, user_crud: UserRepository, password_hasher: PasswordHasher, secret_key: str, algorithm: str,
                 token_expires_in_minutes: float | int = 30):
        self._token_expires_in_minutes = token_expires_in_minutes
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._user_crud = user_crud
        self._password_hasher = password_hasher

    async def authenticate_user(self, form_data: OAuth2PasswordRequestForm) -> JWTToken:
        user = await self._user_crud.get_by_email(form_data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='account not found',
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not self._password_hasher.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect password',
                headers={"WWW-Authenticate": "Bearer"},
            )
        if 'admin' in form_data.scopes and user.is_superuser is False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='the account does not have administrator rights or scope is not selected',
                headers={"WWW-Authenticate": "Bearer"},
            )
        return JWTToken(self._generate_jwt_token({
            "sub": form_data.username,
            "scopes": form_data.scopes,
        }))

    async def identification_user_token(self, username: str, email: str):
        return JWTToken(self._generate_jwt_token({
            "username": username,
            "email": email,
        }))

    def _generate_jwt_token(self, token_payload: dict[str, Any]) -> str:
        token_payload = {
            "exp": datetime.utcnow() + timedelta(self._token_expires_in_minutes),
            **token_payload
        }
        filtered_payload = {k: v for k, v in token_payload.items() if v is not None}
        return jwt.encode(filtered_payload, self._secret_key, algorithm=self._algorithm)


class JWTSecurityService:

    def __init__(self, user_crud: UserRepository,
                 password_hasher: PasswordHasher, secret_key: str, algorithm: str):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._user_crud = user_crud
        self._password_hasher = password_hasher

    async def __call__(self, security_scopes: SecurityScopes, jwt_token: str = Depends(reusable_oauth2)) -> User:
        if jwt_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='account no admin',
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_payload = self._decode_token(token=jwt_token)
        for scope in security_scopes.scopes:
            if scope not in token_payload.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='account has no rights or scope is not selected',
                    headers={"WWW-Authenticate": "Bearer"},
                )
        return await self._retrieve_user_or_raise_exception(token_payload.sub)

    async def decode_identification_user_token(self, token: str):
        try:
            return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='An error occurred while decoding',
            )

    def _decode_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return TokenPayload(sub=payload["sub"], scopes=payload.get("scopes", []))
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='error while receiving token or account is not authorized',
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def _retrieve_user_or_raise_exception(self, username: str) -> User:
        if user := await self._user_crud.get_by_email(email=username):
            return user

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='account not received',
            headers={"WWW-Authenticate": "Bearer"},
        )


class JWTSecurityHead:

    async def __call__(self, security_scopes: SecurityScopes, jwt_token: str = Depends(reusable_oauth2),
                       service: JWTSecurityService = (Depends(JWTSecurityMarker))) -> User:
        return await service(jwt_token=jwt_token, security_scopes=security_scopes)
