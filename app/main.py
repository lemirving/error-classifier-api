
from fastapi import FastAPI

app = FastAPI()

from app.routes.analyze import analyze_router
from app.routes.utils import utils_router

app.include_router(analyze_router)
app.include_router(utils_router)







# para rodar o código, executar uvicorn main:app --reload no terminal