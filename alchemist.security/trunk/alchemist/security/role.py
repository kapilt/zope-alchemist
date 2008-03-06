from zope import interface
from zope.securitypolicy.interfaces import IPrincipalRoleMap 

import sqlalchemy as rdb
import schema

class PrincipalRoleMap( object ):
    
    interface.implements( IPrincipalRoleMap )
    
    def getPrincipalsForRole(self, role_id):
        """Get the principals that have been granted a role.

        Return the list of (principal id, setting) who have been assigned or
        removed from a role.

        If no principals have been assigned this role,
        then the empty list is returned.
        """
        prm = schema.principal_role_map
        s = rdb.select( [prm.principal_id, prm.setting] ).where( prm.role_id == role_id )  
        return s.execute()

    def getRolesForPrincipal(self, principal_id):
        """Get the roles granted to a principal.

        Return the list of (role id, setting) assigned or removed from
        this principal.

        If no roles have been assigned to
        this principal, then the empty list is returned.
        """
        prm = schema.principal_role_map
        s = rdb.select( [prm.role_id, prm.setting] ).where( prm.principal_id == principal_id )
        return s.execute()

    def getSetting(self, role_id, principal_id):
        """Return the setting for this principal, role combination
        """
        prm = schema.principal_role_map
        s = rdb.select( [prm.settings] ).where( 
                rdb.and_( prm.principal_id == principal_id, prm.role_id == role_id )
                )
        results = s.execute()
        return results.fetchone()[0]

    def getPrincipalsAndRoles():
        """Get all settings.

        Return all the principal/role combinations along with the
        setting for each combination as a sequence of tuples with the
        role id, principal id, and setting, in that order.
        """
        prm = schema.principal_role_map
        return prm.select( [prm.role_id, prm.principle_id, prm.setting ] ).execute()
        
