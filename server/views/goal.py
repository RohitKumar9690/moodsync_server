from pydantic import BaseModel
from datetime import datetime, date

class GoalCreate(BaseModel):
    title: str
    description: str = ""
    completed: bool = False
    target_date: date | None = None

class GoalResponse(GoalCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
