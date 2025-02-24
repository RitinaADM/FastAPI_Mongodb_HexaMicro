"""
Определение зависимостей для FastAPI.
Здесь предоставляются функции для получения текущего пользователя и менеджера заметок.
"""

from fastapi import Depends, HTTPException, Request
from note_service.app.application.note_manager import NoteManager
from note_service.app.domain.models.user import User

async def get_current_user() -> User:
    """
    Возвращает текущего пользователя (stub-реализация).
    В продакшене здесь должна быть реализована аутентификация.
    """
    return User(id="test_user_id", username="test_user")

def get_note_manager(request: Request) -> NoteManager:
    """
    Извлекает NoteManager из состояния приложения.
    """
    manager: NoteManager | None = getattr(request.app.state, "note_manager", None)
    if manager is None:
        raise HTTPException(status_code=500, detail="NoteManager not initialized")
    return manager
