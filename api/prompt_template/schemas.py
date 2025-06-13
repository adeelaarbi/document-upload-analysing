from pydantic import BaseModel, Field
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime

class Variable(BaseModel):
    name: str
    required: bool

class PromptTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    prompt_text: str
    category: Optional[str] = None
    variables: Optional[List[Variable]] = None
    example_output: Optional[str] = None
    is_public: bool = True

class PromptTemplateCreate(PromptTemplateBase):
    pass

class PromptTemplateUpdate(PromptTemplateBase):
    pass

class PromptTemplateOut(PromptTemplateBase):
    id: UUID
    usage_count: int
    created_at: datetime

    class Config:
        from_attributes = True
