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
SQLAlchemy to Zope3 Schemas

$Id$
"""

import sys
from zope.interface import Interface, moduleProvides, directlyProvides
from zope.interface.interface import InterfaceClass
from zope import schema
from zope.schema.interfaces import ValidationError
from zope.component import provideAdapter

from sqlalchemy import types as rt
import sqlalchemy as rdb
from sqlalchemy import attributes

from interfaces import ITableSchema, TransmutationException, IAlchemistTransmutation, \
     IModelAnnotation, IIModelInterface

class ValidatedProperty( object ):
    """
    Computed attributes based on schema fields that collaborate with sqlalchemy
    properties, and provide validation, error messages, and default values.
    """
    def __init__(self, field, prop, name=None):
        self.__field = field
        self.__prop = prop
        self.__name = name or field.__name__
    
    def __get__(self, inst, klass):
        if inst is None:
            return self
        return self.__prop.__get__( inst, klass )
    
    def __set__(self, inst, value):
        field = self.__field.bind(inst)
        field.validate(value)
        if field.readonly and inst.__dict__.has_key(self.__name):
            raise ValueError(self.__name, 'field is readonly')
        self.__prop.__set__( inst, value )

    def __delete__(self, obj):
        if self.__field.readonly and inst.__dict__.has_key(self.__name):
            raise ValueError(self.__name, 'field is readonly')
        self.__prop.__delete__( obj )

def providedByInstances( klass ):
    """ return all the interfaces implemented by instances of a klass.. why isn't this in z.i?
    """
    class_provides = getattr( klass, '__provides__', None )
    if class_provides is None:
        return ()
    return iter( class_provides._implements )
    
def bindClass( klass, mapper=None ):
    """ insert validated properties into a class based on its primary mapper, and model schemas
    """
    # compile the klass mapper, this will add instrumented attributes to the class
    # we could alternatively do.. mapper.compile() compiles all extant mappers

    if mapper is None:
        mapper = getattr( klass, 'mapper')

    mapper.compile()

    # find all the model schemas implemented by the class
    for iface in providedByInstances( klass ):
        if not IIModelInterface.providedBy( iface ):
            continue

        # for any field in the schema, see if we have an sa property
        for field_name in schema.getFieldNames( iface ):
            v = klass.__dict__.get( field_name )

            # if so then wrap it in a field property
            if not isinstance( v, attributes.InstrumentedAttribute):
                continue
            field = iface[ field_name ]
            vproperty = ValidatedProperty( field, v, field_name )
            setattr( klass, field_name, vproperty )


moduleProvides( IAlchemistTransmutation )

class ColumnTranslator( object ):

    def __init__(self, schema_field):
        self.schema_field = schema_field
        
    def extractInfo( self, column, info ):
        d = {}
        d['title'] = unicode( info.get('title', column.name )  )
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
        d = self.extractInfo( column, annotation)
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

        if column_handler is None:
            raise TransmutationException("no column handler for %r"%column)

        return column_handler( column, self.info )


class SQLAlchemySchemaTranslator( object ):

    def translate( self, table, annotation, __module__, **kw):

        annotation = annotation or {}
        visitor = ColumnVisitor(annotation)
        iname ='I%sTable'%table.name

        d = {}
        for column in table.columns:
            if annotation.get( column.name, {}).get('omit', False ):
                continue
            for column in table.columns:
                d[ column.name ] = visitor.visit( column )

        DerivedTableSchema = InterfaceClass( iname,
                                             (ITableSchema,),
                                             attrs=d,
                                             __module__ = __module__ )
        return DerivedTableSchema
        
def transmute(  table, annotation=None, __module__=None, **kw):

    # if no module given, use the callers module
    if __module__ is None:
        __module__ = sys._getframe(1).f_globals['__name__']

    z3iface = SQLAlchemySchemaTranslator().translate( table,
                                                      annotation,
                                                      __module__,
                                                      **kw )

    # mark the interface itself as being model driven
    directlyProvides( z3iface, IIModelInterface)
        
    # provide a named annotation adapter to go from the iface back to the annotation
    if annotation is not None:
        name = "%s.%s"%(z3iface.__module__, z3iface.__name__)
        provideAdapter( annotation, adapts=(IIModelInterface,), provides=IModelAnnotation, name = name )

    return z3iface
