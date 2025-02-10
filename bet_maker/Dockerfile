FROM python:3.10

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true && poetry install --without dev --no-interaction --no-ansi --no-root

COPY . .

RUN poetry run uvicorn --version

CMD ["poetry", "run", "uvicorn", "bet_maker.main:app", "--host", "0.0.0.0", "--port", "8001"]
