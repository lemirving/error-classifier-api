
from fastapi import APIRouter
from database import supabase  # <--- AQUI você chama o banco!
from textProcessing.processor import processar_teste_manual, tool
from textProcessing.schemas import AnalysisRequest 

classify_router = APIRouter(prefix="/classify", tags=["classify"])

@classify_router.get("/")
async def classify():
    """
    Essa é a rota de classificação e tratamento de textos padrão
    Toda requisição aqui precias de autenticação
    Returns:
        _type_: _description_
    """
    return {"mensagem" : "Voce acessou /classify"}
    
    
    
    
#apenas pra testar conexão e correção de textos enviados
# @classify_router.post("/test-corrector")
# async def rota_de_teste(request: AnalysisRequest):
#     # Chama a função que está no seu arquivo processor.py
#     dados_processados = processar_teste_manual(request.text)
    
#     return {
#         "student_id": request.student_id,
#         "erros": dados_processados
#     }



#Apenas pra testar conexão com supabase
# @classify_router.get("/test-db")
# async def test_connection():
#     # Tenta buscar algo simples só para ver se conecta
#     try:
#         response = supabase.table("author").select("*").limit(10).execute()
#         return {"status": "Conectado!", "data": response.data}
#     except Exception as e:
#         return {"status": "Erro", "details": str(e)}


