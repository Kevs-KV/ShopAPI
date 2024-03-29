from sqlalchemy import Column, Integer, Identity, VARCHAR
from sqlalchemy.orm import relationship

from app.services.database.models.base import Base


class Category(Base):
    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    name = Column(VARCHAR(255), unique=True, index=True)
    products = relationship('Product', back_populates="category", lazy=True)
