from pydantic import BaseModel
from typing import Optional

class MoodTagCreate(BaseModel):
    mood_id: int
    tag: str

class MoodTagResponse(MoodTagCreate):
    id: int

    class Config:
        orm_mode = True
