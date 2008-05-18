from zope.publisher.browser import BrowserView
from zope import component

class FavIconView( BrowserView ):

    def __call__( self ):
        resource_dir = component.getAdapter( self.request, name='images')
        icon = resource_dir['favicon.ico']
        return icon.GET()
