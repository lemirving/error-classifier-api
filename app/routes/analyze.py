from fastapi import APIRouter, Depends
from app.database import supabase
from app.services.auth import get_current_user
from app.services.processor import processar_texto_completo
from app.services.schemas import AnalysisRequest, AnalysisResponse # Importei o Response aqui

analyze_router = APIRouter(tags=["analyze"])

# 1. Mudamos para POST
# 2. Adicionamos o response_model para o FastAPI validar a saída automaticamente
@analyze_router.post("/analyze", response_model=AnalysisResponse)
async def process(request: AnalysisRequest):
    # O processor vai lá no Hugging Face e traz a lista de dicionários
    resultado_ia = await processar_texto_completo(request.text)
    
    # Retorna o dicionário exatamente no formato que o AnalysisResponse exige
    return {
        "student_id": request.student_id,
        "error_list": resultado_ia
    }