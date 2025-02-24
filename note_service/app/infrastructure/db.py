"""
Реализация репозитория заметок для MongoDB.
Обеспечивает CRUD-операции для сущности Note с использованием библиотеки motor.
"""

from typing import List, Optional
from bson.objectid import ObjectId, InvalidId
from datetime import datetime
from note_service.app.domain.models.note import Note
from note_service.app.domain.interfaces import NoteRepository
import logging

logger = logging.getLogger(__name__)

class MongoNoteRepository(NoteRepository):
    """
    Репозиторий для работы с заметками в MongoDB.
    """
    def __init__(self, db) -> None:
        """
        Инициализирует репозиторий с заданной базой данных.
        """
        self.collection = db.get_collection("notes")

    async def init_indexes(self) -> None:
        """
        Создаёт индексы в коллекции заметок.
        """
        await self.collection.create_index("user_id")
        logger.info("Note indexes initialized")

    async def create_note(self, note: Note) -> Note:
        """
        Вставляет новую заметку в базу данных.
        """
        note_dict = note.dict(exclude={"id"})
        result = await self.collection.insert_one(note_dict)
        note.id = str(result.inserted_id)
        return note

    async def get_note(self, note_id: str) -> Optional[Note]:
        """
        Получает заметку по идентификатору.
        """
        try:
            object_id = ObjectId(note_id)
        except (InvalidId, TypeError):
            logger.debug("Invalid note_id format: %s", note_id)
            return None
        document = await self.collection.find_one({"_id": object_id})
        if document:
            document["_id"] = str(document["_id"])
            return Note.parse_obj(document)
        return None

    async def update_note(self, note_id: str, note_data: dict) -> Optional[Note]:
        """
        Обновляет существующую заметку.
        """
        try:
            object_id = ObjectId(note_id)
        except (InvalidId, TypeError):
            logger.debug("Invalid note_id format for update: %s", note_id)
            return None
        update_command = {"$set": {**note_data, "updated_at": datetime.utcnow()}}
        result = await self.collection.update_one({"_id": object_id}, update_command)
        if result.matched_count == 0:
            return None
        document = await self.collection.find_one({"_id": object_id})
        if document:
            document["_id"] = str(document["_id"])
            return Note.parse_obj(document)
        return None

    async def delete_note(self, note_id: str) -> bool:
        """
        Удаляет заметку по идентификатору.
        """
        try:
            object_id = ObjectId(note_id)
        except (InvalidId, TypeError):
            logger.debug("Invalid note_id format for deletion: %s", note_id)
            return False
        result = await self.collection.delete_one({"_id": object_id})
        return result.deleted_count > 0

    async def get_notes_by_user(self, user_id: str) -> List[Note]:
        """
        Получает все заметки для заданного пользователя.
        """
        notes: List[Note] = []
        cursor = self.collection.find({"user_id": user_id})
        async for document in cursor:
            document["_id"] = str(document["_id"])
            notes.append(Note.parse_obj(document))
        return notes
