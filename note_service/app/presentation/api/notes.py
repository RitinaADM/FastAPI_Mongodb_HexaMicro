"""
API-эндпоинты для управления заметками.
Реализует CRUD-операции, используя зависимости для получения менеджера заметок и текущего пользователя.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from time import time
from note_service.app.application.note_manager import NoteManager
from note_service.app.core.dependencies import get_current_user, get_note_manager
from note_service.app.domain.models.note import Note, NoteView, NoteCreate, NoteUpdate
from note_service.app.domain.models.user import User
from note_service.app.core.metrics import REQUEST_COUNT, REQUEST_LATENCY

router = APIRouter(prefix="/api/notes", tags=["notes"])

@router.post("/", response_model=NoteView)
async def create_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    manager: NoteManager = Depends(get_note_manager)
) -> NoteView:
    """
    Создаёт новую заметку для текущего пользователя.
    """
    start_time = time()
    REQUEST_COUNT.labels(method="POST", endpoint="/api/notes/").inc()
    try:
        created_note = await manager.create_note(note, current_user.id)
        return created_note
    finally:
        elapsed = time() - start_time
        REQUEST_LATENCY.labels(endpoint="/api/notes/").observe(elapsed)

@router.get("/", response_model=List[NoteView])
async def list_notes(
    current_user: User = Depends(get_current_user),
    manager: NoteManager = Depends(get_note_manager)
) -> List[NoteView]:
    """
    Возвращает список всех заметок текущего пользователя.
    """
    return await manager.get_notes_by_user(current_user.id)

@router.get("/{note_id}", response_model=NoteView)
async def get_note(
    note_id: str,
    current_user: User = Depends(get_current_user),
    manager: NoteManager = Depends(get_note_manager)
) -> NoteView:
    """
    Получает заметку по идентификатору.
    """
    note = await manager.get_note(note_id)
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this note")
    return note

@router.put("/{note_id}", response_model=NoteView)
async def update_note(
    note_id: str,
    note_update: NoteUpdate,
    current_user: User = Depends(get_current_user),
    manager: NoteManager = Depends(get_note_manager)
) -> NoteView:
    """
    Обновляет существующую заметку.
    """
    note = await manager.get_note(note_id)
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this note")
    updated_note = await manager.update_note(note_id, note_update)
    return updated_note

@router.delete("/{note_id}", response_model=dict)
async def delete_note(
    note_id: str,
    current_user: User = Depends(get_current_user),
    manager: NoteManager = Depends(get_note_manager)
) -> dict:
    """
    Удаляет заметку по её идентификатору.
    """
    note = await manager.get_note(note_id)
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this note")
    success = await manager.delete_note(note_id)
    return {"success": success}
