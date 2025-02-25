import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from user_service.app.application.user_manager import UserManager
from user_service.app.infrastructure.db import MongoUserRepository
from user_service.app.infrastructure.rabbitmq import RabbitMQBroker
from user_service.app.core.config import Settings
import threading
import json
from user_service.app.domain.models.user import UserCreate

logger = logging.getLogger(__name__)


class Container:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client: AsyncIOMotorClient | None = None
        self.db: AsyncIOMotorDatabase | None = None
        self.broker: RabbitMQBroker | None = None

    async def get_mongo_client(self) -> tuple[AsyncIOMotorClient, AsyncIOMotorDatabase]:
        if self.client is None:
            self.client = AsyncIOMotorClient(self.settings.mongo_url)
            self.db = self.client[self.settings.database_name]
        return self.client, self.db

    async def get_user_manager(self) -> UserManager:
        if self.client is None or self.db is None:
            self.client, self.db = await self.get_mongo_client()
        if self.broker is None:
            self.broker = RabbitMQBroker()
            await self.broker.connect()
        repository = MongoUserRepository(self.db)
        manager = UserManager(repository)
        asyncio.create_task(self.start_consuming(manager))
        return manager

    async def start_consuming(self, manager):
        async def callback(body: str):
            message = json.loads(body)
            user_create = UserCreate(username=message["username"], email=message["email"], password=message["password"])
            try:
                await manager.register_user(user_create)
                logger.info(f"User registered from event: {message}")
            except Exception as e:
                logger.error(f"Failed to register user from event: {e}")
        await self.broker.consume("user.created", callback)

    async def close(self) -> None:
        if self.client:
            self.client.close()
        if self.broker:
            self.broker.close()
        logger.info("Resources closed")