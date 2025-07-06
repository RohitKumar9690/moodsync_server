from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.database import Base

class HabitDefinition(Base):
    __tablename__ = "habit_definitions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    type = Column(String)  # e.g., good / bad / quit
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # models.py
    entries = relationship("HabitEntry", back_populates="habit", cascade="all, delete-orphan")
    user = relationship("User", back_populates="habit_definitions")


class HabitEntry(Base):
    __tablename__ = "habit_entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    habit_id = Column(Integer, ForeignKey("habit_definitions.id"))
    date = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)
    skipped = Column(Boolean, default=False)

    habit = relationship("HabitDefinition", back_populates="entries")
    user = relationship("User", back_populates="habit_entries")
