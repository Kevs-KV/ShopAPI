from datetime import datetime, timedelta
from typing import NewType, Dict, Any

import jwt
from fastapi.security import OAuth2PasswordRequestForm

ALGORITHM = "HS256"

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
