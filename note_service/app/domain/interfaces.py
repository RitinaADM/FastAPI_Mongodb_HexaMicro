"""
Интерфейсы доменного уровня для Note Service.
Определяет контракт для реализации репозитория заметок.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from note_service.app.domain.models.note import Note

class NoteRepository(ABC):
    @abstractmethod
    async def create_note(self, note: Note) -> Note:
        """
        Сохраняет новую заметку в хранилище.
        """
        pass

    @abstractmethod
    async def get_note(self, note_id: str) -> Optional[Note]:
        """
        Получает заметку по идентификатору.
        """
        pass

    @abstractmethod
    async def update_note(self, note_id: str, note_data: dict) -> Optional[Note]:
        """
        Обновляет данные заметки.
        """
        pass

    @abstractmethod
    async def delete_note(self, note_id: str) -> bool:
        """
        Удаляет заметку по идентификатору.
        """
        pass

    @abstractmethod
    async def get_notes_by_user(self, user_id: str) -> List[Note]:
        """
        Получает список заметок для конкретного пользователя.
        """
        pass
