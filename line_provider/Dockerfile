FROM python:3.10

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true && poetry install --without dev --no-interaction --no-ansi --no-root

COPY . .

RUN chmod +x /app/line_provider/start.sh

CMD ["poetry", "run", "uvicorn", "line_provider.main:app", "--host", "0.0.0.0", "--port", "8000"]