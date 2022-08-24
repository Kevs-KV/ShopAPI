from app.services.database.models.order import Order
from app.services.worker.tasks import task_send_mail_order_list
from app.utils.serializer_utils import OrderSerializer


async def _get_order_payload(order: Order) -> dict:
    order_payload = OrderSerializer(order).serializer()
    return order_payload


async def order_alert_user(order: Order, mail_config: dict, total_price: int) -> bool:
    order_payload = await _get_order_payload(order)
    order_payload['total_price'] = total_price
    task_send_mail_order_list.delay(mail_config, order_payload, order.email)
    return True
