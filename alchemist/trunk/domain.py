"""
$Id$
"""

from Acquisition import Explicit
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from zope.interface import implements

from ore.alchemist.interfaces import ITableSchema

class DomainRecord( Explicit ):

    implements( ITableSchema )

    _mapper = None

    security = ClassSecurityInfo()

    def __init__(self, **kw):
        for k,v in kw.iteritems():
            setattr( self, k, v)

    security.declarePrivate('getMapper')
    def getMapper( self ):
        assert self._mapper is not None, "Domain class has no mapper"
        return self._mapper

InitializeClass( DomainRecord )
