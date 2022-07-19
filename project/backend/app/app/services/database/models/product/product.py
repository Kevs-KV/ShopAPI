import enum

from sqlalchemy import Column, Integer, Identity, VARCHAR, Numeric, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from services.database.models.base import Base


class ColorEnum(enum.Enum):
    BLACK = 'BLACK'
    WHITE = 'WHITE'


class Product(Base):
    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    name = Column(VARCHAR(255), unique=True, index=True)
    category_id = Column(Integer, ForeignKey('category.id', ondelete="CASCADE"), nullable=False)
    category = relationship('Category', backref="products")
    unit_price = Column(Numeric(precision=8), server_default="1")
    description = Column(Text, default=None, nullable=True)
    created_at = Column(DateTime(), server_default=func.now())
