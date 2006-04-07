
import sqlalchemy as rdb

class PlonePASModel( object ):        
    
    class table_names:
        users = 'users'
        roles = 'roles'
        groups = 'groups'
        user_role_map = 'user_role_map'
        group_role_map = 'group_role_map'

    def __init__(self, engine):
        self.engine = engine
        self.users = None
        self.roles = None
        self.groups = None
        self.user_role_map = None
        self.User = None
        self.Group = None
        self.Role = None
        
    def generateDefaults(self):
        users = rdb.Table(self.table_names.users,
                          self.engine,
                          rdb.Column("user_id", rdb.String(60), primary_key=True),
                          rdb.Column("name", rdb.String(100)  ),
                          )


        groups = rdb.Table(self.table_names.groups,
                           self.engine,
                           rdb.Column("group_id", rdb.String(60), primary_key=True),
                           rdb.Column("name", rdb.String(100) ),
                           )

        roles = rdb.Table(self.table_names.roles,
                          self.engine,
                          rdb.Column("role_id", rdb.String(60), primary_key=True),
                          rdb.Column("name", rdb.String(100) ),
                          )

        user_role_map = rdb.Table( self.table_names.user_role_map,
                                   self.engine,
                                   rdb.Column('role_id',
                                              rdb.String(60),
                                              rdb.ForeignKey( "%s.role_id"%self.table_names.roles ),
                                              ),
                                   rdb.Column('user_id',
                                              rdb.String(60),
                                              rdb.ForeignKey( "%s.user_id"%self.table_names.users ),
                                   )
                                   )

        group_role_map = rdb.Table( self.table_names.group_role_map,
                                    self.engine,
                                    rdb.Column('role_id',
                                               rdb.String(60),
                                               rdb.ForeignKey( "%s.role_id"%self.table_names.roles ),
                                               ),                                    
                                    rdb.Column("group_id",
                                               rdb.String(60),
                                               rdb.ForeignKey( "%s.group_id"%self.table_names.groups ),
                                               ),                                               

                                    )






        class User( object ):
            def __init__(self, user_id, name='' ):
                self.user_id = user_id
                self.name = name

        class Role( object ):
            def __init__(self, role_id, name='' ):
                self.role_id = role_id
                self.name = name

        class Group( object ):
            def __init__(self, group_id, name='' ):
                self.group_id = group_id
                self.name = name
                
        rdb.assign_mapper( Role, roles )
        rdb.assign_mapper( User, users, 
                           properties = { 'roles' : rdb.relation(Role.mapper,
                                                                 user_role_map,
                                                                 backref=rdb.backref('users'))
                                          }
                               )

        rdb.assign_mapper( Group, groups, 
                           properties = { 'roles' : rdb.relation(Role.mapper,
                                                             group_role_map,
                                                             backref=rdb.backref('groups'))
                                          }
                           )      

                                    

        return locals()
    
##         local_roles = rdb.Table( self.table_names.context_roles,
##                                  self.engine,
##                                  rdb.Column("uid", rdb.String(50) ),
##                                  rdb.Column("role_id", rdb.String(50) ),
##                                  rdb.Column("principal_id", rdb.String(60) ),
##                                  )


                           
if __name__ == '__main__':

    from Products.Alchemist.engine import get_engine
    engine = get_engine("postgres://database=alchemy", echo=True )    
    model = PlonePASModel(engine)
    parts = model.generateDefaults()

    test_user = parts['User']('test_user')
    test_role = parts['Role']('test_role')
    test_user.roles.append( test_role )

    for i in test_role.users:
        print i

    test_group = parts['Group']('test_group')

    test_group.roles.append( test_role )


    

    for i in test_role.groups:
        print i

