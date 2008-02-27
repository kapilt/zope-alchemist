"""

$Id$
"""

from ore.alchemist import Session
from zope import interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema import vocabulary

class DatabaseSource( object ):
    """
    a simple implementation of vocabularies on top of a domain model, ideally should
    only be used with small skinny tables, actual value stored is the id
    """
    interface.implements( IContextSourceBinder )
    
    def __init__( self, domain_model, token_field, value_field ):
        self.domain_model = domain_model
        self.token_field = token_field
        self.value_field = value_field
        
    def constructQuery( self, context ):
        session = Session()
        query = session.query( self.domain_model )
        return query
        
    def __call__( self, context ):
        query = self.constructQuery( context )
        results = query.all()
        keyvalues = [ (getattr( ob, self.token_field), getattr( ob, self.value_field) ) \
                      for ob in results ]
                      
        return vocabulary.SimpleVocabulary.fromItems( keyvalues )

class ObjectSource( DatabaseSource ):
    """
    a vocabulary source, where objects are the values, for suitable for o2m fields.
    """
    
    def constructQuery( self, context ):
        session = Session()
        query = session.query( self.domain_model )
        return query        
        
    def __call__( self, context ):
        query = self.constructQuery( context )
        results = query.all()
        terms = [vocabulary.SimpleTerm( value=ob, token=getattr( ob, self.value_field), title=getattr( ob, self.token_field ) ) \
                 for ob in results ]
        return vocabulary.SimpleVocabulary( terms )


class VocabularyTable( object ):
    """
    a database source implementation which caches values for the lifetime of the app, useful
    if the vocabulary definition is static.
    """
    
    def __init__( self, table, token_field, value_field ):
        self.table = table
        self.token_field = token_field
        self.value_field = value_field
        
        terms = select( [getattr( table.c, value_field ),
                         getattr( table.c, token_field ) ] ).execute().fetchall()
        self.vocabulary = vocabulary.SimpleVocabulary.fromItems( terms )
        
    def __getattr__( self, name ):
        return getattr( self.vocabulary, name )
    
    def __call__( self, *args, **kw):
        return self.vocabulary
