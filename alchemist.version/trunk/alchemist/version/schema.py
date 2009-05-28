
import sqlalchemy as rdb

def make_versions_table( table, metadata ):
    """
    create a versions table, requires change log table for which some version metadata information will be stored.
    """
    table_name = table.name
    entity_name =  table_name.endswith('s') and table_name[:-1] or table_name
    
    versions_name = "%s_versions"%( entity_name )
    fk_id = "%s_id"%( entity_name )
    
    columns = [
        rdb.Column( "version_id", rdb.Integer, primary_key=True ),
        #rdb.Column( "version_created", rdb.DateTime, default=rdb.PassiveDefault('now') ),
        rdb.Column( "content_id", rdb.Integer, rdb.ForeignKey( table.c[ fk_id ] ) ),
        rdb.Column( "change_id", rdb.Integer, rdb.ForeignKey('%s_changes.change_id'%entity_name)),
        rdb.Column( "manual", rdb.Boolean, nullable=False, default=False),
    ]
    
    columns.extend( [ c.copy() for c in table.columns if not c.primary_key ] )
    
    #primary = [ c.copy() for c in table.columns if c.primary_key ][0]
    #primary.primary_key = False
    #columns.insert( 2, primary )
    
    versions_table = rdb.Table(
            versions_name,
            metadata,
            *columns 
            )
            
    return versions_table


