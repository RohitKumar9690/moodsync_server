from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MoodCreate(BaseModel):
    user_id: int
    mood_level: int
    mood_type: str
    note: Optional[str]

class MoodUpdate(BaseModel):
    mood_level: int
    mood_type: str
    note: Optional[str]

class MoodResponse(BaseModel):
    id: int
    user_id: int
    mood_level: int
    mood_type: str
    note: Optional[str]
    created_at: datetime  

    class Config:
        orm_mode = True
