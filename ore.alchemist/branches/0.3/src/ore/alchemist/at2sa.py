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

archetypes to sqlalchemy. incomplete port of original in milestone-0. no ref handling here.
$Id$

"""

from sqlalchemy import types as rt
import sqlalchemy as rdb

class ListType( rdb.TypeDecorator, rdb.String ):

    def convert_bind_param( self, value, engine):
        if value is None:
            return None
        return "\n".join( value )

    def convert_result_value( self, value, engine):
        return value.split("\n")

class BooleanType( rdb.TypeDecorator, rdb.Boolean ):

    def convert_bind_param( self, value, engine ):
        if value is None: return None
        return bool( value )

    def convert_result_value( self, value, engine ):
        return value

class DateType( rdb.TypeDecorator, rdb.DateTime ):

    def convert_bind_param( self, value, engine ):
        if value is None:
            return None
        if isinstance( value, DateTime ):
            value = datetime.fromtimestamp( value.timeTime() )

        return value

def peerFactory( klass, metadata ):
    
    klass_name = "%s_serializer"%klass.__name__.lower()
    type_klass = type( klass_name, (object,), {} )
    type_table = transmute( klass.Schema(), metadata, klass_name )
    mapper = rdb.mapper(  type_klass, type_table )

    return type_klass


class FieldTranslator( object ):

    def __init__(self, column_type ):
        self.column_type = column_type
        
    def ident_translate( identifier ):
        if identifier.lower() == 'end':
            return "at_end"
        
        return identifier.lower().replace(' ', '_')

    ident_translate = staticmethod( ident_translate )

    def extractInfo( self, field, info ):
        d = {
            'nullable' : not field.required,
            'name' : self.ident_translate( field.getName() ),
            'type' : self.column_type
            }
        return d

    def __call__( self, field, metadata ):
        d = self.extractInfo( field, info )
        return rdb.Column( **d)

class StringTranslator( FieldTranslator ):
    column_type = rdb.String

class ListTranslator( StringTranslator ):
    column_type = ListType

class DateTranslator( FieldTranslator ):
    column_type = DateType
    
class BooleanTranslator( FieldTranslator ):
    column_type = BooleanType

class FileTranslator( FieldTranslator ):
    column_type = rdb.BLOB 

class FixedPointTranslator( FieldTranslator ):
    column_type = rdb.Numeric
    
    def extractInfo( self, field, info ):
        d = super( FixedPointTranslator, self ).extractInfo( field, info )
        d['precision'] = field.precision
        return d

field_map = {
    'StringField': StringTranslator(),
    'FileField': FileTranslator(),
    'ImageField' : FileTranslator(),
    'PhotoField' : FileTranslator(),
    'DateTimeField': DateTranslator(),
    'FixedPointField' : FixedPointTranslator(),
    'IntegerField' : FieldTranslator( rdb.Integer ),
    'FloatField' : FieldTranslator( rdb.Float ),
    'LinesField' : ListTranslator(),
    'TextField' : StringTranslator(),
    'BooleanField' : BooleanTranslator()
    }


def transmute( archetypes_schema, metadata, table_name=""):

    columns = []

    for field in archetypes_schema.fields():
        class_name = field.__class__.__name__
        translator = field_map.get(class_name)
        if translator is None:
            print "Not translator found for %s" % class_name
            continue

        columns.append(translator(field, metadata))

    if not table_name:
        table_name = archetypes_schema.getName()

    columns.insert(0, rdb.Column(get_pk_name(table_name), Integer,
                                 primary_key=True)
                   )

    return rdb.Table(table_name, metadata, *columns)

def get_pk_name(tablename):

    return "%s_id" % tableṅame.lower()

