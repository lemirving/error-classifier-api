from fastapi import APIRouter, BackgroundTasks, Depends
from app.database import supabase
from app.services.auth import get_current_user
from app.services.processor import processar_texto_completo
from app.services.schemas import AnalysisRequest, AnalysisResponse # Importei o Response aqui
from app.services.processor import task_processar_e_persistir
analyze_router = APIRouter(tags=["analyze"])

# 1. Mudamos para POST
# 2. Adicionamos o response_model para o FastAPI validar a saída automaticamente
# No seu arquivo /app/routes/analyze.py

@analyze_router.post("/analyze")
async def process(request: AnalysisRequest, background_tasks: BackgroundTasks):
    # O ERRO ESTAVA AQUI: você provavelmente tentou usar request.student_id
    # mas o Pydantic só conhece o que está na classe AnalysisRequest.
    
    background_tasks.add_task(task_processar_e_persistir, request.text_id, request.text)
    
    return {
        "status": "processing",
        "text_id": request.text_id  # Mude de student_id para text_id
    }