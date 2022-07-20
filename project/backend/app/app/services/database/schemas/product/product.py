import datetime
from dataclasses import dataclass
from typing import Optional, Any

from fastapi import Body
from pydantic import BaseModel


@dataclass
class ProductBodySpec:
    item: Any = Body(
        ...,
        example={
            "name": "Apple MacBook 15",
            "unit_price": 7000,
            "description": "Light and fast laptop, Light and fast laptop, Light and fast laptop, Light and fast laptop",
            'category_id': '1',
            'brand_id': '1',
        },
    )


class ProductDTO(BaseModel):
    id: Optional[int] = None
    name: str
    unit_price: float
    description: str
    created_at: Optional[datetime.datetime] = None
    category_id: int
    brand_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Apple MacBook 15",
            "unit_price": 7000,
            "description": "Light and fast laptop",
        }
        keep_untouched = ()
        use_enum_values = True

    def patch_enum_values(self) -> None:
        self.Config.use_enum_values = False

