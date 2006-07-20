"""
$Id$
"""

from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem

from zope.dottedname.resolve import resolve

from sqlalchemy.orm.mapper import ClassKey
from sqlalchemy import objectstore

from interfaces import IAlchemistContainer

def get_dottedname( klass ):
    return "%s.%s"%(klass.__module__, klass.__name__)


class AlchemistContainer( SimpleItem ):

    implements( IAlchemistContainer )

    def __init__(self, id, domain_class, title=''):

        if isinstance( domain_class, type ):
            domain_class = get_dottedname( domain_class )
        else:
            assert isinstance( domain_class, str)
            
        self.domain_class = domain_class
        self.id = id
        sel

    def getDomainClass( self ):
        return resolve( self.domain_class )

    def add( self, *args, **kw):
        domain_class = self.getDomainClass()
        return domain_class( *args, **kw )

    def get( self, identity, **kwargs):
        domain_class = self.getDomainClass()
        return objectstore.get( domain_class, identity, **kwargs )
    
    def remove( self, object ):
        assert isinstance( object, self.getDomainClass() )
        objectstore.delete( object )

    def __len__(self):
        domain_class = self.getDomainClass()
        return domain_class.count()

        
InitializeClass(AlchemistContainer)    
