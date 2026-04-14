
from fastapi import FastAPI

app = FastAPI()

from routes.classify_routes import classify_router
from routes.validate_tuple_routes import validate_tuple_router
from routes.utils_routes import utils_router

app.include_router(classify_router)
app.include_router(validate_tuple_router)
app.include_router(utils_router)







# para rodar o código, executar uvicorn main:app --reload no terminal