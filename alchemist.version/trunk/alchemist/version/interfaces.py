from zope import interface, schema, lifecycleevent
from zope.container.interfaces import IContainer
from zope.component.interfaces import IObjectEvent, ObjectEvent

#####################
# Versioned Object Interfaces
#

class IVersion( interface.Interface ):
    """
    a version of an object is identical in attributes to the actual object, based
    on that object's domain schema
    """

class IVersioned( IContainer ):
    """ a versioning system interface to an object, versioned is a container
        of versions.
    """    

    def create( ):
        """
        store the existing state of the adapted context as a new version
        """
        
    def revert( version ):
        """
        revert the current state of the adapted object to the values specified
        in version.
        """

class IVersionEvent( IObjectEvent ):
    """
    a versioning event
    """
    
    versioned = schema.Object( IVersioned )
    version = schema.Object( IVersion )    
    message = schema.Text(description=u"Message accompanying versioning event")
    
class VersionEvent( ObjectEvent ):
    """
    """
    interface.implements( IVersionEvent )

    def __init__( self, object, versioned, version, msg ):
        self.object = object
        self.versioned = versioned
        self.version = version
        self.message = msg
        
class IVersionCreated( IVersionEvent ):
    """ a new version was created, but is not yet
    saved to the db
    """

class VersionCreated( VersionEvent ):
    
    interface.implements( IVersionCreated )


class IVersionReverted( IVersionEvent, lifecycleevent.IObjectModifiedEvent ):
    """
    the context version was reverted
    """
    
class VersionReverted( VersionEvent ):
    
    interface.implements( IVersionReverted )
    
    descriptions = ()

