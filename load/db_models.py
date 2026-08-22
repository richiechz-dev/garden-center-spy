from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class ProductModel(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sku: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    store: Mapped[str]
    description: Mapped[str | None]
    image_url: Mapped[str | None]
    product_url: Mapped[str | None]

    price_history: Mapped[list["PriceHistoryModel"]] = relationship(
        back_populates="product"
    )


class PriceHistoryModel(Base):
    __tablename__ = "price_history"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    price: Mapped[float]
    currency: Mapped[str]
    scraped_at: Mapped[datetime]

    product: Mapped["ProductModel"] = relationship(back_populates="price_history")
