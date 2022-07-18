from dataclasses import dataclass
from typing import Any

from fastapi import Body
from pydantic import BaseModel


@dataclass
class CategoryBodySpec:
    item: Any = Body(
        ...,
        example={
            "name": "Laptop"
        },
    )


class CategoryDTO(BaseModel):
    name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Laptop"
        }
