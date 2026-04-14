from fastapi import APIRouter

validate_tuple_router = APIRouter(prefix="/validate-tuple", tags = ["validate tuple"])

@validate_tuple_router.get("/")
async def validate_tuple():
    return {"Tupla válida"}