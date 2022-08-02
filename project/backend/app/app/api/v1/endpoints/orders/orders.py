from fastapi import APIRouter, Depends
from starlette.requests import Request

from api.v1.dependencies.database_marker import OrderRepositoryDependencyMarker, \
    ItemRepositoryDependencyMarker
from services.cart.cart import Cart
from services.database.repositories.order.item_repository import ItemRepository
from services.database.repositories.order.order_repository import OrderRepository
from services.database.schemas.order.order import OrderDTO, OrderBodySpec

router = APIRouter()


@router.post('/create/')
async def add_order(request: Request,
                    order: OrderDTO = OrderBodySpec.item,
                    order_crud: OrderRepository = Depends(OrderRepositoryDependencyMarker),
                    item_crud: ItemRepository = Depends(ItemRepositoryDependencyMarker)):
    cart = Cart(request).__dict__['cart']
    order_obj = await order_crud.add_order(order)
    for product in cart.values():
        await item_crud.add_order(order_id=order_obj.id, product_id=product)
    return {'saccess': True}
