"""
$Id$
"""

import sqlalchemy as rdb
from archetypes import ArchetypesSchemaModel

class PloneSerializer( self, content ):

    def saveAspects( self, peer, content ):
        pass

class PloneSchemaModel( ArchetypesSchemaModel ):

    def generatDefaults(self):

        
        workflow_history = rdb.Table( self.table_names.workflow_history,
                                      self.engine,
                                      rdb.Column("uid", rdb.String(50) ),
                                      rdb.Column("workflow_id", rdb.String(50) ),
                                      rdb.Column("action_time", rdb.DateTime() ),
                                      rdb.Column("comments", rdb.String(1000) ),
                                      rdb.Column("principal_id", rdb.Column(60) ),
                                      )

        workflow_idx = rdb.Index(  (workflow_history.c.uid,
                                    workflow_history.c.workflow_id,
                                    workflow_history.c.action_time ) )

        local_roles = rdb.Table( self.table_names.context_roles,
                                 self.engine,
                                 rdb.Column("uid", rdb.String(50) ),
                                 rdb.Column("role_id", rdb.String(50) ),
                                 rdb.Column("principal_id", rdb.String(60) ),
                                 )

        

class SchemaLoader( object ):
    def load( self, context, model ):
        pass
        

