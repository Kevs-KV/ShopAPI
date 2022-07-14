from datetime import datetime, timedelta
from typing import NewType, Dict, Any

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import SecurityScopes
from jose import jwt
from pydantic import ValidationError
from starlette import status

from api.v1.dependencies.security import JWTSecurityMarker
from services.database.models.user import User
from services.database.repositories.user_repository import UserRepository
from services.database.schemas.token import TokenPayload
from services.security.oauth import reusable_oauth2
from utils.password_hashing import PasswordHasher

JWTToken = NewType("JWTToken", str)


class JWTAuthenticationService:

    def __init__(self, user_crud, password_hasher, secret_key, algorithm, token_expires_in_minutes):
        self._token_expires_in_minutes = token_expires_in_minutes
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._user_crud = user_crud
        self._password_hasher = password_hasher

    async def authenticate_user(self, form_data: OAuth2PasswordRequestForm):
        user = await self._user_crud.get_by_email(form_data.username)
        if not user:
            return None
        if not self._password_hasher.verify_password(form_data.password, user.hashed_password):
            return None
        return JWTToken(self._generate_jwt_token({
            "sub": form_data.username,
            "scopes": form_data.scopes,
        }))

    def _generate_jwt_token(self, token_payload: Dict[str, Any]) -> str:
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
                detail='error call',
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_payload = self._decode_token(token=jwt_token)
        for scope in security_scopes.scopes:
            if scope not in token_payload.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='erorr scope',
                    headers={"WWW-Authenticate": "Bearer"},
                )
        return await self._retrieve_user_or_raise_exception(token_payload.sub)

    def _decode_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return TokenPayload(sub=payload["sub"], scopes=payload.get("scopes", []))
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='erorr decode_token',
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def _retrieve_user_or_raise_exception(self, username: str) -> User:
        if user := await self._user_crud.get_by_email(email=username):
            return user

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='error raise_exception',
            headers={"WWW-Authenticate": "Bearer"},
        )


class JWTSecurityHead:

    async def __call__(self, security_scopes: SecurityScopes, jwt_token: str = Depends(reusable_oauth2),
                       service: JWTSecurityService = (Depends(JWTSecurityMarker))):
        return await service(jwt_token=jwt_token, security_scopes=security_scopes)
