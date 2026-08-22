from sqlalchemy import select

from load.connection import get_session
from load.db_models import PriceHistoryModel, ProductModel
from models import Product


def load_products(products_list: list[Product]):

    with get_session() as session:
        for product in products_list:
            stmt = select(ProductModel).where(ProductModel.sku == product.sku)
            existing_product = session.execute(stmt).scalar_one_or_none()
            if existing_product is None:
                new_product = ProductModel(
                    sku=product.sku,
                    name=product.name,
                    store=product.store,
                    description=product.description,
                    image_url=product.image_url,
                    product_url=product.product_url,
                )
                session.add(new_product)
                session.flush()
                product_id = new_product.id
            else:
                product_id = existing_product.id

            new_price = PriceHistoryModel(
                product_id=product_id,
                price=product.price,
                currency=product.currency,
                scraped_at=product.scraped_at,
            )
            session.add(new_price)

        session.commit()
