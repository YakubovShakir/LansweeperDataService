from fastapi import APIRouter, Depends, HTTPException, Response
from classes.service_database import ServiceDatabase
from classes.lansweeper_database import LansweeperDatabase
from models.service_models import LansweeperData
from asyncio import create_task
from functions.asset_is_server import asset_is_server, asset_is_desktop
import logging

ERROR_LANSWEEPER_ASSETS_NOT_FETCHED = "Error while fetching assets from lansweeper"
ERROR_SERVICE_ASSETS_NOT_FETCHED = "Error while fetching assets from service"


def get_service_db() -> ServiceDatabase:
    from app import app

    return app.state.service_db


def get_lansweeper_db() -> LansweeperDatabase:
    from app import app

    return app.state.lansweeper_db


router = APIRouter()


@router.post("/sync")
async def start_sync(
    service_db: ServiceDatabase = Depends(get_service_db),
    lansweeper_db: LansweeperDatabase = Depends(get_lansweeper_db),
):
    try:
        fetched_assets = await lansweeper_db.get_assets()
        service_assets = await service_db.get(table=LansweeperData)

        if fetched_assets is None or len(fetched_assets) == 0:
            raise Exception(ERROR_LANSWEEPER_ASSETS_NOT_FETCHED)
        if service_assets is None:
            raise Exception(ERROR_SERVICE_ASSETS_NOT_FETCHED)

        fetched_dicts = [dict(asset) for asset in fetched_assets if asset is not None]

        for asset in fetched_dicts:
            if asset_is_server(asset):
                asset["host_type"] = "Server"
            if asset_is_desktop(asset):
                asset["host_type"] = "Workstation"

        task = service_db.sync_table(table=LansweeperData, fetched_items=fetched_dicts, comprasion_key="name")
        create_task(task)
        return Response(status_code=200)
    except Exception as e:
        logging.error(f"Error starting synchronization: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
