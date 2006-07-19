"""

Annotations for Table objects, to annotate as nescessary

$Id$
"""

class TableAnnotation( dict ):

    __slots__ = ("table_name",)

    def __init__(self, table_name, **kw):
        self.table_name = table_name
        super( TableAnnotation, self).__init__( **kw )


class ColumnAnnotation( dict ): pass        
