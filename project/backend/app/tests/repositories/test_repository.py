import pytest
from sqlalchemy.orm import sessionmaker

from app.services.database.models.order import Order, Item
from app.services.database.models.product import Product, Brand, Category, Comment
from app.services.database.models.user import User
from app.services.database.repositories.order.item_repository import ItemRepository
from app.services.database.repositories.order.order_repository import OrderRepository
from app.services.database.repositories.product.brand_repository import BrandRepository
from app.services.database.repositories.product.category_repository import CategoryRepository
from app.services.database.repositories.product.comment_repositiry import CommentRepository
from app.services.database.repositories.product.product_repository import ProductRepository
from app.services.database.repositories.user.user_repository import UserRepository


@pytest.fixture(name="test_user", scope="module")
async def user_for_test(session_maker: sessionmaker) -> User:  # type: ignore
    repository = UserRepository(session_maker)
    return await repository.add_user(full_name='Kevs', email='kevs@gmail.com',
                                     hashed_password='password', is_active=True, is_superuser=True)


@pytest.fixture(name="test_brand", scope="module")
async def category_for_test(session_maker: sessionmaker) -> Category:  # type: ignore
    category_repository = CategoryRepository(session_maker)
    return await category_repository.add_category(name="Laptop")


@pytest.fixture(name="test_category", scope="module")
async def category_for_test(session_maker: sessionmaker) -> Brand:  # type: ignore
    brand_repository = BrandRepository(session_maker)
    return await brand_repository.add_brand(name='Apple')


@pytest.fixture(name="test_product", scope="module")
async def product_for_test(session_maker: sessionmaker) -> Product:  # type: ignore
    product_repository = ProductRepository(session_maker)
    return await product_repository.add_product(name="Apple MacBook 15", unit_price=7000,
                                                description="Light and fast laptop, Light and fast laptop",
                                                category_id=1, brand_id=1)


@pytest.fixture(name="test_comment", scope="module")
async def comment_for_test(session_maker: sessionmaker) -> Comment:
    comment_repository = CommentRepository(session_maker)
    return await comment_repository.add_comment(product_id=1,
                                                text="Light and fast laptop, Light and fast laptop",
                                                rating=5)


@pytest.fixture(name="test_order", scope="module")
async def order_for_test(session_maker: sessionmaker) -> Order:
    comment_repository = OrderRepository(session_maker)
    return await comment_repository.add_order(full_name='Kirill Vashchenko', email='k.vashhenko@gmail.com',
                                              address='1790 Broadway, NY 10019',
                                              city='New York',
                                              country='USA',
                                              telephone='+375291234567')


@pytest.fixture(name="test_item", scope="module")
async def item_for_test(sessision_marker: sessionmaker) -> Item:
    item_repository = ItemRepository(sessision_marker)
    return await item_repository.add_item(order_id=int,
                                          name='Apple MacBook 15',
                                          product_id=1, quantity=1,
                                          price=7000)
