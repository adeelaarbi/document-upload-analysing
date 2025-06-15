from datetime import datetime

from pydantic import BaseModel
from typing import Optional, Dict
from uuid import UUID

class AnalyzeRequest(BaseModel):
    document_id: UUID
    prompt_template_id: UUID
    variables: Optional[Dict[str, str]] = None  # Optional overrides

class AnalyzeResponse(BaseModel):
    response_text: str
    model: str
    tokens_used: int
    cached: bool
    
class HistoryPromptTemplate(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True


class HistoryDocument(BaseModel):
    id: UUID
    filename: str

    class Config:
        from_attributes = True


class AIAnalysisHistoryOut(BaseModel):
    id: UUID
    document: Optional[HistoryDocument]
    prompt_template: Optional[HistoryPromptTemplate]
    final_prompt: str
    gemini_response: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
