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
