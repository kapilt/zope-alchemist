"""
Annotations for Table objects, to annotate as needed, the notion

is that the annotation keys correspond to column, and values correspond
to application specific column metadata.

$Id$
"""

from zope.interface import implements
from interfaces import IModelAnnotation

    
class ModelAnnotation( object ):
    
    implements( IModelAnnotation )
    
    def __init__(self, context, annotation):
        self.context = context
        self.annotation = annotation

    def getDisplayColumns(self):
        from zc.table.column import GetterColumn        
        columns = []
        for i in self.annotation.values():
            column = GetterColumn( title = i.title,
                                   name = i.title,
                                   getter = lambda ob: getattr( ob, i.title ) )
            columns.append( column )


class TableAnnotation( dict ):

    __slots__ = ("table_name",)

    def __init__(self, table_name, **kw):
        self.table_name = table_name
        super( TableAnnotation, self).__init__( **kw )

    def __call__( self, context ):
        return ModelAnnotation( context, self )

        
class ColumnAnnotation( dict ): pass        
