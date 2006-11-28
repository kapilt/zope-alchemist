"""
Transient Domain Classes managed by SQLAlchemy

$Id$
"""

from zope.interface import implements
from OFS.SimpleItem import SimpleItem
from interfaces import IPersonTable, IAddressTable

class DomainRecord( SimpleItem ):
#class DomainRecord( object ):

    def foolish( self ):
        import pdb; pdb.set_trace()
        return None

    _p_jar = property( lambda self: None, foolish )
    
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




    

