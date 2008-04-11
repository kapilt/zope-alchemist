import sqlalchemy as rdb

metadata = rdb.MetaData()

permissions = rdb.Table(
   "zope_permissions",
   metadata,
   rdb.Column( "permission_id", rdb.Integer, primary_key=True ),
   rdb.Column( "name", rdb.Unicode(30), unique=True  ),
   )

roles = rdb.Table(
   "zope_roles",
   metadata,
   rdb.Column( "role_id", rdb.Integer, primary_key=True ),
   rdb.Column( "name", rdb.Unicode(30), primary_key=True ),   
   )

permission_role_map = rdb.Table(
   "zope_role_permission_map",
   metadata,
   rdb.Column( "role_id", rdb.Unicode(50) ),
   rdb.Column( "permission_id", rdb.Unicode(50) ),
   rdb.Column( "object_type", rdb.Unicode(50), ),
   rdb.Column( "object_id", rdb.Unicode(40),  ),   
   )
   
principal_role_map = rdb.Table(
   "zope_principal_role_map",
   metadata,
#   rdb.Column( "principal_id", rdb.Integer, index=True, nullable=False ),
   rdb.Column( "principal_id", rdb.Unicode(50), index=True, nullable=False ),#    # 
   rdb.Column( "role_id", rdb.Unicode(50), nullable=False ),   
   rdb.Column( "setting", rdb.Boolean, default=True, nullable=False ),
#   rdb.Column( "object_type", rdb.Un, ),      
#   rdb.Column( "object_id", rdb.Integer, ),         
   )
  
def main( ):
    db = rdb.create_engine('postgres://localhost/bungeni')
    metadata.bind = db
    metadata.create_all()
    
if __name__ == '__main__':
    main()

