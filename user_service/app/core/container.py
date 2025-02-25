import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from user_service.app.application.user_manager import UserManager
from user_service.app.infrastructure.db import MongoUserRepository
from user_service.app.infrastructure.rabbitmq import RabbitMQBroker
from user_service.app.core.config import Settings
from user_service.app.domain.interfaces import MessageBroker

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

    async def get_user_manager(self) -> UserManager:
        if self.client is None or self.db is None:
            self.client, self.db = await self.get_mongo_client()
        repository = MongoUserRepository(self.db)
        broker = await self.get_message_broker()
        manager = UserManager(repository, broker)  # Передаем брокер как зависимость
        asyncio.create_task(self.start_consuming(manager))
        return manager

    async def start_consuming(self, manager: UserManager):
        async def callback(body: str):
            logger.info(f"Received message: {body}")  # Заглушка для потребления
        broker = await self.get_message_broker()
        await broker.consume("user.events", callback)

    async def close(self) -> None:
        if self.client:
            self.client.close()
        if self.broker:
            await self.broker.close()
        logger.info("Resources closed")