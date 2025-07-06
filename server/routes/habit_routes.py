from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from db.database import get_db
from models.habits import HabitDefinition, HabitEntry
from views.habit import (
    HabitDefCreate, HabitDefResponse,
    HabitCreateEntry, HabitEntryResponse,
    HabitProgress, HabitUpdate
)
from models.user import User
from utilities.auth import get_current_user

router = APIRouter()

# ==================== Habit Definition Routes ====================

@router.post("/", response_model=HabitDefResponse)
def create_habit(
    def_data: HabitDefCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = HabitDefinition(**def_data.dict(), user_id=current_user.id)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


@router.get("/", response_model=List[HabitDefResponse])
def get_all_habits(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(HabitDefinition).filter(HabitDefinition.user_id == current_user.id).all()


@router.get("/{habit_id}", response_model=HabitDefResponse)
def get_habit_by_id(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = db.query(HabitDefinition).filter(HabitDefinition.id == habit_id).first()
    if not habit or habit.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Habit not found")

    entries = habit.entries.all() if hasattr(habit.entries, 'all') else habit.entries

    total_days = (habit.end_date - habit.start_date).days + 1
    completed_days = sum(1 for e in entries if e.completed)
    skipped_days = sum(1 for e in entries if e.skipped)
    remaining_days = total_days - (completed_days + skipped_days)

    progress = HabitProgress(
        total_days=total_days,
        completed_days=completed_days,
        skipped_days=skipped_days,
        remaining_days=remaining_days,
        completion_percentage=(completed_days / total_days) * 100 if total_days else 0,
        skip_percentage=(skipped_days / total_days) * 100 if total_days else 0,
    )

    response = HabitDefResponse.from_orm(habit)
    response.entries = entries
    response.progress = progress
    return response


@router.get("/user/{user_id}", response_model=List[HabitDefResponse])
def get_habits_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    habits = db.query(HabitDefinition).filter(HabitDefinition.user_id == user_id).all()
    result = []

    for habit in habits:
        entries = habit.entries.all() if hasattr(habit.entries, 'all') else habit.entries
        total_days = (habit.end_date - habit.start_date).days + 1
        completed_days = sum(1 for e in entries if e.completed)
        skipped_days = sum(1 for e in entries if e.skipped)
        remaining_days = total_days - (completed_days + skipped_days)

        progress = HabitProgress(
            total_days=total_days,
            completed_days=completed_days,
            skipped_days=skipped_days,
            remaining_days=remaining_days,
            completion_percentage=(completed_days / total_days) * 100 if total_days else 0,
            skip_percentage=(skipped_days / total_days) * 100 if total_days else 0
        )

        habit_response = HabitDefResponse.from_orm(habit)
        habit_response.progress = progress
        result.append(habit_response)

    return result


@router.put("/update/{habit_id}", response_model=HabitDefResponse)
def update_habit(
    habit_id: int,
    updated: HabitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = db.query(HabitDefinition).filter(HabitDefinition.id == habit_id).first()
    if not habit or habit.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Habit not found")

    for key, value in updated.dict(exclude_unset=True).items():
        setattr(habit, key, value)

    db.commit()
    db.refresh(habit)
    return habit


@router.delete("/{habit_id}")
def delete_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = db.query(HabitDefinition).filter(HabitDefinition.id == habit_id).first()
    if not habit or habit.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Habit not found")

    db.delete(habit)
    db.commit()
    return {"detail": "Habit deleted successfully"}


# ==================== Habit Entry Routes ====================

@router.post("/entry", response_model=HabitEntryResponse)
def add_habit_entry(
    entry: HabitCreateEntry,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = db.query(HabitDefinition).filter(HabitDefinition.id == entry.habit_id).first()
    if not habit or habit.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Habit not found")

    existing = db.query(HabitEntry).filter(
        HabitEntry.habit_id == entry.habit_id,
        HabitEntry.date == entry.date
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Entry for this date already exists")

    new_entry = HabitEntry(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@router.patch("/entry/{entry_id}/complete", response_model=HabitEntryResponse)
def mark_completed(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = db.query(HabitEntry).filter(HabitEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    if entry.habit.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    entry.completed = True
    entry.skipped = False
    db.commit()
    db.refresh(entry)
    return entry


@router.patch("/entry/{entry_id}/skip", response_model=HabitEntryResponse)
def mark_skipped(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = db.query(HabitEntry).filter(HabitEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    if entry.habit.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    entry.completed = False
    entry.skipped = True
    db.commit()
    db.refresh(entry)
    return entry
