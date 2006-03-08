##################################################################
#
# (C) Copyright 2006 ObjectRealms, LLC
# All Rights Reserved
#
# This file is part of Alchemist.
#
# Alchemist is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Alchemist is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CMFDeployment; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##################################################################
"""
$Id$
"""

from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem

from Products.Archetypes import public as atapi

from Products.ATSchemaEditorNG import SchemaEditor
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore import CMFCorePermissions as permissions
from Products.CMFCore.TypesTool import FactoryTypeInformation

from content import AlchemistWebContent
from model import getModelFor

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
        self._type_map = {}

    def initializeArchetype( self ):
        atapi.BaseFolder.initializeArchetype( self )
        self.atse_init()
        self.atse_registerObject( AlchemistWebContent,
                                  undeletable_fields=('title',) )
        self._clear()

    def createType(self,
                   type_name,
                   typeinfo_name='Alchemist Content: Alchemist Web Content',
                   type_factory = FactoryTypeInformation.meta_type ):

        types_tool = self.portal_types
        types_tool.manage_addTypeInformation(
            type_factory,
            id = type_name,
            typeinfo_name = typeinfo_name
            )

    def createSchema(self, schema_id ):

        schema_base = Schema()

    def getPeerFor( self, instance ):

        factory = self.getPeerFactory( instance )
        peer = factory.get( instance.UID() )

        model = getModelFor( instance ) # refactor ?
        
        if peer is None:
            peer = factory( uid = instance.UID() )
            model.initializePeer( instance, peer )
            
        return peer
        
    def getPeerFactory( self, instance ):

        model = getModelFor( instance )
        peer_factory = model[ instance.portal_type ]

        if peer_factory is None:
            peer_factory = model.loadInstance( instance )
            model.engine.create_tables()
        return peer_factory
            

atapi.registerType( AlchemistTool )




