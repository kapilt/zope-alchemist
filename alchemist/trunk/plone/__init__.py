"""
$Id$
"""

try:
    from Products.Archetypes import public as atapi
except ImportError:
    atapi = None

try:    
    from Products.CMFCore.utils import ContentInit
    from Products.CMFCore.utils import ToolInit
    from Products.CMFCore.DirectoryView import registerDirectory
except:
    ToolInit = None
    registerDirectory = None

import config
import engine
import strategy
#import model
    
## model.registerModel(
##     model.archetypes.ArchetypesSchemaModel(
##        engine.create_engine("postgres://database=alchemy", echo=True)
##        )
##     )  


if registerDirectory is not None:
    registerDirectory( 'skins', globals() )


def initialize( context ):

    if ToolInit is None:
        return

    ToolInit(
        'Alchemist Tools',
        tools=(tool.AlchemistTool,),
        product_name='Alchemist',
        icon='tool.gif'
        ).initialize( context )

    if atapi is None:
        return

    listOfTypes = atapi.listTypes( config.PROJECTNAME )
    content_types, constructors, ftis = atapi.process_types( listOfTypes, config.PROJECTNAME )

    ContentInit(
        "Alchemist Content",
        content_types = content_types,
        permission    = permissions.AddAlchemistContent,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
        

    
