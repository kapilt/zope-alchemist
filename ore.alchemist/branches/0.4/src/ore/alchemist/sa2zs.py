##################################################################
#
# (C) Copyright 2006-2007 ObjectRealms, LLC
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
SQLAlchemy to Zope3 Schemas

$Id$
"""

from zope import interface, schema, component
from zope.interface.interface import InterfaceClass
from zope.schema.interfaces import ValidationError

from sqlalchemy.util import OrderedDict
from sqlalchemy import types as rt
import sqlalchemy as rdb

from interfaces import ITableSchema, TransmutationException, IAlchemistTransmutation, \
     IModelDescriptor, IIModelInterface

interface.moduleProvides( IAlchemistTransmutation )

class TableAnnotation( object ):
    """
    Annotations for Table objects, to annotate as needed, the notion
    is that the annotation keys correspond to column, and values correspond
    to application specific column metadata.
    """

    _marker = object()
    
    def __init__(self, table_name, columns=(), properties=(), schema_order=(), listing_columns=(), order_by=()):
        self.table_name = table_name
        self._options = {}
        self._annot = OrderedDict()

        for info in columns:
            self._annot[ info['name'] ] = info

        self.properties = properties
        self.schema_order = schema_order        
        self.listing_columns = listing_columns
        self.order_by = order_by

    def setOption( self, name, value ):
        self._options[ name ] = value
        
    def getOption( self, name, default=None ):
        return self._options.get( name, default )

    def __call__( self, iface ):
        return self
    
    def __setitem__(self, name, value ):
        self._annot[name] = value

    def get( self, name, default=None ):
        return self._annot.get( name, default )

    def __getitem__(self, name):
        return self.get( name )

    def values( self ):
        return self._annot.values()

    def __contains__(self, name ):
        return not self._marker == self.get( name, self._marker )


class ColumnTranslator( object ):

    def __init__(self, schema_field):
        self.schema_field = schema_field
        
    def extractInfo( self, column, info ):
        d = {}
        d['title'] = unicode( info.get('label', column.name )  )
        d['description'] = unicode( info.get('description', '' ) )
        d['required'] = not column.nullable

        # this could be all sorts of things ...
        if isinstance( column.default, rdb.ColumnDefault ):
            default = column.default.arg
        else:
            default = column.default

        # create a field on the fly to validate the default value... 
        # xxx there is a problem with default value somewhere in the stack
        # 
        validator = self.schema_field()
        try:
            validator.validate( default )
            d['default'] = default
        except ValidationError:
            pass
        
        return d

    def __call__( self, column, annotation ):
        info = annotation.get( column.name, {} )
        d = self.extractInfo( column, info)
        return self.schema_field( **d )

class SizedColumnTranslator( ColumnTranslator ):

    def extractInfo( self, column, info ):
        d = super( SizedColumnTranslator, self).extractInfo( column, info )
        d['max_length'] = column.type.length
        return d
        

class ColumnVisitor( object ):

    column_type_map = [
        ( rt.Float,  ColumnTranslator( schema.Float )   ),
        ( rt.SmallInteger, ColumnTranslator( schema.Int ) ),
        ( rt.Date, ColumnTranslator( schema.Date ) ),
        ( rt.DateTime, ColumnTranslator( schema.Datetime ) ),
#        ( rt.Time, ColumnTranslator( schema.Datetime ),
        ( rt.TEXT, ColumnTranslator( schema.Text ) ),
        ( rt.Boolean, ColumnTranslator( schema.Bool ) ),
        ( rt.String, SizedColumnTranslator( schema.TextLine ) ),
        ( rt.Binary, ColumnTranslator( schema.Bytes ) ),
        ( rt.Unicode, SizedColumnTranslator( schema.Bytes ) ),
        ( rt.Numeric, ColumnTranslator( schema.Float ) ),
        ( rt.Integer,  ColumnTranslator( schema.Int ) )
        ]

    def __init__(self, info ):
        self.info = info or {}

    def visit( self, column ):
        column_handler = None
        
        for ctype, handler in self.column_type_map:
            if isinstance( column.type, ctype ):
                if isinstance( handler, str ):
                    # allow for instance method customization
                    handler = getattr( self, handler )
                column_handler = handler
                break

        if column_handler is None:
            raise TransmutationException("no column handler for %r"%column)

        return column_handler( column, self.info )


class SQLAlchemySchemaTranslator( object ):

    def applyProperties( self, field_map, properties ):
        # apply manually overridden fields/properties
        order_max = max( [field.order for field in field_map.values()] )
        for name in properties:
            field = properties[ name ]
            # append new fields
            if name not in field_map:
                order_max = order_max + 1
                field.order = order_max
            # replace in place old fields
            else:
                field.order = field_map[name].order
            field_map[ name ] = field

    def applyOrdering( self, field_map, schema_order ):
        """ apply global ordering to all fields, any fields not specified have ordering
            preserved, but are now located after fields specified in the schema order, which is
            a list of field names.
        """
        self.verifyNames( field_map, schema_order ) # verify all names are in present
        visited = set() # keep track of fields modified
        order = 1  # start off ordering values
        for s in schema_order:
            field_map[s].order = order
            visited.add( s )
            order += 1
        remainder = [ (field.order, field) for field_name, field in field_map.items() if field_name not in visited ]
        remainder.sort()
        for order, field in remainder:
            field.order = order
            order += 1
            
    def verifyNames( self, field_map, names ):
        for n in names:
            if not n in field_map:
                raise AssertionError("invalid field specified  %s"%( n ) )
        
    def generateFields( self, table, annotation ):
        visitor = ColumnVisitor(annotation)        
        d = {}
        for column in table.columns:
            if annotation.get( column.name, {}).get('omit', False ):
                continue
            d[ column.name ] = visitor.visit( column )
        return d
    
    def translate( self, table, annotation, __module__, **kw):
        annotation = annotation or TableAnnotation( table.name ) 
        iname = kw.get('interface_name') or 'I%sTable'%table.name

        field_map = self.generateFields( table, annotation )

        # apply manually overridden fields/properties
        properties = kw.get('properties', None) or annotation.properties
        if properties:
            self.applyProperties( field_map, properties )
        
        # apply global schema ordering
        schema_order = kw.get('schema_order', None) or annotation.schema_order
        if schema_order:
            self.applyOrdering( field_map, schema_order )

        # verify table columns
        #if annotation.listing_columns:
        #    self.verifyNames( field_map, annotation.listing_columns )


        # extract base interfaces
        if 'bases' in kw:
            bases = (ITableSchema,) + kw.get('bases')
        else:
            bases = (ITableSchema,)
        DerivedTableSchema = InterfaceClass( iname,
                                             attrs = field_map,
                                             bases = bases,
                                             __module__ = __module__ )

        return DerivedTableSchema
        
def transmute(  table, annotation=None, __module__=None, **kw):
    #import pdb; pdb.set_trace()
    # if no module given, use the callers module
    if __module__ is None:
        import sys
        __module__ = sys._getframe(1).f_globals['__name__']


    z3iface = SQLAlchemySchemaTranslator().translate( table,
                                                      annotation,
                                                      __module__,
                                                      **kw )

    # mark the interface itself as being model driven
    interface.directlyProvides( z3iface, IIModelInterface)
        
    # provide a named annotation adapter to go from the iface back to the annotation
    if annotation is not None:
        name = "%s.%s"%(z3iface.__module__, z3iface.__name__)
        component.provideAdapter( annotation,
                                  adapts=(IIModelInterface,),
                                  provides=IModelDescriptor, name = name )

    return z3iface


def transmute_mapper( mapper, annotation=None, __module__=None, **kw):
    pass
    
