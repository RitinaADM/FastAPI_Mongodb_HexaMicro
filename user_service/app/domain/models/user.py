from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    username: str
    email: EmailStr
    password_hash: Optional[str] = None
    role: UserRole = Field(default=UserRole.USER)  # По умолчанию пользователь
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserView(BaseModel):
    id: str
    username: str
    email: str
    role: UserRole
    created_at: datetime
    updated_at: datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.USER  # Опционально, по умолчанию user

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None  # Обновление роли