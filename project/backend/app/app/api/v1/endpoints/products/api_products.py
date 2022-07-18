from fastapi import APIRouter

from api.v1.endpoints.products import products

api_router = APIRouter()

api_router.include_router(products.router, prefix="/products", tags=["products"])
