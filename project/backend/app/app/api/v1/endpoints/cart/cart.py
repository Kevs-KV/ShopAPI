from fastapi import APIRouter, Depends
from starlette.requests import Request

from api.v1.dependencies.database_marker import ProductRepositoryDependencyMarker
from services.cart.cart import Cart
from services.database.repositories.product.product_repository import ProductRepository

router = APIRouter()


@router.post('/add/')
async def cart_add(request: Request, product_id: int, quntity=1,
                   product_crud: ProductRepository = Depends(ProductRepositoryDependencyMarker)):
    cart = Cart(request)
    product = await product_crud.get_product(product_id)
    cart.add(product, int(quntity), update_quantity=False)
    return {"success": True}


@router.get('/get/')
async def cart_get(request: Request):
    cart = Cart(request).__dict__['cart']
    return {"cart": cart}
