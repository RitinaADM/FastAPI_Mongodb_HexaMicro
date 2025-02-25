from abc import ABC, abstractmethod
from typing import List, Optional
from note_service.app.domain.models.note import Note

class NoteRepository(ABC):
    @abstractmethod
    async def create_note(self, note: Note) -> Note:
        pass

    @abstractmethod
    async def get_note(self, note_id: str) -> Optional[Note]:
        pass

    @abstractmethod
    async def update_note(self, note_id: str, note_data: dict) -> Optional[Note]:
        pass

    @abstractmethod
    async def delete_note(self, note_id: str) -> bool:
        pass

    @abstractmethod
    async def get_notes_by_user(self, user_id: str) -> List[Note]:
        pass

class MessageBroker(ABC):
    @abstractmethod
    async def publish(self, queue: str, message: dict) -> None:
        """Публикует сообщение в очередь."""
        pass

    @abstractmethod
    async def consume(self, queue: str, callback) -> None:
        """Подписывается на очередь и вызывает callback для каждого сообщения."""
        pass