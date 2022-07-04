import enum

from sqlalchemy import Column, Integer, Identity, VARCHAR, Numeric, Enum, Text, DateTime, func

from services.database.models.base import Base


class ColorEnum(enum.Enum):
    BLACK = 'BLACK'
    WHITE = 'WHITE'


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    name = Column(VARCHAR(255), unique=True, index=True)
    color = Enum(ColorEnum)
    unit_price = Column(Numeric(precision=8), server_default="1")
    description = Column(Text, default=None, nullable=True)
    created_at = Column(DateTime(), server_default=func.now())
