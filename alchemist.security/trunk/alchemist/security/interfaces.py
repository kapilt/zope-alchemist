"""
$Id: $
"""

from zope import interface

class IAlchemistUser( interface.Interface):
    """ the domain class for authentication """

    def checkPassword( password ):
        """
        return true if the password matches
        """

class IAlchemistAuth( interface.Interface ):
    """ marker interface on alchemist security components
    for adaptation."""
    
class ISecurityLocalPrincipalRoleMap( interface.Interface ):
    """
    marker interface for alchemist objects that want to provide
    a local security context
    """
    
class ISecurityLocalRolePermissionMap( interface.Interface ):
    """
    marker interface for alchemist objects that want to provide
    a local security context
    """
    