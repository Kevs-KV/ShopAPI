from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.exc import DBAPIError
from starlette.requests import Request

from api.v1.dependencies.database_marker import OrderRepositoryDependencyMarker, \
    ItemRepositoryDependencyMarker
from services.cart.cart import Cart
from services.database.repositories.order.item_repository import ItemRepository
from services.database.repositories.order.order_repository import OrderRepository
from services.database.schemas.order.order import OrderDTO, OrderBodySpec
from services.security.jwt import JWTSecurityHead

router = APIRouter()


@router.post('/create/')
async def add_order(request: Request,
                    order: OrderDTO = OrderBodySpec.item,
                    order_crud: OrderRepository = Depends(OrderRepositoryDependencyMarker),
                    item_crud: ItemRepository = Depends(ItemRepositoryDependencyMarker)):
    cart = Cart(request)
    values = cart.__dict__['cart']
    if len(cart) < 1:
        return {'detail': 'There are no products in the cart'}
    total_price = cart.get_total_price()
    order_obj = await order_crud.add_order(order)
    for product in values:
        await item_crud.add_order(order_id=order_obj.id, product_id=int(product),
                                  quantity=values[product]['quantity'], price=values[product]['price'])
    result_order = await order_crud.get_order(order_obj.id)
    cart.clear()
    return {'total_price': total_price, 'order': result_order}


@router.get('/{order_id}/')
async def get_order(order_id: int,
                    order_crud: OrderRepository = Depends(OrderRepositoryDependencyMarker)):
    return await order_crud.get_order(order_id)


@router.get('/list/{page}/{limit}', dependencies=[Security(JWTSecurityHead(), scopes=['admin'])])
async def get_order_list(page: int, limit: int, order_crud: OrderRepository = Depends(OrderRepositoryDependencyMarker)):
    try:
        return await order_crud.get_list_order(page, limit)
    except DBAPIError:
        raise HTTPException(
            status_code=400, detail=f"Incorrect data to display"
        )
