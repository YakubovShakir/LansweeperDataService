from fastapi import APIRouter, Depends, HTTPException
from classes.service_database import ServiceDatabase
import datetime
import logging
from models.service_models import LansweeperData


def get_db() -> ServiceDatabase:
    from app import app

    return app.state.service_db


router = APIRouter()


@router.get("/hosts")
async def fetchHosts(db: ServiceDatabase = Depends(get_db)):
    try:

        hosts = await db.get(table=LansweeperData)
        return hosts
    except Exception as e:
        logging.error(f"Error in handlers.py -> fetchHosts: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@router.get("/hosts-discovered")
async def get_host_after_datetime(date_param: datetime.datetime, db: ServiceDatabase = Depends(get_db)):
    try:
        hosts = await db.get(table=LansweeperData)
        if not hosts:
            raise HTTPException(status_code=404, detail="Hosts not found or failed to retrieve")

        result = []

        for host in hosts:

            first_seen_date = host["first_seen"]

            if (first_seen_date) is None:
                continue

            # Make date_param timezone-aware if it's naive and first_seen_date is aware
            if first_seen_date.tzinfo is not None and date_param.tzinfo is None:
                date_param = date_param.replace(tzinfo=datetime.timezone.utc)

            if first_seen_date >= date_param:
                result.append(host)

        return result
    except Exception as e:
        logging.error(f"Error in handlers.py -> get_host_after_timestamp: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@router.get("/host")
async def get_host(
    host_id: int | None = None,
    name: str | None = None,
    ip_address: str | None = None,
    mac: str | None = None,
    processor: str | None = None,
    manufacturer: str | None = None,
    model: str | None = None,
    serial_number: str | None = None,
    db: ServiceDatabase = Depends(get_db),
):
    try:
        masked_host = {
            "host_id": host_id,
            "name": name,
            "ip_address": ip_address,
            "mac": mac,
            "processor": processor,
            "manufacturer": manufacturer,
            "model": model,
            "serial_number": serial_number,
        }

        hosts = await db.get(table=LansweeperData)
        if not hosts:
            raise HTTPException(status_code=404, detail="Hosts not found or failed to retrieve")
        if host_id:
            return [host for host in hosts if host["host_id"] == host_id]

        hosts = list(hosts)
        for i in range(len(hosts) - 1, -1, -1):

            for key in masked_host:
                if masked_host[key] and (
                    not hosts[i][key] or (not masked_host[key].lower() in hosts[i][key].lower())
                ):
                    hosts.pop(i)
                    break

        return hosts
    except Exception as e:
        logging.error(f"Error in handlers.py -> get_host: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
