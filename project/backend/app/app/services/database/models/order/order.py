from sqlalchemy import Column, Integer, Identity, ForeignKey, String, Numeric
from sqlalchemy.orm import relationship

from app.services.database.models.base import Base


class Order(Base):
    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True, nullable=False)
    address = Column(String, index=True)
    city = Column(String, index=True)
    country = Column(String, index=True)
    telephone = Column(String, index=True)
    items = relationship('Item', back_populates="order")


class Item(Base):
    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id', ondelete="CASCADE"), nullable=False)
    order = relationship('Order', back_populates="items")
    product_id = Column(Integer, ForeignKey('product.id', ondelete="CASCADE"), nullable=False)
    price = Column(Numeric(precision=8), server_default="1")
    quantity = Column(Integer)
