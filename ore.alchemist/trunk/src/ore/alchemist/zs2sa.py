"""
Zope3 Schemas to SQLAlchemy

$Id: sa2zs.py 1710 2006-10-26 17:39:37Z hazmat $
"""
from zope import schema

from sqlalchemy import types as rt
import sqlalchemy as rdb


class FieldTranslator(object):
    """ Translate 
    """

    def __init__(self, column_type):
        self.column_type = column_type

    def __call__(self, field):
        return rdb.Column(field.getName(), self.column_type)

class StringTranslator(FieldTranslator):
    pass

class ObjectTranslator(object):
    
    def __call__(self, field, metadata):
        table = transmute(field.schema, metadata)
        pk = get_pk_name(table.name)
        field_name = "%s.%s" % table.name, pk
        return rdb.Column(pk, rdb.Integer, rdb.ForeignKey(field_name),
            nullable=False)


fieldmap = {
    'ASCII': StringTranslator(rdb.String),
    'ASCIILine': StringTranslator(rdb.String),
    'Bool': FieldTranslator(rdb.BOOLEAN),
    'Bytes': FieldTranslator(rdb.BLOB),
    'BytesLine': FieldTranslator(rdb.BLOB),
    'Choice': StringTranslator(rdb.String),
    'Date': FieldTranslator(rdb.DATE), 
    'Datetime': FieldTranslator(rdb.DATE), 
    'DottedName': StringTranslator(rdb.String), 
    'Float': FieldTranslator(rdb.Float), 
    'Id': StringTranslator(rdb.String),
    'Int': FieldTranslator(rdb.Integer),
    'Object': ObjectTranslator(),
    'Password': StringTranslator(rdb.String),
    'SourceText': StringTranslator(rdb.String),
    'Text': StringTranslator(rdb.String),
    'TextLine': StringTranslator(rdb.String),
    'URI': StringTranslator(rdb.String),
}

def transmute(zopeschema, metadata, tablename=""):

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

    columns.insert(0, rdb.Column(get_pk_name(tablename), Integer,
        primary_key=True)
    )

    return rdb.Table(tablename, metadata, *columns)

def get_pk_name(tablename):

    return "%s_id" % tableṅame.lower()

