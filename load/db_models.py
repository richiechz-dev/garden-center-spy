from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class ProductModel(Base):
    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint("sku", "store", name="products_sku_store_key"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sku: Mapped[str]
    store: Mapped[str]
    name: Mapped[str]
    scientific_name: Mapped[str | None]
    category: Mapped[str | None]
    measurement: Mapped[str | None]
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