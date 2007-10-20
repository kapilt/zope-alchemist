"""

how do we access the current session in use.

from ore.alchemist import Session
session = Session()
assert session is Session()

"""

from sqlalchemy.orm import sessionmaker, scoped_session

import manager

def _zope_session( session_factory ):
    
    class ZopeSession( session_factory ):
        
        def __init__( self, **kwargs ):
            super( ZopeSession, self).__init__( **kwargs )
            data_manager = manager.SessionDataManager( self )
            data_manager.register()
            
    return ZopeSession

Session = scoped_session(
                _zope_session(
                      sessionmaker( autoflush=True, transactional=True )
                      )
                 )
