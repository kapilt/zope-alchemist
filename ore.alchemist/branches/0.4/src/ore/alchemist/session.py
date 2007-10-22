"""

how do we access the current session in use.

from ore.alchemist import Session
session = Session()
assert session is Session()

"""

from sqlalchemy.orm import sessionmaker, scoped_session

import manager

class zope_txn_session( object ):
    # transaction integration
    def __init__( self, session_factory ):
        self.session_factory = session_factory

    def __call__( self, **kwargs ):
        session = self.session_factory( **kwargs )
        if not session.joined:
            data_manager = manager.SessionDataManager( session )
            data_manager.register()
            session.joined = True
        if not session.transaction:
            session.begin()
        return session

def _zope_session( session_factory ):
    # session factory
    class ZopeSession( session_factory ):
        joined = False
        def __init__( self, **kwargs ):
            super( ZopeSession, self).__init__( **kwargs )
    return ZopeSession

Session = zope_txn_session(
               scoped_session(
                     _zope_session(
                           sessionmaker( autoflush=True, transactional=True )
                           )
                     )
               )


