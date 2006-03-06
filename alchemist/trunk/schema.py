"""
Parent Managed Schema for TTW Schema Development

$Id$
"""

from Products.ATSchemaEditorNG.ParentManagedSchema import ManagedSchemaBase
from utils import getAlchemist


class AlchemistManagedSchema( ManagedSchemaBase ):

    def lookup_provider(self):
        return getAlchemist( self )

        
        
