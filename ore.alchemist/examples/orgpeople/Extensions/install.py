"""
$Id$
"""

from Products.alchemist.container import AlchemistContainer
from Products.Five.utilities.marker import mark
from Products.orgpeople.interfaces import IPersonContainer

from StringIO import StringIO

def install( self ):

    out = StringIO()

    print >> out, "Installing Alchemist OrgPeople Example"

    # ensure dependencies
    self.portal_quickinstaller.installProduct('CMFonFive')

    print >> out, "Adding Person Container"
    container = AlchemistContainer( "people", "Products.orgpeople.domain.Person", "People")
    mark( container, IPersonContainer )
    
    portal = self.portal_url.getPortalObject()    
    portal._setObject( container.id, container )

    return out.getvalue()
