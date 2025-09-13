from models.service_models import LansweeperData
from .database import Database
from models.service_models import ServiceBase as Base, SyncStates
from typing import Sequence
import logging

ERROR_NOT_FOUND_EXISTING_ITEMS = "Failed get existing_items"


class ServiceDatabase(Database):
    async def get(self, table: type[Base], conditionals: list | None = None):
        return await self._select(table.get_columns(), conditionals=conditionals)

    async def add(self, table: type[Base], value, comprasion_key: str = "id"):
        await self._insert(table, value)
        logging.info(f"Added new {table.__tablename__} {comprasion_key} = {value[comprasion_key]}")

    async def update(self, table: type[Base], value: dict, comprasion_key: str, comprasion_key_value):
        await self._update(
            table, value, conditionals=[getattr(table, comprasion_key) == comprasion_key_value]
        )
        logging.info(f"Updated {table.__tablename__} {comprasion_key} = {comprasion_key_value}")

    async def sync_table(self, table: type[Base], fetched_items: Sequence, comprasion_key: str = "id"):
        """
        Синхронизация определенной таблицы
        """
        try:
            # Алгоритм
            # 1. Получаем существующие объекты
            # 2. Получаем множества ID объектов и вычитаем множество тех что пришли от множество тех что есть
            # 3. Помечаем как необнаруженные те, которых больше нет
            # 4. Добавляем новые или апдейтим существующие объекты
            logging.info(f"Starting {table.__tablename__} synchronization...")

            existing_items = await self.get(table)
            if existing_items == None:
                raise Exception(ERROR_NOT_FOUND_EXISTING_ITEMS)

            existing_keys = set([item.get(comprasion_key) for item in existing_items])
            fetched_keys = set([item.get(comprasion_key) for item in fetched_items])

            not_detected_keys = existing_keys - fetched_keys
            for key in not_detected_keys:
                await self.update(
                    table=table,
                    value={"detected": False},
                    comprasion_key_value=key,
                    comprasion_key=comprasion_key,
                )
                logging.info(f"Marked {table.__tablename__} {comprasion_key} as not detected")

            # Добавляем или обновляем данные
            for fetched_item in fetched_items:
                item_dict = dict(fetched_item)
                item_dict["detected"] = True

                # Апдейтим
                if fetched_item[comprasion_key] in existing_keys:
                    await self.update(
                        table,
                        item_dict,
                        comprasion_key=comprasion_key,
                        comprasion_key_value=fetched_item[comprasion_key],
                    )
                else:
                    # Обновляем
                    await self.add(table, fetched_item, comprasion_key=comprasion_key)

            logging.info(f"{table.__tablename__} synchronization completed")
            await self._insert(
                SyncStates,
                {"service_name": "lansweeper", "table_name": table.__tablename__, "result": True},
            )
        except Exception as e:
            logging.error(f"Error in sync_table {table.__tablename__}: {e}")
            await self._insert(
                SyncStates, {"service_name": "lansweeper", "table_name": table.__tablename__, "result": False}
            )
