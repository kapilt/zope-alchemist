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
a zope transaction manager for sqlalchemy

make engine transaction methods noops, except for ensuring registration.
"""

from zope.interface import implements
from sqlalchemy import objectstore
from transaction.interfaces import IDataManager
        
class AlchemyDataManager( object ):
    """
    a data manager facade for alchemy engines participating in zope.transactions
    """
    implements( IDataManager )

    def __init__(self):
        self.transaction = None
        # not sure if we need to reference data managers
        #objectstore.context.current.zope_tpc = self
        
    def abort(self, transaction):
        """Abort a transaction and forget all changes.

        Abort must be called outside of a two-phase commit.


        Abort is called by the transaction manager to abort transactions
        that are not yet in a two-phase commit.
        """
        if self.transaction is not None:
            self.transaction.rollback()
        objectstore.clear()

    # Two-phase commit protocol.  These methods are called by the ITransaction
    # object associated with the transaction being committed.  The sequence
    # of calls normally follows this regular expression:
    #     tpc_begin commit tpc_vote (tpc_finish | tpc_abort)

    def tpc_begin(self, transaction):
        """Begin commit of a transaction, starting the two-phase commit.

        transaction is the ITransaction instance associated with the
        transaction being committed.
        """
        self.transaction = objectstore.create_transaction( autoflush = False )
        
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

    def tpc_vote(self, transaction):
        """Verify that a data manager can commit the transaction.

        This is the last chance for a data manager to vote 'no'.  A
        data manager votes 'no' by raising an exception.

        transaction is the ITransaction instance associated with the
        transaction being committed.
        """

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
        self.transaction = None
        
    def tpc_abort(self, transaction):
        """Abort a transaction.

        This is called by a transaction manager to end a two-phase commit on
        the data manager.  Abandon all changes to objects modified by this
        transaction.

        transaction is the ITransaction instance associated with the
        transaction being committed.

        This should never fail.
        """
        objectstore.clear()
        self.transaction.abort()
        self.transaction = None
        
    def sortKey(self):
        """Return a key to use for ordering registered DataManagers.

        ZODB uses a global sort order to prevent deadlock when it commits
        transactions involving multiple resource managers.  The resource
        manager must define a sortKey() method that provides a global ordering
        for resource managers.
        """
        return "100-alchemist"
    
