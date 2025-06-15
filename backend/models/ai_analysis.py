import uuid
from sqlalchemy import Column, Text, Integer, DateTime, ForeignKey, String, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from sqlalchemy.orm import relationship

from models.base import Base

class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    prompt_template_id = Column(UUID(as_uuid=True), ForeignKey("prompt_templates.id"))
    final_prompt = Column(Text, nullable=False)
    gemini_response = Column(Text)
    response_metadata = Column(JSON)
    execution_time_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    error_message = Column(Text)
    status = Column(String(50), default="success")
    cached = Column(Boolean, default=False)

    document = relationship("Document", back_populates="analyses")
    prompt_template = relationship("PromptTemplate", back_populates="analyses")
