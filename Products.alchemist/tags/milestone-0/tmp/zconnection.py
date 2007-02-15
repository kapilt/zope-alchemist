"""
model a relational database connection, that manages a
sqlalchemy engine/connection pool

$Id$
"""

from AccessControl import ClassSecurityInfo
from Globals import DTMLFile, InitializeClass
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager


#from thread import get_ident
#from threading import Lock

from engine import create_engine

_connections = {}

def getConnectionFor( alchemist_conn ):
    engine = _connections.get( alchemist_conn.db_uri )
    if engine is None:
        _connections[ alchemist.db_uri ] = engine = create_engine( db_uri )
    return engine

def addAlchemistConnection( self, id, db_uri, RESPONSE=None):
    """
    add an alchemist database connection
    """
    conn = AlchemistConnection( id, db_uri )
    self._setObject( id, conn )

    if RESPONSE is not None:
        wrapped = self._getOb( id )
        RESPONSE.redirect( wrapped.absolute_url() + '/manage_workspace' )

class AlchemistConnection( SimpleItem, PropertyManager ):

    meta_type = "Alchemist Connection"

    def __init__(self, id, db_uri=''):
        self.id = id
        self.db_uri = self.title = db_uri
        self.validateSelf()

    def validateSelf(self):
        pass

    def getConnection(self):
        return getConnectionFor( self )

    def edit(self, db_uri, RESPONSE=None ):
        """
        """
        self.db_uri = db_uri
        self.validateSelf()

        if RESPONSE is not None:
            RESPONSE.redirect('manage_workspace')
        
        
        
