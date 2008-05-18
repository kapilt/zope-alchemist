from z3c.menu.ready2go import item
from zope.app.security.interfaces import IUnauthenticatedPrincipal

class GlobalMenuItem( item.GlobalMenuItem ):

    selected = False
    
class LoginAction( item.GlobalMenuItem ):

    css = ""
    
    @property
    def available( self ):
        available = IUnauthenticatedPrincipal.providedBy( self.request.principal )
        return available
    
class LogoutAction( item.SiteMenuItem ):

    css = ""
    
    @property
    def available( self ):
        authenticated = not IUnauthenticatedPrincipal.providedBy( self.request.principal )
        return authenticated
