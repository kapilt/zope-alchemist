"""
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


class SchemaTableView( object ):
    pass

class SchemaColumnView( object ):
    pass


class SchemaBrowser( atapi.BaseFolder ):

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
        return SchemaTable( table )
        
        

atapi.registerType( SchemaBrowser )        


        
        
