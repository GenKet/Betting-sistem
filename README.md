# 🏆 Betting System

## 📌 Описание проекта

**Betting System** — это микросервисная система для приема ставок на спортивные события.  
Система состоит из двух основных микросервисов:

- **Line Provider** — отвечает за генерацию событий и их обновление.
- **Bet Maker** — принимает ставки, валидирует их и сохраняет в базе данных PostgreSQL.

Микросервисы взаимодействуют между собой через **RabbitMQ**, обеспечивая асинхронную обработку запросов. Запросы из **Bet Maker** в **Line Provider** кешируются.

---

## 🛠️ Технологический стек

- 🚀 **FastAPI** — основа сервисов  
- 🗄️ **PostgreSQL** — база данных для хранения ставок  
- ⚡ **Redis** — кеширование событий  
- 📩 **RabbitMQ** — брокер сообщений между сервисами  
- 🐳 **Docker & Docker Compose** — контейнеризация  
- 🏗️ **SQLAlchemy** — ORM для работы с БД  
- 🔄 **Asyncio** — асинхронная обработка запросов  

---

## 🔧 Установка и запуск

### 1️⃣ Клонирование репозитория

```bash
git clone https://github.com/GenKet/Betting-sistem.git
cd betting-system
```

### 2️⃣ Настройка переменных окружения

Файлы `.env` уже сгенерированы для удобства.

### 3️⃣ Запуск через Docker Compose

```bash
docker-compose up --build
```

### 4️⃣ Проверка работы сервисов

После запуска сервисов доступны:

- 📄 **Swagger UI (Line Provider)**: [http://localhost:8000/docs](http://localhost:8000/docs)  
- 📄 **Swagger UI (Bet Maker)**: [http://localhost:8001/docs](http://localhost:8001/docs)  
- 🐰 **RabbitMQ Management UI**: [http://localhost:15672](http://localhost:15672)  
  - **Логин**: `guest`  
  - **Пароль**: `guest`