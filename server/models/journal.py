from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from db.database import Base

class Journal(Base):
    __tablename__ = "journal"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    mood_linked = Column(Integer, ForeignKey("mood.id"))  # 👈 existing
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="journals")
    mood = relationship("Mood", back_populates="journal_entry")
