from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import json
from ..core.database import get_db
from ..models.database import TestRecord, QuestionOption
from ..schemas.question import TestSubmission

router = APIRouter(prefix="/records", tags=["records"])

@router.post("/submit")
async def submit_test(submission: TestSubmission, db: AsyncSession = Depends(get_db)):
    # Calculate scores
    scores = {"red": 0, "blue": 0, "yellow": 0, "green": 0}
    
    # Extract option IDs for calculation
    option_ids = [a['opt_id'] for a in submission.answers]
    
    result = await db.execute(
        select(QuestionOption).where(QuestionOption.id.in_(option_ids))
    )
    selected_options = result.scalars().all()
    
    for opt in selected_options:
        scores[opt.color_type] += opt.score_value
        
    # Determine final color (the one with the max score)
    final_color = max(scores, key=scores.get)
    
    # Save record
    new_record = TestRecord(
        user_id=submission.user_id,
        answers_json=json.dumps(submission.answers),
        score_detail=json.dumps(scores),
        final_color=final_color
    )
    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)
    
    return {
        "record_id": new_record.id,
        "scores": scores,
        "final_color": final_color
    }
