"""
$Id$
"""

from Products.Archetypes import public as atapi

from Products.CMFCore.utils import ContentInit
from Products.CMFCore.utils import ToolInit
from Products.CMFCore.DirectoryView import registerDirectory

import config
import permissions
import tool

registerDirectory( 'skins', globals() )

   
def initialize( context ):

    ToolInit(
        'Alchemist Tools',
        tools=(tool.AlchemistTool,),
        product_name='Alchemist',
        icon='tool.gif'
        ).initialize( context )

    listOfTypes = atapi.listTypes( config.PROJECTNAME )
    content_types, constructors, ftis = atapi.process_types( listOfTypes, config.PROJECTNAME )

    ContentInit(
        "Alchemist Content",
        content_types = content_types,
        permission    = permissions.AddAlchemistContent,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
        

    
