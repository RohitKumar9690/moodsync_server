from pydantic import BaseModel
from datetime import date
from typing import List, Optional


# ====== Habit Entry Schema ======
class HabitEntryBase(BaseModel):
    date: date
    completed: bool = False
    skipped: bool = False

    class Config:
        from_attributes = True


class HabitCreateEntry(HabitEntryBase):
    habit_id: int


class HabitEntryResponse(HabitEntryBase):
    id: int
    habit_id: int

    class Config:
        from_attributes = True


# ====== Habit Definition Schema ======
class HabitDefBase(BaseModel):
    title: str
    type: str  # good / bad / quit
    start_date: date
    end_date: date

    class Config:
        from_attributes = True


class HabitDefCreate(HabitDefBase):
    # user_id: int
    pass


class HabitProgress(BaseModel):
    total_days: int
    completed_days: int
    skipped_days: int
    remaining_days: int
    completion_percentage: float
    skip_percentage: float

    class Config:
        from_attributes = True


class HabitDefResponse(HabitDefBase):
    id: int
    user_id: int
    entries: List[HabitEntryResponse] = []
    progress: Optional[HabitProgress] = None

class HabitUpdate(BaseModel):
    title: Optional[str]
    type: Optional[str]  # good / bad / quit
    start_date: Optional[date]
    end_date: Optional[date]

    class Config:
        from_attributes = True
