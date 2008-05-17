
from zope.viewlet.interfaces import IViewletManager
from zope import interface
from zope.interface.common.sequence import ISequence

class IAlchemistLayer( interface.Interface ):
    """ Alchemist UI Layer """

class IContentEditManager( IViewletManager ):
    """ viewlet manager interface """

class IContentViewManager( IViewletManager ):
    """ viewlet manager interface """    

class IIterableSequence( ISequence ):
    def __iter__(  ):
        """iterate through elements of a sequence
        """
