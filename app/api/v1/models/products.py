from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    stock: int


class ProductUpdate(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

    name: str | None = None
    description: str | None = None
    price: int | None = None
    stock: int | None = None
    labels_to_add: list[str] = []
    labels_to_remove: list[str] = []


class ProductIn(ProductBase):
    labels: list[str] | None = None


class LabelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ProductOut(ProductBase):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True
    )

    id: int
    created_at: datetime

    labels: list[LabelOut] = []
