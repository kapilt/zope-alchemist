
from datetime import datetime
import sqlalchemy as rdb


def make_changes_table( table, metadata ):
    """ create an object log table for an object """
    table_name = table.name
    entity_name =  table_name.endswith('s') and table_name[:-1] or table_name
    
    changes_name = "%s_changes"%( entity_name )
    fk_id = "%s_id"%( entity_name )
    #print entity_name, fk_id
    
    changes_table = rdb.Table(
            changes_name,
            metadata,
            rdb.Column( "change_id", rdb.Integer, primary_key=True ),
            rdb.Column( "content_id", rdb.Integer, rdb.ForeignKey( table.c[ fk_id ] ) ),
            rdb.Column( "action", rdb.Unicode(16) ),
            rdb.Column( "date", rdb.Date, default=datetime.now),
            rdb.Column( "description", rdb.UnicodeText),
            rdb.Column( "notes", rdb.UnicodeText),
            rdb.Column( "user_id", rdb.Unicode(32) ) # Integer, rdb.ForeignKey('users.user_id') ),
    )
    
    return changes_table