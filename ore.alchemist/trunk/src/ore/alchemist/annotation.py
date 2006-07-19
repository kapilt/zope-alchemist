"""
Annotations for Table objects, to annotate as needed, the notion

is that the annotation keys correspond to column, and values correspond
to application specific column metadata.

$Id$
"""

class TableAnnotation( dict ):

    __slots__ = ("table_name",)

    def __init__(self, table_name, **kw):
        self.table_name = table_name
        super( TableAnnotation, self).__init__( **kw )


class ColumnAnnotation( dict ): pass        
