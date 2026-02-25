from fastapi import FastAPI
from backend.routers import auth, products, orders

app = FastAPI(title="DM for Price API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

@app.get("/")
def root():
    return {"status": "DM for Price API running"}
