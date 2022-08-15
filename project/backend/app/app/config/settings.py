import secrets
from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator, AnyUrl, EmailStr


class PostgresDsn(AnyUrl):
    allowed_schemes = {'postgres', 'postgresql', 'postgresql+asyncpg'}
    user_required = True


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    API_V1_STR: str = ""
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    MAIL_USERNAME: str
    MAIL_FROM: EmailStr
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_TLS: bool
    MAIL_SSL: bool

    EMAIL_TEMPLATES_DIR: str = "./app/email-templates/"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
