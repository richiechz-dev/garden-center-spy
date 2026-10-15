from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from load.db_models import ProductModel


def get_products_with_latest_price(db: Session, skip: int = 0, limit: int = 100):
    """Consulta productos y arma cada uno con su precio más reciente.

    skip/limit = paginación (saltar N, tomar M).
    """
    stmt = (
        select(ProductModel)
        # .options(selectinload(ProductModel.price_history))
        # Analogía: sin esto, pedirías "dame 100 productos" y luego, por cada
        # producto, "dame su historial" = 1 + 100 queries (problema N+1).
        # Con selectinload haces 2 queries: una para productos, otra para TODOS
        # esos historiales en un solo query. Como pedir la lista de platos de una
        # vez vs. preguntar por cada plato individualmente.
        .options(selectinload(ProductModel.price_history))
        .order_by(ProductModel.id)
        .offset(skip)
        .limit(limit)
    )
    products = db.scalars(stmt).all()

    result = []
    for product in products:
        # De todo el historial, nos quedamos solo con el más reciente
        # (el que tiene scraped_at mayor). Si no tiene historial, lo saltamos.
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