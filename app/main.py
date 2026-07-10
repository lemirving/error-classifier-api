from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import analyze

# 1. Inicializa a aplicação FastAPI
app = FastAPI(
    title="Classificador de Erros API - PIBEC",
    description="API intermediária para processamento de textos via IA e persistência direta no PostgreSQL.",
    version="1.0.0"
)


origins = [
    "http://localhost:3000",   
    # "https://seu-site-nextjs.vercel.app", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,         
    allow_methods=["*"],           
    allow_headers=["*"],            
)

app.include_router(analyze.router)

@app.get("/", tags=["Healthcheck"])
async def root():
    return {
        "status": "healthy",
        "message": "API do Classificador de Erros rodando perfeitamente."
    }