from typing import List

from app.services.database.models.order import Order


class OrderSerializer:

    def __init__(self, order: Order) -> None:
        self._order = order

    def _items_serializer(self) -> List[dict]:
        payload = [{'name': item.name, 'quantity': item.quantity, 'price': item.price} for item in self._order.items]
        return payload

    def serializer(self) -> dict:
        serializer_dict = {
            'order_id': self._order.id,
            'full_name': self._order.full_name,
            'email': self._order.email,
            'address': self._order.address,
            'city': self._order.city,
            'country': self._order.country,
            'telephone': self._order.telephone,
            'products': self._items_serializer()
        }
        return serializer_dict
