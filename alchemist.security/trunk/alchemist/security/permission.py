from zope import interface
from zope.securitypolicy.interfaces import IRolePermissionMap 
from zope.app.security.settings import Allow, Deny, Unset

from zope.security.proxy import removeSecurityProxy

from sqlalchemy import select, and_, orm
from sqlalchemy.exc import UnboundExecutionError

from ore.alchemist import Session

from schema import rpm

BooleanAsSetting = { True : Allow, False : Deny, None : Unset }

class LocalRolePermissionMap(object):
    """Mappings between roles and permissions."""

    interface.implements( IRolePermissionMap )
    
    def __init__(self, context):
        self.context = context
        session = Session()
        trusted = removeSecurityProxy(context)        
        session.merge(trusted)
        try:
            self.oid = orm.object_mapper( trusted ).primary_key_from_instance(trusted)[0]
        except UnboundExecutionError:
            session.add(trusted)     
            self.oid = orm.object_mapper( trusted ).primary_key_from_instance(trusted)[0]         
        self.object_type = context.__class__.__name__.lower()

    def getPermissionsForRole(self, role_id):
        """Get the premissions granted to a role.

        Return a sequence of (permission id, setting) tuples for the given
        role.

        If no permissions have been granted to this
        role, then the empty list is returned.
        """
        s = select( [rpm.c.permission_id, rpm.c.setting],
                and_( rpm.c.role_id == role_id,
                      rpm.c.object_id == self.oid,
                      rpm.c.object_type == self.object_type )
                      )
        for o in s.execute():
            yield o[0], BooleanAsSetting[ o[1] ]
        
    def getRolesForPermission(self, permission_id):
        """Get the roles that have a permission.

        Return a sequence of (role id, setting) tuples for the given
        permission.

        If no roles have been granted this permission, then the empty list is
        returned.
        """
        s = select( [rpm.c.role_id, rpm.c.setting ],
              and_( rpm.c.permission_id == permission_id,
                    rpm.c.object_id == self.oid,
                    rpm.c.object_type == self.object_type )                    
              )
        for o in s.execute():
            yield o[0], BooleanAsSetting[ o[1] ]

    def getSetting(self, permission_id, role_id):
        """Return the setting for the given permission id and role id

        If there is no setting, Unset is returned
        """
        s = select( [ rpm.c.setting],
              and_( rpm.c.permission_id == permission_id,
                    rpm.c.role_id == role_id,
                    rpm.c.object_id == self.oid,
                    rpm.c.object_type == self.object_type )                            
            )
        res = s.execute().fetchone()
        if not res:
            return Unset
        return BooleanAsSetting[ res[0] ]
        
    def getRolesAndPermissions(self):
        """Return a sequence of (permission_id, role_id, setting) here.

        The settings are returned as a sequence of permission, role,
        setting tuples.

        If no principal/role assertions have been made here, then the empty
        list is returned.
        """
        s = select( [rpm.c.permission_id, rpm.c.role_id, rpm.c.setting],
                and_( rpm.c.object_id == self.oid,
                      rpm.c.object_type == self.object_type )
                      )
        for o in s.execute():
            yield o[0], o[1], BooleanAsSetting[ o[2] ]
        
    def grantPermissionToRole(self, permission_id, role_id):
        """Bind the permission to the role.
        """
        s = select( [rpm.c.permission_id ],
                and_( rpm.c.object_id == self.oid,
                      rpm.c.permission_id == permission_id,
                      rpm.c.role_id == role_id,
                      rpm.c.object_type == self.object_type )
                      )

        if s.execute().fetchone():
            self.unsetPermissionFromRole( permission_id, role_id )
        rpm.insert( 
            values = dict( permission_id = permission_id,
                           role_id = role_id,
                           object_id = self.oid,
                           object_type = self.object_type )
            ).execute()
            
    def denyPermissionToRole(self, permission_id, role_id):
        """Deny the permission to the role
        """
        s = select( [rpm.c.permission_id ],
                and_( rpm.c.object_id == self.oid,
                      rpm.c.permission_id == permission_id,
                      rpm.c.role_id == role_id,
                      rpm.c.object_type == self.object_type )
                      )

        if s.execute().fetchone():
            self.unsetPermissionFromRole( permission_id, role_id )
                                          
        rpm.insert( 
            values = dict( permission_id = permission_id,
                           role_id = role_id,
                           setting = False,
                           object_id = self.oid,
                           object_type = self.object_type )
            ).execute()

    def unsetPermissionFromRole(self, permission_id, role_id):
        """Clear the setting of the permission to the role.
        """        
        rpm.delete(
            and_( rpm.c.role_id == role_id,
                  rpm.c.permission_id == permission_id,
                  rpm.c.object_type == self.object_type,
                  rpm.c.object_id == self.oid )
        ).execute()

class GlobalRolePermissionMap( LocalRolePermissionMap ):
    
    def __init__( self, context):
        self.context = context
        self.oid = None
        self.object_type = None

