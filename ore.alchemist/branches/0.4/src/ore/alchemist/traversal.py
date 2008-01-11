
from zope.app.container.traversal import ItemTraverser
from zope.publisher.interfaces import NotFound
from zope.component import queryMultiAdapter

class ContainerTraverser( ItemTraverser ):
    # basically custom traverser that tries to coerce to
    # a name to integer before doing a sql lookup if
    # if the conversion fails, than its likley not an 
    # contained object ( need separate traversers for other )
    # multi primary keys
    
    def publishTraverse(self, request, name):
        """See zope.publisher.interfaces.IPublishTraverse"""
        try: # check if its directly by primary key
            key = int( name )
            return self.context[key]
        except ValueError, KeyError:
            view = queryMultiAdapter((self.context, request), name=name)
            if view is not None:
                return view
        raise NotFound(self.context, name, request)

