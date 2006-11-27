"""

simple implementation of vocabularies on top of an rdb table. this is a sample implementation
it doesn't really do well if the vocab table is being modified.

$Id$
"""
from sqlalchemy import select
from zope.schema.vocabulary import SimpleVocabulary

class VocabularyTable( object ):

    def __init__( self, table, token_field, value_field ):
        self.table = table
        self.token_field = token_field
        self.value_field = value_field

        terms = select( [getattr( table.c, value_field ),
                         getattr( table.c, token_field ) ] ).execute().fetchall()
        self.vocabulary = SimpleVocabulary.fromItems( terms )
        
    def __getattr__( self, name ):
        return getattr( self.vocabulary, name )
    
    def __call__( self, *args, **kw):
        return self.vocabulary
