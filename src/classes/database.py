from sqlalchemy import update, insert, select, Result, URL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import Sequence
import logging

INFO_DATABASE_CONNECTED = "Database connection initialized successfully"
ERROR_DATABASE_NOT_CONNECTED = "Failed to initialize database connection"
ERROR_DATABASE_IN_SELECT_QUERY = "Database error in select query"
ERROR_DATABASE_UPDATE_QUERY = "Database error during update commit"
ERROR_DATABASE_IN_INSERT_QUERY = "Error in insert query"


class Database:

    def __init__(self, connection_url: str | URL):
        try:
            self.__engine = create_async_engine(connection_url, pool_recycle=3600, pool_pre_ping=True)
            self.__session = async_sessionmaker(self.__engine)
            logging.info(INFO_DATABASE_CONNECTED)
        except Exception as e:
            logging.error(ERROR_DATABASE_NOT_CONNECTED + " : " + str(e))

    async def _select(
        self,
        columns: list | tuple,
        conditionals: list | None = None,
        joins: list[dict] | tuple[dict] | None = None,
    ) -> Sequence | None:
        try:

            async with self.__session() as session:
                query = select(*columns)

                if joins:

                    for j in joins:
                        query = query.join(j["table"], j["on"], isouter=j["isouter"])

                if conditionals:
                    for cond in conditionals:
                        query = query.where(cond)

                result = await session.execute(query)
                return [row._mapping for row in result.all()]

        except Exception as e:
            logging.error(ERROR_DATABASE_IN_SELECT_QUERY + " : " + str(e))

    async def _update(self, table: type[DeclarativeBase], values: dict, conditionals: list | None = None):

        try:

            async with self.__session() as session:
                try:
                    query = update(table)

                    if conditionals:
                        for cond in conditionals:
                            query = query.where(cond)

                    query = query.values(values)
                    await session.execute(query)
                    await session.commit()
                except SQLAlchemyError as commit_error:
                    await session.rollback()
                    raise commit_error

        except Exception as e:
            logging.error(ERROR_DATABASE_UPDATE_QUERY + " : " + str(e))

    async def _insert(self, table: type[DeclarativeBase], values: dict):

        try:
            async with self.__session() as session:
                try:
                    await session.execute(insert(table).values(values))
                    await session.commit()
                except SQLAlchemyError as commit_error:
                    await session.rollback()
                    raise commit_error

        except Exception as e:
            logging.error(ERROR_DATABASE_IN_INSERT_QUERY + " : " + str(e))
