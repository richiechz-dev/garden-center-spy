from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.crud.product import (
    get_price_history,
    get_product,
    get_products_with_latest_price,
)
from api.dependencies import get_db
from api.schemas.price_history import PricePointOut
from api.schemas.product import ProductOut

# prefix="/products" => todas las rutas de este router quedan bajo /products.
# tags solo agrupa en /docs de Swagger.
router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """GET /products — lista paginada de productos con su último precio.

    Este router SOLO maneja HTTP: recibe parámetros, llama al CRUD y devuelve
    la respuesta. Aquí va cero SQL (la capa de datos vive en crud/).
    - skip: cuántos productos saltar (para paginar)
    - limit: cuántos regresar (máx. 100 por defecto)
    - Depends(get_db): FastAPI ejecuta get_db() y te pasa la sesión viva
    """
    return get_products_with_latest_price(db, skip=skip, limit=limit)


@router.get("/{product_id}/price-history", response_model=list[PricePointOut])
def read_price_history(product_id: int, db: Session = Depends(get_db)):
    """GET /products/{product_id}/price-history — historial de precios.

    Devuelve todos los precios del producto, del más viejo al más nuevo.
    - Producto inexistente → 404 "Product not found"
    - Producto sin precios → 200 con lista vacía
    """
    product = get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return get_price_history(db, product_id)
