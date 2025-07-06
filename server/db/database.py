from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# 👇 Make sure this has ?sslmode=require at the end
DATABASE_URL = os.getenv("DATABASE")

# ✅ Correct engine config for PostgreSQL with SSL
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}  # <- Required for Render
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
