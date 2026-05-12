from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from ..core.database import get_db
from ..models.database import Question, QuestionOption, PersonalityConfig
from ..schemas.question import QuestionSchema

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("/", response_model=List[QuestionSchema])
async def read_questions(db: AsyncSession = Depends(get_db)):
    # Use selectinload to eagerly load options
    result = await db.execute(
        select(Question).options(selectinload(Question.options)).order_by(Question.sort_order)
    )
    questions = result.scalars().all()
    return questions

@router.get("/config/{color_type}")
async def get_personality_config(color_type: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PersonalityConfig).where(PersonalityConfig.color_type == color_type)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    return config
