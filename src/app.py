from config.lansweeper_db import get_connection_url as get_lansweeper_con
from config.service_db import get_connection_url as get_service_con
from config.logging_config import logging
from routers.sync_router import router as sync_router
from routers.host_router import router as host_router
from classes.service_database import ServiceDatabase
from classes.lansweeper_database import LansweeperDatabase
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
import urllib3

urllib3.disable_warnings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация и завершение работы приложения"""
    # Инициализация базы данных

    app.state.service_db = ServiceDatabase(get_service_con())
    app.state.lansweeper_db = LansweeperDatabase(get_lansweeper_con())

    logging.info("Application started - database initialized")
    yield
    logging.info("Application shutting down")


# Создание FastAPI приложения
app = FastAPI(title="Lansweeper Data Service", lifespan=lifespan)

# Подключение роутеров
app.include_router(host_router, tags=["Hosts"])
app.include_router(sync_router, tags=["Synchronization"])


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
