import json
import asyncio
import aio_pika
import aioredis
from bet_maker.src.schemas.event import EventSchema

RABBITMQ_URL = "amqp://guest:guest@betting_rabbitmq/"
REDIS_URL = "redis://betting_redis:6379"
CACHE_TTL = 10  

class EventMessagingService:
    def __init__(self):
        self.redis = None

    async def setup_redis(self):
        self.redis = await aioredis.from_url(REDIS_URL, decode_responses=True)

    async def request_events(self):
        if self.redis is None:
            await self.setup_redis()

        cached_events = await self.redis.get("cached_events")
        if cached_events:
            print("[⚡] Отдаём события из кеша")
            return [EventSchema(**event) for event in json.loads(cached_events)]

        connection = await aio_pika.connect_robust(RABBITMQ_URL)
        async with connection:
            channel = await connection.channel()

            exchange = await channel.declare_exchange("event_requests", aio_pika.ExchangeType.DIRECT, durable=True)
            response_exchange = await channel.declare_exchange("event_responses", aio_pika.ExchangeType.DIRECT, durable=True)
            response_queue = await channel.declare_queue("event_responses", durable=True)
            await response_queue.bind(response_exchange, routing_key="event_responses")

            print("[🔄] Отправляем запрос в RabbitMQ...")
            await exchange.publish(
                aio_pika.Message(
                    body=json.dumps({"action": "get_events"}).encode(),
                    reply_to=response_queue.name
                ),
                routing_key="get_events"
            )

            future = asyncio.get_event_loop().create_future()

            async def on_message(message: aio_pika.IncomingMessage):
                async with message.process():
                    response_data = json.loads(message.body)
                    print(f"[✅] Получен ответ в bet-maker: {response_data}")
                    await self.redis.setex("cached_events", CACHE_TTL, json.dumps(response_data))
                    future.set_result([EventSchema(**event) for event in response_data])

            await response_queue.consume(on_message)

            return await asyncio.wait_for(future, timeout=20)
