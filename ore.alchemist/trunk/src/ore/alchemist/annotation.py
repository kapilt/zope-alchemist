"""
Annotations for Table objects, to annotate as needed, the notion

is that the annotation keys correspond to column, and values correspond
to application specific column metadata.

$Id$
"""

from zope.interface import implements
from interfaces import IModelAnnotation
from sqlalchemy.util import OrderedDict
    
class ModelAnnotation( object ):
    
    implements( IModelAnnotation )
    
    def __init__(self, context, annotation):
        self.context = context
        self.annotation = annotation

    def getDisplayColumns(self):
        from zc.table.column import GetterColumn        
        columns = []
        for i in self.annotation.values():
            if i.get('table_column') is not True:
                continue
            def getter( ob, format, name=i['name']):
                return getattr( ob, name )
            column = GetterColumn( title = i['label'],
                                   name = i['name'],
                                   getter = getter )
            columns.append( column )
        return columns

class TableAnnotation( object ):

    #__slots__ = ("table_name", "_annot", "_options")

    def __init__(self, table_name, **columns):
        self.table_name = table_name
        self._options = {}
        self._annot = OrderedDict()
        if columns:
            for k,c in columns.items():
                self._annot[ k ] = c

    def setOption( self, name, value ):
        self._options[ name ] = value
    def getOption( self, name, default=None ):
        return self._options.get( name, default )
    
    def __call__( self, context ):
        return ModelAnnotation( context, self )


    def __setitem__(self, name, value ):
        self._annot[name] = value

    def get( self, name, default=None ):
        return self._annot.get( name, default )

    def __getitem__(self, anme):
        return self.get( name )

    def values( self ):
        return self._annot.values()

    def __contains__(self, name ):
        marker = object()
        return not marker == self.get( name, marker )
