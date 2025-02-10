import json
import aio_pika
import asyncio
from line_provider.src.services.event import EventService
from line_provider.src.core.dependecies import repo

RABBITMQ_URL = "amqp://guest:guest@betting_rabbitmq/"

async def event_request_handler():
    try:
        print("[🚀] Запуск обработчика событий...")

        connection = await aio_pika.connect_robust(RABBITMQ_URL)
        
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange("event_requests", aio_pika.ExchangeType.DIRECT, durable=True)
            queue = await channel.declare_queue("get_events", durable=True)
            await queue.bind(exchange, routing_key="get_events")

            async def process_request(message: aio_pika.IncomingMessage):
                async with message.process():
                    try:
                        request_data = json.loads(message.body)
                        print(f"[📩] Получен запрос: {request_data}")

                        if request_data.get("action") == "get_events":
                            event_service = EventService(repo)
                            events = await event_service.list_events()

                            # Конвертируем datetime в строку
                            response_data = [
                                {
                                    "id": event.id,
                                    "odds": event.odds,
                                    "name": event.name,
                                    "deadline": event.deadline.isoformat(),  # 🟢 Фикс JSON ошибки
                                    "status": event.status.value  # 🟢 Конвертируем Enum в строку
                                }
                                for event in events
                            ]

                            print(f"[📤] Отправляем ответ в event_responses: {response_data}")

                            response_exchange = await channel.declare_exchange("event_responses", aio_pika.ExchangeType.DIRECT, durable=True)
                            await response_exchange.publish(
                                aio_pika.Message(body=json.dumps(response_data).encode()),
                                routing_key="event_responses"
                            )
                    except Exception as e:
                        print(f"[❌] Ошибка обработки запроса: {e}")

            await queue.consume(process_request)
            print("[✅] Ожидание запросов...")

            await asyncio.Future()  # Бесконечный цикл ожидания

    except Exception as e:
        print(f"[❌] Ошибка запуска обработчика событий: {e}")
