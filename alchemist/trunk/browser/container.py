

from Products.Five import BrowserView

from zope.table import table

from ore.alchemist.interfaces import IModelAnnotation

class ContainerView( BrowserView ):

    def __init__(self, context, request):
        super( ContainerView, self).__init__( context, request )
        self.info = IModelAnnotation( context )

    def _getTable( self ):


        columns = self.info.getDisplayColumns()

    table = property( _getTable )
    
        
