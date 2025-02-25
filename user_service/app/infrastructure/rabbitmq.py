import json
import logging
from aio_pika import connect_robust, Message
from user_service.app.domain.interfaces import MessageBroker
from user_service.app.core.config import settings

logger = logging.getLogger(__name__)

class RabbitMQBroker(MessageBroker):
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await connect_robust(settings.rabbitmq_url)
        self.channel = await self.connection.channel()
        logger.info("Connected to RabbitMQ")

    async def consume(self, queue: str, callback):
        if not self.channel:
            await self.connect()
        queue_obj = await self.channel.declare_queue(queue, durable=True)
        async with queue_obj.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await callback(message.body.decode())

    # В rabbitmq.py
    async def publish(self, queue: str, message: dict):
        if not self.channel:
            await self.connect()
        queue_obj = await self.channel.declare_queue(queue, durable=True)
        await self.channel.default_exchange.publish(
            Message(json.dumps(message).encode()),
            routing_key=queue
        )
        logger.info(f"Published message to {queue}: {message}")

    async def close(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()
        logger.info("RabbitMQ connection closed")