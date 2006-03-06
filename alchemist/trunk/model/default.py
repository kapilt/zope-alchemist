"""
$Id$
"""

from Products.Alchemist.archetypes import ArchetypesSchemaModel
from sqlalchemy.util import OrderedDict

class DefaultSchemaModel( ArchetypesSchemaModel ):

    def match( self, object ):
        return True

    def clear( self ):
        self._tables = OrderedDict()
        self._peer_factories = {}
        self.engine.tables = {}
        self.generateDefaults()
