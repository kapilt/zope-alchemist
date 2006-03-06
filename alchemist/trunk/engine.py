"""
SQLAlchemy Zope Transaction Integration.

savepoint integration requires further work in sqlalchemy uow, to snapshot
attributes.

$Id$
"""

import re

from zope.interface import implements

from sqlalchemy.engine import SQLEngine
from sqlalchemy import objectstore
from sqlalchemy.databases.postgres import PGSQLEngine

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

class ZopeEngine( SQLEngine ):
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

    # null implement the builtin sql alchemy transaction interface, zope's driving
    def begin(self):
        print "sa begin"
        pass
    
    def rollback(self):
        print "roll"
        pass

    def commit(self):
        print "comit"
        pass

    def multi_transaction(self, tables, func):
        func()
        
    def transaction(self, func):
        func()

    def do_begin(self, connection):
        print "dobegin"
        pass

    def do_rollback(self, connection):
        print "dorollback"
        pass

    def do_commit(self, connection):
        print "docommit"
        pass


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

    def has_table( self, table_name):
        cursor = self.execute("""\
        select relname from pg_class
        where relname = %(name)s
        """, {'name':table_name}, return_raw=True
        )
        return not not cursor.rowcount

    def create_tables( self, tables=(), drop_existing=False):
        if not tables:
            tables = self.tables.values()

        if drop_existing:
            for table in tables:
                if self.has_table( table.name ):
                    self.drop( table )

        for table in tables:
            if not self.has_table( table.name ):
                print "Create Table", table.name
                self.create( table )
    
register_engine_factory( 'zpgsql', ZopePostgresqlEngine )

