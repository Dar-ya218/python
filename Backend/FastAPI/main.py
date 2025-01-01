from fastapi import FastAPI
from routers import products

app = FastAPI()

app.include_router(products.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/url")
async def read_root():
    return {"url": "Url"}