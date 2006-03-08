##################################################################
#
# (C) Copyright 2006 ObjectRealms, LLC
# All Rights Reserved
#
# This file is part of Alchemist.
#
# Alchemist is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Alchemist is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CMFDeployment; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##################################################################
"""
ddl delta generation between two different engines.

currently supported and tested only with postgresql

supported via ansi standard

  - add table

  - drop column

  - change column default
  
db specific

  - add column 

  - change column foreign key

limitations..

  - lots

  - architecturally no rename support

$Id$
"""

from sqlalchemy import ansisql
from sqlalchemy.schema import Table
from sqlalchemy.sql import ClauseElement
from sqlalchemy.util import OrderedDict

try:
    set
except NameError:
    from sets import Set as set

class ANSISchemaModifier( ansisql.ANSISchemaGenerator, ansisql.ANSISchemaDropper ):

    def __init__(self, source_engine, target_engine, **params):
        self.source_engine = source_engine
        super( ansisql.ANSISchemaGenerator, self).__init__( target_engine, **params)
        assert self.engine is target_engine
        
    # remap
    visit_table_create = ansisql.ANSISchemaGenerator.visit_table
    visit_table_drop   = ansisql.ANSISchemaDropper.visit_table
    
    def visit_add_table( self, change ):
        table = self.resolve( change.name )
        self.visit_table_create( table )
        
    #def visit_drop_table( self, change ):
    #    entity = change.resolveEntity()
    #    self.visit_table_drop( entity )

    def visit_add_column( self, change ):
        raise NotImplemented

    def visit_drop_column( self, change ):
        column = self.resolve( change.name, source=False )
        table  = column.table
        self.append(
            "ALTER TABLE %s DROP COLUMN %s\n"%( table.fullname, column.name )
            )

    def visit_change_column_type( self, change ):
        raise NotImplemented

    def visit_drop_column_constraint( self, change ):
        raise NotImplemented        
    
    def visit_change_column_fk( self, change ):
        raise NotImplemented

    def visit_change_column_default( self, change ):
        # can only change passive defaults
        column = self.resolve( change.name )
        table  = column.table

        if column.default:
            default_expression = str( column.default.args )
            self.append(
                "ALTER TABLE %s ALTER %s SET DEFAULT %s"%( table.fullname, column.name, default_expression )
                )
        else:
            self.append(
                "ALTER TABLE %s ALTER %s DROP DEFAULT\n"%( table.fullname, column.name )
                )

    def resolve( self, name, source=True, exact=True ):
        parts = name.split('.')
        if len(parts) == 3:
            parts = parts[1:] # don't care about schemas..

class PostgresSchemaModifier( ANSISchemaModifier ):

    def visit_add_column( self, change ):
        # pg needs multiple calls.. add col, set default, set contraints
        column = self.resolve( change.name )
        table  = column.table
        column_spec = self.engine.schemagenerator().get_column_specification( column )
        self.append(
            "ALTER TABLE %s ADD COLUMN %s"%( table.fullname, column_spec )
            )

    def visit_change_column_fk( self, change ):
        column = self.resolve( change.name )
        table  = column.table
        foreign_key_target = str(column.foreign_key.column)
        constraint_name = "%s_fk"%(foreign_key_target.replace('.','_') )
        self.append(
            "ALTER TABLE %s ADD CONSTRAINT %s FOREIGN KEY (%s) REFERENCES %s"
            )

    def visit_change_column_type( self, change ):
        s_column = self.resolve( change.name )
        t_column = self.resolve( change.name, source=False)

        # check if its a castable type
        castable = True

        if not castable:
            self.visit_drop_column( change )
            self.visit_add_column( change )
            return

        # if it is castable create a temporary column
        # cast old values to new
        # drop old
        # rename new
        
        table  = s_column.table

        column_temporary_id = "tmp_%s"%column.name
        add_col_change = SchemaChange( "%s.%s"%( table.fullname, column_temporary_id ),
                                       "add_column")
        
        
        self.append(
            "ALTER TABLE %s ADD COLUMN %s %s"%( table.fullname,
                                                column.name,
                                                column.type )
            )



        

class AlterClause( ClauseElement ):

    def accept_visitor(self, visitor):
        pass
    
class SchemaChange( object ):

    def __init__(self, target_name, kind ):
        self.target_name = target_name
        self.change_kind = kind

    def accept_visitor( self, visitor ):
        visit_method = getattr( visitor, 'visit_%s'%self.change_kind )
        visit_method( self )

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
        self._changes = None
        #self.introspect()

    def pprint(self):
        """
        """
        if self._changes is None:
            print "No Changes"

        for c in self._changes.values():
            print c
        
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
