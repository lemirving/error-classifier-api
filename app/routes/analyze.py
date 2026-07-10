from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from uuid import UUID
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models.text_error import TextError
from app.routes.auth import get_current_user
from app.services.hf_client import HuggingFaceClient
from app.services.text_processor import TextProcessor

router = APIRouter(prefix="/analyze", tags=["Análise"])
hf_client = HuggingFaceClient()

class AnalysisRequest(BaseModel):
    text_id: UUID
    text: str

text_processor = TextProcessor()

@router.post("/process")
async def processar_analise(
    dados: AnalysisRequest,
    user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    try:

        pares_para_ia = text_processor.extrair_pares_erros(dados.text)
        
        if not pares_para_ia:
            return {
                "status": "success", 
                "message": "Nenhum desvio ortográfico detectado no texto.",
                "errors_persisted_count": 0
            }

        erros_classificados = await hf_client.classificar_erros(pares_para_ia)

        # persiste os dados
        for erro in erros_classificados:
            novo_erro_db = TextError(
                text_id=dados.text_id,
                word_found=erro["errada"],
                suggestion=erro["correta"],
                classification=erro["classe"],
                diff=erro["diff"],
                is_recognized=erro["reconhecida"],
                explanation=f"A palavra '{erro['errada']}' foi classificada como um desvio de {erro['classe']}.",
                is_corrected=False
            )
            session.add(novo_erro_db)

        await session.commit()

        return {
            "status": "success",
            "text_id": dados.text_id,
            "errors_persisted_count": len(erros_classificados)
        }

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro no processador ou na persistência: {str(e)}"
        )