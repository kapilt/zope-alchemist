"""
$Id$
"""

from zope.component import getAdapter
from zope.interface import implementedBy
from zc.table import table

from ore.alchemist.interfaces import IModelAnnotation, IIModelInterface
from ore.alchemist import named
from Products.Five import BrowserView

class ContainerView( BrowserView ):

    def __init__(self, context, request):
        super( ContainerView, self).__init__( context, request )

        model_iface = None
        # xxx single model interface domains implementations..
        for iface in implementedBy( context.domain_model ):
            if IIModelInterface.isImplementedBy( iface ):
                model_iface = iface
                break
        if model_iface is None:
            raise SyntaxError("domain model has no domain interfaces")
        
        self.info = getAdapter( model_iface, IModelAnnotation, named( model_iface ) )
        
    def _getTable( self ):
        columns = self.info.getDisplayColumns()
        results = self.context.values()

        return table.StandaloneFullFormatter( self.context,
                                              self.request,
                                              results,
                                              visible_column_names = [c.name for c in columns],
                                              columns = columns )
                                              
    table = property( _getTable )
    
        
