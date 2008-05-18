
from zope import interface
from zope.app.component import site
from zope.app.container.sample import SampleContainer
from zope.app.security.interfaces import IAuthentication
from zope.app.authentication import PluggableAuthentication


from ore.wsgiapp import app

#from ore.alchemist import Session
# tell elixir to use alchemist sessions
#import elixir
#elixir.session = Session

import domain, interfaces

class Application( app.Application ):
    interface.implements( interfaces.IApplication )

def setUpSubscriber( object, event ):
    initializer = interfaces.IApplicationSetup( object )
    initializer.setUp()
    
class AppSetup( object ):

    interface.implements( interfaces.IApplicationSetup )

    def __init__( self, context ):
        self.context = context
        
    def setUp( self ):
        sm = site.LocalSiteManager( self.context )
        self.context.setSiteManager( sm )
    
        # setup authentication plugin
        auth = PluggableAuthentication()
        auth.credentialsPlugins = ('Cookie Credentials',)
        auth.authenticatorPlugins = ('rdb-auth',)
        sm.registerUtility( auth, IAuthentication )
    
        #elixir.setup_all()
        
        # populate root
        
        # populate admin section
        self.context['admin'] = admin = SampleContainer()
        
        
        
