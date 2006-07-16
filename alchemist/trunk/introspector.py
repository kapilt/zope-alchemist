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

odd thoughts.. don't wrap svnb style..

just a tool.. accessor to z2 style objects


Author: Kapil Thangavelu <hazmat@objectrealms.net>
$Id$
"""

from Products.Archetypes import public as atapi

from engine import get_engine, list_engines


schema_browser_schema = Schema( (
    atapi.StringField('db_uri',
                      mutator='setDatabase',
                      )
))

actions = (

    { 'id':'view',
      'name':'View',
      'action':'string:${object_url}/base_view',
      'permissions':( CMFCorePermissions.View, ), 
      'category':'object' },

    
    { 'id': 'edit',
      'name': 'Edit',
      'action': 'string:${object_url}/base_edit',
      'permissions': (CMFCorePermissions.ModifyPortalContent,),
      },
    
    { 'id':'sharing',
      'name':'Sharing',
      'action':'string:${object_url}/folder_localrole_form',
      'permissions':( CMFCorePermissions.View, ), 
      'category':'object' },  
      
   )

def modify_fti( fti ):
    fti['actions'] = actions

class PortalView:

    index_html = None

    def __call__(self):
        '''
        Invokes the default view.
        '''
        view = _getViewFor(self)
        return view()
    
    def view(self):
        """
        invoke default view
        """
        return self()

class SchemaElement( object ): pass

class SchemaTable( PortalView, DynamicType, SimpleItem, SchemaElement  ):

    def __init__(self, id, table ):
        self.id = id
        self._table = table
        
    def getColumns( self ):
        return map( self._mapColumn, self._table.columns.items() )

    columns = property( getColumns )

    def getTable( self ):
        return self._table

    table = property( getTable )

    def _mapColumn(self, column_id, column):
        schema_column = SchemaColumn( column_id, column )
        return schema_column.__of__( self )

class SchemaColumn( PortalView, DynamicType, SimpleItem, SchemaElement ):

    def __init__(self, id, column):
        self.id = id
        self.column = column

        # initialize column values for display

        self.type = repr( column.type )
        self.unique = column.unique
        self.nullable = column.nullable
        self.index = column.index
        

class SchemaInspector( atapi.BaseFolder ):

    portal_type = archetype_name = meta_type = "Schema Browser"
    global_allow = True

    schema = atapi.BaseContent.Schema + schema_browser_schema

    def setDatabase( self, db_uri ):
        assert db_uri in list_engines()
        self.db_uri = db_uri

    def _getEngine(self ):
        return get_engine( self.db_uri )

    def getTables( self ):
        engine = self._getEngine()
        return map( self._mapTable, engine.tables.values() )

    def _mapTable( self, table ):
        return SchemaTable( table ).__of__(self)

    def createTypeFor( self, table_id, options=None):
        pass


        
        
