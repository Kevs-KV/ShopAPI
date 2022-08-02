from dataclasses import dataclass
from typing import Any

from fastapi import Body
from pydantic import BaseModel


@dataclass
class OrderBodySpec:
    item: Any = Body(
        ...,
        example={
            "full_name": "Kirill Vashchenko",
            'email': 'k.vashhenko@gmail.com',
            'address': '1790 Broadway, NY 10019',
            'city': 'New York',
            'country': 'USA',
            'telephone': '+375291234567'
        },
    )


class OrderDTO(BaseModel):
    full_name: str
    email: str
    address: str
    city: str
    country: str
    telephone: str

    class Config:
        orm_mode = True
        schema_extra = {
            "full_name": "Kirill Vashchenko",
            'email': 'k.vashhenko@gmail.com',
            'address': '1790 Broadway, NY 10019',
            'city': 'New York',
            'country': 'USA',
            'telephone': '+375291234567'
        }
        keep_untouched = ()
        use_enum_values = True

    def patch_enum_values(self) -> None:
        self.Config.use_enum_values = False
