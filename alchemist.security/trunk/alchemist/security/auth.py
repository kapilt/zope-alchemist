"""
zope3 authenticator plugin against a relational database
"""

from zope import interface
from zope.app.authentication import interfaces
from zope.app.container.contained import Contained

from ore.alchemist import Session

from interfaces import IAlchemistUser, IAlchemistAuth


class PrincipalInfo( object ):

    interface.implements(interfaces.IPrincipalInfo)
    
    def __init__(self, id, login, title, description, auth_plugin=None):
        self.id = id
        self.login = login
        self.title = title
        self.description = description
        self.authenticatorPlugin = auth_plugin
        
    def __repr__(self):
        return 'PrincipalInfo(%r)' % self.id

class DatabaseAuthentication( Contained ):
    
    interface.implements( interfaces.IAuthenticatorPlugin, IAlchemistAuth )

    def authenticateCredentials( self, credentials ):
        if not credentials:
            return None
        login, password = credentials.get('login'), credentials.get('password')
        User = IAlchemistUser( self )
        results = Session().query( User ).filter_by( login = unicode(login) ).all()

        if len(results) != 1:
            return None

        user = results[0]
        if not user.checkPassword( password ):
            return None

        return self._makeInfo( user )
        
    def principalInfo( self, id ):
        # short circuit evaluation of these, defer to global definitions
        if id in ('zope.Everybody', 'zope.Anybody'):
            return None
        User = IAlchemistUser( self )            
        results = Session().query( User ).filter_by( login = id ).all()
        if len(results) != 1: # unique index on column
            return None

        user = results[0]
        return self._makeInfo( user )

    def _makeInfo( self, user ):
        return PrincipalInfo( "users.%s"%user.login,    # userid
                              user.login,               # login
                              u"%s, %s"%(user.last_name, user.first_name), # title
                              user.email,               # description
                              self                      # auth plugin
                              )
        
        
    def __repr__(self):
        return "<DatabaseAuthPlugin>"