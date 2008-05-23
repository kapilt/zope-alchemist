##############################################################################
#
# Copyright (c) 2006-2008 Kapil Thangavelu <kapil.foss@gmail.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
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
        self.session.joined = False        
        self.session.transaction.commit()
        self.session.clear()
        
    def tpc_abort(self, transaction):
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
        
