##################################################################
#
# (C) Copyright 2005-2007 ObjectRealms, LLC
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

from zope import interface

import transaction
import transaction.interfaces

class SessionDataManager( object ):
    """
    a data manager facade for sqlalchemy sessions participating in
    zope transactions.    
    """
    
    interface.implements( transaction.interfaces.IDataManager )

    def __init__(self, session):
        self.session = session
        self.joined = False

    def _check( self ):
        return bool( self.session.new or self.session.deleted or self.session.dirty )
    
    def abort(self, transaction):
        self.session.joined = False
        if self.session.transaction:
            self.session.transaction.rollback()
        self.session.clear()
        
    def commit(self, transaction):
        if not self.session.transaction:
            self.session.begin()
        if self.session.autoflush:
            return
        self.session.flush()

    def tpc_finish(self, transaction):
        print 'tf'*5
        self.session.joined = False        
        self.session.transaction.commit()
        self.session.clear()
        
    def tpc_abort(self, transaction):
        print 'ta'*5      
        self.session.joined = False                
        self.session.transaction.rollback()
        self.session.clear()
        
    def sortKey(self):
        return "100-alchemist"
    
    def null( self, *args, **kw): pass

    tpc_vote = tpc_begin = null

    def register( self ):
        txn = transaction.get()
        txn.join( self )
        
