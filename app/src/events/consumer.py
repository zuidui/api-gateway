import aio_pika  # type: ignore
from aio_pika import connect_robust, IncomingMessage
from aio_pika.exceptions import ConnectionClosed, ChannelClosed  # type: ignore
import json
import asyncio

from fastapi import FastAPI

from service.gateway_service import GatewayService

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()


class Consumer:
    def __init__(
        self,
        connection: aio_pika.abc.AbstractRobustConnection,
        exchange_name: str = settings.EXCHANGE_NAME,
    ):
        self.exchange_name = exchange_name
        self.connection = connection
        self.channel = None
        self.exchange = None
        self.queue = None

    async def connect(self):
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            self.exchange_name, aio_pika.ExchangeType.FANOUT, durable=True
        )
        self.queue = await self.channel.declare_queue(exclusive=True, durable=True)
        await self.queue.bind(self.exchange)
        if not self.queue:
            raise ConnectionError(
                f"Failed to declare and bind queue to {self.exchange_name}"
            )

    async def consume(self, app: FastAPI):
        while True:
            try:
                if not self.queue:
                    await self.connect()
                if self.queue:
                    await self.queue.consume(
                        lambda message: self._callback(app, message), no_ack=False
                    )
                    log.info(f"Starting to consume messages from {self.exchange_name}")
                    break
            except (ConnectionClosed, ChannelClosed) as e:
                log.error(f"Connection closed, retrying... {e}")
                await asyncio.sleep(5)
                await self.connect()

    async def _callback(self, app: FastAPI, message: IncomingMessage):
        async with message.process():
            try:
                message_data = json.loads(message.body.decode("utf-8"))
                log.info(f"Received message: {message_data}")
                await GatewayService.handle_message(app, message_data)
            except json.JSONDecodeError as e:
                log.error(
                    f"Failed to decode message: {message.body.decode('utf-8')} - Error: {e}"
                )

    async def close(self):
        if self.connection:
            await self.connection.close()
            log.info("Connection closed")


async def start_consumer(loop, app: FastAPI) -> Consumer:
    connection = await connect_robust(
        host=settings.BROKER_HOST,
        port=settings.BROKER_PORT,
        loop=loop,
        heartbeat=settings.BROKER_HEARTBEAT,
        connection_attempts=settings.BROKER_CONNECTION_ATTEMPTS,
        connection_timeout=settings.BROKER_CONNECTION_TIMEOUT,
        attempt_delay=settings.BROKER_ATTEMPT_DELAY,
    )
    consumer = Consumer(connection)
    await consumer.connect()
    asyncio.create_task(consumer.consume(app))
    return consumer
