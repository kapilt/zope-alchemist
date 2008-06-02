"""

Local And Global Principal Role Maps.

These are somewhat naive implementations, for hybrid zodb/rdb systems, use of this implementation
is not recommended, instead use alchemist keyreferences in conjunction with ore.annotation 
(utility annotations).

"""

from zope import interface
from zope.securitypolicy.interfaces import IPrincipalRoleMap 
from zope.securitypolicy.interfaces import Allow, Deny, Unset

from sqlalchemy import select, and_, orm
from schema import prm

BooleanAsSetting = { True : Allow, False : Deny, None : Unset }

class LocalPrincipalRoleMap( object ):
    
    interface.implements( IPrincipalRoleMap )
    
    def __init__( self, context ):
        self.context = context
        self.oid = orm.object_mapper( self.context ).primary_key_from_instance(self.context)[0]
        self.object_type = context.__class__.__name__.lower()
                                    
    def getPrincipalsForRole(self, role_id):
        """Get the principals that have been granted a role.

        Return the list of (principal id, setting) who have been assigned or
        removed from a role.

        If no principals have been assigned this role,
        then the empty list is returned.
        """
        s = select( [prm.c.principal_id, prm.c.setting],
                and_( prm.c.role_id == role_id,
                          prm.c.object_type == self.object_type,
                          prm.c.object_id == self.oid )
                )
        for o in s.execute():
            yield o[0], BooleanAsSetting[ o[1] ]

    def getRolesForPrincipal(self, principal_id):
        """Get the roles granted to a principal.

        Return the list of (role id, setting) assigned or removed from
        this principal.

        If no roles have been assigned to
        this principal, then the empty list is returned.
        """
        s = select( [prm.c.role_id, prm.c.setting],
                and_( prm.c.principal_id == principal_id,
                          prm.c.object_type == self.object_type,
                          prm.c.object_id == self.oid )
            )
        for o in s.execute():
            yield o[0], BooleanAsSetting[ o[1] ]

    def getSetting(self, role_id, principal_id):
        """Return the setting for this principal, role combination
        """
        s = select( [prm.c.setting],
                and_( prm.c.principal_id == principal_id,
                          prm.c.role_id == role_id, 
                          prm.c.object_type == self.object_type,
                          prm.c.object_id == self.oid )                          
                )
        results = s.execute().fetchone()
        if not results:
            return Unset
        return BooleanAsSetting[ results[0] ]

    def getPrincipalsAndRoles( self ):
        """Get all settings.

        Return all the principal/role combinations along with the
        setting for each combination as a sequence of tuples with the
        role id, principal id, and setting, in that order.
        """
        s =select( [prm.c.role_id, prm.c.principal_id, prm.c.setting ],
                    and_( prm.c.object_type == self.object_type,
                          prm.c.object_id == self.oid )
               )
        for role_id, principal_id, setting in s.execute():
            yield role_id, principal_id, BooleanAsSetting[ setting ]
        
    def assignRoleToPrincipal( self, role_id, principal_id ):
        prm.insert(
            values=dict( role_id = role_id, 
                         principal_id = principal_id,
                         object_id = self.oid,
                         object_type = self.object_type )
            ).execute()

    def removeRoleFromPrincipal( self, role_id, principal_id ):
        s = select( [prm.c.role_id, prm.c.setting],
                and_( prm.c.principal_id == principal_id,
                      prm.c.object_type == self.object_type,
                      prm.c.role_id == role_id, 
                      prm.c.object_id == self.oid )
            )
        if s.execute().fetchone():
            self.unsetRoleForPrincipal( role_id, principal_id )

        prm.insert(
            values=dict( role_id = role_id, 
                         principal_id = principal_id,
                         setting = False,
                         object_id = self.oid,
                         object_type = self.object_type )
            ).execute()    
        

        
    def unsetRoleForPrincipal( self, role_id, principal_id ):
        prm.delete(
            and_( prm.c.role_id == role_id,
                      prm.c.principal_id == principal_id,
                      prm.c.object_type == self.object_type,
                      prm.c.object_id == self.oid )                                                
            ).execute()
        

class GlobalPrincipalRoleMap( LocalPrincipalRoleMap ):
    
    def __init__( self, context ):
        self.context = context
        self.object_type = None
        self.oid = None
