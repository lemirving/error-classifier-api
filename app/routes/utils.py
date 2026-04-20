from fastapi import APIRouter

utils_router = APIRouter(prefix="/utils", tags = ["utils"])

@utils_router.get("/health")
async def health():
    return {"Servidor": "rodando"}

