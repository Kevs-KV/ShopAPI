from fastapi.security import OAuth2PasswordBearer

from config.settings import settings

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token", scopes={
        'user': 'Only users', 'admin': 'Only admins'
    }
)
