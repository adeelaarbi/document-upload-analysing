import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from database import SessionLocal
from models.document import Document
from uuid import UUID

router = APIRouter()


async def status_stream(file_id: UUID):
    last_progress = -1

    while True:
        try:
            # Create new session for each iteration
            db = SessionLocal()
            doc = db.query(Document).filter(Document.id == file_id).first()

            if not doc:
                error_data = json.dumps({
                    "error": "Document not found",
                    "details": "document not provided or does not exist"
                })
                yield f"event: error\ndata: {error_data}\n\n"
                break

            # If there's a progress change, send update
            if doc.progress != last_progress:
                last_progress = doc.progress
                event_data = json.dumps({
                    "progress": doc.progress,
                    "current_stage": doc.current_stage
                })
                # Properly format SSE with JSON-encoded data
                yield f"data: {event_data}\n\n"

            # Check for completion
            if doc.progress >= 100:
                break

            # Check for errors
            if doc.status == "error":
                error_data = json.dumps({
                    "error": "Processing failed",
                    "details": doc.error_message if hasattr(doc, 'error_message') else "Unknown error"
                })
                yield f"event: error\ndata: {error_data}\n\n"
                break

        except Exception as e:
            error_data = json.dumps({
                "error": "Unknown error",
                "details": str(e)
            })
            yield f"event: error\ndata: {error_data}\n\n"
            break

        finally:
            db.close()

        # Wait before next check
        await asyncio.sleep(1)


@router.get("/stream/{file_id}")
async def get_status(file_id: UUID):
    return StreamingResponse(
        content=status_stream(file_id),
        media_type="text/event-stream"
    )

