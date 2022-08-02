from fastapi import APIRouter

from api.v1.endpoints.orders import orders

api_router = APIRouter()

api_router.include_router(orders.router, prefix="/order", tags=["order"])
