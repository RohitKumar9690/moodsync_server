from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class MoodTag(Base):
    __tablename__ = "mood_tags"

    id = Column(Integer, primary_key=True, index=True)
    mood_id = Column(Integer, ForeignKey("mood.id"))
    tag = Column(String, nullable=False)

    mood = relationship("Mood", back_populates="tags")
