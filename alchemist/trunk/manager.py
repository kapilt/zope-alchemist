"""
a zope transaction manager for sqlalchemy

make engine transaction methods noops, except for ensuring registration.
"""

import re

from zope.interface import implements
from sqlalchemy import objectstore
from transaction.interfaces import IDataManager, IDataManagerSavepoint

class AlchemySavePoint( object ):

    implements( IDataManagerSavepoint )

    def __init__(self, name, manager ):
        self.name = name
        self.manager = manager

    def rollback( self ):
        """
        rollback to this savepoint
        """
        self.manager.engine.do_zope_rollback_savepoint( self.name )
        
        
class AlchemyDataManager( object ):
    """
    a data manager facade for alchemy engines participating in zope.transactions
    """
    implements( IDataManager )

    def __init__(self, engine):
        self.engine = engine
    
    def abort(self, transaction):
        """Abort a transaction and forget all changes.

        Abort must be called outside of a two-phase commit.


        Abort is called by the transaction manager to abort transactions
        that are not yet in a two-phase commit.
        """
        self.engine.do_zope_rollback()

    # Two-phase commit protocol.  These methods are called by the ITransaction
    # object associated with the transaction being committed.  The sequence
    # of calls normally follows this regular expression:
    #     tpc_begin commit tpc_vote (tpc_finish | tpc_abort)

    def tpc_begin(self, transaction):
        """Begin commit of a transaction, starting the two-phase commit.

        transaction is the ITransaction instance associated with the
        transaction being committed.
        """
        
        
    def commit(self, transaction):
        """Commit modifications to registered objects.

        Save changes to be made persistent if the transaction commits (if
        tpc_finish is called later).  If tpc_abort is called later, changes
        must not persist.

        This includes conflict detection and handling.  If no conflicts or
        errors occur, the data manager should be prepared to make the
        changes persist when tpc_finish is called.
        """
        objectstore.commit()
        

    def tpc_vote(self, transaction):
        """Verify that a data manager can commit the transaction.

        This is the last chance for a data manager to vote 'no'.  A
        data manager votes 'no' by raising an exception.

        transaction is the ITransaction instance associated with the
        transaction being committed.
        """
        #savepoint_name = self.engine.do_zope_savepoint()

    def tpc_finish(self, transaction):
        """Indicate confirmation that the transaction is done.

        Make all changes to objects modified by this transaction persist.

        transaction is the ITransaction instance associated with the
        transaction being committed.

        This should never fail.  If this raises an exception, the
        database is not expected to maintain consistency; it's a
        serious error.
        """
        self.engine.do_zope_commit()

    def tpc_abort(self, transaction):
        """Abort a transaction.

        This is called by a transaction manager to end a two-phase commit on
        the data manager.  Abandon all changes to objects modified by this
        transaction.

        transaction is the ITransaction instance associated with the
        transaction being committed.

        This should never fail.
        """
        self.engine.do_zope_rollback()

    def sortKey(self):
        """Return a key to use for ordering registered DataManagers.

        ZODB uses a global sort order to prevent deadlock when it commits
        transactions involving multiple resource managers.  The resource
        manager must define a sortKey() method that provides a global ordering
        for resource managers.
        """
        return "0-PloneAlchemist"
    
    #def savepoint(self):
    #    """Return a data-manager savepoint (IDataManagerSavepoint).
    #    """
        #savepoint_name = self.engine.do_zope_savepoint()
        
        
