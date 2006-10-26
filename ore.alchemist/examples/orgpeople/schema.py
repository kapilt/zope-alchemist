"""
Table Definitions for database structure

$Id$
"""

from sqlalchemy import *
from ore.alchemist.metadata import ZopeBoundMetaData
from db import database

__all__ = ['rdb_schema', 'PersonTable', 'AddressTable']

rdb_schema = ZopeBoundMetaData(database)

AddressTable = Table(
    'Addresses',
    rdb_schema,
    autoload = True
    )

# incidenally if we autoload person table first sqlalchemy will autoload addrreesses becaues
# of the fk relationship. so we could just use the below.. but we won't have an addressable
# table, though its retrievable from the metadata.

PersonTable = Table(
    'Persons',
    rdb_schema,
    autoload = True 
    )


