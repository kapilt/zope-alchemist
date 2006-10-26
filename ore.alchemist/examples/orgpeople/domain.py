"""
Transient Domain Classes managed by SQLAlchemy

$Id$
"""

from zope.interface import implements
from interfaces import IPersonTable, IAddressTable

class DomainRecord( object ): 
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



    

