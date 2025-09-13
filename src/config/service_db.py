import os
from dotenv import load_dotenv

load_dotenv()


def get_connection_url() -> str:
    try:
        username = os.getenv("SERVICE_DATABASE_USERNAME")
        password = os.getenv("SERVICE_DATABASE_PASSWORD")
        name = os.getenv("SERVICE_DATABASE_NAME")
        port = os.getenv("SERVICE_DATABASE_PORT")
        host = os.getenv("SERVICE_DATABASE_HOST")

        if not username:
            raise Exception("Missing SERVICE_DATABASE_USERNAME in .env")
        if not password:
            raise Exception("Missing SERVICE_DATABASE_PASSWORD in .env")
        if not name:
            raise Exception("Missing SERVICE_DATABASE_NAME in .env")
        if not port:
            raise Exception("Missing SERVICE_DATABASE_PORT in .env")
        if not host:
            raise Exception("Missing SERVICE_DATABASE_HOST in .env")

        return f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{name}"

    except Exception as e:
        raise e
