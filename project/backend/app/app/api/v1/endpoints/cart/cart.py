from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from app.api.v1.dependencies.database_marker import ProductRepositoryDependencyMarker
from app.services.cart.cart import Cart
from app.services.database.repositories.product.product_repository import ProductRepository

router = APIRouter()


@router.post('/add/')
async def cart_add(request: Request, product_id: int, quntity: int = 1,
                   product_crud: ProductRepository = Depends(ProductRepositoryDependencyMarker)):
    cart = Cart(request)
    product = await product_crud.get_product(product_id)
    cart.add(product, int(quntity), update_quantity=False)
    return {"success": True}


@router.get('/get/')
async def cart_get(request: Request):
    cart = Cart(request)
    values = cart.__dict__['cart']
    quantity = cart.__len__()
    return {'quantity': quantity, "cart": values}


@router.delete('/delete/')
async def cart_delete(request: Request, product_id: str):
    cart = Cart(request)
    if product_id in cart.__dict__['cart']:
        cart.remove(product_id)
        return {"success": True}
    raise HTTPException(
        status_code=404, detail=f"There is no product with id={product_id} in the cart"
    )
