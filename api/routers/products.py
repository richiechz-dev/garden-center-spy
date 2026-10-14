from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.crud.product import get_products_with_latest_price
from api.dependencies import get_db
from api.schemas.product import ProductOut

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_products_with_latest_price(db, skip=skip, limit=limit)
