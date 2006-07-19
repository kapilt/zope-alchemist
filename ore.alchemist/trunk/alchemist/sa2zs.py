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

from zope.interface import Interface, moduleProvides
from zope.interface.interface import InterfaceClass
from zope import schema
from zope.schema.interfaces import ValidationError

from sqlalchemy import types as rt
import sqlalchemy as rdb

from interfaces import ITableSchema, TransmutationException, IAlchemistTransmutation

moduleProvides( IAlchemistTransmutation)

class ColumnTranslator( object ):

    def __init__(self, schema_field):
        self.schema_field = schema_field
        
    def extractInfo( self, column, info ):
        d = {}
        d['title'] = unicode( info.get('title', column.name )  )
        d['description'] = unicode( info.get('description', '' ) )

        # this could be all sorts of things ...
        if isinstance( column.default, rdb.ColumnDefault ):
            default = column.default.arg
        else:
            default = column.default

        # create a field on the fly to validate the default value... 
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

class ColumnVisitor( object ):

    column_type_map = [
        ( rt.Float,  ColumnTranslator( schema.Float )   ),
        ( rt.SmallInteger, ColumnTranslator( schema.Int ) ),
        ( rt.Date, ColumnTranslator( schema.Date ) ),
        ( rt.DateTime, ColumnTranslator( schema.Datetime ) ),
#        ( rt.Time, ColumnTranslator( schema.Datetime ),
        ( rt.Boolean, ColumnTranslator( schema.Bool ) ),
        ( rt.String, ColumnTranslator( schema.ASCII ) ),
        ( rt.Binary, ColumnTranslator( schema.Bytes ) ),
        ( rt.Unicode, ColumnTranslator( schema.Bytes ) ),
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
        
def transmute(  table, annotation=None, __module__='alchemist.derived.interfaces', **kw):
    
    return SQLAlchemySchemaTranslator().translate( table,
                                                   annotation,
                                                   __module__,
                                                   **kw )
