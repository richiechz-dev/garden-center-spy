from fastapi import FastAPI

from api.routers import products

# Crea la app FastAPI. title aparece en /docs (Swagger UI).
app = FastAPI(title="Garden Center Spy API")

# Monta el router de products: todas sus rutas quedan bajo /products.
app.include_router(products.router)

@app.get("/")
def read_root():
    """Endpoint raíz de prueba para verificar que la API responde."""
    return {"Hello": "World"}
