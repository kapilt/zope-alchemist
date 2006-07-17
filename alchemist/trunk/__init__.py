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
import archetypes
import permissions
import tool
import databases
import strategy
import model
    
model.registerModel(
    model.archetypes.ArchetypesSchemaModel(
       engine.create_engine("postgres://database=alchemy", echo=True)
       )
    )    

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
        

    
