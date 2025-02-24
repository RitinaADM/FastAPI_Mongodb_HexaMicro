"""
Модели доменного уровня для заметок.
Определяются структуры данных с использованием pydantic.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Note(BaseModel):
    """
    Сущность заметки в системе.
    """
    id: Optional[str] = Field(None, alias='_id')
    title: str
    content: str
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class NoteView(BaseModel):
    """
    Модель представления заметки для API.
    """
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

class NoteCreate(BaseModel):
    """
    Модель для создания новой заметки.
    """
    title: str
    content: str

class NoteUpdate(BaseModel):
    """
    Модель для обновления существующей заметки.
    """
    title: Optional[str] = None
    content: Optional[str] = None
