from sqlalchemy.orm import Session

from models.ai_analysis import AIAnalysis


async def db_get_history(db: Session):
    history = (
        db.query(AIAnalysis)
        .order_by(AIAnalysis.created_at.desc())
        .all()
    )
    return history