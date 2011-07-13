##############################################################################
#
# Copyright (c) 2006-2008 Kapil Thangavelu <kapil.foss@gmail.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
Schema Introspection

$Id$
"""

from zope import interface

from sqlalchemy.schema import MetaData, Table
from sqlalchemy import (sql,
                        __version__)
from interfaces import ISchemaIntrospector, ISQLAlchemyMetadata

interface.classImplements( MetaData, ISQLAlchemyMetadata )

# Begining with SQLAlchemy 0.6.x there is no such thing as an 
# information_schema. Instead there is a fully functional Introspector in
# sqlalchemy.engine.reflaction.
# We include the TableSchemaIntrospector for backword compitability, but it is 
# strongly recommended to use the Introspector of SQLAlchemy
if __version__ < "0.6.0":
    
    from sqlalchemy.databases import information_schema
    
    class TableSchemaIntrospector( object ):
    
        interface.implements( ISchemaIntrospector )
        
        def __init__(self, context=None ):
            self._metadata = context
            self._information_schema = None
            
        def keys( self ):
            return self._listTables()
    
        def __iter__( self ):
            return self.keys()
    
        def values( self ):
            return list( self.itervalues() )
    
        def itervalues( self ):
            return self._getTables()
    
        def items( self ):
            return list( self.iteritems() )
    
        def iteritems( self ):
            for table in self.values():
                yield table.name, table
    
        def __len__( self ):
            return len( self.keys() )
    
        def __getitem__( self, key ):
            return self._getTable( key )
    
        def __contains__( self, name):
            return self._hasTable( name )
        
        def get( self, key, default=None ):
            try:
                return self._getTable( key )
            except KeyError:
                return default
    
        #################################
        # bindEngine( schema_name=None ) 
        def bindEngine( self, engine, schema_name=None):
            self._metadata = MetaData( engine, schema_name )
            self._clear()
            
        def bindMetadata( self, metadata ):
            if not metadata.is_bound():
                raise SyntaxError("metadata bind arguement must be bound")
            self._metadata = metadata
            self._clear()
    
        def _getMetadata( self ):
            if self._metadata is None:
                raise AttributeError( "_metadata" )
            return self._metadata
    
        metadata = property( _getMetadata, bindMetadata )
        context = metadata
    
        def _getInformationSchema( self ):
            if self._information_schema is None:
                bound_ischema = MetaData(self.metadata.engine)
                for table in information_schema.ischema.table_iterator():
                    table.tometadata( bound_ischema )
                self._information_schema = bound_ischema
            return self._information_schema
    
        information_schema = property( _getInformationSchema )
    
        def orderedKeys( self, reverse=False ):
            # side affect of loading all the tables.. so we
            # can use their metadata to order based on fk chains
    
            # order is non deterministic, it just preserves ordering
            # of fk dependencies.
            self.values()
    
            for table in self.metadata.table_iterator( reverse ):
                yield table.name
    
        def itemInfo( self, key ):
            return self._getTableInfo( key )
        
        #################################
        # internals
        def _clear(self):
            self._information_schema = None
    
        def _getTableInfo( self, table_name ):
            t = self.information_schema.tables['information_schema.tables']
            s = sql.select()
            if self.metadata.name:
                s.append_whereclause( t.c.table_schema == self.metadata.name )
            s.append_whereclause( t.c.table_name == sql.bindparam("table_name") )
            results = s.execute( table_name = table_name )
            return dict( results[0].items() )
    
        def _getTable( self, table_name ):
            if not table_name in self:
                raise KeyError( table_name )
            d = self._tableConstructorArgs( table_name )
            return Table( **d )
    
        def _tableConstructorArgs( self, table_name ):
            d = {'autoload':True,
                 'useexisting':True}
            if self.metadata.name:
                d['schema'] = self.metadata.name
    
            d[ 'name' ] = table_name
            d[ 'metadata' ] = self.metadata
            return d
        
        def _getTables( self ):
            for table_name in self.keys():
                d = self._tableConstructorArgs( table_name )
                yield Table( **d )
    
        def _listTables( self ):
            t = self.information_schema.tables['information_schema.tables']
            s = sql.select( [t.c.table_name] )
    
            if self.metadata.name:
                s.append_whereclause( t.c.table_schema == self.metadata.name )
            results = s.execute()
            return [ row[ t.c.table_name ] for row in results.fetchall()]
    
        def _hasTable( self, table_name ):
            # go to information schema
            t = self.information_schema.tables['information_schema.tables']
            s = sql.select( [t.c.table_name] )
    
            if self.metadata.name:
                s.append_whereclause( t.c.table_schema == self.metadata.name )
                
            s.append_whereclause( t.c.table_name == sql.bindparam("table_name") )
            results = s.execute( table_name = table_name )
            return results.rowcount == 1
    
    
else:
    
    class TableSchemaIntrospector(object):
    
        interface.implements( ISchemaIntrospector )
        
        def __init__(self, context=None ):
            raise NotImplementedError("The adapter is no longer supported. "
                                      "Use sqlalchemy.engine.reflection.")