from zope import interface
from zope.securitypolicy.interfaces import IRolePermissionMap 

import sqlalchemy as rdb
import schema

class RolePermissionMap(object):
    """Mappings between roles and permissions."""

    interface.implements( IRolePermissionMap )
    
    def getPermissionsForRole(self, role_id):
        """Get the premissions granted to a role.

        Return a sequence of (permission id, setting) tuples for the given
        role.

        If no permissions have been granted to this
        role, then the empty list is returned.
        """
        prm = schema.permission_role_map         
        s = prm.select( 
            [prm.permission_id, prm.setting] ).where( prm.role_id == role_id )
        return s.execute()
        
    def getRolesForPermission(self, permission_id):
        """Get the roles that have a permission.

        Return a sequence of (role id, setting) tuples for the given
        permission.

        If no roles have been granted this permission, then the empty list is
        returned.
        """
        prm = schema.permission_role_map 
        s = prm.select(
            [prm.role_id, prm.setting ]
            ).where( prm.permission_id == permission_id )
        return s.execute()        

    def getSetting(self, permission_id, role_id):
        """Return the setting for the given permission id and role id

        If there is no setting, Unset is returned
        """
        prm = schema.permission_role_map        
        return prm
        
    def getRolesAndPermissions(self ):
        """Return a sequence of (permission_id, role_id, setting) here.

        The settings are returned as a sequence of permission, role,
        setting tuples.

        If no principal/role assertions have been made here, then the empty
        list is returned.
        """
        prm = schema.permission_role_map        