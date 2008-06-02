
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces import NotFound
from zope.publisher.browser import BrowserView
from zope.contentprovider.interfaces import IContentProvider
from zope.viewlet.interfaces import IViewlet
import zope.security.checker

import zope.interface

class MethodPublisher( BrowserView, zope.location.Location ):

    zope.interface.implements( IBrowserPublisher )

    __Security_checker__ = zope.security.checker.NamesChecker((
        '__call__', 'browserDefault', 'publishTraverse'))
    
    def __init__( self, context, request, method):
        self.context = context
        self.request = request
        self.method = method

    def browserDefault( self, request ):
        return self, ()

    def publishTraverse( self, request, name ):
        # shouldn't ever be sub traversing from here
        raise NotFound( self, name, request )
    
    def __call__( self ):
        return self.method()

    def __getParent(self):
        return hasattr(self, '_parent') and self._parent or self.context

    def __setParent(self, parent):
        self._parent = parent

    __parent__ = property(__getParent, __setParent)


class ViewletTraversableMixin( object ):

    def publishTraverse(self, request, name):
        # could encapsulate to separate view
        value = getattr( self, name, None)
        if not callable( value ):
            raise NotFound(self, name, request)
        return MethodPublisher( self, self.request, self.viewlets ) 

    provider_name = ""
    
    def viewlets( self ):
        """
        traversable viewlets
        """
        # find the action in the request
        action = None
        for i in self.request.form.keys():
            if 'actions' in i:
                action = i
                break

        # XXX - send error status message
        if not action:
            return ""

        # do a dance to find the applicable viewlet
        # we need to know which viewlet managers we're using to do
        # this.
        
        # first lookup the edit manager
        viewlet_manager = zope.component.queryMultiAdapter(
            ( self.context, self.request, self ),
            IContentProvider,
            self.provider_name
            )

        # next lookup its viewlets
        viewlets = zope.component.getAdapters(
            (self.context, self.request, self, viewlet_manager),
            IViewlet
            )

        active_viewlet = None
        
        # determine the applicable viewlet based on prefix
        for name, viewlet in viewlets:
            prefix = getattr( viewlet, 'prefix', None)
            if prefix and action.startswith( prefix ):
                active_viewlet = viewlet

        # render the viewlet
        active_viewlet.update()
        rendered =  active_viewlet.render()
        return rendered    
