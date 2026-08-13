from datetime import datetime

from pydantic import BaseModel


class Product(BaseModel):
    # Modelo de como deberia lucir un producto
    name: str
    sku: str
    price: float
    currency: str = "MXN" # Valor por defecto 
    store: str
    scraped_at: datetime
