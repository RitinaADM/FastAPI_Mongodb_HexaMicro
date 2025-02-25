import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from note_service.app.application.note_manager import NoteManager
from note_service.app.infrastructure.db import MongoNoteRepository
from note_service.app.infrastructure.rabbitmq import RabbitMQBroker
from note_service.app.core.config import Settings
from note_service.app.domain.interfaces import MessageBroker

logger = logging.getLogger(__name__)

class Container:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client: AsyncIOMotorClient | None = None
        self.db: AsyncIOMotorDatabase | None = None
        self.broker: MessageBroker | None = None

    async def get_mongo_client(self) -> tuple[AsyncIOMotorClient, AsyncIOMotorDatabase]:
        if self.client is None:
            self.client = AsyncIOMotorClient(self.settings.mongo_url)
            self.db = self.client[self.settings.database_name]
        return self.client, self.db

    async def get_message_broker(self) -> MessageBroker:
        if self.broker is None:
            self.broker = RabbitMQBroker()
            await self.broker.connect()
        return self.broker

    async def get_note_manager(self) -> NoteManager:
        if self.client is None or self.db is None:
            self.client, self.db = await self.get_mongo_client()
        repository = MongoNoteRepository(self.db)
        broker = await self.get_message_broker()
        manager = NoteManager(repository, broker)  # Передаем брокер как зависимость
        asyncio.create_task(self.start_consuming(manager))
        return manager

    async def start_consuming(self, manager: NoteManager):
        async def callback(body: str):
            from json import loads
            message = loads(body)
            event_type = message.get("event_type")
            user_id = message.get("user_id")
            if event_type == "user.created":
                from note_service.app.domain.models.note import NoteCreate
                welcome_note = NoteCreate(title="Welcome!", content="Thanks for joining us!")
                await manager.create_note(welcome_note, user_id)
                logger.info(f"Created welcome note for user: {user_id}")
            elif event_type == "user.deleted":
                notes = await manager.get_notes_by_user(user_id)
                for note in notes:
                    await manager.delete_note(note.id)
                logger.info(f"Deleted all notes for user: {user_id}")
        broker = await self.get_message_broker()
        await broker.consume("user.events", callback)

    async def close(self) -> None:
        if self.client:
            self.client.close()
        if self.broker:
            await self.broker.close()
        logger.info("MongoDB connection closed")