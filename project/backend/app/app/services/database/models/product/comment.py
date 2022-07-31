from sqlalchemy import Column, Integer, Identity, Text, ForeignKey
from sqlalchemy.orm import relationship

from services.database.models.base import Base


class Comment(Base):
    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates="comments")
    product_id = Column(Integer, ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    product = relationship('Product', back_populates="comments")

