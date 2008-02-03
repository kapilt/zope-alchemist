"""
$Id: $
"""

from zope import interface
from zope.publisher.interfaces import NotFound
from z3c.traverser import interfaces

class CollectionTraverserTemplate(object):
    """A traverser that knows how to look up objects by sqlalchemy collections """

    interface.implements(interfaces.ITraverserPlugin)

    collection_attributes = ()
    
    def __init__(self, container, request):
        self.context = container
        self.request = request

    def publishTraverse(self, request, name):
        """See zope.publisher.interfaces.IPublishTraverse"""
        
        for cname in self.collection_attributes:
            if cname == name:
                container = getattr( self.context, cname )
                return container

def CollectionTraverser( *names ):
    return type( "CollectionsTraverser", (CollectionTraverserTemplate, ), { collection_attributes: names} )

