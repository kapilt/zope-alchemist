from zope import interface, component
from zope.securitypolicy.interfaces import IPrincipalRoleMap 
from zope.securitypolicy.interfaces import Allow, Deny, Unset
import sqlalchemy as rdb
import schema

def get_parent_names( ob ):
    names = []
    while ob is not None:
        names.append( ob.__name__ )
        ob = ob.__parent__
    return names
    
@interface.implementer( IPrincipalRoleMap )
def adaptprm( object ):
    prm = PrincipalRoleMap()
    return prm

BooleanAsSetting = { True : Allow, False : Deny, None : Unset }

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
        s = rdb.select( [prm.c.principal_id, prm.c.setting] ).where( prm.c.role_id == role_id )  
        return s.execute()

    def getRolesForPrincipal(self, principal_id):
        """Get the roles granted to a principal.

        Return the list of (role id, setting) assigned or removed from
        this principal.

        If no roles have been assigned to
        this principal, then the empty list is returned.
        """
        prm = schema.principal_role_map
        s = rdb.select( [prm.c.role_id, prm.c.setting] ).where( prm.c.principal_id == principal_id )
        for o in s.execute():
            yield o[0], BooleanAsSetting[ o[1] ]

    def getSetting(self, role_id, principal_id):
        """Return the setting for this principal, role combination
        """
        prm = schema.principal_role_map
        s = rdb.select( [prm.c.settings] ).where( 
                rdb.and_( prm.c.principal_id == principal_id, prm.c.role_id == role_id )
                )
        results = s.execute()
        return results.fetchone()[0]

    def getPrincipalsAndRoles( self ):
        """Get all settings.

        Return all the principal/role combinations along with the
        setting for each combination as a sequence of tuples with the
        role id, principal id, and setting, in that order.
        """
        prm = schema.principal_role_map
        return prm.select( [prm.c.role_id, prm.c.principle_id, prm.c.setting ] ).execute()
        
    def assignRoleToPrincipal( self, role_id, principal_id ):
        schema.principal_role_map.insert(
            values=dict( role_id = role_id, principal_id = principal_id )
            ).execute()

    def removeRoleFromPrincipal( self, role_id, principal_id ):
        prm = schema.principal_role_map
        prm.delete(
            rdb.and_( prm.c.role_id == role_id,
                      prm.c.principal_id == principal_id )
            ).execute()

    def unsetRoleForPrincipal( self, role_id, principal_id ):
        raise NotImplemented
    
