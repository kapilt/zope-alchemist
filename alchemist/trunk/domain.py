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
$Id$
"""

from Acquisition import Explicit
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from zope.interface import implements

from ore.alchemist.interfaces import ITableSchema

from OFS.SimpleItem import SimpleItem

def getId( inst ):
    # XXX temp hack.. issues with multi key objects, remapped primary keys
    if inst is None:
        return ''

    for column_name in inst.c.keys():
        column = inst.c[ column_name ]
        if inst.c[column_name].primary_key is True:
            return str(getattr(  inst, column.name, ''))

    return ''

class DomainRecord( SimpleItem ):

    implements( ITableSchema )

    _mapper = None

    security = ClassSecurityInfo()

    id = property( getId )

    def __init__(self, **kw):
        for k,v in kw.iteritems():
            setattr( self, k, v)

    security.declarePrivate('getMapper')
    def getMapper( self ):
        assert self._mapper is not None, "Domain class has no mapper"
        return self._mapper

InitializeClass( DomainRecord )
