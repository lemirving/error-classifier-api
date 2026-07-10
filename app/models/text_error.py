from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID
import uuid
from datetime import datetime

# table=True avisa que essa classe representa uma tabela no banco
class TextError(SQLModel, table=True):
    __tablename__ = "text_errors" # O nome exato da tabela no banco
    
    # O id gerado pelo banco. Usamos Optional para o Python não reclamar na hora de inserir
    id: Optional[UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    text_id: UUID = Field(foreign_key="texts.id", nullable=False)
    
    word_found: str = Field(max_length=255, nullable=False)
    suggestion: str = Field(max_length=255, nullable=False)
    classification: str = Field(max_length=100, nullable=False)
    diff: str = Field(max_length=255, nullable=False)
    is_recognized: bool = Field(nullable=False)
    
    explanation: Optional[str] = Field(default=None)
    is_corrected: bool = Field(default=False, nullable=False)
    
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)