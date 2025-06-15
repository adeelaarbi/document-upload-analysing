from fastapi import APIRouter

from api import documents, stream, prompt_template, analyzes

router = APIRouter(prefix="/api")

router.include_router(documents.router, tags=["documents"])
router.include_router(stream.router, tags=["stream"])

router.include_router(prompt_template.router, tags=["prompt-template"])

router.include_router(analyzes.router, tags=["analyzes"])