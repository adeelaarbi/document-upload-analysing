import asyncio
import os
import tempfile
import time
import uuid
from io import BytesIO

import magic
from PyPDF2 import PdfReader
from fastapi import UploadFile
from sqlalchemy.orm import Session

from database import SessionLocal
from models.document import Document

CHUNK_SIZE = 1024 * 1024
MAX_FILE_SIZE_MB = 5
ALLOWED_TYPES = ["application/pdf", "text/plain"]


async def extract_text(file: UploadFile, content: bytes) -> str:
    if file.content_type == "application/pdf":
        reader = PdfReader(file.file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    elif file.content_type == "text/plain":
        return content.decode("utf-8")
    else:
        raise ValueError("Unsupported file type")


async def create_document(data: dict, db: Session):
    doc = Document(**data)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


async def save_file_chunks(file: BytesIO, temp_path: str, doc_id: uuid.UUID):
    """Save uploaded file in chunks while updating progress"""
    db = SessionLocal()
    doc = db.query(Document).filter(Document.id == doc_id).first()
    try:
        with open(temp_path, 'wb') as temp_file:
            total_size = 0
            while chunk := file.read(CHUNK_SIZE):
                total_size += len(chunk)
                temp_file.write(chunk)
                # Update progress (10-30%)
                progress = min(30, 10 + int((total_size / doc.file_size) * 20))
                doc.progress = progress
                doc.current_stage = "Extracting text"
                db.commit()
                await asyncio.sleep(1)
        return True
    except Exception as e:
        doc.status = "error"
        doc.current_stage = f"Upload failed: {str(e)}"
        db.commit()
        return False
    finally:
        db.close()


async def process_text_extraction(temp_path: str, doc_id: uuid.UUID, mime_type: str):
    """Process text extraction in background"""
    db = SessionLocal()
    doc = db.query(Document).filter(Document.id == doc_id).first()
    try:
        doc.current_stage = "Preparing for analysis"
        doc.progress = 40
        db.commit()

        # Extract text based on file type
        if mime_type == "application/pdf":
            with open(temp_path, 'rb') as pdf_file:
                reader = PdfReader(pdf_file)
                text = ""
                total_pages = len(reader.pages)

                for i, page in enumerate(reader.pages):
                    text += (page.extract_text() or "") + "\n"
                    # Update progress (40-90%)
                    progress = 40 + int((i + 1) / total_pages * 50)
                    doc.progress = progress
                    db.commit()
                    await asyncio.sleep(1)

        else:  # text/plain
            with open(temp_path, 'r') as txt_file:
                text = txt_file.read()
                doc.progress = 90
                db.commit()

        # Final update
        doc.extracted_text = text
        doc.text_length = len(text)
        doc.current_stage = "Ready for AI analysis"
        doc.progress = 100
        doc.status = "success"
        db.commit()

    except Exception as e:
        doc.status = "error"
        doc.current_stage = f"Text extraction failed: {str(e)}"
        doc.progress = 0
        db.commit()
    finally:
        db.close()
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)


async def process_upload(file: BytesIO, doc_id: uuid.UUID):
    """Main background processing function"""
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = temp_file.name

    # Explicitly seek using the UploadFile method
    success = await save_file_chunks(file, temp_path, doc_id)
    if not success:
        return

    # Validate MIME type
    with open(temp_path, 'rb') as f:
        mime = magic.from_buffer(f.read(2048), mime=True)

    if mime not in ALLOWED_TYPES:
        db = SessionLocal()
        doc = db.query(Document).filter(Document.id == doc_id).first()
        doc.status = "error"
        doc.current_stage = "Extracting text"
        db.commit()
        db.close()
        os.remove(temp_path)
        return
    # Process text extraction
    await process_text_extraction(temp_path, doc_id, mime)


async def db_get_documents(db: Session):
    return db.query(Document).order_by(Document.upload_time.desc()).all()
