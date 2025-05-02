from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.user import User, Task
from schemas.user import UserCreate, UserResponse, UserUpdate, TaskCreate, TaskResponse
from typing import List
from database import get_db
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Create User
@router.post("/users/", response_model=UserResponse,tags=['User'])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, email=user.email.lower(), password=hashed_password, role=user.role, created_by=user.created_by)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ✅ Get All Users
@router.get("/users/", response_model=List[UserResponse],tags=['User'])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# ✅ Extra GET API to fetch a specific user by ID
@router.get("/users/{user_id}",tags=['User'])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ✅ Update User
@router.put("/users/{user_id}", response_model=UserResponse,tags=['User'])
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

# ✅ Delete User
@router.delete("/users/{user_id}",tags=['User'])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# ✅ Create Task
@router.post("/tasks/", response_model=TaskResponse,tags=['Task'])
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(activity=task.activity, status=task.status, user_id=task.user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# ✅ Get All Tasks
@router.get("/tasks/", response_model=List[TaskResponse],tags=['Task'])
def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

# ✅ Get Task by ID
@router.get("/tasks/{task_id}", response_model=TaskResponse,tags=['Task'])
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# ✅ Update Task
@router.put("/tasks/{task_id}", response_model=TaskResponse,tags=['Task'])
def update_task(task_id: int, task_update: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

# ✅ Delete Task
@router.delete("/tasks/{task_id}",tags=['Task'])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
