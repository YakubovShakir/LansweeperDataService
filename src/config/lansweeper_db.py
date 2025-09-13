from sqlalchemy import URL
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection_url() -> str | URL:
    try:
        username = os.getenv("LANSWEEPER_DATABASE_USERNAME")
        password = os.getenv("LANSWEEPER_DATABASE_PASSWORD")
        name = os.getenv("LANSWEEPER_DATABASE_NAME")
        port = os.getenv("LANSWEEPER_DATABASE_PORT")
        host = os.getenv("LANSWEEPER_DATABASE_HOST")
        driver = "ODBC Driver 17 for SQL Server"

        if not username:
            raise Exception("Missing LANSWEEPER_DATABASE_USERNAME in .env")
        if not password:
            raise Exception("Missing LANSWEEPER_DATABASE_PASSWORD in .env")
        if not name:
            raise Exception("Missing LANSWEEPER_DATABASE_NAME in .env")
        if not port:
            raise Exception("Missing LANSWEEPER_DATABASE_PORT in .env")
        if not host:
            raise Exception("Missing LANSWEEPER_DATABASE_HOST in .env")

        connection_string = f"DRIVER={driver};SERVER={host};DATABASE={name};UID={username};PWD={password}"
        return URL.create("mssql+aioodbc", query={"odbc_connect": connection_string})

    except Exception as e:
        raise e
