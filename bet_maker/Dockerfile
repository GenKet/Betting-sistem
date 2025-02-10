FROM python:3.10

WORKDIR /app

# Установим Poetry
RUN pip install poetry

# Скопируем зависимости и установим их
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true && poetry install --without dev --no-interaction --no-ansi --no-root

# Скопируем код после установки зависимостей
COPY . .

# Убедимся, что Uvicorn доступен
RUN poetry run uvicorn --version

CMD ["poetry", "run", "uvicorn", "bet_maker.main:app", "--host", "0.0.0.0", "--port", "8001"]
