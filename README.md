# Wallet Service

Тестовое задание.

## Функциональность

- Создание новых кошельков
- Пополнение кошельков (DEPOSIT)
- Снятие средств (WITHDRAW)
- Просмотр баланса кошелька

## Технологии

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Docker Compose

## Установка и запуск

### Запуск с помощью Docker

1. Установить Docker и Docker Compose
2. В корневой директории проекта выполнить:
```bash
docker-compose up -d
```

### Запуск локально

1. Создать виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Создайть файл `.env` с содержимым:
```
DATABASE_URL=postgresql+asyncpg://postgres:12345678@localhost:5432/wallet_db
TEST_DATABASE_URL=postgresql+asyncpg://postgres:12345678@localhost:5432/test_wallet_db
```

4. Запустить приложение:
```bash
uvicorn app.main:app --reload
```

## API Документация

Документация API доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Создание кошелька
```http
POST /api/v1/wallets
```

### Получение баланса кошелька
```http
GET /api/v1/wallets/{wallet_id}
```

### Операции с кошельком
```http
POST /api/v1/wallets/{wallet_id}/operation
```

Пример тела запроса:
```json
{
    "operation_type": "DEPOSIT",
    "amount": 1000
}
```

### Просмотр записей БД в контейнере
Подключение к БД в контейнере
```
docker-compose exec db psql -U postgres wallet_db
```

Список таблиц
```
\dt
```

Показать все записи в из таблицы wallets
```
SELECT * FROM wallets;
```

выход из подключения к БД в контейнере
```
\q
```


## Тестирование

### Запуск тестов через Docker
```bash
docker-compose exec web pytest tests/test_wallet.py -v
```

### Запуск тестов локально
```bash
pytest tests/test_wallet.py -v
```

## Структура проекта

```
.
├── app/                 # Основной код приложения
│   ├── __init__.py
│   ├── main.py         # Основной файл приложения
│   ├── models.py       # SQLAlchemy модели
│   ├── database.py     # Настройка базы данных
│   ├── schemas.py      # Pydantic схемы
│   ├── routes/         # API маршруты
│   └── crud/           # CRUD операции
├── tests/              # Тесты
├── docker-compose.yml  # Конфигурация Docker
├── Dockerfile          # Docker образ приложения
├── requirements.txt    # Зависимости проекта
└── README.md          # Документация
```


## Управление миграциями базы данных

### Существующие миграции
Первоначальная миграция находится в:
```
alembic/versions/initial_migration.py
```

Она создает таблицу `wallets` со следующей структурой:
```sql
CREATE TABLE wallets (
    id VARCHAR NOT NULL,
    balance NUMERIC(18,2) NOT NULL DEFAULT '0',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE ON UPDATE now(),
    PRIMARY KEY (id)
)
```

### Процесс изменения модели

1. Изменить модель в `app/models.py`
2. Создайть новую миграцию:
```bash
alembic revision --autogenerate -m "описание_изменений"
```
3. Проверить сгенерированный файл миграции в `alembic/versions/`
4. Применить миграцию:
```bash
alembic upgrade head
```

## Настройка базы данных

Для изменения настроек базы данных необходимо обновить следующие файлы:

1. В `docker-compose.yml`:
```yaml
db:
    environment:
      - POSTGRES_PASSWORD=новый_пароль
      - POSTGRES_DB=новое_имя_бд

web:
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:новый_пароль@db:5432/новое_имя_бд
      - TEST_DATABASE_URL=postgresql+asyncpg://postgres:новый_пароль@db:5432/новое_имя_тестовой_бд
```

2. В `.env`:
```
DATABASE_URL=postgresql+asyncpg://postgres:новый_пароль@db:5432/новое_имя_бд
TEST_DATABASE_URL=postgresql+asyncpg://postgres:новый_пароль@db:5432/новое_имя_тестовой_бд
```

3. В `alembic.ini`:
```
sqlalchemy.url = postgresql+asyncpg://postgres:новый_пароль@db:5432/новое_имя_бд
```

4. В `app/database.py` (если используется прямое подключение):
```python
DATABASE_URL = "postgresql+asyncpg://postgres:новый_пароль@db:5432/новое_имя_бд"
```

После изменения настроек:
1. Остановить текущие контейнеры: `docker-compose down`
2. Удалить старые данные: `docker volume rm wallet_service_postgres_data`
3. Запустить заново: `docker-compose up -d`


## База данных

Доступ к базе данных:
- Хост: localhost
- Порт: 5432
- Пользователь: postgres
- Пароль: 12345678
- База данных: wallet_db

## Зависимости

- fastapi==0.104.1
- uvicorn==0.24.0
- sqlalchemy==2.0.23
- alembic==1.12.1
- asyncpg==0.29.0
- pydantic==2.5.2
- python-dotenv==1.0.0
- pytest==8.0.0
- pytest-asyncio==0.23.5
- httpx==0.25.0
- starlette==0.27.0
