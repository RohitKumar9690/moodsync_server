from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.mood_tag import MoodTag
from models.mood import Mood
from views.mood_tag import MoodTagCreate, MoodTagResponse

router = APIRouter()

@router.post("/", response_model=MoodTagResponse)
def create_tag(tag_data: MoodTagCreate, db: Session = Depends(get_db)):
    mood = db.query(Mood).filter(Mood.id == tag_data.mood_id).first()
    if not mood:
        raise HTTPException(status_code=404, detail="Mood not found")
    
    tag = MoodTag(**tag_data.dict())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

@router.get("/mood/{mood_id}", response_model=list[MoodTagResponse])
def get_tags_for_mood(mood_id: int, db: Session = Depends(get_db)):
    return db.query(MoodTag).filter(MoodTag.mood_id == mood_id).all()
