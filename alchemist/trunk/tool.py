"""
$Id$
"""

from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem

from Products.Archetypes import public as atapi
from Products.ATSchemaEditorNG import SchemaEditor
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore import CMFCorePermissions as permissions


from content import AlchemistWebContent

class AlchemistModeler( SchemaEditor ):

    meta_type = "Alchemist Modeler"
    
    

class AlchemistTool( UniqueObject, AlchemistModeler, atapi.BaseFolder ):
    
    meta_type = portal_type = "Alchemist Tool"

    id = "portal_alchemist"
    security = ClassSecurityInfo()    

    global_allow = False

    actions = ({
        'id'          : 'view',
        'name'        : 'View',
        'action'      : 'string:${object_url}/folder_contents',
        'permissions' : (permissions.View,)
         },
               
        {
        'id'          : 'edit',
        'name'        : 'Edit',
        'action'      : 'string:${object_url}/base_edit',
        'permissions' : (permissions.ModifyPortalContent,),
         },
               
        {
        'id'          : 'schema_editor',
        'name'        : 'Properties',
        'action'      : 'string:${object_url}/atse_editor',
        'permissions' : (permissions.ModifyPortalContent,),
         },
               
        {
        'id'          : 'metadata',
        'name'        : 'Properties',
        'action'      : 'string:${object_url}/properties',
        'permissions' : (permissions.ModifyPortalContent,),
         },
        )
    

    def __init__(self, *args, **kw):
        pass

    def initializeArchetype( self ):
        atapi.BaseFolder.initializeArchetype( self )
        self.atse_init()
        self.atse_registerObject( AlchemistWebContent,
                                  undeletable_fields=('title',) )
        self._clear()

    def getPeerFactory( self, instance ):

        model = getModelFor( instance )
        peer_factory = model[ instance.portal_type ]

        if peer_factory is None:
            peer_factory = model.loadInstance( instance )

        return peer_factory
            

atapi.registerType( AlchemistTool )


