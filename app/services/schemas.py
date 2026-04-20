from pydantic import BaseModel
from typing import List

class ErrorClassification(BaseModel):
    incorrect: str
    correct: str
    classification: str
    
    
class AnalysisResponse(BaseModel):
    student_id: str
    error_list: List[ErrorClassification]
    
class AnalysisRequest(BaseModel):
    student_id: str
    text: str