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

how do we access the current session in use.

from ore.alchemist import Session
session = Session()
assert session is Session()

"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import ScopedSession

import manager

class TransactionScoped( ScopedSession ):
    def __call__( self, **kwargs ):
        session = super( TransactionScoped, self).__call__( **kwargs )
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

Session = TransactionScoped( _zope_session( sessionmaker( autoflush=True,
                                                          transactional=True ) ) )


