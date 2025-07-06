# server/views/journal.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JournalCreate(BaseModel):
    # user_id: int
    title: str
    content: str
    mood_linked: Optional[int] = None

class JournalUpdate(BaseModel):
    title: str
    content: str
    mood_linked: Optional[int] = None

class JournalResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    mood_linked: Optional[int]
    mood_level: Optional[int] 
    created_at: datetime



    class Config:
        orm_mode = True
