"""
$Id$
"""

from sqlalchemy.ansisql import ANSISQLEngine
from sqlalchemy.schema import Table
from sqlalchemy.sql import ClauseElement

class SQLChange( object ):

class ChangeDropTable( SQLChange ):

    def __init__(self, name):
        self.name = name

class ChangeDropColumn( SQLChange ):
    pass

class ChangeDropConstraint( SQLChange ):
    pass

class ChangeColumn( SQLChange ):
    pass

class ChangeSetEngine( ANSISQLEngine ):

    allowed_sources = ('rdbms', 'sqlalchemy')

    def __init__(self, engine, tables, source='sqlalchemy'):

        assert source in self.allowed_sources
        
        kw = {}
        kw['pool'] = getattr( engine, '_pool' )
        kw['echo'] = getattr( engine, 'echo' )
        kw['echo_uow'] = getattr( engine, 'echo_uow']        
        kw['logger'] = getattr( engine, 'logger' )
        kw['convert_unicode'] = getattr( engine, 'convert_unicode')
        kw['default_ordering'] = getattr( engine, 'default_ordering')

        super( ANSISQLEngine, self).__init__( **kw )

        self._parent_engine = engine
        self._parent_tables = [table.name for table in tables]
        self._sync_source = source
        
    def differences(self):
        for table_name in self._parent_tables:
            rdb_table = Table( table_name, autoload = True )
            parent_table = self._parent_engine.tables[ table_name ]

            if self._sync_source == 'sqlalchemy':
                source = parent_table
                target = rdb_table
            else:
                source = rdb_table
                target = parent_table

            
            
