"""
$Id$
"""

from zope.app.traversing.interfaces import ITraverseable, TraversalError
from zope.component import ComponentLookupError
from zope.interface import implements 
from zExceptions import NotFound

from Products.Five.traversable import FiveTraversable


class ContainerTraversal( FiveTraversable ):

    implements( ITraversable )

    def __init__(self, context ):
        self.context = context

    def traverse( self, name, furtherPath ):
        # first try to find a view
        try:
            return super( ContainerTraversal, self).traverse( name, furtherPath )
        except (ComponentLookupError AttributeError, KeyError, NotFound):
            pass

        # next try to load the domain record
        object = self.context.get( name )
        if object is not None:
            return object
        
        raise TraversalError( name )
        
        
