from decimal import Decimal

from starlette.requests import Request

from services.database.models.product import Product

secret_key = 'cart'


class Cart:

    def __init__(self, request: Request):
        self.session = request.session
        cart = self.session.get(secret_key)
        if not cart:
            cart = self.session[secret_key] = {}
        self.cart = cart

    def add(self, product: Product, quantity: int = 1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.unit_price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

    def remove(self, product: Product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )
