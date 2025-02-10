#!/bin/bash
set -e 

echo "[✅] Запускаем FastAPI (HTTP API) + RabbitMQ Listener..."

poetry run uvicorn line_provider.main:app --host 0.0.0.0 --port 8000 &

poetry run python -m line_provider.src.services.event_request_handler

wait