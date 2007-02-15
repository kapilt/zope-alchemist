"""

 - Base class for schemas developed through the web

 - Parent Managed Schema for TTW Schema Development

$Id$
"""

from Products.Archetypes import public as atapi
from Products.ATSchemaEditorNG.ParentManagedSchema import ManagedSchemaBase

from utils import getAlchemist

class AlchemistManagedSchema( ManagedSchemaBase ):

    def lookup_provider(self):
        return getAlchemist( self )


class AlchemistWebContent( AlchemistManagedSchema, atapi.BaseContent ):

    portal_type = meta_type = archetype_name = "Alchemist Web Content"

atapi.registerType( AlchemistWebContent )
