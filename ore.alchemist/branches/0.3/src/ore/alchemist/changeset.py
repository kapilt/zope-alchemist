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

  - we don't track ddl changes, we compare final states and there is no ancestry metadata.
    so architecturally no rename support.

$Id$
"""

from sqlalchemy import ansisql
from sqlalchemy.schema import Table
from sqlalchemy.sql import ClauseElement
from sqlalchemy.util import OrderedDict
from sqlalchemy.engine import ComposedSQLEngine

from ore.alchemist import introspector
from pprint import pprint

try:
    set
except NameError: # be nice to py2.3
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
        
    def visit_drop_table( self, change ):
        entity = change.resolveEntity()
        self.visit_table_drop( entity )

    def visit_add_column( self, change ):
        raise NotImplemented

    def visit_drop_column( self, change ):
        column = self.resolve( change.name, source=False )
        table  = column.table
        self.append(
            "ALTER TABLE %s DROP COLUMN %s\n"%( table.fullname, column.name )
            )

    def visit_add_constraint( self, change ):
        raise NotImplemented

    def visit_drop_constraint( self, change ):
        raise NotImplemented

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

    def __repr__( self):
        return "<SchemaChange %s %s>"%( self.target_name, self.change_kind )
    

def metadata_from_engine( engine ):
    # return a metadata loaded with all tables accessible from the engine
    introspector = introspector.TableIntrospector()
    introspector.bindEngine(  source )
    source = introspector.metadata
    introspector.values() # load all the tables

def changeset( source, target ):
    # if called with an engine, generate the metadata from the relational
    if isinstance( source, ComposedSQLEngine ):
        source = metadata_from_engine( source )
    if isinstance( target, ComposedSQLEngine ):
        target = metadata_from_engine( target )

    return SchemaChangeSet( source, target )

class SchemaChangeSet( object ):

    allowed_sources = ('rdbms', 'sqlalchemy')

    def __init__(self, source, target, source_type='sqlalchemy'):
        self._target_metadata = target
        self._source_metadata  = source
        self._sync_source = source_type
        self._changes = None
        #self.introspect()

    def pprint(self):
        """
        """
        if self._changes is None:
            print "No Changes"
            return
        pprint( self._changes )

    def introspect(self):

        source_metadata = self._source_metadata
        target_metadata = self._target_metadata

        changes = OrderedDict()

        def make_change( name, change_kind ):
            if '.' in name:
                parts = name.split('.')
                for i in range(len(parts)):
                    n = parts[i]
                    if i+1 ==len(parts):
                        local_changes = local_changes.setdefault( n, [] )
                    else:
                        local_changes = changes.setdefault( n, {} )
            else:
                local_changes = changes.setdefault( name, [] )                
            change = SchemaChange( name, change_kind )
            local_changes.append( change )

        for source in source_metadata.table_iterator():
            if not source.name in target_metadata.tables:
                make_change( str( source.name ), "create_table")
                continue
            
            target = target_metadata.tables[ source.name ]

            for column_id in source.columns.keys():

                source_column = source.columns[ column_id ]

                column_name = "%s.%s"%(source.name, column_id)
                print "Colname", column_name, column_id, str( source_column )

                # assert existance
                if not column_id in target.columns:
                    make_change( column_name, 'add_column')
                    continue
                
                target_column = target.columns[ column_id ]
                
                # assert type is same
                if not normalize_type( source_column.type ) \
                   ==  normalize_type( target_column.type ):
                    make_change( column_name, 'change_column_type')

                # assert defaults are the same
                if not normalize_default( source_column.default ) \
                   ==  normalize_default( target_column.default ):
                    make_change( column_name, 'change_column_default')
                    
                # assert foreign keys are same
                if not normalize_fk( source_column.foreign_key ) \
                   == normalize_fk( target_column.foreign_key ):
                    make_change( column_name, 'change_column_fk')
                    
            # process deleted columns
            target_columns = set( target.columns.keys() )
            source_columns = set( source.columns.keys() )
            
            deleted = target_columns - source_columns
            for deleted_column in deleted:
                make_change( "%s.%s"%( target.fullname, deleted_column ), "delete_column")
            
        # generate table deletions?

        self._changes = changes
        self.introspected = True

    def toFile(self, file_name):
        if not self.introspected:
            self.introspect()

    def toString(self):
        if not self.introspected:
            self.introspect()        
            
    def sync(self):
        if not self.introspected:
            self.introspect()        


def normalize_type( satype ):
    if satype is None:
        return None
    return satype.__class__.__name__

normalize_fk = normalize_default = normalize_type
