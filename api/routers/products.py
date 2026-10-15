from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.crud.product import get_products_with_latest_price
from api.dependencies import get_db
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
