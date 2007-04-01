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
Zope3 Schemas to SQLAlchemy

$Id: sa2zs.py 1710 2006-10-26 17:39:37Z hazmat $
"""
from zope import schema
import sqlalchemy as rdb

class FieldTranslator( object ):
    """ Translate a zope schema field to an sa  column
    """

    def __init__(self, column_type):
        self.column_type = column_type

    def extractInfo( self, field, info ):
        d = {}
        d['name'] = field.getName()
        if field.required:
            d['nullable'] = False
        d['default'] = field.default
        d['type'] = self.column_type        
        return d
    
    def __call__(self, field, annotation):
        d = self.extractInfo( field, annotation )
        return rdb.Column( **d)

class StringTranslator(FieldTranslator):
    
    column_type = rdb.String

    def __init__(self, column_type=None):
        self.column_type = column_type or self.column_type
        
    def extractInfo( self, field, info ):
        d = super( StringTranslator, self ).extractInfo( field, info )
        if schema.interfaces.IMinMaxLen.providedBy( field ):
            ti['length'] = field.max_length
        return d

class ObjectTranslator(object):
    
    def __call__(self, field, metadata):
        table = transmute(field.schema, metadata)
        pk = get_pk_name(table.name)
        field_name = "%s.%s" % table.name, pk
        return rdb.Column(pk, rdb.Integer, rdb.ForeignKey(field_name),
            nullable=False)


fieldmap = {
    'ASCII': StringTranslator(),
    'ASCIILine': StringTranslator(),
    'Bool': FieldTranslator(rdb.BOOLEAN),
    'Bytes': FieldTranslator(rdb.BLOB),
    'BytesLine': FieldTranslator(rdb.BLOB),
    'Choice': StringTranslator(),
    'Date': FieldTranslator(rdb.DATE), 
    'Datetime': FieldTranslator(rdb.DATE), 
    'DottedName': StringTranslator(),
    'Float': FieldTranslator(rdb.Float), 
    'Id': StringTranslator(),
    'Int': FieldTranslator(rdb.Integer),
    'Object': ObjectTranslator(),
    'Password': StringTranslator(),
    'SourceText': StringTranslator(),
    'Text': StringTranslator(),
    'TextLine': StringTranslator(),
    'URI': StringTranslator(),
}

def transmute(zopeschema, metadata, tablename="", add_primary=True):

    columns = []

    for name, field in schema.getFieldsInOrder(zopeschema):
        classname = field.__class__.__name__
        translator = fieldmap.get(classname)
        if translator is None:
            print "Not translator found for %s" % classname
            continue

        columns.append(translator(field, metadata))

    if not tablename:
        tablename = zopeschema.getName()[1:]
        
    if add_primary:
        columns.insert(0, rdb.Column(get_pk_name(tablename), rdb.Integer,
                                     primary_key=True)
                       )

    return rdb.Table(tablename, metadata, *columns)

def get_pk_name(tablename):

    return "%s_id" % tablename.lower()

