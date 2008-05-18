import re
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

class NotAnEmailAddress(schema.ValidationError):
    """This is not a valid email address"""
    
def check_email( email ):
    if EMAIL_RE.match( email ) is None:
        raise NotAnEmailAddress(email)
        return False
    return True

EMAIL_RE = "([0-9a-zA-Z_&.+-]+!)*[0-9a-zA-Z_&.+-]+@(([0-9a-zA-Z]([0-9a-zA-Z-]*[0-9a-z-A-Z])?\.)+[a-zA-Z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$"
EMAIL_RE = re.compile( EMAIL_RE )            


class IUser( IApplicationContent ):
    """ """
    
    login = schema.TextLine(title=_(u"User Id"))
    first_name = schema.TextLine(title=_(u"First Name"))
    last_name = schema.TextLine(title=_(u"Last Name"))
    email = schema.TextLine(title=_(u"Email Address"), constraint=check_email )
    

    
    empNum = schema.Int( title=_(u"Employee Number"))
    status = schema.Choice( title=_(u"Status"), values=["A", "I"] )
    role = schema.TextLine(title=_(u"Role") )

    actionsLead = interface.Attribute("actionsLead")
    actionsInvolved = interface.Attribute("actionsInvolved")
    offices = interface.Attribute('offices')
    
class IEmployeeContainer( IApplicationContainer ):
    """ """
