import pytest

from app.services.database.repositories.product.product_repository import ProductRepository
from app.services.database.repositories.user.user_repository import UserRepository



@pytest.fixture(name="test_user", scope="module")
async def user_for_test(session_maker: sessionmaker) -> User:  # type: ignore
    repository = UserRepository(session_maker)
    return await repository.add_user(full_name='Kevs', email='kevs@gmail.com',
                                     hashed_password='password', is_active=True, is_superuser=True)


@pytest.fixture(name="test_product", scope="module")
async def product_for_test(session_maker: sessionmaker) -> Product:  # type: ignore
    product_repository = ProductRepository(session_maker)
    return await product_repository.add_product(name="Apple MacBook 15", unit_price=7000,
                                                description="Light and fast laptop, Light and fast laptop",
                                                category_id=1, brand_id=1)
