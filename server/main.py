from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from db.database import engine, Base
from routes import user_routes, mood_routes, mood_tag_routes, journal_routes, goal_routes, habit_routes

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB setup
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
except Exception as e:
    print("❌ Error creating tables:", e)

# Routers
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(mood_routes.router, prefix="/moods", tags=["Moods"])
app.include_router(mood_tag_routes.router, prefix="/tags", tags=["Tags"])
app.include_router(journal_routes.router, prefix="/journals", tags=["Journals"])
app.include_router(goal_routes.router, prefix="/goals", tags=["Goals"])
app.include_router(habit_routes.router, prefix="/habits", tags=["Habits"])

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
