from pydantic import BaseModel, Field
from typing import List, Optional

# 1. O que vem da IA (deve bater com os campos do modelo)
class ErrorClassification(BaseModel):
    errada: str
    correta: str
    classe: str
    diff: str
    reconhecida: bool

# 2. O contrato de Resposta para o seu Frontend (Next.js)
class AnalysisResponse(BaseModel):
    student_id: str
    text_id: Optional[str] = None # Útil se você salvar no banco depois
    error_list: List[ErrorClassification]

# 3. O contrato de Entrada (o que o site envia)
class AnalysisRequest(BaseModel):
    text_id: str
    text: str