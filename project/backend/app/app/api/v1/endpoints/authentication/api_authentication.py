from fastapi import APIRouter

from app.api.v1.endpoints.authentication import login, account

api_router = APIRouter()

api_router.include_router(login.router, tags=['login'])
api_router.include_router(account.router, tags=['account'])