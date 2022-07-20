from dataclasses import dataclass
from typing import Any

from fastapi import Body
from pydantic import BaseModel


@dataclass
class BrandBodySpec:
    item: Any = Body(
        ...,
        example={
            "name": "Apple"
        },
    )


class BrandDTO(BaseModel):
    name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "Apple"
        }
