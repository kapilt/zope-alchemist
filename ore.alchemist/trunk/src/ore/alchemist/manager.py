##################################################################
#
# (C) Copyright 2006 ObjectRealms, LLC
# All Rights Reserved
#
# This file is part of Alchemist.
#
# Alchemist is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Alchemist is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CMFDeployment; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##################################################################
"""
zope transaction manager integration for sqlalchemy

$Id$
"""

import sqlalchemy.mods.threadlocal
from sqlalchemy import objectstore
from zope.interface import implements
from transaction.interfaces import IDataManager, ISynchronizer

import transaction
import patches

class AlchemyObserver( object ):
    """
    a transaction synchronizer/observer that ensures alchemy transactions
    are begun when zope transactions are.

    XXX not really nescesary, the engine registration handles for us.
    """
    implements( ISynchronizer )

    def newTransaction( self, transaction ):
        self.attach( transaction )
        
    def afterCompletion( self, transaction ):
        if hasattr( objectstore.context.current, 'zope_tpc'):
            del objectstore.context.current.zope_tpc 
        #if getattr( objectstore.context.current, 'transaction', None) is not None:
        #    objectstore.context.current.transaction = None
            
    def beforeCompletion( self, transaction ):
        pass
    
    def attach( self, transaction ):
        from engine import iter_engines
        dm = AlchemyDataManager()
        transaction.join( dm )
        zope_tpc = observer.getDataManager()
        # attach extant engines
        map( zope_tpc.transaction.get_or_add, iter_engines() )
             
    def getDataManager( self ):
        return getattr( objectstore.context.current, 'zope_tpc', None )

# install the observer with zope's transaction manager        
observer = AlchemyObserver()
transaction.manager.registerGlobalSynch( observer )

def register( engine ):
    # register alchemy data manager for transaction if not registered
    zope_tpc  = observer.getDataManager()
    if zope_tpc is None:
        observer.attach( transaction.get() )
        zope_tpc = observer.getDataManager()
        
    # register engine if not registered (begins connection's transaction)
    zope_tpc.transaction.get_or_add( engine )
        
class AlchemyDataManager( object ):
    """
    a data manager facade for alchemy sessions participating in zope transactions
    """
    implements( IDataManager )

    def __init__(self):
        self.transaction = objectstore.create_transaction( autoflush = False )
        objectstore.context.current.zope_tpc = self
        
    def abort(self, transaction):
        """Abort a transaction and forget all changes.

        Abort must be called outside of a two-phase commit.

        Abort is called by the transaction manager to abort transactions
        that are not yet in a two-phase commit.
        """
        self.transaction.rollback()
        objectstore.clear()
        
    def commit(self, transaction):
        """Commit modifications to registered objects.

        Save changes to be made persistent if the transaction commits (if
        tpc_finish is called later).  If tpc_abort is called later, changes
        must not persist.

        This includes conflict detection and handling.  If no conflicts or
        errors occur, the data manager should be prepared to make the
        changes persist when tpc_finish is called.
        """
        objectstore.flush()

    def tpc_finish(self, transaction):
        """Indicate confirmation that the transaction is done.

        Make all changes to objects modified by this transaction persist.

        transaction is the ITransaction instance associated with the
        transaction being committed.

        This should never fail.  If this raises an exception, the
        database is not expected to maintain consistency; it's a
        serious error.
        """
        self.transaction.commit()
        
    def tpc_abort(self, transaction):
        """Abort a transaction.

        This is called by a transaction manager to end a two-phase commit on
        the data manager.  Abandon all changes to objects modified by this
        transaction.

        transaction is the ITransaction instance associated with the
        transaction being committed.

        This should never fail.
        """
        self.transaction.abort()
        objectstore.clear()
        
    def sortKey(self):
        """Return a key to use for ordering registered DataManagers.

        ZODB uses a global sort order to prevent deadlock when it commits
        transactions involving multiple resource managers.  The resource
        manager must define a sortKey() method that provides a global ordering
        for resource managers.
        """
        return "100-alchemist"
    

    def null( self, *args, **kw): pass

    tpc_vote = tpc_begin = null

        
