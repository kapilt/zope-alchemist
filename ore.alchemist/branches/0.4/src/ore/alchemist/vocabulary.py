"""


$Id$
"""

from ore.alchemist import Session
from zope import interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary


class DatabaseSource( object ):
    """
    a simple implementation of vocabularies on top of a domain model, ideally should
    only be used with small skinny tables.
    """
    interface.implements( IContextSourceBinder )

    def __init__( self, domain_model, token_field, value_field ):
        self.domain_model = domain_model
        self.token_field = token_field
        self.value_field = value_field
        
    def __call__( self, context ):
        session = Session()
        query = session.query( self.domain_model )
        results = query.all()
        keyvalues = [ (getattr( ob, self.token_field), getattr( ob, self.value_field) ) \
                      for ob in results ]
                      
        return SimpleVocabulary.fromItems( keyvalues )
        

class VocabularyTable( object ):
    """
    simple implementation of vocabularies on top of an rdb table. this is a sample implementation
    it doesn't really do well if the vocab table is being modified.
    """

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
