
from zope.viewlet.interfaces import IViewletManager
from zope import interface

class IAlchemistLayer( interface.Interface ):
    """ Alchemist UI Layer """

class IContentEditManager( IViewletManager ):
    """ viewlet manager interface """

class IContentViewManager( IViewletManager ):
    """ viewlet manager interface """    
