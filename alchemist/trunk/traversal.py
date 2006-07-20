"""
$Id$
"""

from zope.app.traversing.interfaces import ITraversable, TraversalError
from zope.component import ComponentLookupError
from zope.interface import implements 
from zExceptions import NotFound

from Products.Five.traversable import FiveTraversable

class ContainerTraversal( FiveTraversable ):

    implements( ITraversable )

    def __init__(self, context ):
        self._subject = context

    def traverse( self, name, furtherPath ):

        # first try to find a view
        try:
            next = super( ContainerTraversal, self).traverse( name, furtherPath )
            if next is not None:
                return next
        except (ComponentLookupError, AttributeError, KeyError, NotFound, TraversalError):
            pass

        # next try to load the domain record

        # ugh.. XXX temp hack convert to int
        try:
            oid = int( name )
        except:
            oid = name
            
        object = self._subject.get( oid )
        if object is not None:
            return object
        
        raise TraversalError( name )
        
        
