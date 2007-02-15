"""
$Id$
"""

from StringIO import StringIO

from Products.Alchemist.tool import AlchemistTool
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



def install_config_ui(self, out):
    portal_panels = getToolByName(self,'portal_controlpanel')
    portal_panels.registerConfiglet( 'alchemist'
                                     , "Relational Databases"
                                     , 'string:${portal_url}/%s/alchemist_view' % TOOLNAME
                                     , ''                 # a condition   
                                     , 'Manage portal'    # access permission
                                     , 'Products'         # section to which the configlet should be added: 
                                     #(Plone,Products,Members) 
                                     , 1                  # visibility
                                     , PROJECTNAME
                                     , 'kupuimages/kupu_icon.gif' # icon in control_panel
                                     , 'Relational Database Wizardardy' # description
                                     , None
                                     )
        
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

    # install config

    portal = self.portal_url.getPortalObject()

    if not AlchemistTool.id in portal.objectIds():
        portal._setObject( AlchemistTool.id, AlchemistTool() )
    
    #portal.portal_types.constructContent( "Alchemist Tool",
    #                                      portal,
    #                                      config.ALCHEMIST_TOOL
    #                                      )

    return out.getvalue()
