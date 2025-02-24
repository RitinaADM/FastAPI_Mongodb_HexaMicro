"""
Слой бизнес-логики для управления заметками.
Класс NoteManager реализует операции создания, получения, обновления и удаления заметок,
используя репозиторий (интерфейс) для работы с хранилищем.
"""

import logging
from typing import List
from fastapi import HTTPException
from note_service.app.domain.models.note import Note, NoteCreate, NoteUpdate
from note_service.app.domain.interfaces import NoteRepository

logger = logging.getLogger(__name__)

class NoteManager:
    """
    Менеджер заметок, отвечающий за выполнение бизнес-операций над заметками.
    """
    def __init__(self, repository: NoteRepository) -> None:
        self.repository = repository

    async def create_note(self, note: NoteCreate, user_id: str) -> Note:
        """
        Создаёт новую заметку для пользователя.
        """
        logger.info("Creating note", extra={"context": f"user_id={user_id}, title={note.title}"})
        try:
            new_note = Note(title=note.title, content=note.content, user_id=user_id)
            return await self.repository.create_note(new_note)
        except Exception as e:
            logger.error("Failed to create note: %s", str(e), extra={"context": f"user_id={user_id}"})
            raise HTTPException(status_code=500, detail="Failed to create note") from e

    async def get_note(self, note_id: str) -> Note:
        """
        Получает заметку по её идентификатору.
        """
        logger.debug("Fetching note", extra={"context": f"note_id={note_id}"})
        note = await self.repository.get_note(note_id)
        if not note:
            logger.warning("Note not found", extra={"context": f"note_id={note_id}"})
            raise HTTPException(status_code=404, detail="Note not found")
        return note

    async def update_note(self, note_id: str, note_update: NoteUpdate) -> Note:
        """
        Обновляет существующую заметку.
        """
        logger.info("Updating note", extra={"context": f"note_id={note_id}"})
        updated_note = await self.repository.update_note(note_id, note_update.dict(exclude_unset=True))
        if not updated_note:
            logger.warning("Note not found", extra={"context": f"note_id={note_id}"})
            raise HTTPException(status_code=404, detail="Note not found")
        return updated_note

    async def delete_note(self, note_id: str) -> bool:
        """
        Удаляет заметку по её идентификатору.
        """
        logger.info("Deleting note", extra={"context": f"note_id={note_id}"})
        success = await self.repository.delete_note(note_id)
        if not success:
            logger.warning("Note not found", extra={"context": f"note_id={note_id}"})
            raise HTTPException(status_code=404, detail="Note not found")
        return success

    async def get_notes_by_user(self, user_id: str) -> List[Note]:
        """
        Получает список заметок, принадлежащих указанному пользователю.
        """
        logger.debug("Fetching notes for user", extra={"context": f"user_id={user_id}"})
        notes = await self.repository.get_notes_by_user(user_id)
        logger.info("Found %d notes for user", len(notes), extra={"context": f"user_id={user_id}"})
        return notes
