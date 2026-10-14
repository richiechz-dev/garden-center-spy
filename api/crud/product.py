from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from load.db_models import ProductModel


def get_products_with_latest_price(db: Session, skip: int = 0, limit: int = 100):
    stmt = (
        select(ProductModel)
        .options(selectinload(ProductModel.price_history))
        .order_by(ProductModel.id)
        .offset(skip)
        .limit(limit)
    )
    products = db.scalars(stmt).all()

    result = []
    for product in products:
        latest = None
        for ph in product.price_history:
            if latest is None or ph.scraped_at > latest.scraped_at:
                latest = ph

        if latest is None:
            continue

        result.append(
            {
                "name": product.name,
                "sku": product.sku,
                "store": product.store,
                "image_url": product.image_url,
                "price": latest.price,
                "currency": latest.currency,
            }
        )
    return result