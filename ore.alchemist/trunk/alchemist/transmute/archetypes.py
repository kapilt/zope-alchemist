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
$Id$
"""

import sqlalchemy as rdb
from base import AlchemistTranslation

class ListType( rdb.TypeDecorator, rdb.String ):

    def convert_bind_param( self, value, engine):
        if value is None:
            return None
        return "<n/>".join( value )

    def convert_result_value( self, value, engine):
        return value.split("<n/>")

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
            value = DateFromTicks( DateTime.timeTime() )

        # psycopg1 specific hack
        if hasattr( engine, 'version') and engine.version == 1:
            return engine.module.TimestampFromMx( value )

        return value


class ArchetypesFieldTranslator( object ):

    def __init__( self, metadata, table_name ):
        self.collection = metadata
        self.table_name = table_name
        
    def ident_translate( identifier ):
        if identifier.lower() == 'end':
            return "at_end"
        
        return identifier.lower().replace(' ', '_')

    ident_translate = staticmethod( ident_translate )

    def getDefaultArgs( self, field, use_field_default=False ):
        args = []

        #if use_field_default and field.default:
        #    args.append( rdb.PassiveDefault( field.default ) )
        kwargs = {
            'nullable' : not field.required,
            'key' : field.getName(),            
            }
        return args, kwargs
     
    # hack around some objects with bad metadata fields.
    field_overrides = {('allowDiscussion', 'StringField'):'visit_BooleanField'}

    def visit( self, field ):
        field_visitor = "visit_%s"%( field.__class__.__name__ )
        visitor = getattr( self, field_visitor, None )

        if visitor is None:
            print "No Visitor", field_visitor, field.getName()
            return None

        override_key = (field.getName(), field.__class__.__name__)
        if override_key in self.field_overrides:
            visitor = getattr( self, self.field_overrides[override_key] )
        
        return visitor( field )
    
    def visit_StringField( self, field ):
        
        args, kwargs = self.getDefaultArgs( field, use_field_default=True )
            
        return rdb.Column(
            self.ident_translate( field.getName() ),
            rdb.String(4000),
            *args,
            **kwargs )

    visit_TextField = visit_StringField

    def visit_LinesField( self, field ):
        
        args, kwargs = self.getDefaultArgs( field, use_field_default=True )
            
        return rdb.Column(
            self.ident_translate( field.getName() ),
            ListType(4000),
            *args,
            **kwargs )

    def visit_FileField( self, field ):
        args, kwargs = self.getDefaultArgs( field )

        return rdb.Column(
            self.ident_translate( field.getName() ),
            rdb.Binary(),
            *args,
            **kwargs)

    visit_ImageField = visit_FileField
    visit_PhotoField = visit_FileField

    def visit_BooleanField( self, field ):
        args, kwargs = self.getDefaultArgs( field, use_field_default=True )

        return rdb.Column(
            self.ident_translate( field.getName() ),
            BooleanType(),
            *args,
            **kwargs )

    def visit_IntegerField( self, field ):
        args, kwargs = self.getDefaultArgs( field, use_field_default=True )

        return rdb.Column(
            self.ident_translate( field.getName() ),
            rdb.Integer(),
            *args,
            **kwargs )

    def visit_FloatField( self, field ):
        args, kwargs = self.getDefaultArgs( field, use_field_default=True )

        return rdb.Column(
            self.ident_translate( field.getName() ),
            rdb.Float(),
            *args,
            **kwargs )        

    def visit_FixedPointField( self, field ):
        args, kwargs = self.getDefaultArgs( field, use_field_default=True )
        return rdb.Column(
            self.ident_translate( field.getName() ),
            rdb.Numeric( precision = field.precision ),
            *args,
            **kwargs )

    def visit_DateTimeField( self, field ):
        args, kwargs = self.getDefaultArgs( field, use_field_default=True )
        return rdb.Column(
            self.ident_translate( field.getName() ),
            DateType(),
            *args,
            **kwargs )            

    def visit_ReferenceField( self, field ):
        table = rdb.Table(
            "%s_%s"%(self.table_name, self.ident_translate( field.getName() )),
            self.collection,
            rdb.Column('source',
                   rdb.String(50),
                   rdb.ForeignKey('%s.uid'%self.table_name),
                   nullable=False),
            rdb.Column('target',
                   rdb.String(50),
                   rdb.ForeignKey('object_identity.uid'),
                   nullable=False)
            )


        table.reference_name = self.ident_translate( field.getName() )
        return table

class ArchetypesSchemaTranslator( object ):

    translator_factory = ArchetypesFieldTranslator

    def __init__(self, context):
        self.context = context
    
    def translate( self, metadata, table_name):
        relation_tables = []
        primary_columns = [ rdb.Column( "uid", rdb.String(50), primary_key=True ) ]

        field_translator = self.translator_factory( metadata, table_name )
        
        d = {}
        for field in self.context.fields():
            # filter badness from fields with same speling but different captilization.
            field_name = self.ident_translate( field.getName() )
            if field_name in d:
                continue

            result = field_translator.visit( field )

            if result is None:
                continue
            elif isinstance( result, rdb.Column):
                primary_columns.append( result )
            elif isinstance( result, rdb.Table ):
                relation_tables.append( result )
            else:
                print "Unexpected", result
                raise RuntimeError

            d[field_name] = None


        # define type primary table
        type_table = rdb.Table( table_name,
                                self.engine,
                                *primary_columns )        
        
        properties = {}        
        for relation_table in relation_tables:
            properties[ relation_table.reference_name ] = rdb.relation( identity.mapper, relation_table, lazy = False)            

        return AlchemistTranslation( type_table, relation_tables, properties )

