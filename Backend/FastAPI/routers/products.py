from fastapi import APIRouter

router = APIRouter()

@router.get("/products")
async def get_products():
    return ["Product 1", "Product 2", "Product 3", "Product 4"]