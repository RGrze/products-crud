from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Table, Integer, ForeignKey, Column, func

from app.database.db import Base


association_table = Table(
    'association', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('label_id', Integer, ForeignKey('labels.id'), primary_key=True)
)


class Label(Base):
    __tablename__ = "labels"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    name: Mapped[str] = mapped_column(String(64))

    def __repr__(self):
        return f"<Label name={self.name}>"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    name: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(255))
    stock: Mapped[int] = mapped_column(default=0, nullable=False)
    price: Mapped[int]

    labels: Mapped[set["Label"]] = relationship(secondary=association_table)

    def __repr__(self):
        return f"<Product name={self.name} price={self.price} stock={self.stock}>"
