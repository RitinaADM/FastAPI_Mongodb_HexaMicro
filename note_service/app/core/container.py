"""
Контейнер зависимостей для инициализации и управления ресурсами приложения.
Реализует паттерн dependency injection для отделения бизнес-логики от инфраструктуры.
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from note_service.app.application.note_manager import NoteManager
from note_service.app.infrastructure.db import MongoNoteRepository
from note_service.app.core.config import Settings

logger = logging.getLogger(__name__)

class Container:
    """
    Контейнер приложения, создающий и предоставляющий зависимости.
    """
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client: AsyncIOMotorClient | None = None
        self.db: AsyncIOMotorDatabase | None = None

    async def get_mongo_client(self) -> tuple[AsyncIOMotorClient, AsyncIOMotorDatabase]:
        """
        Инициализирует и возвращает клиента MongoDB и базу данных.
        """
        if self.client is None:
            self.client = AsyncIOMotorClient(self.settings.mongo_url)
            self.db = self.client[self.settings.database_name]
        return self.client, self.db

    async def get_note_manager(self) -> NoteManager:
        """
        Инициализирует и возвращает экземпляр NoteManager с репозиторием.
        """
        try:
            if self.client is None or self.db is None:
                self.client, self.db = await self.get_mongo_client()
            repository = MongoNoteRepository(self.db)
            return NoteManager(repository)
        except Exception as e:
            logger.error("Failed to initialize NoteManager: %s", e)
            raise

    async def close(self) -> None:
        """
        Закрывает активное соединение с базой данных.
        """
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
