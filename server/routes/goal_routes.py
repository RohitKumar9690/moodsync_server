from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.goal import Goal
from models.user import User
from views.goal import GoalCreate, GoalResponse
from utilities.auth import get_current_user  # your auth dependency

router = APIRouter()

@router.post("/", response_model=GoalResponse)
def create_goal(goal: GoalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_goal = Goal(**goal.dict(), user_id=current_user.id)
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal

@router.get("/", response_model=list[GoalResponse])
def get_all_goals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Return only goals of the logged-in user
    return db.query(Goal).filter(Goal.user_id == current_user.id).all()

@router.get("/user", response_model=list[GoalResponse])
def get_goals_by_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # No user_id param, use current user
    return db.query(Goal).filter(Goal.user_id == current_user.id).all()

@router.put("/{goal_id}", response_model=GoalResponse)
def update_goal(goal_id: int, updated_goal: GoalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this goal")

    for field, value in updated_goal.dict().items():
        setattr(goal, field, value)

    db.commit()
    db.refresh(goal)
    return goal

@router.delete("/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this goal")

    db.delete(goal)
    db.commit()
    return {"message": "Goal deleted successfully"}
