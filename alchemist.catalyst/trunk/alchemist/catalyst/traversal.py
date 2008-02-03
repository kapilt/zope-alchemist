"""
generate traversers for domain classes, if specified in configuration.
"""
from alchemist.traversal.interfaces import IManaagedContainer
from alchemist.traversal.collection import CollectionTraverser

def GenerateCollectionTraversal( ctx ):
    
    collection_names = []
    for k,v in ctx.domain_model.__dict__.items():
         if IManagedContainer.providedBy( v ):
             collection_names.append( k )
    
    traverser = CollectionTraverser( *collection_names )
    
    # register collection traversal subscription adapter
    
    