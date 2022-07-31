from fastapi import APIRouter

from api.v1.endpoints.products import products, category, brands, comments

api_router = APIRouter()

api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(category.router, prefix="/categories", tags=["categories"])
api_router.include_router(brands.router, prefix="/brands", tags=["brands"])
api_router.include_router(comments.router, prefix='/comments', tags=['comments'])