"""
a decorating mapper for sqlalchemy that utilizes field properties for attribute validation

-- pass on set and structs
-- currently has issues with fk references
"""

from bind import bindClass
from sqlalchemy import mapper

from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary
from zope import interface
import interfaces

class DomainVocabularyUtility( object ):
    
    interface.implements( interfaces.IDomainVocabularyUtility )

    def __init__( self ):
        self._domain_classes = []

    def add( self, klass ):
        self._domain_classes.append( "%s.%s"%(klass.__module__, klass.__name__ ) )

    def __iter__( self ):
        return iter( self._domain_classes )

    def __call__( self ):
        return self

DomainUtility = DomainVocabularyUtility()
    
def DomainVocabulary( context ):
    utility = getUtility( interfaces.IDomainVocabularyUtility )
    return SimpleVocabulary.fromValues( utility )

def bind_mapper( klass, *args, **kw):
    klass_mapper = mapper( klass, *args, **kw )
    bindClass( klass, klass_mapper )
    
    return klass_mapper
