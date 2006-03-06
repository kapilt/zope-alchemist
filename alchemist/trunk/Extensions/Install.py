"""
$Id$
"""

from StringIO import StringIO

from Products.Alchemist import config
from Products.Archetypes import public as atapi
from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.Extensions.utils import install_subskin
from Products.CMFCore.utils import getToolByName

def install_dependencies( self, out ):
    # install dependencies
    portal = getToolByName(self,'portal_url').getPortalObject()
    quickinstaller = portal.portal_quickinstaller
    for dependency in config.DEPENDENCIES:
        print >> out, "Installing dependency %s:" % dependency
        quickinstaller.installProduct(dependency)
        get_transaction().commit(1)
        
def install( self ):

    out = StringIO()
    print >> out, "Installation log of %s:" % config.PROJECTNAME

    # install dependencies
    install_dependencies( self, out )

    # install types 
    classes = atapi.listTypes(config.PROJECTNAME)
    installTypes(self, out, classes, config.PROJECTNAME)

    # install skin
    install_subskin(self, out, config.GLOBALS)

    portal = self.portal_url.getPortalObject()

    portal.portal_types.constructContent( "Alchemist Tool",
                                          portal,
                                          config.ALCHEMIST_TOOL
                                          )

    return out.getvalue()
