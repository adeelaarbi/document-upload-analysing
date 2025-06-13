from fastapi import HTTPException
from uuid import UUID

from sqlalchemy.orm import Session

from models.prompt_template import PromptTemplate


def db_create_prompt_template(prompt_template, db: Session):
    prompt_template_obj = PromptTemplate(**prompt_template.dict())
    db.add(prompt_template_obj)
    db.commit()
    db.refresh(prompt_template_obj)
    return prompt_template_obj

def db_get_prompt_templates(db: Session):
    return db.query(PromptTemplate).all()

def db_get_prompt_template(prompt_template_id: UUID, db: Session):
    prompt = db.query(PromptTemplate).filter(PromptTemplate.id == prompt_template_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt template not found.")
    return prompt

def db_update_prompt_template(prompt_template_id: UUID, prompt_template, db: Session):
    prompt = db.query(PromptTemplate).filter(PromptTemplate.id == prompt_template_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt template not found.")
    for key, value in prompt_template.dict(exclude_unset=True).items():
        setattr(prompt, key, value)
    db.commit()
    db.refresh(prompt)
    return prompt

def db_delete_prompt_template(prompt_template_id: UUID, db: Session):
    prompt = db.query(PromptTemplate).filter(PromptTemplate.id == prompt_template_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt template not found.")
    db.delete(prompt)
    db.commit()
    return True