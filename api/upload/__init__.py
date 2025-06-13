import io
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from api.upload.service import CHUNK_SIZE, create_document, MAX_FILE_SIZE_MB, process_upload
from database import get_db

router = APIRouter()


@router.post("/upload")
async def upload_file(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    contents = await file.read()
    file_size = len(contents)

    # Validate file size
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 5MB limit.")

    file_like_object = io.BytesIO(contents)

    # Generate UUID
    file_id = uuid.uuid4()
    file_db_in = {
        "id": file_id,
        "filename": file.filename,
        "file_size": file_size,
        "progress": 10,
        "language": "en"
    }
    doc_obj = await create_document(file_db_in, db)
    background_tasks.add_task(process_upload, file_like_object, doc_obj.id)
    return {"file_id": str(file_id), "message": "File uploaded and text extracted."}
