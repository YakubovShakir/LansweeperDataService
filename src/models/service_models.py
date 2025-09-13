from sqlalchemy import INTEGER, DATE, VARCHAR, TEXT, BOOLEAN, JSON, DateTime
from sqlalchemy.orm import mapped_column, DeclarativeBase

from datetime import datetime, timezone


class ServiceBase(DeclarativeBase):
    __table_args__ = {"schema": "integration_modules"}

    id = mapped_column("id", INTEGER, primary_key=True, autoincrement=True)
    created_at = mapped_column("created_at", DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = mapped_column(
        "updated_at",
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    @classmethod
    def get_columns(cls) -> list:
        return [cls.id, cls.created_at, cls.updated_at]


class SyncStates(ServiceBase):
    __tablename__ = "sync_states"
    service_name = mapped_column("service_name", TEXT, nullable=False)
    table_name = mapped_column("table_name", TEXT, nullable=False)
    result = mapped_column("result", BOOLEAN, nullable=False)


class LansweeperData(ServiceBase):
    __tablename__ = "lansweeper_data"
    asset_id = mapped_column("asset_id", INTEGER, nullable=False)
    typename = mapped_column("typename", VARCHAR)
    operating_system = mapped_column("operating_system", TEXT)
    ou = mapped_column("ou", TEXT)
    name = mapped_column("name", VARCHAR)
    ip_address = mapped_column("ip_address", VARCHAR)
    mac = mapped_column("mac", VARCHAR)
    processor = mapped_column("processor", VARCHAR)
    first_seen = mapped_column("first_seen", DateTime(timezone=True), default=datetime.now(timezone.utc))
    description = mapped_column("description", TEXT)
    manufacturer = mapped_column("manufacturer", TEXT)
    model = mapped_column("model", TEXT)
    serial_number = mapped_column("serial_number", TEXT)
    detected = mapped_column("detected", BOOLEAN, default=True)
    host_type = mapped_column("host_type", TEXT, default="Unknown")
    custom_fields = mapped_column("custom_fields", JSON)

    @classmethod
    def get_columns(cls) -> list:
        return [
            *super().get_columns(),
            cls.asset_id,
            cls.typename,
            cls.operating_system,
            cls.ou,
            cls.name,
            cls.ip_address,
            cls.mac,
            cls.processor,
            cls.first_seen,
            cls.description,
            cls.manufacturer,
            cls.model,
            cls.serial_number,
            cls.detected,
            cls.host_type,
            cls.custom_fields,
        ]
