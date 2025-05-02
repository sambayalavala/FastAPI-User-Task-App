from pydantic import BaseModel, EmailStr
from typing import List, Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"
    created_by: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_by: Optional[int]

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    created_by: Optional[int] = None

class TaskCreate(BaseModel):
    
    activity: str
    status: str
    user_id: int

class TaskResponse(BaseModel):
    id: int
    activity: str
    status: str
    user_id: int

    class Config:
        from_attributes = True

class UserTaskResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    tasks: List[TaskResponse]
