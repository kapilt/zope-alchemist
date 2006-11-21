"""
Transient Domain Classes managed by SQLAlchemy

$Id$
"""

from zope.interface import implements
from OFS.SimpleItem import SimpleItem
from interfaces import IPersonTable, IAddressTable

class DomainRecord( SimpleItem ): 
    def __init__( self, **kw):
        for k,v in kw.items():
            setattr( self, k, v )

class Person( DomainRecord ):

    implements( IPersonTable )

    id = property( lambda self: str(self.person_id) )

    def Title( self ):
        return "%s %s"%(self.first_name, self.last_name )
    
    def sayHello(self):
        """
        meet my little friend
        """
        return "Hi World"
    
class Address( DomainRecord ):

    implements( IAddressTable )



    

