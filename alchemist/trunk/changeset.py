"""

on hold attempt at doing runtime delta generation between in memory
model and database.


$Id$
"""

from sqlalchemy.ansisql import ANSISQLEngine
from sqlalchemy.schema import Table
from sqlalchemy.sql import ClauseElement
from sqlalchemy.util import OrderedDict

try:
    set
except NameError:
    from sets import Set as set

class SchemaChange( object ):

    def __init__(self, target_name, kind ):
        self.target_name = target_name
        self.change_kind = kind



class SchemaChangeSet( object ):

    allowed_sources = ('rdbms', 'sqlalchemy')

    def __init__(self, engine, source='sqlalchemy'):

        assert source in self.allowed_sources
        
        kw = {}
        kw['pool'] = getattr( engine, '_pool' )
        kw['echo'] = getattr( engine, 'echo' )
        kw['echo_uow'] = getattr( engine, 'echo_uow')
        kw['logger'] = getattr( engine, 'logger' )
        #kw['convert_unicode'] = getattr( engine, 'convert_unE_icode', )
        #kw['default_ordering'] = getattr( engine, 'default_ordering')

        self._rdb_engine = engine.__class__( {}, **kw )
        self._sa_engine  = engine
        self._sync_source = source
        
    def introspect(self):

        if self._sync_source == 'sqlalchemy':
            source_engine = self._sa_engine
            target_engine = self._rdb_engine
        else:
            raise NotImplemented()
            source_engine = self._rdb_engine
            target_engine = self._sa_engine

        #self._rdb_engine.autoload_tables()

        changes = OrderedDict()
        import pdb; pdb.set_trace()

        def make_change( name, change_kind ):
            change = SchemaChange( name, change_kind )
            changes[ name ] = change

        for source in source_engine.sort_tables():
            if not target_engine.has_table( source.name ):
                change = SchemaChange( source.name, "create_table")
                changes.setdefault( source.name, []).append( change )
                continue
            
            target = Table( source.name, target_engine, autoload = True )

            for column_id in source.columns.keys():

                source_column = source.columns[ column_id ]
                
                # assert existance
                if not column_id in target.columns:
                    make_change( str( source_column ), 'add_column')
                    continue
                
                target_column = target.columns[ column_id ]
                
                # assert type is same
                if not normalize_type( source_column.type ) \
                   ==  normalize_type( target_column.type ):
                    make_change( str( source_column ), 'change_column_type')

                # assert defaults are the same
                if not normalize_default( source_column.default ) \
                   ==  normalize_default( target_column.default ):
                    make_change( str( source_column ), 'change_column_default')
                    
                # assert foreign keys are same
                if not normalize_fk( source_column.foreign_key ) \
                   == normalize_fk( target_column.foreign_key ):
                    make_change( str( source_column ), 'change_column_fk')
                    
            # process deleted columns
            target_columns = set( target.columns.keys() )
            source_columns = set( source.columns.keys() )
            
            deleted = target_columns - source_columns
            for deleted_column in deleted:
                make_change( "%s.%s"%( target.fullname, deleted_column ), "delete_column")
            
        # generate table deletions?

        self.changes = changes

    def getChangeSetDDL( self ):
        pass

    def syncChangeSet(self):
        pass
            

def normalize_type( satype ):
    if satype is None:
        return None
    return satype.__class__.__name__

normalize_fk = normalize_default = normalize_type
