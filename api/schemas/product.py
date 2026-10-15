from pydantic import BaseModel, ConfigDict


class ProductOut(BaseModel):
    """Shape del JSON de salida de un producto (lo que ve el cliente)."""
    # from_attributes=True permite construir el modelo desde un objeto ORM/dict
    # con atributos, no solo desde un dict exacto (dict → attrs).
    # Sin esto: ProductOut(**dict) o ProductOut.model_validate(dict)
    # Con esto:  ProductOut.model_validate(objeto_orm) también funciona
    # porque Pydantic "lee" los atributos del objeto (name, sku, price...).
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sku: str
    price: float
    store: str
    currency: str
    image_url: str | None = None