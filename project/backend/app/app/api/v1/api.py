from fastapi import APIRouter

from api.v1.endpoints.authentication import api_authentication
from api.v1.endpoints.cart import api_cart
from api.v1.endpoints.orders import api_order
from api.v1.endpoints.products import api_products
from api.v1.endpoints.users import api_users

api_router = APIRouter()

api_router.include_router(api_authentication.api_router)
api_router.include_router(api_users.api_router)
api_router.include_router(api_products.api_router)
api_router.include_router(api_cart.api_router)
api_router.include_router(api_order.api_router)
