from models.lansweeper_models import (
    tblAssets,
    tblADComputers,
    tblAssetCustom,
    tsysAssetTypes,
    tblOperatingSystem,
    tsysCustomNames,
)
from .database import Database
from typing import Sequence
import logging


ERROR_SELECT_CUSTOM_NAMES = "Error in get_mapped_custom_names"
ERROR_SELECT_ASSETS = "Assets is None"


class LansweeperDatabase(Database):
    """Класс для взаимодействия с базой данных Lansweeper.

    Наследуется от базового класса Database и предоставляет методы для извлечения
    данных об активах, включая их кастомные поля.
    """

    __JOIN_TSYS_ASSET_TYPES = {
        "table": tsysAssetTypes,
        "on": tblAssets.type == tsysAssetTypes.type,
        "isouter": True,
    }
    __JOIN_TBL_OPERATING_SYSTEM = {
        "table": tblOperatingSystem,
        "on": tblOperatingSystem.asset_id == tblAssets.asset_id,
        "isouter": True,
    }
    __JOIN_TBL_ADC_COMPUTERS = {
        "table": tblADComputers,
        "on": tblAssets.asset_id == tblADComputers.asset_id,
        "isouter": True,
    }
    __JOIN_TBL_ASSET_CUSTOM = {
        "table": tblAssetCustom,
        "on": tblAssetCustom.asset_id == tblAssets.asset_id,
        "isouter": True,
    }

    __ALL_ASSETS = {
        "select": (
            *tblAssets.get_columns(),
            *tblADComputers.get_columns(),
            *tblAssetCustom.get_columns(),
            *tsysAssetTypes.get_columns(),
            *tblOperatingSystem.get_columns(),
        ),
        "joins": [
            __JOIN_TSYS_ASSET_TYPES,
            __JOIN_TBL_OPERATING_SYSTEM,
            __JOIN_TBL_ADC_COMPUTERS,
            __JOIN_TBL_ASSET_CUSTOM,
        ],
    }

    async def __get_mapped_custom_names(self) -> Sequence | None:
        """Извлекает и возвращает сопоставленные имена кастомных полей из Lansweeper.

        Returns:
            Sequence | None: Список словарей с 'custom_name' и 'display_name' или None в случае ошибки.
        """
        try:
            mapped_names = await self._select(
                columns=[tsysCustomNames.custom_name, tsysCustomNames.display_name]
            )
            return mapped_names
        except Exception as e:
            logging.error(ERROR_SELECT_CUSTOM_NAMES + " : " + str(e))

    async def get_assets(self):
        """Извлекает все активы из базы данных Lansweeper и сопоставляет их с кастомными именами.

        Raises:
            Exception: Если активы не были получены из базы данных.

        Returns:
            list[dict] | None: Список словарей, представляющих активы с сопоставленными кастомными полями,
                               или None, если сопоставленные имена не найдены или произошла ошибка.
        """
        try:
            assets = await self._select(
                LansweeperDatabase.__ALL_ASSETS["select"],
                joins=LansweeperDatabase.__ALL_ASSETS["joins"],
            )
            if assets is None:
                raise Exception(ERROR_SELECT_ASSETS)

            mapped_custom_names = await self.__get_mapped_custom_names()
            if not mapped_custom_names:
                return None

            return [self.__map_custom_names(asset, mapped_custom_names) for asset in assets]
        except Exception as e:
            logging.error(str(e))

    def __map_custom_names(self, lw_asset: dict, mapped_names: Sequence) -> dict | None:
        """Сопоставляет кастомные имена полей активам Lansweeper.

        Args:
            lw_asset (dict): Словарь, представляющий актив Lansweeper.
            mapped_names (Sequence): Список сопоставленных кастомных имен и их отображаемых значений.

        Returns:
            dict | None: Словарь, представляющий актив с добавленными кастомными полями или None, если актив не может быть сопоставлен.
        """
        return {
            "asset_id": lw_asset["asset_id"],
            "typename": lw_asset["typename"],
            "operating_system": lw_asset["operating_system"],
            "ou": lw_asset["ou"],
            "name": lw_asset["name"],
            "ip_address": lw_asset["ip_address"],
            "mac": lw_asset["mac"],
            "processor": lw_asset["processor"],
            "first_seen": lw_asset["first_seen"],
            "description": lw_asset["description"],
            "manufacturer": lw_asset["manufacturer"],
            "model": lw_asset["model"],
            "serial_number": lw_asset["serial_number"],
            "custom_fields": {
                f"custom_{i}": {
                    "name": mapped_names[i - 1]["display_name"],
                    "value": lw_asset[f"custom_{i}"],
                }
                for i in range(1, 21)
            },
        }
