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
