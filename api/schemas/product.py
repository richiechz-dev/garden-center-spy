from pydantic import BaseModel, ConfigDict


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    sku: str
    price: float
    store: str
    currency: str
    image_url: str | None = None