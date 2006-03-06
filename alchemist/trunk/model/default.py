"""
$Id$
"""

from Products.Alchemist.archetypes import ArchetypesSchemaModel

class DefaultSchemaModel( ArchetypesSchemaModel ):

    def match( self, object ):
        return True
