"""
Тесты для класса NoteManager.
Используется мок-репозиторий для имитации работы с базой данных.
"""

import pytest
from fastapi import HTTPException
from note_service.app.application.note_manager import NoteManager
from note_service.app.domain.models.note import NoteCreate, Note

class MockNoteRepository:
    """
    Мок-реализация репозитория заметок для тестирования.
    """
    async def create_note(self, note: Note) -> Note:
        note.id = "mock_id"
        return note

    async def get_note(self, note_id: str) -> Note | None:
        if note_id == "mock_id":
            return Note(id="mock_id", title="Test", content="Content", user_id="user123")
        return None

    async def update_note(self, note_id: str, note_data: dict) -> Note | None:
        if note_id == "mock_id":
            return Note(id="mock_id", title=note_data.get("title", "Test"), content=note_data.get("content", "Content"), user_id="user123")
        return None

    async def delete_note(self, note_id: str) -> bool:
        return note_id == "mock_id"

    async def get_notes_by_user(self, user_id: str) -> list[Note]:
        return [Note(id="mock_id", title="Test", content="Content", user_id=user_id)]

@pytest.mark.asyncio
async def test_create_note():
    repo = MockNoteRepository()
    manager = NoteManager(repo)
    note_create = NoteCreate(title="Test", content="Content")
    user_id = "user123"

    note = await manager.create_note(note_create, user_id)

    assert note.id == "mock_id"
    assert note.title == "Test"
    assert note.content == "Content"
    assert note.user_id == "user123"

@pytest.mark.asyncio
async def test_get_note_success():
    repo = MockNoteRepository()
    manager = NoteManager(repo)

    note = await manager.get_note("mock_id")

    assert note is not None
    assert note.id == "mock_id"
    assert note.title == "Test"

@pytest.mark.asyncio
async def test_get_note_not_found():
    repo = MockNoteRepository()
    manager = NoteManager(repo)

    with pytest.raises(HTTPException) as exc_info:
        await manager.get_note("invalid_id")
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_get_notes_by_user():
    repo = MockNoteRepository()
    manager = NoteManager(repo)
    notes = await manager.get_notes_by_user("user123")
    assert len(notes) == 1
    assert notes[0].title == "Test"
