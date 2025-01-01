from fastapi import APIRouter

router = APIRouter()

@router.get("/products")
async def get_products():
    return [{"name": "Product 1"}, {"name": "Product 2"}]