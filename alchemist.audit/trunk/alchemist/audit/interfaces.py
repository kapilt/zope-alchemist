from zope import interface

class IAuditable( interface.Interface ):
    """
    marker interface to apply auditing/object log feature
    """

class IRecorder( interface.Interface ):
    """
    a recorder for changes to an object
    """

    def objectAdded( object, event ):
        " "
    def objectModified( object, event ):
        " "
    def objectStateChanged( object, event ):
        " "
    def objectDeleted( object, event ):
        " "
    def objectNewVersion( object, event ):
        " "
    def objectRevertedVersion( object, event ):
        " "

    
