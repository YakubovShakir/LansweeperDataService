from sqlalchemy import INTEGER, VARCHAR, TEXT, DateTime
from sqlalchemy.orm import mapped_column, DeclarativeBase
from datetime import datetime, timezone


class LansweepeerBase(DeclarativeBase):

    @classmethod
    def get_columns(cls) -> list:
        return []


class tblAssets(LansweepeerBase):
    __tablename__ = "tblAssets"
    asset_id = mapped_column("AssetID", INTEGER, primary_key=True, nullable=False)
    name = mapped_column("AssetName", VARCHAR, nullable=False)
    type = mapped_column("Assettype", INTEGER)
    ip_address = mapped_column("IPAddress", VARCHAR)
    mac = mapped_column("Mac", VARCHAR)
    processor = mapped_column("Processor", TEXT)
    first_seen = mapped_column("FirstSeen", DateTime(timezone=True), default=datetime.now(timezone.utc))

    @classmethod
    def get_columns(cls) -> list:
        return [
            *super().get_columns(),
            cls.asset_id,
            cls.name,
            cls.type,
            cls.ip_address,
            cls.mac,
            cls.processor,
            cls.first_seen,
        ]


class tblADComputers(LansweepeerBase):
    __tablename__ = "tblADComputers"
    adcomputerID = mapped_column("AdcomputerID", INTEGER, primary_key=True)
    asset_id = mapped_column("AssetID", INTEGER, nullable=False)
    description = mapped_column("Description", TEXT)
    ou = mapped_column("OU", TEXT)

    @classmethod
    def get_columns(cls) -> list:
        return [*super().get_columns(), cls.description, cls.ou]


class tblAssetCustom(LansweepeerBase):
    __tablename__ = "tblAssetCustom"
    cust_id = mapped_column("CustID", INTEGER, primary_key=True)
    asset_id = mapped_column("AssetID", INTEGER, nullable=False)
    manufacturer = mapped_column("Manufacturer", VARCHAR)
    model = mapped_column("Model", VARCHAR)
    serial_number = mapped_column("Serialnumber", VARCHAR)

    custom_1 = mapped_column("Custom1", VARCHAR)
    custom_2 = mapped_column("Custom2", VARCHAR)
    custom_3 = mapped_column("Custom3", VARCHAR)
    custom_4 = mapped_column("Custom4", VARCHAR)
    custom_5 = mapped_column("Custom5", VARCHAR)
    custom_6 = mapped_column("Custom6", VARCHAR)
    custom_7 = mapped_column("Custom7", VARCHAR)
    custom_8 = mapped_column("Custom8", VARCHAR)
    custom_9 = mapped_column("Custom9", VARCHAR)
    custom_10 = mapped_column("Custom10", VARCHAR)
    custom_11 = mapped_column("Custom11", VARCHAR)
    custom_12 = mapped_column("Custom12", VARCHAR)
    custom_13 = mapped_column("Custom13", VARCHAR)
    custom_14 = mapped_column("Custom14", VARCHAR)
    custom_15 = mapped_column("Custom15", VARCHAR)
    custom_16 = mapped_column("Custom16", VARCHAR)
    custom_17 = mapped_column("Custom17", VARCHAR)
    custom_18 = mapped_column("Custom18", VARCHAR)
    custom_19 = mapped_column("Custom19", VARCHAR)
    custom_20 = mapped_column("Custom20", VARCHAR)

    @classmethod
    def get_columns(cls) -> list:
        return [
            *super().get_columns(),
            cls.manufacturer,
            cls.serial_number,
            cls.model,
            cls.custom_1,
            cls.custom_2,
            cls.custom_3,
            cls.custom_4,
            cls.custom_5,
            cls.custom_6,
            cls.custom_7,
            cls.custom_8,
            cls.custom_9,
            cls.custom_10,
            cls.custom_11,
            cls.custom_12,
            cls.custom_13,
            cls.custom_14,
            cls.custom_15,
            cls.custom_16,
            cls.custom_17,
            cls.custom_18,
            cls.custom_19,
            cls.custom_20,
        ]


class tblOperatingSystem(LansweepeerBase):
    __tablename__ = "tblOperatingsystem"
    asset_id = mapped_column("AssetID", INTEGER, nullable=False, primary_key=True)
    operating_system = mapped_column("Caption", TEXT)

    @classmethod
    def get_columns(cls) -> list:
        return [*super().get_columns(), cls.operating_system]


class tsysAssetTypes(LansweepeerBase):
    __tablename__ = "tsysAssetTypes"
    type = mapped_column("AssetType", INTEGER, nullable=False, primary_key=True)
    typename = mapped_column("AssetTypename", VARCHAR)

    @classmethod
    def get_columns(cls) -> list:
        return [*super().get_columns(), cls.typename]


class tsysCustomNames(LansweepeerBase):
    __tablename__ = "tsysCustomNames"
    custom_name = mapped_column("Customname", VARCHAR, nullable=False, primary_key=True)
    display_name = mapped_column("Displayname", VARCHAR, nullable=False)
