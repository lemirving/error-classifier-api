
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from app.routes.analyze import analyze_router
from app.routes.utils import utils_router

app.include_router(analyze_router)
app.include_router(utils_router)


# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # No desenvolvimento, o "*" libera tudo. 
    allow_credentials=True,
    allow_methods=["*"], # Libera POST, GET, OPTIONS, etc.
    allow_headers=["*"], # Libera Content-Type e outros headers
)





# para rodar o código, executar uvicorn main:app --reload no terminal