# Lansweeper Data Service

## Описание Проекта
`Lansweeper Data Service` — это микросервис на базе FastAPI, предназначенный для извлечения, синхронизации и обновления инвентарных данных из развернутого сервиса Lansweeper (через прямое подключение к его базе данных) в локальную базу данных PostgreSQL. Этот сервис может быть использован для целей инвентаризации, аудита активов и формирования отчетов, предоставляя актуальные и унифицированные данные.

### Ключевые Функции:
- **Синхронизация данных:** Автоматическое извлечение данных об активах (серверах, компьютерах, пользователях и т.д.) из базы данных Lansweeper.
- **Локальное хранение:** Сохранение синхронизированных данных в собственной базе данных для быстрого доступа и анализа.
- **Обновление данных:** Поддержание актуальности данных посредством регулярных обновлений.
- **API Интерфейс:** Предоставление RESTful API для доступа к инвентарным данным.

## Используемые Технологии
Проект построен на современном стеке технологий, обеспечивающем высокую производительность, надежность и легкость в разработке:

- **FastAPI:** Высокопроизводительный, легковесный веб-фреймворк для создания API на Python.
- **SQLAlchemy:** Мощный ORM для взаимодействия с базами данных, обеспечивающий гибкость и надежность.
- **Alembic:** Инструмент для миграции баз данных, позволяющий управлять изменениями схемы.
- **`asyncpg` / `aioodbc`:** Асинхронные драйверы для работы с PostgreSQL и MSSQL (Lansweeper).
- **`python-dotenv`:** Для управления переменными окружения.
- **`uvicorn`:** ASGI-сервер для запуска FastAPI приложения.
- **PostgreSQL:** Локальная база данных для хранения синхронизированных данных.
- **Microsoft SQL Server:** База данных, используемая Lansweeper.

## Установка и Запуск

### Предварительные Требования
- Python 3.12+
- Docker (рекомендуется для локальной разработки)
- PostgreSQL (для локальной базы данных)
- Доступ к базе данных Lansweeper (Microsoft SQL Server)

### Шаги Установки

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/YourGitHubUsername/LansweeperDataService.git
    cd LansweeperDataService
    ```

2.  **Установите зависимости (с использованием `poetry`):**
    ```bash
    poetry install
    ```

3.  **Настройте переменные окружения:**
    Создайте файл `.env` в корневой директории проекта на основе `.env.example`.

    ```ini
    # .env
    # --- Lansweeper Database Configuration ---
    LANSWEEPER_DB_DRIVER={ODBC Driver 17 for SQL Server} # Example: {ODBC Driver 17 for SQL Server}
    LANSWEEPER_DB_SERVER=your_lansweeper_db_server
    LANSWEEPER_DB_PORT=1433
    LANSWEEPER_DB_NAME=lansweeperdb
    LANSWEEPER_DB_USERNAME=your_lansweeper_db_username
    LANSWEEPER_DB_PASSWORD=your_lansweeper_db_password

    # --- Service Database Configuration (PostgreSQL) ---
    SERVICE_DB_HOST=localhost
    SERVICE_DB_PORT=5432
    SERVICE_DB_NAME=service_db
    SERVICE_DB_USERNAME=service_user
    SERVICE_DB_PASSWORD=service_password
    ```

4.  **Примените миграции базы данных:**
    ```bash
    poetry run alembic upgrade head
    ```

5.  **Запустите приложение:**
    ```bash
    poetry run uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
    ```
    Или с помощью Docker:
    ```bash
    docker-compose up --build
    ```

## Использование API
После запуска сервис будет доступен по адресу `http://localhost:8000`.

Документация API (Swagger UI) доступна по адресу `http://localhost:8000/docs`.

### Примеры Эндпоинтов:
- `GET /hosts`: Получить список всех хостов.
- `GET /hosts/{host_id}`: Получить информацию о конкретном хосте.
- `POST /sync/start`: Запустить процесс синхронизации данных.

## Структура Проекта

```
.
├── alembic.ini             # Конфигурация Alembic
├── Dockerfile              # Dockerfile для сборки образа
├── poetry.lock             # Зафиксированные версии зависимостей
├── pyproject.toml          # Конфигурация проекта и зависимостей Poetry
├── README.md               # Этот файл
└── src/
    ├── app.py              # Основной файл приложения FastAPI
    ├── classes/            # Классы для работы с базой данных и внешними сервисами
    │   ├── AIClient.py
    │   ├── database.py     # Базовый класс для работы с БД
    │   ├── lansweeper_database.py # Класс для взаимодействия с БД Lansweeper
    │   └── service_database.py    # Класс для взаимодействия с локальной БД
    ├── config/             # Файлы конфигурации
    │   ├── ai_config.py
    │   ├── lansweeper_db.py  # Конфигурация подключения к Lansweeper БД
    │   ├── logging_config.py # Конфигурация логирования
    │   ├── parameters.py
    │   └── service_db.py     # Конфигурация подключения к локальной БД
    ├── functions/          # Вспомогательные функции
    │   └── asset_is_server.py
    ├── logs/               # Директория для логов
    ├── migrations/         # Скрипты миграции Alembic
    ├── models/             # Модели SQLAlchemy
    │   ├── lansweeper_models.py
    │   └── service_models.py
    ├── packages/           # Дополнительные пакеты (например, ODBC драйвер)
    └── routers/            # Роутеры FastAPI
        ├── host_router.py
        └── sync_router.py
```