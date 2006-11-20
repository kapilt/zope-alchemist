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
    
    def sayHello(self):
        """
        meet my little friend
        """
        return "Hi World"
    
class Address( DomainRecord ):

    implements( IAddressTable )



    

