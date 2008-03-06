from zope import interface
from zope.securitypolicy.interfaces import IPrincipalRoleMap 

import sqlalchemy as rdb
import schema

class IPrincipalRoleMap(Interface):
    """Mappings between principals and roles."""

    def getPrincipalsForRole(role_id):
        """Get the principals that have been granted a role.

        Return the list of (principal id, setting) who have been assigned or
        removed from a role.

        If no principals have been assigned this role,
        then the empty list is returned.
        """

    def getRolesForPrincipal(principal_id):
        """Get the roles granted to a principal.

        Return the list of (role id, setting) assigned or removed from
        this principal.

        If no roles have been assigned to
        this principal, then the empty list is returned.
        """

    def getSetting(role_id, principal_id):
        """Return the setting for this principal, role combination
        """

    def getPrincipalsAndRoles():
        """Get all settings.

        Return all the principal/role combinations along with the
        setting for each combination as a sequence of tuples with the
        role id, principal id, and setting, in that order.
        """

