"""
generate collection traversers for domain classes
"""

from alchemist.traversal.interfaces import IManagedContainer
from alchemist.traversal.collection import CollectionTraverser

from zope.component.zcml import subscriber, adapter
from zope.publisher.interfaces import IPublisherRequest, IPublishTraverse

from z3c.traverser.interfaces import ITraverserPlugin
from z3c.traverser.traverser import PluggableTraverser

def GenerateCollectionTraversal( ctx ):
    
    collection_names = []
    for k,v in ctx.domain_model.__dict__.items():
        if IManagedContainer.providedBy( v ):
            collection_names.append( k )


    
    if not collection_names:
        return
    print "collection names", collection_names

    traverser = CollectionTraverser( *collection_names )
    
    # register collection traversal subscription adapter
    subscriber( ctx.zcml, 
                for_=(ctx.domain_interface, IPublisherRequest ),
                factory=traverser,
                provides=ITraverserPlugin
                )
    
    adapter( ctx.zcml,
             for_ = ( ctx.domain_interface, IPublisherRequest ),
             factory = (PluggableTraverser,),
             provides = IPublishTraverse )
    
