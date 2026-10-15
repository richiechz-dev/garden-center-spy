from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PricePointOut(BaseModel):
    """Un punto en el historial de precios de un producto."""
    # from_attributes=True: permite construir desde el objeto ORM
    # (mismo patrón que ProductOut).
    model_config = ConfigDict(from_attributes=True)

    price: float
    currency: str
    scraped_at: datetime
