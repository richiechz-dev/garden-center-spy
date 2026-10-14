from fastapi import FastAPI

from api.routers import products

app = FastAPI(title="Garden Center Spy API")

app.include_router(products.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
