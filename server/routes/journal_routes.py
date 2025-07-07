from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db.database import get_db
from models.journal import Journal
from models.user import User
from models.mood import Mood
from views.journal import JournalCreate, JournalResponse, JournalUpdate
from utilities.auth import get_current_user

router = APIRouter()

# ✅ Create Journal Entry (protected)
@router.post("/", response_model=JournalResponse)
def create_journal(journal: JournalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if journal.mood_linked:
        mood = db.query(Mood).filter(Mood.id == journal.mood_linked).first()
        if not mood:
            raise HTTPException(status_code=404, detail="Linked mood not found")

    new_entry = Journal(
        user_id=current_user.id,
        title=journal.title,
        content=journal.content,
        mood_linked=journal.mood_linked
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

# ✅ Get All Journals (admin-style only — consider disabling or protecting further)
@router.get("/", response_model=list[JournalResponse])
def get_all_journals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Journal).filter(Journal.user_id == current_user.id).all()

# ✅ Get Journals by Current User
@router.get("/user/", response_model=list[JournalResponse])
def get_user_journals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    journals = (
        db.query(Journal)
        .options(joinedload(Journal.mood))
        .filter(Journal.user_id == current_user.id)
        .all()
    )

    return [
        {
            "id": j.id,
            "title": j.title,
            "content": j.content,
            "user_id": j.user_id,
            "mood_linked": j.mood_linked,
            "mood_level": j.mood.mood_level if j.mood else None,
            "created_at": j.created_at,
        }
        for j in journals
    ]

# ✅ Delete Journal (only if belongs to current user)
@router.delete("/{journal_id}", response_model=JournalResponse)
def delete_journal(journal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    journal = db.query(Journal).filter(Journal.id == journal_id, Journal.user_id == current_user.id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found or unauthorized")
    
    db.delete(journal)
    db.commit()
    return journal

# ✅ Update Journal (only if belongs to current user)
@router.put("/{journal_id}", response_model=JournalResponse)
def update_journal(journal_id: int, updated: JournalUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    journal = db.query(Journal).filter(Journal.id == journal_id, Journal.user_id == current_user.id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found or unauthorized")

    journal.title = updated.title
    journal.content = updated.content
    journal.mood_linked = updated.mood_linked
    db.commit()
    db.refresh(journal)
    return journal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db.database import get_db
from models.journal import Journal
from models.user import User
from models.mood import Mood
from views.journal import JournalCreate, JournalResponse, JournalUpdate
from utilities.auth import get_current_user

router = APIRouter()

# ✅ Create Journal Entry (protected)
@router.post("/", response_model=JournalResponse)
def create_journal(journal: JournalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if journal.mood_linked:
        mood = db.query(Mood).filter(Mood.id == journal.mood_linked).first()
        if not mood:
            raise HTTPException(status_code=404, detail="Linked mood not found")

    new_entry = Journal(
        user_id=current_user.id,
        title=journal.title,
        content=journal.content,
        mood_linked=journal.mood_linked
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

# ✅ Get All Journals (admin-style only — consider disabling or protecting further)
@router.get("/", response_model=list[JournalResponse])
def get_all_journals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Journal).filter(Journal.user_id == current_user.id).all()

# ✅ Get Journals by Current User
@router.get("/user/", response_model=list[JournalResponse])
def get_user_journals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    journals = (
        db.query(Journal)
        .options(joinedload(Journal.mood))
        .filter(Journal.user_id == current_user.id)
        .all()
    )

    return [
        {
            "id": j.id,
            "title": j.title,
            "content": j.content,
            "user_id": j.user_id,
            "mood_linked": j.mood_linked,
            "mood_level": j.mood.mood_level if j.mood else None,
            "created_at": j.created_at,
        }
        for j in journals
    ]

# ✅ Delete Journal (only if belongs to current user)
@router.delete("/{journal_id}", response_model=JournalResponse)
def delete_journal(journal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    journal = db.query(Journal).filter(Journal.id == journal_id, Journal.user_id == current_user.id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found or unauthorized")
    
    db.delete(journal)
    db.commit()
    return journal

# ✅ Update Journal (only if belongs to current user)
@router.put("/{journal_id}", response_model=JournalResponse)
def update_journal(journal_id: int, updated: JournalUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    journal = db.query(Journal).filter(Journal.id == journal_id, Journal.user_id == current_user.id).first()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found or unauthorized")

    journal.title = updated.title
    journal.content = updated.content
    journal.mood_linked = updated.mood_linked
    db.commit()
    db.refresh(journal)
    return journal
