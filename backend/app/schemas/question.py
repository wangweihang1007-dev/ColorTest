from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class OptionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    label: str
    content: str
    color_type: str
    sort_order: int

class QuestionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    content: str
    sort_order: int
    options: List[OptionSchema]

class TestSubmission(BaseModel):
    user_id: int
    answers: List[dict] # [{"q_id": 1, "opt_id": 1}, ...]
