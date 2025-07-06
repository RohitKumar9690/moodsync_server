from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import SessionLocal
from models.mood import Mood
from models.user import User
from views.mood import MoodCreate, MoodResponse, MoodUpdate
from utilities.auth import get_current_user

router = APIRouter()

# ✅ DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Create Mood (only for logged-in user)
@router.post("/", response_model=MoodResponse)
def create_mood(
    mood: MoodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_mood = Mood(
        user_id=current_user.id,
        mood_level=mood.mood_level,
        mood_type=mood.mood_type,
        note=mood.note,
    )
    db.add(new_mood)
    db.commit()
    db.refresh(new_mood)
    return new_mood

# ✅ Get All Moods (for current user only)
@router.get("/", response_model=List[MoodResponse])
def get_all_moods(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Mood).filter(Mood.user_id == current_user.id).all()

# ✅ Get Moods by User ID (protected & validated)
@router.get("/user/{user_id}", response_model=List[MoodResponse])
def get_user_moods(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view these moods")
    return db.query(Mood).filter(Mood.user_id == user_id).all()

# ✅ Update Mood (only if mood belongs to current user)
@router.put("/{mood_id}", response_model=MoodResponse)
def update_mood(
    mood_id: int,
    mood_data: MoodUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    mood = db.query(Mood).filter(Mood.id == mood_id, Mood.user_id == current_user.id).first()
    if not mood:
        raise HTTPException(status_code=404, detail="Mood not found")

    mood.mood_level = mood_data.mood_level
    mood.mood_type = mood_data.mood_type
    mood.note = mood_data.note

    db.commit()
    db.refresh(mood)
    return mood

# ✅ Delete Mood (only if mood belongs to current user)
@router.delete("/{mood_id}")
def delete_mood(
    mood_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    mood = db.query(Mood).filter(Mood.id == mood_id, Mood.user_id == current_user.id).first()
    if not mood:
        raise HTTPException(status_code=404, detail="Mood not found")

    db.delete(mood)
    db.commit()
    return {"detail": "Mood deleted successfully"}
