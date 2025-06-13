import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from models.base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="uploaded")
    current_stage = Column(String(100))
    progress = Column(Integer, default=0)
    extracted_text = Column(Text)
    text_length = Column(Integer)
    language = Column(String(10))
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
