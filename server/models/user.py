from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    moods = relationship("Mood", back_populates="user", cascade="all, delete-orphan")
    journals = relationship("Journal", back_populates="user")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    habit_entries = relationship("HabitEntry", back_populates="user")
    habit_definitions = relationship("HabitDefinition", back_populates="user")
