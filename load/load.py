from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from load.connection import get_session
from load.db_models import PriceHistoryModel, ProductModel
from models import Product


def load_products(products_list: list[Product]):
    # Intenta cargar todos los productos a la BD, si falla lanza un error
    try:
        with get_session() as session:  # Abre una sesion
            for product in products_list:
                # Busca si el producto ya existe por SKU
                stmt = select(ProductModel).where(ProductModel.sku == product.sku)
                existing_product = session.execute(stmt).scalar_one_or_none()

                if existing_product is None:
                    # Si no existe es porque es un producto nuevo y lo crea en la tabla de products
                    new_product = ProductModel(
                        sku=product.sku,
                        name=product.name,
                        store=product.store,
                        description=product.description,
                        image_url=product.image_url,
                        product_url=product.product_url,
                    )
                    session.add(new_product)
                    session.flush() # Obtiene el id antes de crear el historial
                    product_id = new_product.id
                else:
                    # En caso contrario de que si exista reutiliza su ID
                    product_id = existing_product.id
                # Agrega la entrada a la tabla de historial de precios
                new_price = PriceHistoryModel(
                    product_id=product_id,
                    price=product.price,
                    currency=product.currency,
                    scraped_at=product.scraped_at,
                )
                session.add(new_price)
            # Confirma todos los cambios en la BD
            session.commit()
    except SQLAlchemyError as e:
        # Si falla, sqlalchemy hace un rollback automatico
        raise e
