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
from Products.alchemist.engine import get_engine

def plone2rdb( self, db_uri='postgres://database=plone'):
    dump_site( self, db_uri )

def dump_content( self, model ):
    # dump content
    for brain in self.portal_catalog():
        content = brain.getObject()
        
        if content is None: continue
        elif isinstance( content, UniqueObject): continue

        peer = model.saveObject( content )

def dump_site( self, db_uri="postgres://database=alchemy" ):

    # setup up the schema definitions
    engine = get_engine( db_uri, echo=True )

    # connect to database
    schema_model = ArchetypesSchemaModel( engine )

    # load up schemas
    for archetype_info in self.archetype_tool.listRegisteredTypes():
        schema_model.loadType( archetype_info['klass'], context=self )

    engine.create_tables()

    try:
        dump_content( self, schema_model )
    except:
        raise
        import traceback, pdb, sys
        ec,e,tb = sys.exc_info()
        print ec, e
        traceback.print_tb( tb )
        pdb.post_mortem( tb )
        
        
    import pdb;
    return "Success"

