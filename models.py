from datetime import datetime

from pydantic import BaseModel


class Product(BaseModel):
    # Modelo de como deberia lucir un producto
    name: str
    sku: str
    price: float
    currency: str = "MXN" # Valor por defecto 
    store: str 
    description: str | None = None # Atributo str o nada (opcional) con valor por defecto None
    image_url: str | None = None
    product_url: str | None = None
    scientific_name: str | None = None
    category: str | None = None
    measurement: str | None = None
    scraped_at: datetime
