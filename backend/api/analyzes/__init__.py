from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
import time

from database import get_db
from models import document, prompt_template, ai_analysis
from .schemas import AnalyzeRequest, AnalyzeResponse, AIAnalysisHistoryOut
from .service import db_get_history
from .utils.gemini_client import call_gemini
from .utils.ratelimiter import check_rate_limit

router = APIRouter(prefix="/analyses")

@router.post("", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request)

    doc = db.query(document.Document).filter_by(id=req.document_id).first()
    prompt_template_obj = db.query(prompt_template.PromptTemplate).filter_by(id=req.prompt_template_id).first()

    if not doc or not prompt_template_obj:
        raise HTTPException(404, detail="Document or Prompt not found")

    # Fill variables in prompt
    final_prompt = prompt_template_obj.prompt_text
    merged_vars = {"document_content": doc.extracted_text, **(req.variables or {})}
    try:
        final_prompt = final_prompt.format(**merged_vars)
    except KeyError as e:
        raise HTTPException(400, detail=f"Missing variable in prompt: {e}")

    # Check cache
    existing = db.query(ai_analysis.AIAnalysis).filter_by(
        document_id=doc.id,
        prompt_template_id=prompt_template_obj.id,
        final_prompt=final_prompt
    ).first()

    if existing:
        return AnalyzeResponse(
            response_text=existing.gemini_response.strip(),
            model=existing.response_metadata.get("model", ""),
            tokens_used=existing.response_metadata.get("tokens", 0),
            cached=True
        )

    # Call Gemini
    try:
        start = time.time()
        result = call_gemini(final_prompt)
        duration_ms = int((time.time() - start) * 1000)
    except Exception as e:
        raise HTTPException(500, detail=f"Gemini API failed: {str(e)}")

    # Save result
    new_analysis = ai_analysis.AIAnalysis(
        document_id=doc.id,
        prompt_template_id=prompt_template_obj.id,
        final_prompt=final_prompt,
        gemini_response=result["text"],
        response_metadata=result["metadata"],
        execution_time_ms=duration_ms
    )
    db.add(new_analysis)
    db.commit()

    return AnalyzeResponse(
        response_text=result["text"],
        model=result["metadata"]["model"],
        tokens_used=result["metadata"]["tokens"],
        cached=False
    )


@router.get("/history", response_model=list[AIAnalysisHistoryOut])
async def get_analysis_history(db: Session = Depends(get_db)):
    return await db_get_history(db)