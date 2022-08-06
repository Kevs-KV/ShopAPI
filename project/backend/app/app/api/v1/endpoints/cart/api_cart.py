from fastapi import APIRouter

from app.api.v1.endpoints.cart import cart

api_router = APIRouter()

api_router.include_router(cart.router, prefix="/cart", tags=["cart"])
