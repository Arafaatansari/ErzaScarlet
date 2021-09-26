__all__ = ['get_collection']

import asyncio
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient, AgnosticDatabase, AgnosticCollection
from ErzaScarlet import MONGO_DB

print("Connecting to Database ...")

_MGCLIENT: AgnosticClient = AsyncIOMotorClient(MONGO_DB)
_RUN = asyncio.get_event_loop().run_until_complete

if "Rikka" in _RUN(_MGCLIENT.list_database_names()):
    print("Rikka Database Found :) => Now Logging to it...")
else:
    print("Rikka Database Not Found :( => Creating New Database...")

_DATABASE: AgnosticDatabase = _MGCLIENT["Rikka"]


def get_collection(name: str) -> AgnosticCollection:
    """ Create or Get Collection from your database """
    return _DATABASE[name]


def _close_db() -> None:
    _MGCLIENT.close()