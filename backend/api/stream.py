import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from database import SessionLocal
from models.document import Document
from uuid import UUID

router = APIRouter()

def success_message(message):
    return f"data: {message}\n\n"


async def status_stream(file_id: UUID):
    live_progress = 1
    while live_progress < 100:
        # Create new session for each iteration
        db = SessionLocal()
        doc = db.query(Document).filter(Document.id == file_id).first()

        try:
            if not doc:
                error_data = json.dumps({
                    "error": "Document not found",
                    "details": "document not provided or does not exist"
                })
                yield f"event: error\ndata: {error_data}\n\n"
                break
            live_progress = doc.progress

            event_data = json.dumps({
                "progress": live_progress,
                "current_stage": doc.current_stage
            })
            print("Event data:", event_data, "\n\n")
            # Properly format SSE with JSON-encoded data
            yield success_message(event_data)
        except Exception as e:
            print("Error in stream:", e)
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

