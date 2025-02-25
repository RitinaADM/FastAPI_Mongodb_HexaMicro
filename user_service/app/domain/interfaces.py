from abc import ABC, abstractmethod
from typing import List, Optional
from user_service.app.domain.models.user import User

class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_user(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def update_user(self, user_id: str, user_data: dict) -> Optional[User]:
        pass

    @abstractmethod
    async def delete_user(self, user_id: str) -> bool:
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def list_users(self) -> List[User]:
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