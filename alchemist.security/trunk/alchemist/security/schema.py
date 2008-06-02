import sqlalchemy as rdb

metadata = rdb.MetaData()

role_permission_map = rdb.Table(
   "zope_role_permission_map",
   metadata,
   rdb.Column( "role_id", rdb.Unicode(50) ),
   rdb.Column( "permission_id", rdb.Unicode(50) ),
   rdb.Column( "setting", rdb.Boolean, default=True, nullable=False ),   
   rdb.Column( "object_type", rdb.String(100), ),
   rdb.Column( "object_id", rdb.Integer ),   
   )
   
rpm = role_permission_map   

rdb.Index( "rpm_oid_idx", 
            role_permission_map.c['object_id'],            
            role_permission_map.c['object_type'] )
   
principal_role_map = rdb.Table(
   "zope_principal_role_map",
   metadata,
   rdb.Column( "principal_id", rdb.Unicode(50), index=True, nullable=False ),
   rdb.Column( "role_id", rdb.Unicode(50), nullable=False ),   
   rdb.Column( "setting", rdb.Boolean, default=True, nullable=False ),
   rdb.Column( "object_type", rdb.String(100) ),      
   rdb.Column( "object_id", rdb.Integer ),         
   )
   
prm = principal_role_map   
   
rdb.Index( "prm_oid_idx",
            principal_role_map.c['object_id'],            
            principal_role_map.c['object_type'] )
  

