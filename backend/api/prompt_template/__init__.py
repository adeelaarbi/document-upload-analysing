from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.prompt_template.schemas import PromptTemplateOut, PromptTemplateUpdate, PromptTemplateCreate
from api.prompt_template.service import db_get_prompt_templates, db_get_prompt_template, db_update_prompt_template, \
    db_delete_prompt_template, db_create_prompt_template
from database import get_db

router = APIRouter(prefix="/prompt-templates")

@router.get("", response_model=list[PromptTemplateOut])
async def get_prompt_templates(db: Session = Depends(get_db)):
    return db_get_prompt_templates(db)

@router.get("/{prompt_template_id}", response_model=PromptTemplateOut)
async def get_prompt_template(prompt_template_id: UUID, db: Session = Depends(get_db)):
    return db_get_prompt_template(prompt_template_id, db)

@router.post("", response_model=PromptTemplateOut)
async def create_prompt_template(prompt_template: PromptTemplateCreate, db: Session = Depends(get_db)):
    return db_create_prompt_template(prompt_template, db)

@router.put("/{prompt_template_id}", response_model=PromptTemplateOut)
async def update_prompt_template(prompt_template_id: UUID, prompt_template: PromptTemplateUpdate, db: Session = Depends(get_db)):
    return db_update_prompt_template(prompt_template_id, prompt_template, db)

@router.delete("/{prompt_template_id}", status_code=204)
async def delete_prompt_template(prompt_template_id: UUID, db: Session = Depends(get_db)):
    deleted = db_delete_prompt_template(prompt_template_id, db)
    return {"message": f"Prompt template {prompt_template_id} deleted."} if deleted else {"message": "Prompt template not found."}