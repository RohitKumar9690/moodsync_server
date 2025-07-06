from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.user import User
from views.user import UserCreate, UserResponse, UserUpdate
from typing import List
from datetime import datetime
from utilities.auth import create_access_token,get_current_user
from utilities.pswdhash import hash_pwd,verify_pwd
router = APIRouter()

# === DB DEPENDENCY ===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === CREATE USER ===
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_pwd(user.password),
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# === GET ALL USERS ===
@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db) 
    ,    current_user: User = Depends(get_current_user)
):
    return db.query(User).all()

# === LOGIN USER ===
@router.post("/login")
def login_user(email: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_pwd(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"user_id": user.id})
    print(access_token)
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }
# === UPDATE USER ===
# @router.put("/{user_id}", response_model=UserResponse)
# def update_user(user_id: int, updated: UserUpdate, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if updated.name:
#         user.name = updated.name
#     if updated.email:
#         user.email = updated.email
#     if updated.password:
#         user.password = hash_pwd(updated.password)

#     db.commit()
#     db.refresh(user)
#     return user

# === DELETE USER ===
@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db) ,current_user :int=Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return user

@router.post("/logout")
def logout_user():
    return {"message": "Logged out successfully"}

