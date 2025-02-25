import json
import logging
import asyncio
from aio_pika import connect_robust, Message
from note_service.app.domain.interfaces import MessageBroker
from note_service.app.core.config import settings

logger = logging.getLogger(__name__)

class RabbitMQBroker(MessageBroker):
    def __init__(self):
        self.connection = None
        self.channel = None
        self.url = getattr(settings, "rabbitmq_url", "amqp://guest:guest@rabbitmq:5672/")  # Используем settings или default

    async def connect(self, retries=5, delay=5):
        for attempt in range(retries):
            try:
                if not self.connection or self.connection.is_closed:
                    self.connection = await connect_robust(self.url)
                    self.channel = await self.connection.channel()
                    logger.info("Connected to RabbitMQ")
                    return
            except Exception as e:
                logger.warning(f"Failed to connect to RabbitMQ (attempt {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
                else:
                    logger.error("Max retries reached. Could not connect to RabbitMQ.")
                    raise

    async def publish(self, queue: str, message: dict) -> None:
        await self.connect()
        queue_obj = await self.channel.declare_queue(queue, durable=True)
        await self.channel.default_exchange.publish(
            Message(json.dumps(message).encode()),
            routing_key=queue
        )
        logger.info(f"Published message to {queue}: {message}")

    async def consume(self, queue: str, callback) -> None:
        await self.connect()
        queue_obj = await self.channel.declare_queue(queue, durable=True)
        async with queue_obj.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await callback(message.body.decode())

    async def close(self):
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
        logger.info("RabbitMQ connection closed")