
from sqlalchemy import *
from ore.alchemist.engine import get_engine
db = get_engine('mysql://root@localhost/alc', echo=True )

def loadTables():
    meta = BoundMetaData( db )
    table = Table("Users", meta, autoload=True )

    return meta
        
