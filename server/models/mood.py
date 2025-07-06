from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class Mood(Base):
    __tablename__ = "mood"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # ✅ Use correct table name "users"
    mood_level = Column(Integer, nullable=False)
    mood_type = Column(String, nullable=False)
    note = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="moods")
    tags = relationship("MoodTag", back_populates="mood", cascade="all, delete-orphan")
    journal_entry = relationship("Journal", back_populates="mood")