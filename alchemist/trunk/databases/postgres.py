"""
$Id$
"""

from Products.alchemist.engine import register_engine_factory, ZopeEngineMixin

from sqlalchemy.databases.postgres import PGSQLEngine, PGSchemaGenerator as saPGSchemaGenerator
from sqlalchemy import schema
from sqlalchemy.orm.topological import QueueDependencySorter
from sqlalchemy import types as satypes

class PGSchemaGenerator( saPGSchemaGenerator ):
    def get_column_specification(self, column, override_pk=False, **kwargs):
        colspec = column.name
        if column.primary_key and isinstance(column.type, satypes.Integer) \
           and (column.default is None or (isinstance(column.default, schema.Sequence) \
                                           and column.default.optional)):
            colspec += " SERIAL"
        else:
            colspec += " " + column.type.engine_impl(self.engine).get_col_spec()
            default = self.get_column_default_string(column)
            if default is not None:
                colspec += " DEFAULT " + default

        if not column.nullable:
            colspec += " NOT NULL"
        if column.primary_key and not override_pk:
            colspec += " PRIMARY KEY"
        if column.foreign_key:
            colspec += " REFERENCES %s(%s)" % (column.foreign_key.column.table.fullname, column.foreign_key.column.name)
            if hasattr(column.foreign_key, 'on_delete') and column.foreign_key.on_delete:
                colspec += " " + column.foreign_key.on_delete
            if hasattr(column.foreign_key, 'on_update') and column.foreign_key.on_update:
                colspec += " " + column.foreign_key.on_update
        return colspec
    
class ZopePostgresqlEngine( ZopeEngineMixin, PGSQLEngine ):
    """
    a sqlalchemy postgres database engine with zope integration

    additional features for doing column constraints ri actions
    and table creation and introspection.
    """
    for property_name in ['__init__',
                          'connect_args',
                          'type_descriptor',
                          'compiler',
                          'schemagenerator',
                          'schemadropper',
                          'defaultrunner',
                          'get_default_schema_name',
                          'last_inserted_ids',
                          'oid_column_name',
                          'pre_exec',
                          'post_exec',
                          '_executemany',
                          'dbapi',
                          'reflecttable']:
        
        locals()[property_name] = getattr( PGSQLEngine, property_name)

    def clear(self):
        self.tables = OrderedDict()

    #def schemagenerator( self, **params ):
    #    return PGSchemaGenerator( self, **params )

    def upgrade_tables( self, tables=(), source='model' ):
        """
        compares the tables with the database representation of them,
        
        source is a string denoting whether we should treat the either
        'sqlalchemy''s model as canonical or the 'database'.
        """
        if not tables:
            tables = self.tables.values()

        changeset_engine = ChangeSetEngine( self, tables )
        changeset_engine.generateDDL()
        table = Table( self.tables['orders'].name, self, autoload=True)

    def autoload(self):
        schema_table = gen_tables.toengine( self )

        for table in schema_table.select( schema_table.c.table_schema == 'public' ).execute().fetchall():
            print "Autoloading", table['table_name']
            table_instance = Table( table['table_name'], self, autoload=True)

    def has_table( self, table_name):
        """
        return boolean whether or not the engine/schema contains this table
        """
        cursor = self.execute("""\
        select relname from pg_class
        where relname = %(name)s
        """, {'name':table_name}, return_raw=True
        )
        return not not cursor.rowcount

    def XE_create_tables( self, tables=(), table_names=(), only_new=True):
        """
        create tables in order, which tables can be specified by keyword args of a sequence
        of table objects or table names.

        only_new flag, only create tables which don't exist, defaults to true.
        """
        if not tables and table_names:
            tables = [ self.tables[name] for name in table_names ]
        elif tables and table_names and isinstance( tables, (list, tuple)):
            tables = list( tables )
            tables.extend( [ self.tables[name] for name in table_names ] )

        if not tables:
            tables = self.tables.values()

        tables = self.sort_tables( tables )
        for table in tables:
            if only_new and self.has_table( table.name ):
                continue
            self.create( table )

    def XE_drop_tables( self, tables=(), table_names=() ):
        """
        drop tables in order, which tables can be specified by keyword args of a sequence
        of table objects or table names.
        """
        if not tables and table_names:
            tables = [ self.tables[name] for name in table_names ]
        elif tables and table_names and isinstance( tables, (list, tuple)):
            tables = list( tables )
            tables.extend( [ self.tables[name] for name in table_names ] )

        if not tables:
            tables = self.tables.values()

        tables = self.sort_tables( tables, reverse=False )
        for table in tables:
            if self.has_table( table.name ):
                self.drop( table )

    def sort_tables(self, tables=None, reverse=True ):
        if tables is None:
            tables = self.tables.values()

        sorter = TableSorter()
        for table in tables:
            sorter.set_table( table.name )
            table.accept_schema_visitor( sorter )

        for table_name in sorter.sort( reverse ):
            yield self.tables[ table_name ]
    
class TableSorter( schema.SchemaVisitor ):

    def __init__(self):
        self._names = []
        self._tuples = []
        
    def set_table( self, table_name ):
        self._names.append( table_name )

    def visit_foreign_key(self, join):
        parent_table = join.column.table.name
        self._tuples.append( ( self._names[-1], parent_table ) )

    def sort(self, reverse=True ):
        sorter = QueueDependencySorter( self._tuples, self._names )
        head =  sorter.sort()
        sequence = []
        def to_sequence( node, seq=sequence):
            seq.append( node.item )
            for child in node.children:
                to_sequence( child )
        to_sequence( head )
        if reverse:
            sequence.reverse()
        return sequence
    


register_engine_factory( 'zpgsql', ZopePostgresqlEngine )

