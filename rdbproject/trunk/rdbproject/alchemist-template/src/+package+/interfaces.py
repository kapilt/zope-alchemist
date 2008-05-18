
from zope import interface, schema
from ore.alchemist.interfaces import IAlchemistContent, IAlchemistContainer
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.viewlet.interfaces import IViewletManager
from i18n import _

class IApplication( interface.Interface ):
    """ Public Funds Tracking Application """

class IApplicationSetup( interface.Interface ):
    """ Adapter for application setup  """

class IApplicationSkin( IDefaultBrowserLayer ):
    """ Skin for Public Funds Tracking Application """

class ISiteMenu( IViewletManager ):
    """ Menu for site actions """

class IAddMenu( IViewletManager ):
    """ Navigation menu """

class IContextMenu( IViewletManager ):
    """ menu of actions for the current context/object"""

class IJavaScript( IViewletManager ):
    """ site javascript """

class ICSS( IViewletManager ):
    """ site css """

# Domain and Container Interfaces

class IApplicationContent( IAlchemistContent ):
    """ basic content interface
    """
    id = interface.Attribute("id")
    
class IApplicationContainer( IAlchemistContainer ):
    """ basic container interface
    """

class IUser( IApplicationContent ):
    """ """
    jobTitle = schema.TextLine( title=_(u"Last Name"), max_length=30 )
    empNum = schema.Int( title=_(u"Employee Number"))
    status = schema.Choice( title=_(u"Status"), values=["A", "I"] )
    role = schema.TextLine(title=_(u"Role") )

    actionsLead = interface.Attribute("actionsLead")
    actionsInvolved = interface.Attribute("actionsInvolved")
    offices = interface.Attribute('offices')
    
class IEmployeeContainer( IApplicationContainer ):
    """ """
