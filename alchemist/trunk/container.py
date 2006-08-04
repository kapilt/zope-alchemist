"""
$Id$
"""

from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem

from zope.dottedname.resolve import resolve
from zope.interface import implements

from sqlalchemy.orm.query import Query
from sqlalchemy import objectstore

from ore.alchemist import named
from ore.alchemist.interfaces import IAlchemistContainer


class AlchemistContainer( SimpleItem ):

    implements( IAlchemistContainer )

    def __init__(self, id, domain_class, title=''):

        if isinstance( domain_class, type ):
            domain_class = named( domain_class )
        else:
            assert isinstance( domain_class, str)
            
        self.domain_class = domain_class
        self.id = id
        self.title = title
        
    def getDomainClass( self ):
        return resolve( self.domain_class )

    domain_model = property( getDomainClass )
    
    def add( self, *args, **kw):
        return self.domain_model( *args, **kw )

    def get( self, identity, **kwargs):
        return objectstore.get( self.domain_model, identity, **kwargs )
    
    def remove( self, object ):
        assert isinstance( object, self.domain_model )
        objectstore.delete( object )

    def values(self, offset=0, limit=20):
        query = objectstore.query( self.domain_model )
        return [res.__of__(self) for res in query.select()]

    def query(self, **kw ):
        query = objectstore.query( self.domain_model )
        return [ res.__of__(self) for res in query.select_by( **kw )]

    def __len__(self):
        return Query( self.domain_model ).count()

InitializeClass(AlchemistContainer)    
