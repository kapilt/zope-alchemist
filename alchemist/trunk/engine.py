"""
SQLAlchemy Zope Transaction Integration.

savepoint integration requires further work in sqlalchemy uow, to snapshot
attributes.

$Id$
"""

import re

from zope.interface import implements

from sqlalchemy.engine import SQLEngine
from sqlalchemy import objectstore, Table
from sqlalchemy.util import OrderedDict
from sqlalchemy.schema import SchemaVisitor
from sqlalchemy.databases.postgres import PGSQLEngine, PGSchemaGenerator as saPGSchemaGenerator
from sqlalchemy.mapping.topological import QueueDependencySorter

import transaction
from manager import AlchemyDataManager

def create_engine(uri, opts=None,**kwargs):
    """
    overriden create engine factory function from
    sqlalchemy.engine.create_engine

    we override to create non sqlalchemy contained engines, integrated with zope
    """
    m = re.match(r'(\w+)://(.*)', uri)
    if m is not None:
        (name, args) = m.group(1, 2)
        opts = {}
        def assign(m):
            opts[m.group(1)] = m.group(2)
        re.sub(r'([^&]+)=([^&]*)', assign, args)
        
    kwargs['use_threadlocal'] = True
    engine_factory = get_engine_factory( name )
    print "Opts ", opts
    engine = engine_factory( opts, **kwargs)
    _engines[ uri ] = engine
    return engine

_engines = {}
_engines_factories = {}

def get_engine_factory( name ):
    return _engines_factories[name]

def register_engine_factory( name, factory ):
    _engines_factories[ name ] = factory

def get_engine( dburi, **kwargs ):
    engine =  _engines.get( dburi )
    if engine is None:
        engine = create_engine( dburi, **kwargs )
    engine.do_zope_begin()
    return engine
    

SAVEPOINT_PREFIX = 'alchemy-'

class SANullTransactionMixin( object ):
    """
    null implement the builtin sql alchemy transaction interface, someone else
    is driving.
    """
    def begin(self):
        pass
    
    def rollback(self):
        pass

    def commit(self):
        pass

    def multi_transaction(self, tables, func):
        func()
        
    def transaction(self, func):
        func()

    def do_begin(self, connection):
        pass

    def do_rollback(self, connection):
        pass

    def do_commit(self, connection):
        pass


class ZopeEngine( SANullTransactionMixin, SQLEngine ):
    """
    a sqlalchemy engine that participates in zope transactions, supports savepoints
    for databases implementing ansi savepoints.
    """

    def do_zope_begin( self ):
        if getattr(self.context, 'transaction', None) is None:
            conn = self.connection()
            self.do_begin(conn)
            self.context.transaction = conn

            manager = AlchemyDataManager( self )
            transaction.get().join( manager )

    def do_zope_rollback( self ):
        if self.context.transaction is None:
            return
        self.context.transaction.rollback()
        # not really nesc. sqlalchemy will do attr rollback
        # for clusters, it does need clearing though
        #objectstore.clear()

    def do_zope_rollback_savepoint( self, savepoint_name ):
        if self.context.transaction is None:
            raise RuntimeError("transaction not begun")

        if savepoint_name not in self.context.transaction.savepoints:
            raise RuntimeError("invalid savepoint %s"%savepoint_name)
        self.context.transaction.execute('rollback %s'%str(savepoint_name) )

    def do_zope_savepoint( self ):
        if self.context.transaction is None:
            return

        if self.context.savepoint is None:
            savepoint = 'alchemy-1'
            self.context.savepoints = []
        else:
            savepoint = 'alchemy-%d'%(len(self.context.savepoints))
        self.context.savepoints.append( savepoint )
        objectstore.commit()
        self.context.transaction.execute('SAVEPOINT %s'%savepoint )
        return savepoint

    def do_zope_work( self ):
        if self.context.transaction is None:
            return
        objectstore.commit()

    def do_zope_commit( self ):
        if self.context.transaction is None:
            return
        self.context.transaction.commit()
        self.context.transaction = None

class PGSchemaGenerator( saPGSchemaGenerator ):
    def get_column_specification(self, column, override_pk=False, **kwargs):
        colspec = column.name
        if column.primary_key and isinstance(column.type, types.Integer) and (column.default is None or (isinstance(column.default, schema.Sequence) and column.default.optional)):
            colspec += " SERIAL"
        else:
            colspec += " " + column.type.get_col_spec()
            default = self.get_column_default_string(column)
            if default is not None:
                colspec += " DEFAULT " + default

        if not column.nullable:
            colspec += " NOT NULL"
        if column.primary_key and not override_pk:
            colspec += " PRIMARY KEY"
        if column.foreign_key:
            colspec += " REFERENCES %s(%s)" % (column.column.foreign_key.column.table.fullname, column.column.foreign_key.column.name)
            if hasattr(column.foreign_key, 'on_delete') and column.foreign_key.on_delete:
                colspec += " " + column.foreign_key.on_delete
            if hasattr(column.foreign_key, 'on_update') and column.foreign_key.on_update:
                colspec += " " + column.foreign_key.on_update
        return colspec
    
class ZopePostgresqlEngine( ZopeEngine, PGSQLEngine ):
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

    def schemagenerator( self, **params ):
        return PGSchemaGenerator( self, **params )

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

    def create_tables( self, tables=(), table_names=(), only_new=True):
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

    def drop_tables( self, tables=(), table_names=() ):
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
    
class TableSorter( SchemaVisitor ):

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

